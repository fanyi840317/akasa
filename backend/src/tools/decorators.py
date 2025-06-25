# -*- coding: utf-8 -*-
# Copyright (c) 2024 Lingjing
# SPDX-License-Identifier: MIT

import json
import logging
import time
import functools
import threading
from enum import Enum
from typing import Any, Callable, Dict, Optional, Type
from datetime import datetime

logger = logging.getLogger(__name__)


def log_io(func: Callable) -> Callable:
    """装饰器：记录工具的输入输出和执行时间
    
    Args:
        func: 要装饰的函数
        
    Returns:
        装饰后的函数
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        function_name = getattr(func, '__name__', getattr(func, 'name', str(func)))
        
        # 记录输入
        logger.info(f"[{function_name}] Starting execution")
        logger.debug(f"[{function_name}] Input args: {args}")
        logger.debug(f"[{function_name}] Input kwargs: {kwargs}")
        
        try:
            # 执行函数
            result = func(*args, **kwargs)
            
            # 计算执行时间
            execution_time = time.time() - start_time
            
            # 记录输出
            logger.info(f"[{function_name}] Completed successfully in {execution_time:.3f}s")
            
            # 如果结果是JSON字符串，尝试解析并记录关键信息
            try:
                if isinstance(result, str):
                    result_data = json.loads(result)
                    if "error" in result_data:
                        logger.warning(f"[{function_name}] Function returned error: {result_data['error']}")
                    else:
                        logger.debug(f"[{function_name}] Result keys: {list(result_data.keys()) if isinstance(result_data, dict) else 'non-dict result'}")
            except (json.JSONDecodeError, TypeError):
                logger.debug(f"[{function_name}] Result type: {type(result).__name__}")
            
            # 确保最终返回的是JSON字符串
            if isinstance(result, str):
                try:
                    # 如果已经是json，直接返回
                    json.loads(result)
                    return result
                except (json.JSONDecodeError, TypeError):
                    # 如果不是有效的json，则包装它
                    pass
            
            return json.dumps(result, ensure_ascii=False, indent=4)
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"[{function_name}] Failed after {execution_time:.3f}s with error: {repr(e)}")
            
            # 为batch_crawl_tool返回特殊的错误结构
            if function_name == 'batch_crawl_tool' and len(args) > 0:
                try:
                    urls = args[0] if args else []
                    if isinstance(urls, list):
                        return {
                            "total_urls": len(urls),
                            "successful": 0,
                            "failed": len(urls),
                            "error": str(e),
                            "results": [],
                            "timestamp": datetime.now().isoformat()
                        }
                except:
                    pass
            
            # 为mystery_site_crawler返回特殊的错误结构
            if function_name == 'mystery_site_crawler' and len(args) > 0:
                try:
                    site_type = args[0] if args else "unknown"
                    search_terms = args[1] if len(args) > 1 else []
                    return {
                        "site_type": site_type,
                        "search_terms": search_terms,
                        "total_results": 0,
                        "error": str(e),
                        "results": []
                    }
                except:
                    pass
            
            # 返回通用错误结果
            error_result = {
                "error": str(e),
                "function": function_name,
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            }
            return error_result
    
    return wrapper


def create_logged_tool(tool_class):
    """创建带有日志记录的工具类工厂
    
    Args:
        tool_class: 要包装的工具类
        
    Returns:
        包装后的工具类工厂函数
    """
    class LoggedToolWrapper(tool_class):
        """带有日志记录的工具包装类"""
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            # 包装_run方法
            original_run = super()._run
            self._run = log_io(original_run)
            
            # 包装_arun方法（如果存在）
            if hasattr(super(), '_arun'):
                original_arun = super()._arun
                async def logged_arun(*args, **kwargs):
                    return await log_io(original_arun)(*args, **kwargs)
                self._arun = logged_arun
        
        def invoke(self, query, *args, **kwargs):
            """统一的invoke方法"""
            if hasattr(super(), 'invoke'):
                original_invoke = super().invoke
                return log_io(original_invoke)(query, *args, **kwargs)
            else:
                # 如果没有invoke方法，调用_run
                return self._run(query, *args, **kwargs)
    
    def create_instance(*args, **kwargs):
        return LoggedToolWrapper(*args, **kwargs)
    
    return create_instance


def performance_monitor(threshold_seconds: float = 1.0):
    """装饰器：监控函数性能，当执行时间超过阈值时发出警告
    
    Args:
        threshold_seconds: 性能警告阈值（秒）
        
    Returns:
        装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            function_name = getattr(func, '__name__', getattr(func, 'name', str(func)))
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                if execution_time > threshold_seconds:
                    logger.warning(
                        f"[PERFORMANCE] {function_name} took {execution_time:.3f}s "
                        f"(threshold: {threshold_seconds}s)"
                    )
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(
                    f"[PERFORMANCE] {function_name} failed after {execution_time:.3f}s: {repr(e)}"
                )
                raise
        
        return wrapper
    return decorator


