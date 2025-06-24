# -*- coding: utf-8 -*-
# Copyright (c) 2024 Lingjing
# SPDX-License-Identifier: MIT
import sys
from pathlib import Path
backend_path = str((Path(__file__).parent.parent.parent).resolve())
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)
    
import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from requests.exceptions import RequestException, Timeout, HTTPError

from src.tools.crawl import (
    MysteryWebCrawler,
    crawl_tool,
    batch_crawl_tool,
    mystery_site_crawler
)


class TestMysteryWebCrawler:
    """测试MysteryWebCrawler类"""
    
    def test_crawler_init(self):
        """测试爬虫初始化"""
        crawler = MysteryWebCrawler()
        assert crawler.session is not None
        assert 'User-Agent' in crawler.session.headers
        assert 'Mozilla' in crawler.session.headers['User-Agent']
    
    @patch('requests.Session.get')
    def test_extract_content_success(self, mock_get):
        """测试成功提取内容"""
        # 模拟成功的HTTP响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"Test content"
        mock_response.headers = {
            'content-type': 'text/html',
            'last-modified': 'Wed, 01 Jan 2024 12:00:00 GMT'
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        crawler = MysteryWebCrawler()
        result = crawler.extract_content("https://example.com")
        
        assert result["url"] == "https://example.com"
        assert "title" in result
        assert "text" in result
        assert "metadata" in result
        assert result["metadata"]["status_code"] == 200
        assert result["metadata"]["content_type"] == 'text/html'
        assert result["metadata"]["content_length"] == len(b"Test content")
        assert "timestamp" in result
        assert result["timestamp"] is not None
        
        mock_get.assert_called_once_with("https://example.com", timeout=30)
    
    @patch('requests.Session.get')
    def test_extract_content_with_custom_timeout(self, mock_get):
        """测试自定义超时时间"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"Test content"
        mock_response.headers = {}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        crawler = MysteryWebCrawler()
        result = crawler.extract_content("https://example.com", timeout=60)
        
        assert "url" in result
        mock_get.assert_called_once_with("https://example.com", timeout=60)
    
    @patch('requests.Session.get')
    def test_extract_content_request_exception(self, mock_get):
        """测试请求异常处理"""
        mock_get.side_effect = RequestException("Network error")
        
        crawler = MysteryWebCrawler()
        result = crawler.extract_content("https://example.com")
        
        assert result["url"] == "https://example.com"
        assert "error" in result
        assert "Network error" in result["error"]
        assert "timestamp" in result
    
    @patch('requests.Session.get')
    def test_extract_content_timeout(self, mock_get):
        """测试超时异常"""
        mock_get.side_effect = Timeout("Request timeout")
        
        crawler = MysteryWebCrawler()
        result = crawler.extract_content("https://example.com")
        
        assert "error" in result
        assert "Request timeout" in result["error"]
    
    @patch('requests.Session.get')
    def test_extract_content_http_error(self, mock_get):
        """测试HTTP错误"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        crawler = MysteryWebCrawler()
        result = crawler.extract_content("https://example.com")
        
        assert "error" in result
        assert "404 Not Found" in result["error"]
    
    @patch('requests.Session.get')
    def test_extract_content_metadata_parsing(self, mock_get):
        """测试元数据解析"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"<html><body>Test content</body></html>"
        mock_response.headers = {
            'content-type': 'text/html; charset=utf-8',
            'last-modified': 'Wed, 01 Jan 2024 12:00:00 GMT',
            'content-length': '100'
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        crawler = MysteryWebCrawler()
        result = crawler.extract_content("https://example.com")
        
        metadata = result["metadata"]
        assert metadata["status_code"] == 200
        assert metadata["content_type"] == 'text/html; charset=utf-8'
        assert metadata["last_modified"] == 'Wed, 01 Jan 2024 12:00:00 GMT'
        assert isinstance(metadata["content_length"], int)
    
    @patch.object(MysteryWebCrawler, 'extract_content')
    def test_batch_crawl_success(self, mock_extract):
        """测试批量爬取成功"""
        # 模拟extract_content的返回值
        mock_extract.side_effect = [
            {"url": "https://example1.com", "title": "Page 1", "text": "Content 1"},
            {"url": "https://example2.com", "title": "Page 2", "text": "Content 2"},
            {"url": "https://example3.com", "title": "Page 3", "text": "Content 3"}
        ]
        
        crawler = MysteryWebCrawler()
        urls = ["https://example1.com", "https://example2.com", "https://example3.com"]
        results = crawler.batch_crawl(urls)
        
        assert len(results) == 3
        assert results[0]["url"] == "https://example1.com"
        assert results[1]["title"] == "Page 2"
        assert results[2]["text"] == "Content 3"
        assert mock_extract.call_count == 3
    
    @patch.object(MysteryWebCrawler, 'extract_content')
    def test_batch_crawl_with_errors(self, mock_extract):
        """测试批量爬取包含错误"""
        # 模拟部分成功，部分失败
        mock_extract.side_effect = [
            {"url": "https://example1.com", "title": "Page 1", "text": "Content 1"},
            Exception("Network error"),
            {"url": "https://example3.com", "title": "Page 3", "text": "Content 3"}
        ]
        
        crawler = MysteryWebCrawler()
        urls = ["https://example1.com", "https://example2.com", "https://example3.com"]
        results = crawler.batch_crawl(urls)
        
        assert len(results) == 3
        assert results[0]["url"] == "https://example1.com"
        assert "error" in results[1]
        assert "Network error" in results[1]["error"]
        assert results[2]["url"] == "https://example3.com"
    
    def test_batch_crawl_empty_urls(self):
        """测试空URL列表的批量爬取"""
        crawler = MysteryWebCrawler()
        results = crawler.batch_crawl([])
        
        assert results == []
    
    @patch.object(MysteryWebCrawler, 'extract_content')
    def test_batch_crawl_max_workers_parameter(self, mock_extract):
        """测试max_workers参数"""
        mock_extract.return_value = {"url": "test", "content": "test"}
        
        crawler = MysteryWebCrawler()
        urls = ["https://example1.com", "https://example2.com"]
        
        # 测试不同的max_workers值
        results1 = crawler.batch_crawl(urls, max_workers=1)
        results2 = crawler.batch_crawl(urls, max_workers=10)
        
        assert len(results1) == 2
        assert len(results2) == 2


class TestCrawlTool:
    """测试crawl_tool函数"""
    
    @patch('src.tools.crawl._crawler.extract_content')
    def test_crawl_tool_success(self, mock_extract):
        """测试爬取工具成功"""
        mock_extract.return_value = {
            "url": "https://example.com",
            "title": "Test Page",
            "text": "Test content",
            "metadata": {"status_code": 200}
        }
        
        result = crawl_tool("https://example.com")
        
        assert result["url"] == "https://example.com"
        assert result["title"] == "Test Page"
        assert result["metadata"]["extract_links"] is False
        assert result["metadata"]["extract_images"] is False
        mock_extract.assert_called_once_with("https://example.com", 30)
    
    @patch('src.tools.crawl._crawler.extract_content')
    def test_crawl_tool_with_options(self, mock_extract):
        """测试带选项的爬取工具"""
        mock_extract.return_value = {
            "url": "https://example.com",
            "title": "Test Page",
            "metadata": {}
        }
        
        result = crawl_tool(
            "https://example.com",
            extract_links=True,
            extract_images=True,
            timeout=60
        )
        
        assert result["metadata"]["extract_links"] is True
        assert result["metadata"]["extract_images"] is True
        mock_extract.assert_called_once_with("https://example.com", 60)
    
    @patch('src.tools.crawl._crawler.extract_content')
    def test_crawl_tool_exception(self, mock_extract):
        """测试爬取工具异常处理"""
        mock_extract.side_effect = Exception("Crawl error")
        
        result = crawl_tool("https://example.com")
        
        assert result["url"] == "https://example.com"
        assert "error" in result
        assert "Crawl error" in result["error"]
        assert "timestamp" in result
    
    @patch('src.tools.crawl._crawler.extract_content')
    def test_crawl_tool_no_metadata(self, mock_extract):
        """测试没有metadata的情况"""
        mock_extract.return_value = {
            "url": "https://example.com",
            "title": "Test Page"
        }
        
        result = crawl_tool("https://example.com")
        
        assert "metadata" in result
        assert result["metadata"]["extract_links"] is False
        assert result["metadata"]["extract_images"] is False


class TestBatchCrawlTool:
    """测试batch_crawl_tool函数"""
    
    @patch('src.tools.crawl._crawler.batch_crawl')
    def test_batch_crawl_tool_success(self, mock_batch_crawl):
        """测试批量爬取工具成功"""
        mock_batch_crawl.return_value = [
            {"url": "https://example1.com", "title": "Page 1"},
            {"url": "https://example2.com", "title": "Page 2"},
            {"url": "https://example3.com", "error": "Failed"}
        ]
        
        urls = ["https://example1.com", "https://example2.com", "https://example3.com"]
        result = batch_crawl_tool(urls)
        
        assert result["total_urls"] == 3
        assert result["successful"] == 2
        assert result["failed"] == 1
        assert len(result["results"]) == 3
        mock_batch_crawl.assert_called_once_with(urls, 5)
    
    @patch('src.tools.crawl._crawler.batch_crawl')
    def test_batch_crawl_tool_with_options(self, mock_batch_crawl):
        """测试带选项的批量爬取工具"""
        mock_batch_crawl.return_value = []
        
        urls = ["https://example1.com", "https://example2.com"]
        result = batch_crawl_tool(urls, max_workers=10, timeout=60)
        
        assert result["total_urls"] == 2
        assert result["successful"] == 0
        assert result["failed"] == 0
        mock_batch_crawl.assert_called_once_with(urls, 10)
    
    @patch('src.tools.crawl._crawler.batch_crawl')
    def test_batch_crawl_tool_exception(self, mock_batch_crawl):
        """测试批量爬取工具异常处理"""
        mock_batch_crawl.side_effect = Exception("Batch crawl error")
        
        urls = ["https://example1.com", "https://example2.com"]
        result = batch_crawl_tool(urls)
        
        assert result["total_urls"] == 2
        assert result["successful"] == 0
        assert result["failed"] == 2
        assert "error" in result
        assert "Batch crawl error" in result["error"]
        assert result["results"] == []
    
    def test_batch_crawl_tool_empty_urls(self):
        """测试空URL列表"""
        result = batch_crawl_tool([])
        
        assert result["total_urls"] == 0
        assert result["successful"] == 0
        assert result["failed"] == 0
        assert result["results"] == []
    
    @patch('tools.crawl._crawler.batch_crawl')
    def test_batch_crawl_tool_all_successful(self, mock_batch_crawl):
        """测试全部成功的批量爬取"""
        mock_batch_crawl.return_value = [
            {"url": "https://example1.com", "title": "Page 1"},
            {"url": "https://example2.com", "title": "Page 2"}
        ]
        
        urls = ["https://example1.com", "https://example2.com"]
        result = batch_crawl_tool(urls)
        
        assert result["total_urls"] == 2
        assert result["successful"] == 2
        assert result["failed"] == 0
    
    @patch('tools.crawl._crawler.batch_crawl')
    def test_batch_crawl_tool_all_failed(self, mock_batch_crawl):
        """测试全部失败的批量爬取"""
        mock_batch_crawl.return_value = [
            {"url": "https://example1.com", "error": "Error 1"},
            {"url": "https://example2.com", "error": "Error 2"}
        ]
        
        urls = ["https://example1.com", "https://example2.com"]
        result = batch_crawl_tool(urls)
        
        assert result["total_urls"] == 2
        assert result["successful"] == 0
        assert result["failed"] == 2


class TestMysterySiteCrawler:
    """测试mystery_site_crawler函数"""
    
    def test_mystery_site_crawler_ufo(self):
        """测试UFO网站爬取"""
        result = mystery_site_crawler("ufo", ["sighting", "abduction"], max_pages=2)
        
        assert result["site_type"] == "ufo"
        assert result["search_terms"] == ["sighting", "abduction"]
        assert "total_results" in result
        assert "results" in result
        assert len(result["results"]) > 0
        
        # 检查结果格式
        for item in result["results"]:
            assert "url" in item
            assert "title" in item
            assert "text" in item
            assert "site_type" in item
            assert "search_term" in item
            assert "relevance_score" in item
            assert "timestamp" in item
    
    def test_mystery_site_crawler_paranormal(self):
        """测试超自然网站爬取"""
        result = mystery_site_crawler("paranormal", ["ghost", "haunting"])
        
        assert result["site_type"] == "paranormal"
        assert result["search_terms"] == ["ghost", "haunting"]
        assert len(result["results"]) > 0
    
    def test_mystery_site_crawler_cryptid(self):
        """测试神秘生物网站爬取"""
        result = mystery_site_crawler("cryptid", ["bigfoot", "yeti"])
        
        assert result["site_type"] == "cryptid"
        assert result["search_terms"] == ["bigfoot", "yeti"]
        assert len(result["results"]) > 0
    
    def test_mystery_site_crawler_ancient(self):
        """测试古代谜团网站爬取"""
        result = mystery_site_crawler("ancient", ["pyramid", "atlantis"])
        
        assert result["site_type"] == "ancient"
        assert result["search_terms"] == ["pyramid", "atlantis"]
        assert len(result["results"]) > 0
    
    def test_mystery_site_crawler_unknown_type(self):
        """测试未知网站类型"""
        result = mystery_site_crawler("unknown", ["test"])
        
        assert "error" in result
        assert "Unknown site type" in result["error"]
        assert result["results"] == []
    
    def test_mystery_site_crawler_empty_search_terms(self):
        """测试空搜索词"""
        result = mystery_site_crawler("ufo", [])
        
        assert result["site_type"] == "ufo"
        assert result["search_terms"] == []
        assert result["total_results"] == 0
        assert result["results"] == []
    
    def test_mystery_site_crawler_max_pages_limit(self):
        """测试最大页面限制"""
        result = mystery_site_crawler("ufo", ["test"], max_pages=1)
        
        # 由于mock实现，结果数量应该等于 min(sites, max_pages) * search_terms
        # UFO有2个网站，但max_pages=1，所以只处理1个网站
        expected_results = 1 * 1  # 1个网站 * 1个搜索词
        assert result["total_results"] == expected_results
    
    def test_mystery_site_crawler_result_structure(self):
        """测试结果结构"""
        result = mystery_site_crawler("ufo", ["test"], max_pages=1)
        
        assert "site_type" in result
        assert "search_terms" in result
        assert "total_results" in result
        assert "results" in result
        
        if result["results"]:
            item = result["results"][0]
            required_fields = [
                "url", "title", "text", "site_type", 
                "search_term", "relevance_score", "timestamp"
            ]
            for field in required_fields:
                assert field in item
            
            assert isinstance(item["relevance_score"], (int, float))
            assert item["site_type"] == "ufo"
            assert item["search_term"] == "test"
    
    @patch('tools.crawl.logger')
    def test_mystery_site_crawler_exception_handling(self, mock_logger):
        """测试异常处理"""
        # 通过修改datetime模块来触发异常
        with patch('tools.crawl.datetime') as mock_datetime:
            mock_datetime.now.side_effect = Exception("DateTime error")
            
            result = mystery_site_crawler("ufo", ["test"])
            
            assert "error" in result
            assert "DateTime error" in result["error"]
            assert result["results"] == []
            mock_logger.error.assert_called()


class TestCrawlIntegration:
    """测试爬虫集成功能"""
    
    @patch('requests.Session.get')
    def test_full_crawl_workflow(self, mock_get):
        """测试完整的爬取工作流"""
        # 模拟HTTP响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"<html><body>Test content</body></html>"
        mock_response.headers = {'content-type': 'text/html'}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # 测试单个URL爬取
        single_result = crawl_tool("https://example.com")
        assert single_result["url"] == "https://example.com"
        assert "error" not in single_result
        
        # 测试批量爬取
        urls = ["https://example1.com", "https://example2.com"]
        batch_result = batch_crawl_tool(urls)
        assert batch_result["total_urls"] == 2
        assert batch_result["successful"] == 2
        assert batch_result["failed"] == 0
    
    def test_mystery_site_integration(self):
        """测试神秘网站爬取集成"""
        # 测试不同类型的神秘网站
        site_types = ["ufo", "paranormal", "cryptid", "ancient"]
        
        for site_type in site_types:
            result = mystery_site_crawler(site_type, ["test"], max_pages=1)
            assert result["site_type"] == site_type
            assert "results" in result
            assert "total_results" in result
    
    @patch('requests.Session.get')
    def test_error_recovery(self, mock_get):
        """测试错误恢复"""
        # 模拟网络错误
        mock_get.side_effect = RequestException("Network error")
        
        # 单个URL爬取应该返回错误信息而不是崩溃
        result = crawl_tool("https://example.com")
        assert "error" in result
        assert "Network error" in result["error"]
        
        # 批量爬取应该处理错误并继续
        urls = ["https://example1.com", "https://example2.com"]
        batch_result = batch_crawl_tool(urls)
        assert batch_result["total_urls"] == 2
        assert batch_result["failed"] == 2
        assert batch_result["successful"] == 0
    
    def test_tool_decorators(self):
        """测试工具装饰器"""
        # 验证所有工具函数都有正确的装饰器
        assert hasattr(crawl_tool, '__wrapped__')  # mystery_tool装饰器
        assert hasattr(batch_crawl_tool, '__wrapped__')  # mystery_tool装饰器
        assert hasattr(mystery_site_crawler, '__wrapped__')  # mystery_tool装饰器
        
        # 验证工具函数可以正常调用
        result1 = crawl_tool("https://example.com")
        result2 = batch_crawl_tool(["https://example.com"])
        result3 = mystery_site_crawler("ufo", ["test"])
        
        assert isinstance(result1, dict)
        assert isinstance(result2, dict)
        assert isinstance(result3, dict)