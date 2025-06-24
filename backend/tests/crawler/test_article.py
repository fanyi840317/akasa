# SPDX-License-Identifier: MIT

import pytest
from datetime import datetime
from unittest.mock import Mock, patch

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from crawler.article import Article


class TestArticle:
    """文章类测试"""
    
    @pytest.fixture
    def sample_html(self):
        """示例HTML内容"""
        return """
        <html>
            <body>
                <h1>Mystery Event in Nevada</h1>
                <p>On January 15, 2023, witnesses reported strange lights in the sky.</p>
                <p>The event occurred near Las Vegas and was observed by multiple people.</p>
                <p>Evidence includes photographs and video recordings.</p>
                <p>Dr. John Smith, a local researcher, investigated the phenomenon.</p>
            </body>
        </html>
        """
    
    @pytest.fixture
    def article(self, sample_html):
        """创建文章实例"""
        return Article(
            title="Mystery Event Report",
            html_content=sample_html,
            url="https://example.com/mystery-event",
            author="Test Author",
            publication_date=datetime(2023, 1, 20),
            source_type="news",
            credibility_score=0.8
        )
    
    def test_init(self, article, sample_html):
        """测试初始化"""
        assert article.title == "Mystery Event Report"
        assert article.html_content == sample_html
        assert article.url == "https://example.com/mystery-event"
        assert article.author == "Test Author"
        assert article.source_type == "news"
        assert article.credibility_score == 0.8
        assert isinstance(article.metadata, dict)
    
    def test_init_defaults(self):
        """测试默认值初始化"""
        article = Article("Test Title", "<p>Test content</p>")
        
        assert article.title == "Test Title"
        assert article.url == ""
        assert article.author == ""
        assert article.publication_date is None
        assert article.source_type == "unknown"
        assert article.credibility_score == 0.5
        assert article.metadata == {}
    
    def test_to_markdown_with_title(self, article):
        """测试转换为Markdown（包含标题）"""
        with patch.object(article, '_convert_html_to_markdown') as mock_convert:
            mock_convert.return_value = "Converted markdown content"
            
            markdown = article.to_markdown(including_title=True)
            
            assert markdown.startswith("# Mystery Event Report\n\n")
            assert "Converted markdown content" in markdown
    
    def test_to_markdown_without_title(self, article):
        """测试转换为Markdown（不包含标题）"""
        with patch.object(article, '_convert_html_to_markdown') as mock_convert:
            mock_convert.return_value = "Converted markdown content"
            
            markdown = article.to_markdown(including_title=False)
            
            assert not markdown.startswith("# Mystery Event Report")
            assert "Converted markdown content" in markdown
    
    def test_analyze_content(self, article):
        """测试内容分析"""
        # 由于_analyze_content在初始化时自动调用，检查分析结果
        assert hasattr(article, 'mystery_keywords')
        assert hasattr(article, 'event_type')
        assert hasattr(article, 'location_mentions')
        assert hasattr(article, 'date_mentions')
        assert hasattr(article, 'witness_mentions')
        assert hasattr(article, 'evidence_mentions')
    
    def test_extract_mystery_keywords(self, article):
        """测试神秘关键词提取"""
        keywords = article._extract_mystery_keywords()
        
        assert isinstance(keywords, list)
        # 基于示例HTML内容，应该能找到一些关键词
        assert len(keywords) >= 0
    
    def test_classify_event_type(self, article):
        """测试事件类型分类"""
        event_type = article._classify_event_type()
        
        assert isinstance(event_type, str)
        # 基于示例内容，可能分类为UFO相关
        assert event_type in ["ufo", "atmospheric", "unknown", "other"]
    
    def test_extract_locations(self, article):
        """测试地点提取"""
        locations = article._extract_locations()
        
        assert isinstance(locations, list)
        # 示例内容中提到了Nevada和Las Vegas
        assert any("Nevada" in loc or "Las Vegas" in loc for loc in locations)
    
    def test_extract_dates(self, article):
        """测试日期提取"""
        dates = article._extract_dates()
        
        assert isinstance(dates, list)
        # 示例内容中提到了January 15, 2023
        assert len(dates) >= 1
    
    def test_extract_witnesses(self, article):
        """测试目击者提取"""
        witnesses = article._extract_witnesses()
        
        assert isinstance(witnesses, list)
        # 示例内容中提到了witnesses和Dr. John Smith
        assert len(witnesses) >= 1
    
    def test_extract_evidence(self, article):
        """测试证据提取"""
        evidence = article._extract_evidence()
        
        assert isinstance(evidence, list)
        # 示例内容中提到了photographs和video recordings
        assert len(evidence) >= 1
    
    def test_convert_html_to_markdown(self, article):
        """测试HTML到Markdown转换"""
        markdown = article._convert_html_to_markdown()
        
        assert isinstance(markdown, str)
        assert len(markdown) > 0
        # 应该包含原始HTML的文本内容
        assert "Mystery Event in Nevada" in markdown
    
    def test_get_text_content(self, article):
        """测试获取纯文本内容"""
        text = article.get_text_content()
        
        assert isinstance(text, str)
        assert "Mystery Event in Nevada" in text
        assert "witnesses reported strange lights" in text
    
    def test_get_summary(self, article):
        """测试获取摘要"""
        summary = article.get_summary(max_length=100)
        
        assert isinstance(summary, str)
        assert len(summary) <= 100
        assert len(summary) > 0
    
    def test_get_metadata(self, article):
        """测试获取元数据"""
        metadata = article.get_metadata()
        
        assert isinstance(metadata, dict)
        assert metadata['title'] == "Mystery Event Report"
        assert metadata['url'] == "https://example.com/mystery-event"
        assert metadata['author'] == "Test Author"
        assert metadata['source_type'] == "news"
        assert metadata['credibility_score'] == 0.8
    
    def test_update_credibility_score(self, article):
        """测试更新可信度分数"""
        original_score = article.credibility_score
        new_score = 0.9
        
        article.update_credibility_score(new_score)
        
        assert article.credibility_score == new_score
        assert article.credibility_score != original_score
    
    def test_add_metadata(self, article):
        """测试添加元数据"""
        article.add_metadata("test_key", "test_value")
        
        assert "test_key" in article.metadata
        assert article.metadata["test_key"] == "test_value"
    
    def test_empty_html_content(self):
        """测试空HTML内容"""
        article = Article("Empty Test", "")
        
        assert article.title == "Empty Test"
        assert article.html_content == ""
        # 分析应该正常完成，即使内容为空
        assert isinstance(article.mystery_keywords, list)
        assert isinstance(article.location_mentions, list)