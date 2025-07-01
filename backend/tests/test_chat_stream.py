# SPDX-License-Identifier: MIT

import pytest
import json
import sys
import os
from unittest.mock import patch, AsyncMock, MagicMock
import httpx
from fastapi import FastAPI

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from server.app import app
from server.chat_request import ChatRequest, ChatMessage
from src.config.report_style import ReportStyle


class TestChatStream:
    """测试chat stream接口"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        # 使用 httpx.AsyncClient 来测试 FastAPI 应用
        self.app = app
        self.base_url = "/api/chat/stream"
    
    @pytest.mark.asyncio
    async def test_chat_stream_basic_request(self):
        """测试基本的chat stream请求"""
        # 准备测试数据
        test_request = {
            "messages": [
                {
                    "role": "user",
                    "content": "Hello, this is a test message"
                }
            ],
            "thread_id": "test-thread-123",
            "resources": [],
            "max_plan_iterations": 1,
            "max_step_num": 3,
            "max_search_results": 3,
            "auto_accepted_plan": False,
            "interrupt_feedback": None,
            "mcp_settings": None,
            "enable_background_investigation": True,
            "report_style": "academic",
            "enable_deep_thinking": False
        }
        
        # Mock _astream_workflow_generator to avoid actual workflow execution
        with patch('server.routes.chat._astream_workflow_generator') as mock_generator:
            # Mock generator to yield some test data
            async def mock_async_generator(*args, **kwargs):
                yield "data: {\"type\": \"message\", \"content\": \"Test response\"}\n\n"
                yield "data: {\"type\": \"end\"}\n\n"
            
            mock_generator.return_value = mock_async_generator()
            
            # 使用 httpx.AsyncClient 发送请求
            async with httpx.AsyncClient(app=self.app, base_url="http://test") as client:
                response = await client.post(
                    self.base_url,
                    json=test_request,
                    headers={"Content-Type": "application/json"}
                )
                
                # 验证响应
                assert response.status_code == 200
                assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
                
                # 验证mock被调用
                mock_generator.assert_called_once()
    
    def test_chat_stream_default_thread_id(self):
        """测试默认thread_id的处理"""
        test_request = {
            "messages": [
                {
                    "role": "user",
                    "content": "Test with default thread"
                }
            ],
            "thread_id": "__default__"
        }
        
        with patch('server.routes.chat._astream_workflow_generator') as mock_generator:
            with patch('server.routes.chat.uuid4') as mock_uuid:
                mock_uuid.return_value = "generated-uuid-123"
                
                async def mock_async_generator(*args, **kwargs):
                    yield "data: {\"type\": \"test\"}\n\n"
                
                mock_generator.return_value = mock_async_generator()
                
                response = self.client.post(
                    self.base_url,
                    json=test_request
                )
                
                assert response.status_code == 200
                # 验证uuid4被调用来生成新的thread_id
                mock_uuid.assert_called_once()
    
    def test_chat_stream_with_resources(self):
        """测试包含resources的请求"""
        test_request = {
            "messages": [
                {
                    "role": "user",
                    "content": "Search with resources"
                }
            ],
            "resources": [
                {
                    "uri": "https://example.com",
                    "title": "Test Resource",
                    "description": "A test resource"
                }
            ],
            "thread_id": "test-with-resources"
        }
        
        with patch('server.routes.chat._astream_workflow_generator') as mock_generator:
            async def mock_async_generator(*args, **kwargs):
                yield "data: {\"type\": \"resource_used\"}\n\n"
            
            mock_generator.return_value = mock_async_generator()
            
            response = self.client.post(
                self.base_url,
                json=test_request
            )
            
            assert response.status_code == 200
            # 验证resources参数被正确传递
            call_args = mock_generator.call_args
            assert len(call_args[0]) >= 3  # 至少有messages, thread_id, resources参数
    
    def test_chat_stream_with_interrupt_feedback(self):
        """测试包含interrupt_feedback的请求"""
        test_request = {
            "messages": [
                {
                    "role": "user",
                    "content": "Test with feedback"
                }
            ],
            "thread_id": "test-feedback",
            "interrupt_feedback": "Please modify the plan",
            "auto_accepted_plan": False
        }
        
        with patch('server.routes.chat._astream_workflow_generator') as mock_generator:
            async def mock_async_generator(*args, **kwargs):
                yield "data: {\"type\": \"feedback_processed\"}\n\n"
            
            mock_generator.return_value = mock_async_generator()
            
            response = self.client.post(
                self.base_url,
                json=test_request
            )
            
            assert response.status_code == 200
    
    def test_chat_stream_invalid_json(self):
        """测试无效JSON请求"""
        response = self.client.post(
            self.base_url,
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_chat_stream_missing_required_fields(self):
        """测试缺少必需字段的请求"""
        # ChatRequest的所有字段都是Optional，所以空请求应该也能工作
        test_request = {}
        
        with patch('server.routes.chat._astream_workflow_generator') as mock_generator:
            async def mock_async_generator(*args, **kwargs):
                yield "data: {\"type\": \"empty_request\"}\n\n"
            
            mock_generator.return_value = mock_async_generator()
            
            response = self.client.post(
                self.base_url,
                json=test_request
            )
            
            assert response.status_code == 200
    
    def test_chat_stream_complex_message_content(self):
        """测试复杂的消息内容（包含图片等）"""
        test_request = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this image"
                        },
                        {
                            "type": "image",
                            "image_url": "https://example.com/image.jpg"
                        }
                    ]
                }
            ],
            "thread_id": "test-complex-content"
        }
        
        with patch('server.routes.chat._astream_workflow_generator') as mock_generator:
            async def mock_async_generator(*args, **kwargs):
                yield "data: {\"type\": \"image_analyzed\"}\n\n"
            
            mock_generator.return_value = mock_async_generator()
            
            response = self.client.post(
                self.base_url,
                json=test_request
            )
            
            assert response.status_code == 200
    
    def test_chat_stream_all_parameters(self):
        """测试包含所有参数的完整请求"""
        test_request = {
            "messages": [
                {
                    "role": "user",
                    "content": "Complete test with all parameters"
                }
            ],
            "resources": [
                {
                    "uri": "https://example.com/doc1",
                    "title": "Document 1",
                    "description": "First document"
                },
                {
                    "uri": "https://example.com/doc2",
                    "title": "Document 2",
                    "description": "Second document"
                }
            ],
            "debug": True,
            "thread_id": "complete-test-thread",
            "max_plan_iterations": 2,
            "max_step_num": 5,
            "max_search_results": 10,
            "auto_accepted_plan": True,
            "interrupt_feedback": "Detailed feedback",
            "mcp_settings": {
                "setting1": "value1",
                "setting2": "value2"
            },
            "enable_background_investigation": False,
            "report_style": "technical",
            "enable_deep_thinking": True
        }
        
        with patch('server.routes.chat._astream_workflow_generator') as mock_generator:
            async def mock_async_generator(*args, **kwargs):
                yield "data: {\"type\": \"complete_test\"}\n\n"
            
            mock_generator.return_value = mock_async_generator()
            
            response = self.client.post(
                self.base_url,
                json=test_request
            )
            
            assert response.status_code == 200
            
            # 验证所有参数都被正确传递给_astream_workflow_generator
            call_args = mock_generator.call_args[0]
            assert len(call_args) == 12  # 应该有12个参数
    
    @patch('server.routes.chat._astream_workflow_generator')
    def test_chat_stream_generator_exception(self, mock_generator):
        """测试生成器抛出异常的情况"""
        async def failing_generator(*args, **kwargs):
            yield "data: {\"type\": \"start\"}\n\n"
            raise Exception("Generator failed")
        
        mock_generator.return_value = failing_generator()
        
        test_request = {
            "messages": [
                {
                    "role": "user",
                    "content": "Test exception handling"
                }
            ],
            "thread_id": "exception-test"
        }
        
        # 这个测试可能需要根据实际的错误处理逻辑进行调整
        response = self.client.post(
            self.base_url,
            json=test_request
        )
        
        # 根据FastAPI的StreamingResponse行为，可能返回200但流中断
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])