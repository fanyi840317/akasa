# # SPDX-License-Identifier: MIT
# 
# import pytest
# from unittest.mock import patch, AsyncMock
# from src.crawler.crawler import Crawler, RateLimiter
# from src.config.config import DataSourceConfig, DataSourceType
# from src.rag.retriever import Document
# 
# # 创建一个具体的爬虫子类用于测试
# class ConcreteCrawler(Crawler):
#     async def search(self, query: str, limit: int = 10):
#         return [Document(id="test_id", content=f"Search result for {query}")]
# 
#     async def crawl_url(self, url: str):
#         return Document(id=url, content=f"Crawled content from {url}")
# 
# class TestCrawler:
#     @pytest.fixture
#     def config(self):
#         return DataSourceConfig(
#             name="test_source",
#             source_type=DataSourceType.NEWS,
#             base_url="https://example.com",
#             rate_limit=10
#         )
# 
#     @pytest.fixture
#     def crawler(self, config):
#         return ConcreteCrawler(config)
# 
#     def test_init(self, crawler, config):
#         assert crawler.config == config
#         assert isinstance(crawler.rate_limiter, RateLimiter)
#         assert crawler.rate_limiter.rate_limit == config.rate_limit
# 
#     @pytest.mark.asyncio
#     async def test_batch_crawl(self, crawler):
#         urls = ["http://example.com/1", "http://example.com/2"]
#         with patch.object(crawler, 'crawl_url', new_callable=AsyncMock) as mock_crawl_url:
#             mock_crawl_url.side_effect = lambda url: Document(id=url, content=f"content for {url}")
#             
#             results = await crawler.batch_crawl(urls)
#             
#             assert len(results) == 2
#             assert mock_crawl_url.call_count == 2
# 
#     @pytest.mark.asyncio
#     async def test_fetch_html(self, crawler):
#         with patch('aiohttp.ClientSession.get') as mock_get:
#             mock_response = AsyncMock()
#             mock_response.status = 200
#             mock_response.text.return_value = "<html></html>"
#             mock_get.return_value.__aenter__.return_value = mock_response
# 
#             html = await crawler._fetch_html("http://example.com")
#             assert html == "<html></html>"
# 
#     def test_create_document_from_html(self, crawler):
#         html = "<html><body><h1>Title</h1><p>Paragraph 1.</p><p>Paragraph 2.</p></body></html>"
#         url = "http://example.com/page"
#         doc = crawler._create_document_from_html(html, url)
# 
#         assert isinstance(doc, Document)
#         assert doc.title == "Title"
#         assert "Paragraph 1." in doc.content
# 
#     def test_extract_text_from_html(self, crawler):
#         html = "<html><head><style>.a{color:red}</style><script>alert(1)</script></head><body><p>Hello</p></body></html>"
#         text = crawler._extract_text_from_html(html)
#         assert text == "Hello"
# 
#     def test_clean_text(self, crawler):
#         text = "  Hello\nWorld  \t "
#         cleaned_text = crawler._clean_text(text)
#         assert cleaned_text == "Hello World"
# 
#     def test_is_valid_url(self, crawler):
#         assert crawler._is_valid_url("http://example.com")
#         assert not crawler._is_valid_url("ftp://example.com")
#         assert not crawler._is_valid_url("javascript:alert(1)")