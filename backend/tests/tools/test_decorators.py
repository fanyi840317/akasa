# -*- coding: utf-8 -*-
# Copyright (c) 2024 Lingjing
# SPDX-License-Identifier: MIT

import json
import time
import pytest
import logging
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from src.tools.decorators import (
    log_io,
    create_logged_tool,
    performance_monitor,
    retry_on_failure,
    validate_input,
    cache_result,
    rate_limit,
    sanitize_output,
    measure_memory_usage,
    mystery_tool
)


class TestLogIO:
    """测试log_io装饰器"""
    
    def test_log_io_success(self, caplog):
        """测试成功执行的日志记录"""
        @log_io
        def test_func(x, y=10):
            return x + y
        
        with caplog.at_level(logging.INFO):
            result = test_func(5, y=15)
        
        assert result == 20
        assert "test_func] Starting execution" in caplog.text
        assert "test_func] Completed successfully" in caplog.text
    
    def test_log_io_exception(self, caplog):
        """测试异常情况的日志记录"""
        @log_io
        def test_func():
            raise ValueError("Test error")
        
        with caplog.at_level(logging.ERROR):
            result = test_func()
        
        # 应该返回JSON格式的错误信息
        error_data = json.loads(result)
        assert error_data["error"] == "Test error"
        assert error_data["function"] == "test_func"
        assert "test_func] Failed after" in caplog.text
    
    def test_log_io_json_result(self, caplog):
        """测试JSON结果的解析"""
        @log_io
        def test_func():
            return json.dumps({"status": "success", "data": "test"})
        
        with caplog.at_level(logging.DEBUG):
            result = test_func()
        
        assert json.loads(result)["status"] == "success"
        assert "Result keys:" in caplog.text
    
    def test_log_io_error_result(self, caplog):
        """测试包含错误的JSON结果"""
        @log_io
        def test_func():
            return json.dumps({"error": "Something went wrong"})
        
        with caplog.at_level(logging.WARNING):
            result = test_func()
        
        assert "Function returned error" in caplog.text


class TestCreateLoggedTool:
    """测试create_logged_tool函数"""
    
    def test_create_logged_tool_basic(self):
        """测试基本工具包装"""
        class MockTool:
            def __init__(self, name):
                self.name = name
            
            def _run(self, query):
                return f"Result for {query}"
        
        LoggedMockTool = create_logged_tool(MockTool)
        tool = LoggedMockTool("test_tool")
        
        assert tool.name == "test_tool"
        assert hasattr(tool, '_run')
    
    def test_create_logged_tool_with_arun(self):
        """测试包含异步方法的工具包装"""
        class MockAsyncTool:
            def __init__(self, name):
                self.name = name
            
            def _run(self, query):
                return f"Sync result for {query}"
            
            async def _arun(self, query):
                return f"Async result for {query}"
        
        LoggedMockTool = create_logged_tool(MockAsyncTool)
        tool = LoggedMockTool("async_tool")
        
        assert tool.name == "async_tool"
        assert hasattr(tool, '_run')
        assert hasattr(tool, '_arun')


class TestPerformanceMonitor:
    """测试performance_monitor装饰器"""
    
    def test_performance_monitor_fast_execution(self, caplog):
        """测试快速执行不触发警告"""
        @performance_monitor(threshold_seconds=1.0)
        def fast_func():
            return "quick"
        
        with caplog.at_level(logging.WARNING):
            result = fast_func()
        
        assert result == "quick"
        assert "PERFORMANCE" not in caplog.text
    
    def test_performance_monitor_slow_execution(self, caplog):
        """测试慢执行触发警告"""
        @performance_monitor(threshold_seconds=0.1)
        def slow_func():
            time.sleep(0.2)
            return "slow"
        
        with caplog.at_level(logging.WARNING):
            result = slow_func()
        
        assert result == "slow"
        assert "PERFORMANCE" in caplog.text
        assert "took" in caplog.text
    
    def test_performance_monitor_exception(self, caplog):
        """测试异常情况的性能监控"""
        @performance_monitor(threshold_seconds=1.0)
        def error_func():
            raise RuntimeError("Test error")
        
        with caplog.at_level(logging.ERROR):
            with pytest.raises(RuntimeError):
                error_func()
        
        assert "PERFORMANCE" in caplog.text
        assert "failed after" in caplog.text


class TestRetryOnFailure:
    """测试retry_on_failure装饰器"""
    
    def test_retry_success_first_attempt(self):
        """测试第一次尝试成功"""
        @retry_on_failure(max_retries=3)
        def success_func():
            return "success"
        
        result = success_func()
        assert result == "success"
    
    def test_retry_success_after_failures(self, caplog):
        """测试重试后成功"""
        call_count = 0
        
        @retry_on_failure(max_retries=3, delay_seconds=0.01)
        def flaky_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary error")
            return "success"
        
        with caplog.at_level(logging.WARNING):
            result = flaky_func()
        
        assert result == "success"
        assert call_count == 3
        assert "RETRY" in caplog.text
    
    def test_retry_all_attempts_fail(self, caplog):
        """测试所有重试都失败"""
        @retry_on_failure(max_retries=2, delay_seconds=0.01)
        def always_fail():
            raise ValueError("Always fails")
        
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError, match="Always fails"):
                always_fail()
        
        assert "all 3 attempts failed" in caplog.text


