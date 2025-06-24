# SPDX-License-Identifier: MIT

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from abc import ABC

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from crawler.crawler import Crawler
from config.mystery_config import DataSourceConfig, DataSourceType
from rag.retriever import Document


class ConcreteCrawler(Crawler):
    """具体的爬虫实现，用于测试抽象基类"""
    
    async def crawl_url(self, url: str):
        """实现抽象方法"""
        return Mock(spec=Document)
    
    async def search(self, query: str, limit: int = 10):
        """实现抽象方法"""
        return [Mock(spec=Document) for _ in range(min(limit, 3))]


class TestCrawler:
    """爬虫基类测试"""
    
    @pytest.fixture
    def config(self):
        """创建测试配置"""
        return DataSourceConfig(
            name="test_crawler",
            source_type=DataSourceType.NEWS,
            base_url="https://example.com",
            headers={"User-Agent": "test-agent"}
        )
    
    @pytest.fixture
    def crawler(self, config):
        """创建爬虫实例"""
        return ConcreteCrawler(config)
    
    def test_init(self, crawler, config):
        """测试初始化"""
        assert crawler.config == config
        assert crawler.logger is not None
        assert crawler.session is None
    
    @pytest.mark.asyncio
    async def test_context_manager(self, crawler):
        """测试异步上下文管理器"""
        async with crawler as c:
            assert c.session is not None
            assert c is crawler
        
        # 退出后session应该被关闭
        assert crawler.session is not None  # session对象仍存在但已关闭
    
    @pytest.mark.asyncio
    async def test_batch_crawl(self, crawler):
        """测试批量爬取"""
        urls = [
            "https://example.com/page1",
            "https://example.com/page2",
            "https://example.com/page3"
        ]
        
        with patch.object(crawler, 'crawl_url', new_callable=AsyncMock) as mock_crawl:
            mock_crawl.return_value = Mock(spec=Document)
            
            results = await crawler.batch_crawl(urls)
            
            assert len(results) == len(urls)
            assert mock_crawl.call_count == len(urls)
            assert all(isinstance(doc, type(Mock(spec=Document))) for doc in results)
    
    @pytest.mark.asyncio
    async def test_batch_crawl_with_failures(self, crawler):
        """测试批量爬取时部分失败"""
        urls = [
            "https://example.com/page1",
            "https://example.com/page2",
            "https://example.com/page3"
        ]
        
        with patch.object(crawler, 'crawl_url', new_callable=AsyncMock) as mock_crawl:
            # 模拟第二个URL失败
            mock_crawl.side_effect = [
                Mock(spec=Document),
                None,  # 失败返回None
                Mock(spec=Document)
            ]
            
            results = await crawler.batch_crawl(urls)
            
            # 应该过滤掉None结果
            assert len(results) == 2
            assert mock_crawl.call_count == len(urls)
    
    @pytest.mark.asyncio
    async def test_fetch_html_success(self, crawler):
        """测试成功获取HTML"""
        test_html = "<html><body>Test content</body></html>"
        
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = AsyncMock()
            mock_response.text = AsyncMock(return_value=test_html)
            mock_response.status = 200
            mock_get.return_value.__aenter__.return_value = mock_response
            
            async with crawler:
                html = await crawler._fetch_html("https://example.com/test")
                
                assert html == test_html
    
    @pytest.mark.asyncio
    async def test_fetch_html_failure(self, crawler):
        """测试获取HTML失败"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 404
            mock_get.return_value.__aenter__.return_value = mock_response
            
            async with crawler:
                html = await crawler._fetch_html("https://example.com/notfound")
                
                assert html is None
    
    @pytest.mark.asyncio
    async def test_fetch_html_exception(self, crawler):
        """测试获取HTML时发生异常"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            async with crawler:
                html = await crawler._fetch_html("https://example.com/error")
                
                assert html is None
    
    def test_create_document(self, crawler):
        """测试创建文档"""
        parsed_data = {
            'title': 'Test Title',
            'content': 'Test content',
            'metadata': {
                'url': 'https://example.com/test',
                'source_type': 'news'
            }
        }
        doc_id = "test_doc_id"
        
        document = crawler._create_document(parsed_data, doc_id)
        
        assert isinstance(document, Document)
        assert document.id == doc_id
        assert "Test Title" in document.content
        assert "Test content" in document.content
    
    def test_extract_text_from_html(self, crawler):
        """测试从HTML提取文本"""
        html = "<html><body><h1>Title</h1><p>Paragraph content</p></body></html>"
        
        text = crawler._extract_text_from_html(html)
        
        assert "Title" in text
        assert "Paragraph content" in text
        assert "<h1>" not in text  # HTML标签应该被移除
    
    def test_clean_text(self, crawler):
        """测试文本清理"""
        dirty_text = "  This   has    extra   spaces\n\n\nand\tlines  "
        
        clean_text = crawler._clean_text(dirty_text)
        
        assert clean_text == "This has extra spaces and lines"
    
    def test_is_valid_url(self, crawler):
        """测试URL验证"""
        valid_urls = [
            "https://example.com",
            "http://test.org/path",
            "https://subdomain.example.com/path?query=value"
        ]
        
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",
            "",
            None
        ]
        
        for url in valid_urls:
            assert crawler._is_valid_url(url), f"Should be valid: {url}"
        
        for url in invalid_urls:
            assert not crawler._is_valid_url(url), f"Should be invalid: {url}"
    
    def test_get_domain(self, crawler):
        """测试域名提取"""
        test_cases = [
            ("https://example.com/path", "example.com"),
            ("http://subdomain.test.org", "subdomain.test.org"),
            ("https://example.com:8080/path", "example.com")
        ]
        
        for url, expected_domain in test_cases:
            domain = crawler._get_domain(url)
            assert domain == expected_domain
    
    def test_calculate_credibility_score(self, crawler):
        """测试可信度分数计算"""
        metadata = {
            'source_type': 'academic',
            'author': 'Dr. Test',
            'publication_date': '2023-01-01',
            'citations_count': 10
        }
        
        score = crawler._calculate_credibility_score(metadata)
        
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
    
    def test_abstract_methods_enforcement(self):
        """测试抽象方法强制实现"""
        # 尝试直接实例化抽象类应该失败
        with pytest.raises(TypeError):
            Crawler(Mock())
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self, crawler):
        """测试速率限制"""
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            await crawler._apply_rate_limit()
            
            # 应该调用sleep进行延迟
            mock_sleep.assert_called_once()
    
    def test_parse_robots_txt(self, crawler):
        """测试robots.txt解析"""
        robots_content = """
        User-agent: *
        Disallow: /private/
        Allow: /public/
        Crawl-delay: 1
        """
        
        rules = crawler._parse_robots_txt(robots_content)
        
        assert isinstance(rules, dict)
        assert 'disallow' in rules
        assert 'allow' in rules
        assert 'crawl_delay' in rules
    
    def test_should_crawl_url(self, crawler):
        """测试是否应该爬取URL"""
        # 模拟robots.txt规则
        crawler._robots_rules = {
            'disallow': ['/private/'],
            'allow': ['/public/']
        }
        
        assert crawler._should_crawl_url("https://example.com/public/page")
        assert not crawler._should_crawl_url("https://example.com/private/page")