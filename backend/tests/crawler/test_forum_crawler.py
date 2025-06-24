# SPDX-License-Identifier: MIT

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from crawler.forum_crawler import ForumCrawler
from config.mystery_config import DataSourceConfig, DataSourceType
from rag.retriever import Document


class TestForumCrawler:
    """论坛爬虫测试类"""
    
    @pytest.fixture
    def config(self):
        """创建测试配置"""
        return DataSourceConfig(
            name="test_forum",
            source_type=DataSourceType.FORUM,
            base_url="https://forum.example.com",
            headers={"User-Agent": "test-agent"}
        )
    
    @pytest.fixture
    def crawler(self, config):
        """创建爬虫实例"""
        return ForumCrawler(config)
    
    @pytest.fixture
    def sample_forum_html(self):
        """示例论坛HTML"""
        return """
        <html>
            <head><title>UFO Sighting Discussion - Mystery Forum</title></head>
            <body>
                <h1 class="thread-title">Strange Lights Over Nevada - Anyone Else See This?</h1>
                <div class="forum-info">
                    <span>Forum: UFO Sightings</span>
                    <span>Thread ID: 12345</span>
                </div>
                <div class="post" id="post-1">
                    <div class="post-header">
                        <span class="username">SkyWatcher99</span>
                        <span class="post-date">2023-06-15 22:30</span>
                        <span class="post-number">#1</span>
                    </div>
                    <div class="post-content">
                        Last night around 10 PM, I saw three bright lights moving in formation over Nevada. 
                        They moved too fast to be planes and made no sound. Has anyone else witnessed this?
                    </div>
                </div>
                <div class="post" id="post-2">
                    <div class="post-header">
                        <span class="username">TruthSeeker</span>
                        <span class="post-date">2023-06-16 08:15</span>
                        <span class="post-number">#2</span>
                    </div>
                    <div class="post-content">
                        I saw something similar last week! Three lights in a triangle formation. 
                        Definitely not conventional aircraft.
                    </div>
                </div>
            </body>
        </html>
        """
    
    def test_init(self, crawler):
        """测试初始化"""
        assert crawler.config.source_type == DataSourceType.FORUM
        assert len(crawler.forum_indicators) > 0
        assert "post" in crawler.forum_indicators
        assert "thread" in crawler.forum_indicators
    
    @pytest.mark.asyncio
    async def test_crawl_url_success(self, crawler, sample_forum_html):
        """测试成功爬取论坛URL"""
        with patch.object(crawler, '_fetch_html', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = sample_forum_html
            
            result = await crawler.crawl_url("https://forum.example.com/thread/12345")
            
            assert result is not None
            assert isinstance(result, Document)
            assert "Strange Lights Over Nevada" in result.content
    
    @pytest.mark.asyncio
    async def test_crawl_url_no_html(self, crawler):
        """测试无法获取HTML的情况"""
        with patch.object(crawler, '_fetch_html', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = None
            
            result = await crawler.crawl_url("https://forum.example.com/invalid")
            
            assert result is None
    
    @pytest.mark.asyncio
    async def test_search(self, crawler):
        """测试搜索功能"""
        with patch.object(crawler, 'crawl_url', new_callable=AsyncMock) as mock_crawl:
            mock_doc = Mock(spec=Document)
            mock_crawl.return_value = mock_doc
            
            with patch.object(crawler, '_generate_forum_search_urls') as mock_urls:
                mock_urls.return_value = [
                    "https://forum.example.com/search?q=ufo",
                    "https://forum.example.com/search?q=lights"
                ]
                
                results = await crawler.search("UFO lights", limit=2)
                
                assert len(results) <= 2
                assert all(isinstance(doc, type(mock_doc)) for doc in results)
    
    def test_parse_forum_html(self, crawler, sample_forum_html):
        """测试论坛HTML解析"""
        result = crawler._parse_forum_html(sample_forum_html, "https://forum.example.com/thread/12345")
        
        assert result is not None
        assert "Strange Lights Over Nevada" in result['title']
        assert result['metadata']['source_type'] == 'forum'
        assert result['metadata']['posts_count'] == 2
        assert 'posts' in result['metadata']
    
    def test_parse_forum_html_not_forum(self, crawler):
        """测试非论坛页面"""
        non_forum_html = """
        <html>
            <head><title>Regular Website</title></head>
            <body>
                <h1>Welcome to Our Website</h1>
                <p>This is just a regular webpage with no forum content.</p>
            </body>
        </html>
        """
        
        result = crawler._parse_forum_html(non_forum_html, "https://example.com")
        
        assert result is None
    
    def test_is_forum_page_positive(self, crawler):
        """测试论坛页面识别（正面案例）"""
        from bs4 import BeautifulSoup
        
        forum_html = """
        <html>
            <body>
                <div class="post">Forum post content</div>
                <div class="thread">Thread discussion</div>
                <span>Member since 2020</span>
            </body>
        </html>
        """
        
        soup = BeautifulSoup(forum_html, 'html.parser')
        assert crawler._is_forum_page(soup) == True
    
    def test_is_forum_page_negative(self, crawler):
        """测试论坛页面识别（负面案例）"""
        from bs4 import BeautifulSoup
        
        regular_html = """
        <html>
            <body>
                <h1>Regular Website</h1>
                <p>This is just a normal webpage.</p>
            </body>
        </html>
        """
        
        soup = BeautifulSoup(regular_html, 'html.parser')
        assert crawler._is_forum_page(soup) == False
    
    def test_extract_forum_title(self, crawler):
        """测试论坛标题提取"""
        from bs4 import BeautifulSoup
        
        html = '<h1 class="thread-title">UFO Discussion Thread</h1>'
        soup = BeautifulSoup(html, 'html.parser')
        
        title = crawler._extract_forum_title(soup)
        assert title == "UFO Discussion Thread"
    
    def test_extract_forum_title_no_title(self, crawler):
        """测试无标题情况"""
        from bs4 import BeautifulSoup
        
        html = '<div>No title here</div>'
        soup = BeautifulSoup(html, 'html.parser')
        
        title = crawler._extract_forum_title(soup)
        assert title is None
    
    def test_extract_forum_posts(self, crawler, sample_forum_html):
        """测试论坛帖子提取"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(sample_forum_html, 'html.parser')
        posts = crawler._extract_forum_posts(soup)
        
        assert isinstance(posts, list)
        assert len(posts) == 2
        
        # 检查第一个帖子
        first_post = posts[0]
        assert 'username' in first_post
        assert 'content' in first_post
        assert 'date' in first_post
        assert first_post['username'] == 'SkyWatcher99'
        assert 'three bright lights' in first_post['content']
    
    def test_extract_forum_info(self, crawler, sample_forum_html):
        """测试论坛信息提取"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(sample_forum_html, 'html.parser')
        url = "https://forum.example.com/thread/12345"
        
        forum_info = crawler._extract_forum_info(soup, url)
        
        assert isinstance(forum_info, dict)
        assert 'name' in forum_info
        assert 'thread_id' in forum_info
    
    def test_calculate_forum_credibility(self, crawler, sample_forum_html):
        """测试论坛可信度计算"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(sample_forum_html, 'html.parser')
        posts = crawler._extract_forum_posts(soup)
        forum_info = {'name': 'UFO Forum', 'thread_id': '12345'}
        
        credibility = crawler._calculate_forum_credibility(soup, posts, forum_info)
        
        assert isinstance(credibility, float)
        assert 0.0 <= credibility <= 1.0
    
    def test_combine_posts_content(self, crawler):
        """测试帖子内容合并"""
        posts = [
            {
                'username': 'User1',
                'content': 'First post content',
                'date': '2023-06-15'
            },
            {
                'username': 'User2',
                'content': 'Second post content',
                'date': '2023-06-16'
            }
        ]
        
        combined = crawler._combine_posts_content(posts)
        
        assert isinstance(combined, str)
        assert 'First post content' in combined
        assert 'Second post content' in combined
        assert 'User1' in combined
        assert 'User2' in combined
    
    def test_build_forum_query(self, crawler):
        """测试论坛查询构建"""
        query = "UFO sighting Nevada"
        forum_query = crawler._build_forum_query(query)
        
        assert isinstance(forum_query, str)
        assert "UFO" in forum_query
        assert "sighting" in forum_query
        assert "Nevada" in forum_query
    
    def test_generate_forum_search_urls(self, crawler):
        """测试论坛搜索URL生成"""
        query = "mystery lights"
        urls = crawler._generate_forum_search_urls(query, limit=3)
        
        assert isinstance(urls, list)
        assert len(urls) <= 3
        assert all(isinstance(url, str) for url in urls)
        assert all("mystery" in url.lower() or "lights" in url.lower() for url in urls)
    
    def test_create_forum_document(self, crawler):
        """测试论坛文档创建"""
        parsed_data = {
            'title': 'Test Forum Thread',
            'content': 'Combined forum posts content',
            'metadata': {
                'url': 'https://forum.example.com/thread/123',
                'source_type': 'forum',
                'posts_count': 3,
                'credibility_score': 0.7
            }
        }
        doc_id = "test_forum_doc"
        
        document = crawler._create_forum_document(parsed_data, doc_id)
        
        assert isinstance(document, Document)
        assert document.id == doc_id
        assert "Test Forum Thread" in document.content
        assert "Combined forum posts content" in document.content
    
    def test_extract_post_metadata(self, crawler):
        """测试帖子元数据提取"""
        post_html = """
        <div class="post">
            <div class="post-header">
                <span class="username">TestUser</span>
                <span class="post-date">2023-06-15 14:30</span>
                <span class="post-number">#5</span>
            </div>
            <div class="post-content">This is the post content.</div>
        </div>
        """
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(post_html, 'html.parser')
        post_elem = soup.select_one('.post')
        
        metadata = crawler._extract_post_metadata(post_elem)
        
        assert isinstance(metadata, dict)
        assert metadata['username'] == 'TestUser'
        assert '2023-06-15' in metadata['date']
        assert metadata['post_number'] == '#5'
    
    def test_filter_spam_posts(self, crawler):
        """测试垃圾帖子过滤"""
        posts = [
            {'content': 'This is a legitimate discussion about UFOs.', 'username': 'RealUser'},
            {'content': 'BUY CHEAP VIAGRA NOW!!!', 'username': 'SpamBot'},
            {'content': 'I also saw strange lights last night.', 'username': 'Witness123'},
            {'content': 'CLICK HERE FOR FREE MONEY', 'username': 'Scammer'}
        ]
        
        filtered_posts = crawler._filter_spam_posts(posts)
        
        assert len(filtered_posts) == 2
        assert all('UFOs' in post['content'] or 'lights' in post['content'] for post in filtered_posts)
        assert not any('VIAGRA' in post['content'] or 'FREE MONEY' in post['content'] for post in filtered_posts)
    
    def test_extract_user_reputation(self, crawler):
        """测试用户声誉提取"""
        user_html = """
        <div class="user-info">
            <span class="username">ExpertUser</span>
            <span class="reputation">Reputation: 1250</span>
            <span class="posts-count">Posts: 500</span>
            <span class="join-date">Joined: 2020-01-15</span>
        </div>
        """
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(user_html, 'html.parser')
        
        reputation = crawler._extract_user_reputation(soup)
        
        assert isinstance(reputation, dict)
        assert reputation['score'] == 1250
        assert reputation['posts_count'] == 500
        assert '2020-01-15' in reputation['join_date']
    
    def test_empty_forum_handling(self, crawler):
        """测试空论坛页面处理"""
        empty_html = "<html><body></body></html>"
        
        result = crawler._parse_forum_html(empty_html, "https://forum.example.com")
        
        assert result is None
    
    def test_malformed_forum_html(self, crawler):
        """测试格式错误的论坛HTML"""
        malformed_html = "<html><body><div class='post'>Broken HTML without closing tags"
        
        # 应该能够处理格式错误的HTML而不崩溃
        result = crawler._parse_forum_html(malformed_html, "https://forum.example.com")
        
        # 可能返回None或部分解析的结果，但不应该抛出异常
        assert result is None or isinstance(result, dict)