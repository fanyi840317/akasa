# Copyright (c) 2024 Lingjing
# SPDX-License-Identifier: MIT

import pytest
import asyncio
from unittest.mock import MagicMock, patch



from src.crawler.academic_crawler import AcademicCrawler
from src.crawler.news_crawler import NewsCrawler
from src.crawler.mystery_crawler import MysteryCrawler
from src.config.config import DataSourceConfig, DataSourceType

# Fixtures for configuration
@pytest.fixture
def academic_config():
    return DataSourceConfig(
        name="Semantic Scholar",
        base_url="https://api.semanticscholar.org",
        source_type=DataSourceType.ACADEMIC
    )

@pytest.fixture
def news_config():
    # IMPORTANT: Replace with a valid NewsAPI key for this test to run
    return DataSourceConfig(
        name="NewsAPI",
        base_url="https://newsapi.org",
        source_type=DataSourceType.NEWS
    )

@pytest.fixture
def mystery_config():
    # IMPORTANT: Replace with valid Google Custom Search API key and CSE ID
    return DataSourceConfig(
        name="Google Custom Search",
        base_url="https://www.googleapis.com/customsearch/v1",
        source_type=DataSourceType.MYSTERY
    )

# Test Cases
@pytest.mark.asyncio
async def test_academic_crawler_search(academic_config):
    """Test the real search functionality of AcademicCrawler."""
    crawler = AcademicCrawler(academic_config)
    query = "artificial intelligence"
    
    # We patch the crawl_url to avoid actual HTTP requests to article pages during the test
    with patch.object(crawler, 'crawl_url', new_callable=MagicMock) as mock_crawl:
        mock_crawl.return_value = None # Simulate no document found from URL
        documents = await crawler.search(query, limit=2)
        
        # Assert that the search method was called and it tried to crawl URLs from results
        assert mock_crawl.call_count > 0
        # We can't easily assert documents content as it depends on live API, 
        # but we can check if the process runs without errors.
        assert isinstance(documents, list)

    await crawler.close_session()

@pytest.mark.asyncio
async def test_news_crawler_search(news_config):
    """Test the real search functionality of NewsCrawler."""
    if news_config.api_key == "YOUR_NEWS_API_KEY":
        pytest.skip("NewsAPI key not provided. Skipping test.")

    crawler = NewsCrawler(news_config)
    query = "space exploration"

    with patch.object(crawler, 'crawl_url', new_callable=MagicMock) as mock_crawl:
        mock_crawl.return_value = None
        documents = await crawler.search(query, limit=2)
        
        assert mock_crawl.call_count > 0
        assert isinstance(documents, list)

    await crawler.close_session()

@pytest.mark.asyncio
async def test_mystery_crawler_search(mystery_config):
    """Test the real search functionality of MysteryCrawler."""
    if mystery_config.api_key == "YOUR_GOOGLE_API_KEY" or mystery_config.cse_id == "YOUR_CSE_ID":
        pytest.skip("Google Custom Search API key or CSE ID not provided. Skipping test.")

    crawler = MysteryCrawler(mystery_config)
    query = "UFO sightings 2023"

    with patch.object(crawler, 'crawl_url', new_callable=MagicMock) as mock_crawl:
        mock_crawl.return_value = None
        documents = await crawler.search(query, limit=2)
        
        assert mock_crawl.call_count > 0
        assert isinstance(documents, list)

    await crawler.close_session()