def retry_on_failure(max_retries: int = 3, delay_seconds: float = 1.0, backoff_factor: float = 2.0):
    """装饰器：在失败时重试函数执行
    
    Args:
        max_retries: 最大重试次数
        delay_seconds: 初始延迟时间（秒）
        backoff_factor: 退避因子
        
    Returns:
        装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            function_name = getattr(func, '__name__', getattr(func, 'name', str(func)))
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    if attempt > 0:
                        delay = delay_seconds * (backoff_factor ** (attempt - 1))
                        logger.info(f"[RETRY] {function_name} attempt {attempt + 1}/{max_retries + 1} after {delay:.1f}s delay")
                        time.sleep(delay)
                    
                    return func(*args, **kwargs)
                    
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(f"[RETRY] {function_name} attempt {attempt + 1} failed: {repr(e)}")
                    else:
                        logger.error(f"[RETRY] {function_name} all {max_retries + 1} attempts failed")
            
            # 所有重试都失败了，抛出最后一个异常
            if last_exception is not None:
                raise last_exception
            else:
                raise RuntimeError(f"{function_name} failed but no exception was captured.")
        
        return wrapper
    return decorator


def validate_input(validation_func: Callable[[Any], bool], error_message: str = "Invalid input"):
    """装饰器：验证函数输入
    
    Args:
        validation_func: 验证函数，返回True表示验证通过
        error_message: 验证失败时的错误消息
        
    Returns:
        装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            function_name = getattr(func, '__name__', getattr(func, 'name', str(func)))
            
            try:
                # 验证输入
                if not validation_func(*args, **kwargs):
                    logger.error(f"[VALIDATION] {function_name} input validation failed: {error_message}")
                    error_result = {
                        "error": error_message,
                        "function": function_name,
                        "validation_failed": True,
                        "timestamp": datetime.now().isoformat()
                    }
                    return error_result
                
                return func(*args, **kwargs)
                
            except Exception as e:
                logger.error(f"[VALIDATION] {function_name} validation error: {repr(e)}")
                error_result = {
                    "error": f"Validation error: {str(e)}",
                    "function": function_name,
                    "validation_error": True,
                    "timestamp": datetime.now().isoformat()
                }
                return error_result
        
        return wrapper
    return decorator


def cache_result(duration: int = 3600):
    """Decorator to cache the result of a function for a specified duration.

    Args:
        duration: Cache duration in seconds.
    """
    cache = {}
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            function_name = getattr(func, '__name__', getattr(func, 'name', str(func)))
            
            # 创建缓存键
            cache_key = f"{function_name}_{hash(str(args) + str(sorted(kwargs.items())))}"
            current_time = time.time()
            
            # 检查缓存
            if cache_key in cache:
                cached_result, cached_time = cache[cache_key]
                if current_time - cached_time < duration:
                    logger.debug(f"[CACHE] {function_name} returning cached result")
                    return cached_result
                else:
                    # 缓存过期，删除
                    del cache[cache_key]
                    logger.debug(f"[CACHE] {function_name} cache expired")
            
            # 执行函数并缓存结果
            result = func(*args, **kwargs)
            cache[cache_key] = (result, current_time)
            logger.debug(f"[CACHE] {function_name} result cached")
            
            return result
        
        return wrapper
    return decorator


def rate_limit(calls: int = 30, period: int = 60):
    """Decorator to limit the call rate of a function.

    Args:
        calls (int): The number of calls allowed within the period.
        period (int): The time period in seconds.

    Returns:
        Callable: The decorated function.
    """
    def decorator(func: Callable) -> Callable:
        call_times = []
        lock = threading.Lock()

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            function_name = getattr(func, '__name__', getattr(func, 'name', str(func)))
            with lock:
                current_time = time.time()
                # Remove calls older than the period
                call_times[:] = [t for t in call_times if t > current_time - period]

                if len(call_times) >= calls:
                    # Calculate wait time based on the oldest timestamp in the current window
                    time_to_wait = (call_times[0] + period) - current_time
                    if time_to_wait > 0:
                        logger.warning(
                            f"[RATE_LIMIT] Rate limit reached for {function_name}. "
                            f"Waiting for {time_to_wait:.2f}s"
                        )
                        time.sleep(time_to_wait)
                
                call_times.append(time.time())
            
            return func(*args, **kwargs)

        return wrapper
    return decorator


