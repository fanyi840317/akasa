# Copyright (c) 2024 Lingjing
# SPDX-License-Identifier: MIT

import pytest
from unittest.mock import MagicMock, patch
from src.crawler.forum_crawler import ForumCrawler
from src.config.config import DataSourceConfig

@pytest.fixture
def config():
    return DataSourceConfig(
        name="Test Forum",
        source_type="FORUM",
        base_url="http://testforum.com",
        reliability_score=0.8
    )

@pytest.fixture
def crawler(config):
    return ForumCrawler(config)

class TestForumCrawler:

    def test_initialization(self, crawler, config):
        assert crawler.config == config
        assert crawler.config.name == "Test Forum"
        assert 'post_title' in crawler.selectors

    def test_is_forum_page(self, crawler):
        html_with_post = "<html><body><div class='post-content'>Hello</div></body></html>"
        html_without_post = "<html><body><div>Just a page</div></body></html>"
        assert crawler._is_forum_page(html_with_post) is True
        assert crawler._is_forum_page(html_without_post) is False

    @patch('src.crawler.crawler.Crawler._parse_html')
    def test_parse_html_non_forum_page(self, mock_super_parse, crawler):
        mock_super_parse.return_value = {'title': 'Some Title'}
        html = "<html><body><div>Not a forum</div></body></html>"
        result = crawler._parse_html(html, "http://test.com")
        assert result is None

    def test_extract_replies(self, crawler):
        html = """
        <div id='replies'>
            <div class='reply'>
                <div class='reply-content'>First reply</div>
                <a class='author'>UserA</a>
            </div>
            <div class='reply'>
                <div class='reply-content'>Second reply</div>
                <a class='author'>UserB</a>
            </div>
        </div>
        """
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        replies = crawler._extract_replies(soup)
        assert len(replies) == 2
        assert replies[0]['content'] == 'First reply'
        assert replies[0]['author'] == 'UserA'

    def test_calculate_forum_credibility(self, crawler):
        score = crawler._calculate_forum_credibility("a long post content", [{}, {}, {}, {}, {}, {}])
        assert score > crawler.config.reliability_score

        score_short = crawler._calculate_forum_credibility("short", [])
        assert score_short < crawler.config.reliability_score

    def test_create_document_structure(self, crawler):
        parsed_data = {
            'title': 'Test Post',
            'content': 'This is the main post content.',
            'url': 'http://test.com/post1',
            'publication_date': '2024-01-01T00:00:00',
            'metadata': {
                'author': 'OriginalPoster',
                'tags': ['test', 'forum']
            },
            'replies': [
                {'author': 'ReplyGuy', 'content': 'Nice post!'},
                {'author': 'AnotherUser', 'content': 'I agree.'}
            ]
        }
        with patch('src.crawler.crawler.Crawler._create_document') as mock_super_create:
            mock_document = MagicMock()
            mock_document.chunks = []
            mock_super_create.return_value = mock_document
            document = crawler._create_document(parsed_data)
            assert document is not None
            # Further assertions can be added here to check the structure of the document and its chunks