class TestValidateInput:
    """测试validate_input装饰器"""
    
    def test_validate_input_success(self):
        """测试输入验证成功"""
        def is_positive(x):
            return x > 0
        
        @validate_input(is_positive, "Number must be positive")
        def process_number(x):
            return x * 2
        
        result = process_number(5)
        assert result == 10
    
    def test_validate_input_failure(self, caplog):
        """测试输入验证失败"""
        def is_positive(x):
            return x > 0
        
        @validate_input(is_positive, "Number must be positive")
        def process_number(x):
            return x * 2
        
        with caplog.at_level(logging.ERROR):
            result = process_number(-5)
        
        error_data = json.loads(result)
        assert error_data["error"] == "Number must be positive"
        assert error_data["validation_failed"] is True
        assert "VALIDATION" in caplog.text
    
    def test_validate_input_exception(self, caplog):
        """测试验证函数抛出异常"""
        def bad_validator(x):
            raise TypeError("Validator error")
        
        @validate_input(bad_validator, "Custom error")
        def process_number(x):
            return x * 2
        
        with caplog.at_level(logging.ERROR):
            result = process_number(5)
        
        error_data = json.loads(result)
        assert "Validation error" in error_data["error"]
        assert error_data["validation_error"] is True


class TestCacheResult:
    """测试cache_result装饰器"""
    
    def test_cache_result_basic(self, caplog):
        """测试基本缓存功能"""
        call_count = 0
        
        @cache_result(cache_duration_seconds=1)
        def expensive_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        with caplog.at_level(logging.DEBUG):
            # 第一次调用
            result1 = expensive_func(5)
            # 第二次调用应该使用缓存
            result2 = expensive_func(5)
        
        assert result1 == 10
        assert result2 == 10
        assert call_count == 1  # 只调用了一次
        assert "returning cached result" in caplog.text
    
    def test_cache_result_expiry(self):
        """测试缓存过期"""
        call_count = 0
        
        @cache_result(cache_duration_seconds=0.1)
        def expensive_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        # 第一次调用
        result1 = expensive_func(5)
        # 等待缓存过期
        time.sleep(0.2)
        # 第二次调用应该重新执行
        result2 = expensive_func(5)
        
        assert result1 == 10
        assert result2 == 10
        assert call_count == 2  # 调用了两次
    
    def test_cache_result_different_args(self):
        """测试不同参数的缓存"""
        call_count = 0
        
        @cache_result(cache_duration_seconds=1)
        def expensive_func(x, y=1):
            nonlocal call_count
            call_count += 1
            return x * y
        
        result1 = expensive_func(5)
        result2 = expensive_func(5, y=2)
        result3 = expensive_func(5)  # 应该使用缓存
        
        assert result1 == 5
        assert result2 == 10
        assert result3 == 5
        assert call_count == 2  # 只有两次不同的调用


class TestRateLimit:
    """测试rate_limit装饰器"""
    
    def test_rate_limit_within_limit(self):
        """测试在限制范围内的调用"""
        @rate_limit(calls_per_minute=5)
        def limited_func(x):
            return x * 2
        
        # 连续调用3次，应该都成功
        for i in range(3):
            result = limited_func(i)
            assert result == i * 2
    
    def test_rate_limit_exceeded(self, caplog):
        """测试超出限制的调用"""
        @rate_limit(calls_per_minute=2)
        def limited_func(x):
            return x * 2
        
        # 前两次调用应该成功
        result1 = limited_func(1)
        result2 = limited_func(2)
        
        with caplog.at_level(logging.WARNING):
            # 第三次调用应该被限制
            result3 = limited_func(3)
        
        assert result1 == 2
        assert result2 == 4
        
        # 第三次调用应该返回错误信息
        error_data = json.loads(result3)
        assert "Rate limit exceeded" in error_data["error"]
        assert error_data["rate_limited"] is True
        assert "RATE_LIMIT" in caplog.text


class TestSanitizeOutput:
    """测试sanitize_output装饰器"""
    
    def test_sanitize_output_default(self):
        """测试默认清理功能"""
        @sanitize_output()
        def func_with_sensitive_data():
            return json.dumps({
                "username": "test_user",
                "password": "secret123",
                "api_key": "abc123",
                "data": "normal_data"
            })
        
        result = func_with_sensitive_data()
        data = json.loads(result)
        
        assert data["username"] == "test_user"
        assert data["password"] == "[REDACTED]"
        assert data["api_key"] == "[REDACTED]"
        assert data["data"] == "normal_data"
    
    def test_sanitize_output_custom(self):
        """测试自定义清理功能"""
        def custom_sanitizer(result):
            if isinstance(result, str):
                return result.replace("secret", "***")
            return result
        
        @sanitize_output(custom_sanitizer)
        def func_with_secret():
            return "This is a secret message"
        
        result = func_with_secret()
        assert result == "This is a *** message"
    
    def test_sanitize_output_non_json(self):
        """测试非JSON输出的清理"""
        @sanitize_output()
        def func_with_string():
            return "plain string output"
        
        result = func_with_string()
        assert result == "plain string output"