def sanitize_output(sanitize_func: Optional[Callable[[Any], Any]] = None):
    """装饰器：清理函数输出
    
    Args:
        sanitize_func: 清理函数，如果为None则使用默认清理
        
    Returns:
        装饰器函数
    """
    def default_sanitize(result: Any) -> Any:
        """默认清理函数"""
        if isinstance(result, str):
            try:
                # 尝试解析JSON并移除敏感信息
                data = json.loads(result)
                if isinstance(data, dict):
                    # 移除可能的敏感字段
                    sensitive_keys = ['password', 'token', 'key', 'secret', 'api_key']
                    for key in sensitive_keys:
                        if key in data:
                            data[key] = "[REDACTED]"
                
                return data
            except (json.JSONDecodeError, TypeError):
                return result
        
        return result
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)
            
            # 应用清理函数
            sanitizer = sanitize_func or default_sanitize
            sanitized_result = sanitizer(result)
            
            return sanitized_result
        
        return wrapper
    return decorator


def measure_memory_usage(func: Callable) -> Callable:
    """装饰器：测量函数内存使用情况
    
    Args:
        func: 要装饰的函数
        
    Returns:
        装饰后的函数
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        function_name = getattr(func, '__name__', getattr(func, 'name', str(func)))
        
        try:
            import psutil
            import os
            
            # 获取当前进程
            process = psutil.Process(os.getpid())
            
            # 记录执行前的内存使用
            memory_before = process.memory_info().rss / 1024 / 1024  # MB
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 记录执行后的内存使用
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            memory_diff = memory_after - memory_before
            
            if abs(memory_diff) > 10:  # 如果内存变化超过10MB则记录
                logger.info(
                    f"[MEMORY] {function_name} memory usage: "
                    f"before={memory_before:.1f}MB, after={memory_after:.1f}MB, "
                    f"diff={memory_diff:+.1f}MB"
                )
            
            return result
            
        except ImportError:
            # psutil不可用，直接执行函数
            logger.debug(f"[MEMORY] psutil not available for {function_name}")
            return func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"[MEMORY] Failed to measure memory for {function_name}: {repr(e)}")
            return func(*args, **kwargs)
    
    return wrapper


def mystery_tool(event_type: Optional[Any] = None, tool_config: Optional[Dict] = None):
    """Decorator to add mystery event handling to a tool, including keyword enhancement.

    Args:
        event_type: The mystery event type associated with the tool (can be Enum or string).
        tool_config: Configuration dictionary with keywords.

    Returns:
        A decorator function.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Convert Enum args to their string values for processing
            processed_args = [arg.name if isinstance(arg, Enum) else arg for arg in args]
            processed_kwargs = {k: v.name if isinstance(v, Enum) else v for k, v in kwargs.items()}

            # 1. Get the query string
            query = ""
            if processed_args:
                query = processed_args[0]
            elif 'query' in processed_kwargs:
                query = processed_kwargs['query']

            # 2. Enhance the query based on the event type
            event_name = None
            if 'event_type' in processed_kwargs:
                event_param = processed_kwargs['event_type']
                event_name = event_param.name if isinstance(event_param, Enum) else str(event_param)
            elif event_type:
                event_name = event_type.name if isinstance(event_type, Enum) else str(event_type)

            if event_name and tool_config and 'keywords' in tool_config:
                keywords = tool_config['keywords'].get(event_name, [])
                if keywords:
                    enhanced_query = f"{query} {' '.join(keywords)}".strip()

                    # Update the query argument
                    if processed_args:
                        processed_args[0] = enhanced_query
                    else:
                        processed_kwargs['query'] = enhanced_query

                    logger.info(f"[{func.__name__}] Enhanced query for {event_name}: {enhanced_query}")

            # Execute the original function with processed arguments
            result = func(*processed_args, **processed_kwargs)

            # 3. Wrap the result in a JSON object if it's not already a valid JSON string
            if isinstance(result, str):
                try:
                    json.loads(result)
                    return result  # It's already a valid JSON string
                except (json.JSONDecodeError, TypeError):
                    pass  # Not a valid JSON string, will be wrapped below

            return json.dumps(result, ensure_ascii=False, indent=4)
            
        return wrapper
    return decorator