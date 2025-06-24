# SPDX-License-Identifier: MIT

import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
import time

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from crawler.jina_client import JinaClient


class TestJinaClient:
    """Jina客户端测试类"""
    
    @pytest.fixture
    def client(self):
        """创建客户端实例"""
        return JinaClient(api_key="test_key", timeout=10, max_retries=2)
    
    @pytest.fixture
    def client_no_key(self):
        """创建无API密钥的客户端实例"""
        with patch.dict(os.environ, {}, clear=True):
            return JinaClient()
    
    def test_init_with_api_key(self, client):
        """测试带API密钥的初始化"""
        assert client.api_key == "test_key"
        assert client.timeout == 10
        assert client.max_retries == 2
        assert client.session is not None
    
    def test_init_without_api_key(self, client_no_key):
        """测试无API密钥的初始化"""
        assert client_no_key.api_key is None
        assert client_no_key.timeout == 30  # 默认值
        assert client_no_key.max_retries == 3  # 默认值
    
    @patch.dict(os.environ, {'JINA_API_KEY': 'env_test_key'})
    def test_init_with_env_api_key(self):
        """测试从环境变量获取API密钥"""
        client = JinaClient()
        assert client.api_key == "env_test_key"
    
    def test_crawl_success(self, client):
        """测试成功爬取"""
        mock_response = Mock()
        mock_response.text = "<html><body>Test content</body></html>"
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client.session, 'post', return_value=mock_response) as mock_post:
            result = client.crawl("https://example.com")
            
            assert result == "<html><body>Test content</body></html>"
            mock_post.assert_called_once()
            
            # 检查请求参数
            call_args = mock_post.call_args
            assert call_args[0][0] == "https://r.jina.ai/"
            assert "Authorization" in call_args[1]['headers']
            assert call_args[1]['json']['url'] == "https://example.com"
    
    def test_crawl_with_options(self, client):
        """测试带选项的爬取"""
        mock_response = Mock()
        mock_response.text = "Test content"
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client.session, 'post', return_value=mock_response) as mock_post:
            result = client.crawl(
                "https://example.com",
                return_format="markdown",
                include_links=True,
                include_images=False,
                target_selector=".content",
                wait_for_selector=".loaded",
                headers={"Custom-Header": "value"}
            )
            
            assert result == "Test content"
            
            # 检查请求参数
            call_args = mock_post.call_args
            headers = call_args[1]['headers']
            json_data = call_args[1]['json']
            
            assert headers['X-Return-Format'] == 'markdown'
            assert headers['Custom-Header'] == 'value'
            assert json_data['include_links'] == True
            assert json_data['include_images'] == False
            assert json_data['target_selector'] == '.content'
            assert json_data['wait_for_selector'] == '.loaded'
    
    def test_crawl_without_api_key(self, client_no_key):
        """测试无API密钥的爬取"""
        mock_response = Mock()
        mock_response.text = "Test content"
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client_no_key.session, 'post', return_value=mock_response) as mock_post:
            result = client_no_key.crawl("https://example.com")
            
            assert result == "Test content"
            
            # 检查请求头中没有Authorization
            call_args = mock_post.call_args
            headers = call_args[1]['headers']
            assert "Authorization" not in headers
    
    def test_crawl_request_exception(self, client):
        """测试请求异常"""
        with patch.object(client.session, 'post', side_effect=requests.exceptions.RequestException("Network error")):
            with pytest.raises(requests.exceptions.RequestException):
                client.crawl("https://example.com")
    
    def test_crawl_http_error(self, client):
        """测试HTTP错误"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        
        with patch.object(client.session, 'post', return_value=mock_response):
            with pytest.raises(requests.exceptions.HTTPError):
                client.crawl("https://example.com")
    
    def test_crawl_multiple_success(self, client):
        """测试批量爬取成功"""
        mock_response = Mock()
        mock_response.text = "Test content"
        mock_response.raise_for_status.return_value = None
        
        urls = ["https://example1.com", "https://example2.com"]
        
        with patch.object(client.session, 'post', return_value=mock_response):
            with patch('time.sleep') as mock_sleep:  # 模拟sleep以加速测试
                results = client.crawl_multiple(urls, delay=0.1)
                
                assert len(results) == 2
                assert results["https://example1.com"] == "Test content"
                assert results["https://example2.com"] == "Test content"
                mock_sleep.assert_called_once_with(0.1)
    
    def test_crawl_multiple_with_errors(self, client):
        """测试批量爬取部分失败"""
        def side_effect(*args, **kwargs):
            url = kwargs['json']['url']
            if "error" in url:
                raise requests.exceptions.RequestException("Error")
            
            mock_response = Mock()
            mock_response.text = f"Content for {url}"
            mock_response.raise_for_status.return_value = None
            return mock_response
        
        urls = ["https://example.com", "https://error.com", "https://success.com"]
        
        with patch.object(client.session, 'post', side_effect=side_effect):
            with patch('time.sleep'):  # 模拟sleep
                results = client.crawl_multiple(urls, delay=0)
                
                assert len(results) == 3
                assert "Content for https://example.com" in results["https://example.com"]
                assert results["https://error.com"] == ""  # 失败的URL返回空字符串
                assert "Content for https://success.com" in results["https://success.com"]
    
    def test_crawl_with_fallback_success_first_try(self, client):
        """测试回退机制 - 第一次尝试成功"""
        mock_response = Mock()
        mock_response.text = "HTML content"
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client.session, 'post', return_value=mock_response):
            content, format_used = client.crawl_with_fallback("https://example.com", return_format="html")
            
            assert content == "HTML content"
            assert format_used == "html"
    
    def test_crawl_with_fallback_success_second_try(self, client):
        """测试回退机制 - 第二次尝试成功"""
        def side_effect(*args, **kwargs):
            headers = kwargs.get('headers', {})
            return_format = headers.get('X-Return-Format', 'html')
            
            if return_format == 'html':
                raise requests.exceptions.RequestException("HTML failed")
            
            mock_response = Mock()
            mock_response.text = "Text content"
            mock_response.raise_for_status.return_value = None
            return mock_response
        
        with patch.object(client.session, 'post', side_effect=side_effect):
            content, format_used = client.crawl_with_fallback(
                "https://example.com", 
                return_format="html",
                fallback_formats=["text"]
            )
            
            assert content == "Text content"
            assert format_used == "text"
    
    def test_crawl_with_fallback_all_fail(self, client):
        """测试回退机制 - 全部失败"""
        with patch.object(client.session, 'post', side_effect=requests.exceptions.RequestException("All failed")):
            with pytest.raises(Exception, match="Failed to crawl .* with all attempted formats"):
                client.crawl_with_fallback(
                    "https://example.com",
                    return_format="html",
                    fallback_formats=["text", "markdown"]
                )
    
    def test_test_connection_success(self, client):
        """测试连接测试成功"""
        mock_response = Mock()
        mock_response.text = "Test"
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client.session, 'post', return_value=mock_response):
            result = client.test_connection()
            assert result == True
    
    def test_test_connection_failure(self, client):
        """测试连接测试失败"""
        with patch.object(client.session, 'post', side_effect=requests.exceptions.RequestException("Connection failed")):
            result = client.test_connection()
            assert result == False
    
    def test_get_rate_limit_info_success(self, client):
        """测试获取速率限制信息成功"""
        mock_response = Mock()
        mock_response.headers = {
            'X-Rate-Limit-Remaining': '100',
            'X-Rate-Limit-Reset': '3600',
            'Content-Type': 'application/json'
        }
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client.session, 'post', return_value=mock_response):
            info = client.get_rate_limit_info()
            
            assert 'X-Rate-Limit-Remaining' in info
            assert 'X-Rate-Limit-Reset' in info
            assert 'Content-Type' not in info  # 不包含非速率限制相关的头
    
    def test_get_rate_limit_info_failure(self, client):
        """测试获取速率限制信息失败"""
        with patch.object(client.session, 'post', side_effect=requests.exceptions.RequestException("Failed")):
            info = client.get_rate_limit_info()
            assert info == {}
    
    def test_close(self, client):
        """测试关闭会话"""
        mock_session = Mock()
        client.session = mock_session
        
        client.close()
        
        mock_session.close.assert_called_once()
    
    def test_session_retry_configuration(self, client):
        """测试会话重试配置"""
        # 检查会话是否正确配置了重试适配器
        assert client.session is not None
        
        # 检查HTTP和HTTPS适配器
        http_adapter = client.session.get_adapter('http://example.com')
        https_adapter = client.session.get_adapter('https://example.com')
        
        assert http_adapter is not None
        assert https_adapter is not None
    
    def test_request_headers_construction(self, client):
        """测试请求头构建"""
        mock_response = Mock()
        mock_response.text = "Test"
        mock_response.raise_for_status.return_value = None
        
        custom_headers = {"User-Agent": "Custom Agent", "Accept": "text/html"}
        
        with patch.object(client.session, 'post', return_value=mock_response) as mock_post:
            client.crawl(
                "https://example.com",
                return_format="markdown",
                headers=custom_headers
            )
            
            call_args = mock_post.call_args
            headers = call_args[1]['headers']
            
            # 检查基本头部
            assert headers['Content-Type'] == 'application/json'
            assert headers['X-Return-Format'] == 'markdown'
            assert headers['Authorization'] == 'Bearer test_key'
            
            # 检查自定义头部
            assert headers['User-Agent'] == 'Custom Agent'
            assert headers['Accept'] == 'text/html'
    
    def test_json_data_construction(self, client):
        """测试JSON数据构建"""
        mock_response = Mock()
        mock_response.text = "Test"
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client.session, 'post', return_value=mock_response) as mock_post:
            client.crawl(
                "https://example.com",
                include_links=True,
                include_images=False,
                target_selector=".main",
                wait_for_selector=".loaded"
            )
            
            call_args = mock_post.call_args
            json_data = call_args[1]['json']
            
            assert json_data['url'] == 'https://example.com'
            assert json_data['include_links'] == True
            assert json_data['include_images'] == False
            assert json_data['target_selector'] == '.main'
            assert json_data['wait_for_selector'] == '.loaded'
    
    def test_timeout_configuration(self):
        """测试超时配置"""
        client = JinaClient(timeout=15)
        assert client.timeout == 15
        
        mock_response = Mock()
        mock_response.text = "Test"
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client.session, 'post', return_value=mock_response) as mock_post:
            client.crawl("https://example.com")
            
            call_args = mock_post.call_args
            assert call_args[1]['timeout'] == 15
    
    def test_crawl_multiple_no_delay(self, client):
        """测试批量爬取无延迟"""
        mock_response = Mock()
        mock_response.text = "Test content"
        mock_response.raise_for_status.return_value = None
        
        urls = ["https://example1.com", "https://example2.com"]
        
        with patch.object(client.session, 'post', return_value=mock_response):
            with patch('time.sleep') as mock_sleep:
                results = client.crawl_multiple(urls, delay=0)
                
                assert len(results) == 2
                mock_sleep.assert_not_called()  # 无延迟时不应调用sleep
    
    def test_fallback_formats_default(self, client):
        """测试默认回退格式"""
        with patch.object(client, 'crawl', side_effect=Exception("Failed")) as mock_crawl:
            with pytest.raises(Exception):
                client.crawl_with_fallback("https://example.com")
            
            # 检查调用了默认的回退格式
            expected_calls = [
                ("https://example.com",),  # 第一次调用（主格式）
                ("https://example.com",),  # text格式
                ("https://example.com",)   # markdown格式
            ]
            
            assert mock_crawl.call_count == 3
            for i, call in enumerate(mock_crawl.call_args_list):
                assert call[0][0] == "https://example.com"