class TestMeasureMemoryUsage:
    """测试measure_memory_usage装饰器"""
    
    @patch('psutil.Process')
    def test_measure_memory_usage_success(self, mock_process, caplog):
        """测试内存使用测量成功"""
        # 模拟内存信息
        mock_memory_info = Mock()
        mock_memory_info.rss = 100 * 1024 * 1024  # 100MB
        mock_process.return_value.memory_info.return_value = mock_memory_info
        
        @measure_memory_usage
        def memory_func():
            # 模拟内存使用增加
            mock_memory_info.rss = 120 * 1024 * 1024  # 120MB
            return "result"
        
        with caplog.at_level(logging.INFO):
            result = memory_func()
        
        assert result == "result"
        assert "MEMORY" in caplog.text
    
    @patch('psutil.Process', side_effect=ImportError)
    def test_measure_memory_usage_no_psutil(self, mock_process, caplog):
        """测试psutil不可用的情况"""
        @measure_memory_usage
        def memory_func():
            return "result"
        
        with caplog.at_level(logging.DEBUG):
            result = memory_func()
        
        assert result == "result"
        assert "psutil not available" in caplog.text
    
    @patch('psutil.Process')
    def test_measure_memory_usage_exception(self, mock_process, caplog):
        """测试内存测量异常"""
        mock_process.side_effect = Exception("Memory error")
        
        @measure_memory_usage
        def memory_func():
            return "result"
        
        with caplog.at_level(logging.WARNING):
            result = memory_func()
        
        assert result == "result"
        assert "Failed to measure memory" in caplog.text


class TestMysteryTool:
    """测试mystery_tool组合装饰器"""
    
    def test_mystery_tool_basic(self, caplog):
        """测试mystery_tool基本功能"""
        call_count = 0
        
        @mystery_tool(max_retries=1, cache_duration=1, rate_limit_per_minute=10)
        def mystery_func(x):
            nonlocal call_count
            call_count += 1
            return f"mystery result: {x}"
        
        with caplog.at_level(logging.INFO):
            result1 = mystery_func("test")
            result2 = mystery_func("test")  # 应该使用缓存
        
        assert "mystery result: test" in result1
        assert "mystery result: test" in result2
        assert call_count == 1  # 由于缓存，只调用一次
        assert "Starting execution" in caplog.text
    
    def test_mystery_tool_with_retry(self, caplog):
        """测试mystery_tool的重试功能"""
        call_count = 0
        
        @mystery_tool(max_retries=2, cache_duration=1, rate_limit_per_minute=10)
        def flaky_mystery_func(x):
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Temporary error")
            return f"mystery result: {x}"
        
        with caplog.at_level(logging.WARNING):
            result = flaky_mystery_func("test")
        
        assert "mystery result: test" in result
        assert call_count == 2
        assert "RETRY" in caplog.text
    
    def test_mystery_tool_rate_limit(self, caplog):
        """测试mystery_tool的速率限制"""
        @mystery_tool(max_retries=1, cache_duration=0, rate_limit_per_minute=1)
        def limited_mystery_func(x):
            return f"mystery result: {x}"
        
        # 第一次调用成功
        result1 = limited_mystery_func("test1")
        
        with caplog.at_level(logging.WARNING):
            # 第二次调用应该被限制
            result2 = limited_mystery_func("test2")
        
        assert "mystery result: test1" in result1
        
        # 第二次调用应该返回错误
        error_data = json.loads(result2)
        assert "Rate limit exceeded" in error_data["error"]
        assert "RATE_LIMIT" in caplog.text


class TestDecoratorIntegration:
    """测试装饰器集成"""
    
    def test_multiple_decorators(self, caplog):
        """测试多个装饰器组合使用"""
        call_count = 0
        
        @log_io
        @performance_monitor(threshold_seconds=0.1)
        @cache_result(cache_duration_seconds=1)
        def multi_decorated_func(x):
            nonlocal call_count
            call_count += 1
            time.sleep(0.05)  # 短暂延迟
            return x * 2
        
        with caplog.at_level(logging.INFO):
            result1 = multi_decorated_func(5)
            result2 = multi_decorated_func(5)  # 应该使用缓存
        
        assert result1 == 10
        assert result2 == 10
        assert call_count == 1  # 由于缓存，只调用一次
        assert "Starting execution" in caplog.text
        assert "Completed successfully" in caplog.text
    
    def test_decorator_order_matters(self):
        """测试装饰器顺序的重要性"""
        # 测试不同的装饰器顺序是否影响行为
        call_count = 0
        
        @cache_result(cache_duration_seconds=1)
        @log_io
        def func_order1(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        result1 = func_order1(5)
        result2 = func_order1(5)
        
        assert result1 == 10
        assert result2 == 10
        assert call_count == 1  # 缓存生效