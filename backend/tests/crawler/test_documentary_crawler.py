# SPDX-License-Identifier: MIT

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.crawler.documentary_crawler import DocumentaryCrawler
from src.config.config import DataSourceConfig, DataSourceType
from src.rag.retriever import Document

@pytest.fixture
def config():
    """Provides a mock DataSourceConfig for tests."""
    mock_config = MagicMock(spec=DataSourceConfig)
    mock_config.source_type = DataSourceType.DOCUMENTARY
    mock_config.reliability_score = 0.7
    mock_config.search_url = "https://example.com/search?q={query}"
    mock_config.headers = {"User-Agent": "Test-Crawler"}
    return mock_config

@pytest.fixture
def crawler(config):
    """Creates a DocumentaryCrawler instance with a mock config."""
    return DocumentaryCrawler(config)

class TestDocumentaryCrawler:

    @pytest.fixture
    def sample_documentary_html(self):
        """Example documentary HTML with a video element."""
        return """
        <html>
            <head><title>UFOs: The Hidden Truth</title></head>
            <body>
                <h1>UFOs: The Hidden Truth</h1>
                <p>An in-depth look at UFO phenomena.</p>
                <video>
                    <source src="/videos/ufo_doc.mp4" type="video/mp4">
                </video>
            </body>
        </html>
        """

    @pytest.fixture
    def non_documentary_html(self):
        """Example HTML of a non-documentary page."""
        return """
        <html>
            <head><title>Just a Normal Page</title></head>
            <body><p>This is a standard article.</p></body>
        </html>
        """

    def test_initialization(self, crawler, config):
        """Tests if the crawler is initialized correctly."""
        assert crawler.config == config
        assert crawler.selectors is not None
        assert 'video_container' in crawler.selectors

    @pytest.mark.asyncio
    async def test_is_documentary_page(self, crawler, sample_documentary_html, non_documentary_html):
        """Tests the documentary page detection logic."""
        assert crawler._is_documentary_page(sample_documentary_html) is True
        assert crawler._is_documentary_page(non_documentary_html) is False

    @pytest.mark.asyncio
    async def test_parse_html_for_documentary(self, crawler, sample_documentary_html):
        """Tests parsing a valid documentary page."""
        parsed_data = crawler._parse_html(sample_documentary_html, "https://example.com/doc")
        assert parsed_data is not None
        assert "UFOs: The Hidden Truth" in parsed_data['title']
        assert "/videos/ufo_doc.mp4" in parsed_data['metadata']['video_url']
        assert parsed_data['metadata']['mystery_type'] == 'UFO'

    @pytest.mark.asyncio
    async def test_parse_html_for_non_documentary(self, crawler, non_documentary_html):
        """Tests that non-documentary pages are skipped."""
        parsed_data = crawler._parse_html(non_documentary_html, "https://example.com/article")
        assert parsed_data is None

    def test_calculate_credibility(self, crawler):
        """Tests the credibility calculation logic."""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup("<html><body><p>Expert interview</p></body></html>", "html.parser")
        
        # With a good video URL and expert keywords
        score1 = crawler._calculate_documentary_credibility(soup, "https://youtube.com/watch?v=123")
        assert score1 > crawler.config.reliability_score

        # Without a video URL
        score2 = crawler._calculate_documentary_credibility(soup, None)
        assert score2 < crawler.config.reliability_score

    @pytest.mark.asyncio
    async def test_create_document_structure(self, crawler, sample_documentary_html):
        """Tests the structure of the created Document object."""
        parsed_data = crawler._parse_html(sample_documentary_html, "https://example.com/doc")
        document = crawler._create_document(parsed_data)

        assert isinstance(document, Document)
        assert document.title == "UFOs: The Hidden Truth"
        assert any(c.metadata.get('type') == 'video_link' for c in document.chunks)
        assert any(c.metadata.get('type') == 'mystery_type' for c in document.chunks)