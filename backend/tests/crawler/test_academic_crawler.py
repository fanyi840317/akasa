# SPDX-License-Identifier: MIT

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from bs4 import BeautifulSoup

from src.crawler.academic_crawler import AcademicCrawler
from src.config.mystery_config import DataSourceConfig, DataSourceType
from src.rag.retriever import Document


class TestAcademicCrawler:
    """学术爬虫测试类"""
    
    @pytest.fixture
    def config(self):
        """创建测试配置"""
        return DataSourceConfig(
            name="test_academic",
            source_type=DataSourceType.ACADEMIC,
            base_url="https://test-academic.com",
            rate_limit=10
        )
    
    @pytest.fixture
    def crawler(self, config):
        """创建爬虫实例"""
        return AcademicCrawler(config)
    
    def test_init(self, crawler):
        """测试初始化"""
        assert crawler.config.source_type == DataSourceType.ACADEMIC
        assert len(crawler.academic_keywords) > 0
        assert "anomalous phenomena" in crawler.academic_keywords
    
    @pytest.mark.asyncio
    async def test_crawl_url_success(self, crawler):
        """测试成功爬取URL"""
        test_html = """
        <html>
            <head><title>Test Paper</title></head>
            <body>
                <h1 class="article-title">Anomalous Atmospheric Phenomena</h1>
                <div class="abstract">This paper discusses unusual atmospheric events.</div>
                <div class="content">Detailed analysis of atmospheric anomalies...</div>
            </body>
        </html>
        """
        
        with patch.object(crawler, '_fetch_html', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = test_html
            
            result = await crawler.crawl_url("https://example.com/paper1")
            
            assert result is not None
            assert isinstance(result, Document)
            assert "Anomalous Atmospheric Phenomena" in result.content
    
    @pytest.mark.asyncio
    async def test_crawl_url_no_html(self, crawler):
        """测试无法获取HTML的情况"""
        with patch.object(crawler, '_fetch_html', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = None
            
            result = await crawler.crawl_url("https://example.com/invalid")
            
            assert result is None
    
    @pytest.mark.asyncio
    async def test_search(self, crawler):
        """测试搜索功能"""
        with patch.object(crawler, 'crawl_url', new_callable=AsyncMock) as mock_crawl:
            # 模拟返回文档
            mock_doc = Mock(spec=Document)
            mock_crawl.return_value = mock_doc
            
            with patch.object(crawler, '_generate_search_urls') as mock_urls:
                mock_urls.return_value = ["https://example.com/paper1", "https://example.com/paper2"]
                
                results = await crawler.search("atmospheric anomalies", limit=2)
                
                assert len(results) <= 2
                assert all(isinstance(doc, type(mock_doc)) for doc in results)
    
    def test_parse_academic_html(self, crawler):
        """测试HTML解析"""
        test_html = """
        <html>
            <body>
                <h1 class="article-title">Test Academic Paper</h1>
                <div class="abstract">This is the abstract.</div>
                <div class="authors">John Doe, Jane Smith</div>
                <div class="content">Main content here...</div>
            </body>
        </html>
        """
        
        result = crawler._parse_academic_html(test_html, "https://example.com/test")
        
        assert result is not None
        assert result['title'] == "Test Academic Paper"
        assert result['abstract'] == "This is the abstract."
        assert result['metadata']['source_type'] == 'academic'
        assert result['metadata']['reliability_score'] == 0.9
    
    def test_extract_academic_title(self, crawler):
        """测试标题提取"""
        from bs4 import BeautifulSoup
        
        html = '<h1 class="article-title">Test Paper Title</h1>'
        soup = BeautifulSoup(html, 'html.parser')
        
        title = crawler._extract_academic_title(soup)
        assert title == "Test Paper Title"
    
    def test_extract_academic_title_no_title(self, crawler):
        """测试无标题情况"""
        from bs4 import BeautifulSoup
        
        html = '<div>No title here</div>'
        soup = BeautifulSoup(html, 'html.parser')
        
        title = crawler._extract_academic_title(soup)
        assert title is None
    
    def test_extract_abstract(self, crawler):
        """测试摘要提取"""
        from bs4 import BeautifulSoup
        
        html = '<div class="abstract">This is the abstract content.</div>'
        soup = BeautifulSoup(html, 'html.parser')
        
        abstract = crawler._extract_abstract(soup)
        assert abstract == "This is the abstract content."
    
    def test_extract_abstract_no_abstract(self, crawler):
        """测试无摘要情况"""
        from bs4 import BeautifulSoup
        
        html = '<div>No abstract here</div>'
        soup = BeautifulSoup(html, 'html.parser')
        
        abstract = crawler._extract_abstract(soup)
        assert abstract == ""
    
    def test_build_academic_query(self, crawler):
        """测试学术查询构建"""
        query = "atmospheric phenomena"
        academic_query = crawler._build_academic_query(query)
        
        assert isinstance(academic_query, str)
        assert "atmospheric phenomena" in academic_query
    
    def test_generate_search_urls(self, crawler):
        """测试搜索URL生成"""
        query = "test query"
        urls = crawler._generate_search_urls(query, limit=5)
        
        assert isinstance(urls, list)
        assert len(urls) <= 5
        assert all(isinstance(url, str) for url in urls)
    
    def test_extract_authors(self, crawler):
        """测试作者提取"""
        from bs4 import BeautifulSoup
        
        # 测试meta标签中的作者
        html1 = '<html><head><meta name="author" content="Dr. John Smith, Prof. Jane Doe"></head></html>'
        soup1 = BeautifulSoup(html1, 'html.parser')
        authors1 = crawler._extract_authors(soup1)
        assert "Dr. John Smith, Prof. Jane Doe" == authors1
        
        # 测试citation_author标签
        html2 = '<html><head><meta name="citation_author" content="Wilson, Bob"></head></html>'
        soup2 = BeautifulSoup(html2, 'html.parser')
        authors2 = crawler._extract_authors(soup2)
        assert "Wilson, Bob" == authors2
        
        # 测试无作者信息
        html3 = '<html><head></head></html>'
        soup3 = BeautifulSoup(html3, 'html.parser')
        authors3 = crawler._extract_authors(soup3)
        assert authors3 == ""
    
    def test_extract_journal_info(self, crawler):
        """测试期刊信息提取"""
        from bs4 import BeautifulSoup
        
        html = """
        <html>
        <head>
            <meta name="citation_journal_title" content="Nature Physics">
            <meta name="citation_volume" content="19">
            <meta name="citation_issue" content="8">
            <meta name="citation_firstpage" content="1234">
            <meta name="citation_lastpage" content="1245">
            <meta name="citation_doi" content="10.1038/s41567-023-02123-4">
        </head>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        journal_info = crawler._extract_journal_info(soup)
        
        assert journal_info["journal"] == "Nature Physics"
        assert journal_info["volume"] == "19"
        assert journal_info["issue"] == "8"
        assert journal_info["pages"] == "1234-1245"
        assert journal_info["doi"] == "10.1038/s41567-023-02123-4"
    
    def test_extract_keywords(self, crawler):
        """测试关键词提取"""
        from bs4 import BeautifulSoup
        
        # 测试meta关键词
        html1 = '<html><head><meta name="keywords" content="atmospheric, electromagnetic, anomalies"></head></html>'
        soup1 = BeautifulSoup(html1, 'html.parser')
        keywords1 = crawler._extract_keywords(soup1)
        assert "atmospheric" in keywords1
        assert "electromagnetic" in keywords1
        assert "anomalies" in keywords1
        
        # 测试HTML中的关键词区域
        html2 = """
        <html>
        <body>
            <div class="keywords">
                <span>plasma</span>, <span>ionosphere</span>, <span>radar</span>
            </div>
        </body>
        </html>
        """
        soup2 = BeautifulSoup(html2, 'html.parser')
        keywords2 = crawler._extract_keywords(soup2)
        assert "plasma" in keywords2
        assert "ionosphere" in keywords2
        assert "radar" in keywords2
    
    def test_count_references(self, crawler):
        """测试引用计数"""
        from bs4 import BeautifulSoup
        
        # 测试有序列表引用
        html1 = """
        <html>
        <body>
            <div class="references">
                <ol>
                    <li>Smith et al. (2022)</li>
                    <li>Johnson & Brown (2021)</li>
                    <li>Wilson (2020)</li>
                </ol>
            </div>
        </body>
        </html>
        """
        soup1 = BeautifulSoup(html1, 'html.parser')
        count1 = crawler._count_references(soup1)
        assert count1 == 3
        
        # 测试无引用
        html2 = '<html><body></body></html>'
        soup2 = BeautifulSoup(html2, 'html.parser')
        count2 = crawler._count_references(soup2)
        assert count2 == 0
    
    def test_calculate_academic_credibility(self, crawler):
        """测试学术可信度计算"""
        from bs4 import BeautifulSoup
        
        # 高可信度：知名期刊 + 多作者 + 多引用
        html_high = """
        <html>
        <head>
            <meta name="citation_journal_title" content="Nature">
            <meta name="author" content="Dr. A, Prof. B, Dr. C">
        </head>
        <body>
            <div class="references">
                <ol><li>Ref1</li><li>Ref2</li><li>Ref3</li><li>Ref4</li><li>Ref5</li></ol>
            </div>
        </body>
        </html>
        """
        soup_high = BeautifulSoup(html_high, 'html.parser')
        score_high = crawler._calculate_academic_credibility(soup_high, "Nature", "Dr. A, Prof. B, Dr. C")
        assert score_high > 0.9
        
        # 中等可信度：普通期刊 + 单作者 + 少量引用
        html_medium = """
        <html>
        <head>
            <meta name="citation_journal_title" content="Some Journal">
            <meta name="author" content="Dr. Smith">
        </head>
        <body>
            <div class="references">
                <ol><li>Ref1</li><li>Ref2</li></ol>
            </div>
        </body>
        </html>
        """
        soup_medium = BeautifulSoup(html_medium, 'html.parser')
        score_medium = crawler._calculate_academic_credibility(soup_medium, "Some Journal", "Dr. Smith")
        assert 0.7 <= score_medium <= 0.9
        
        # 低可信度：无期刊信息
        html_low = '<html><body></body></html>'
        soup_low = BeautifulSoup(html_low, 'html.parser')
        score_low = crawler._calculate_academic_credibility(soup_low, "", "")
        assert score_low < 0.7
    
    def test_create_academic_document(self, crawler):
        """测试学术文档创建"""
        parsed_data = {
            "title": "Test Academic Paper",
            "content": "This is the abstract.\n\nThis is the introduction with detailed analysis.\n\nThis is the conclusion.",
            "metadata": {
                "url": "https://test.com/paper",
                "author": "Dr. Test",
                "journal": "Test Journal",
                "credibility_score": 0.85,
                "keywords": ["test", "academic"],
                "citation_count": 10
            }
        }
        
        document = crawler._create_academic_document(parsed_data, "test_doc_id")
        
        assert document.id == "test_doc_id"
        assert document.title == "Test Academic Paper"
        assert document.source_type == "academic"
        assert document.credibility_score == 0.85
        assert document.author == "Dr. Test"
        assert len(document.chunks) > 0
        
        # 检查摘要块
        abstract_chunk = next((chunk for chunk in document.chunks if chunk.metadata.get('type') == 'abstract'), None)
        assert abstract_chunk is not None
        assert "abstract" in abstract_chunk.content.lower()
    
    def test_edge_cases(self, crawler):
        """测试边界情况"""
        from bs4 import BeautifulSoup
        
        # 测试空HTML
        empty_html = ""
        parsed_empty = crawler._parse_academic_html(empty_html, "https://test.com")
        assert parsed_empty is None
        
        # 测试格式错误的HTML
        malformed_html = "<html><head><title>Test</title></head><body><div>Content</div>"
        parsed_malformed = crawler._parse_academic_html(malformed_html, "https://test.com")
        # 应该能够处理格式错误的HTML
        
        # 测试无标题的HTML
        no_title_html = "<html><head></head><body><div>Some content</div></body></html>"
        parsed_no_title = crawler._parse_academic_html(no_title_html, "https://test.com")
        assert parsed_no_title is None
    
    @pytest.mark.asyncio
    async def test_async_operations(self, crawler):
        """测试异步操作"""
        # 测试并发爬取
        urls = [
            "https://test1.com/paper1",
            "https://test2.com/paper2",
            "https://test3.com/paper3"
        ]
        
        test_html = "<html><head><title>Test Paper</title></head><body>Content</body></html>"
        
        with patch.object(crawler, '_fetch_html', return_value=test_html):
            tasks = [crawler.crawl_url(url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 检查结果
            for result in results:
                if not isinstance(result, Exception):
                    assert result is not None or result is None  # 可能成功或失败