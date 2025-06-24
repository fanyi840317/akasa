# SPDX-License-Identifier: MIT

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from crawler.documentary_crawler import DocumentaryCrawler
from config.mystery_config import MysteryEventType, DataSourceType
from rag.retriever import Document, MysteryEvent


class TestDocumentaryCrawler:
    """纪录片爬虫测试类"""
    
    @pytest.fixture
    def crawler(self):
        """创建爬虫实例"""
        return DocumentaryCrawler()
    
    @pytest.fixture
    def sample_documentary_html(self):
        """示例纪录片HTML"""
        return """
        <html>
            <head>
                <title>UFO Encounters: The Truth Behind the Phenomena</title>
                <meta name="description" content="A comprehensive documentary exploring UFO sightings and alien encounters.">
                <meta property="og:title" content="UFO Encounters Documentary">
            </head>
            <body>
                <h1>UFO Encounters: The Truth Behind the Phenomena</h1>
                <div class="info">
                    <span class="duration">1:45:30</span>
                    <time datetime="2023-05-15">Released: 2023-05-15</time>
                    <p>Producer: National Geographic</p>
                    <p>Genre: Documentary, Mystery</p>
                </div>
                <div class="transcript">
                    This documentary examines unexplained aerial phenomena and extraterrestrial encounters.
                </div>
            </body>
        </html>
        """
    
    def test_init(self, crawler):
        """测试初始化"""
        assert hasattr(crawler, 'documentary_patterns')
        assert hasattr(crawler, 'mystery_keywords')
        assert 'title' in crawler.documentary_patterns
        assert 'description' in crawler.documentary_patterns
        assert MysteryEventType.UFO in crawler.mystery_keywords
        assert MysteryEventType.CRYPTID in crawler.mystery_keywords
    
    @pytest.mark.asyncio
    async def test_parse_documentary_html(self, crawler, sample_documentary_html):
        """测试纪录片HTML解析"""
        result = await crawler.parse_documentary_html(sample_documentary_html, "https://example.com/ufo-doc")
        
        assert isinstance(result, dict)
        assert "UFO Encounters" in result['title']
        assert "comprehensive documentary" in result['description']
        assert result['duration'] == "1:45:30"
        assert "2023-05-15" in result['release_date']
        assert "National Geographic" in result['producer']
        assert result['mystery_type'] == MysteryEventType.UFO
        assert isinstance(result['credibility_score'], float)
        assert 0.0 <= result['credibility_score'] <= 1.0
    
    @pytest.mark.asyncio
    async def test_parse_documentary_html_cryptid(self, crawler):
        """测试解析神秘生物纪录片"""
        cryptid_html = """
        <html>
            <head><title>Bigfoot: The Legend Lives</title></head>
            <body>
                <h1>Bigfoot: The Legend Lives</h1>
                <p>An investigation into Sasquatch sightings in the Pacific Northwest.</p>
            </body>
        </html>
        """
        
        result = await crawler.parse_documentary_html(cryptid_html, "https://example.com/bigfoot")
        
        assert result['mystery_type'] == MysteryEventType.CRYPTID
        assert "Bigfoot" in result['title']
    
    @pytest.mark.asyncio
    async def test_parse_documentary_html_paranormal(self, crawler):
        """测试解析超自然纪录片"""
        paranormal_html = """
        <html>
            <head><title>Haunted Houses: Real Ghost Stories</title></head>
            <body>
                <h1>Haunted Houses</h1>
                <p>Exploring paranormal activity in haunted locations.</p>
            </body>
        </html>
        """
        
        result = await crawler.parse_documentary_html(paranormal_html, "https://example.com/ghosts")
        
        assert result['mystery_type'] == MysteryEventType.PARANORMAL
        assert "Haunted" in result['title']
    
    def test_calculate_documentary_credibility_high_score(self, crawler):
        """测试高可信度纪录片评分"""
        data = {
            'producer': 'National Geographic',
            'duration': '1:30:00',
            'release_date': '2023-01-01'
        }
        url = "https://nationalgeographic.com/documentary"
        
        score = crawler._calculate_documentary_credibility(data, url)
        
        assert isinstance(score, float)
        assert score > 0.8  # 应该是高分
    
    def test_calculate_documentary_credibility_medium_score(self, crawler):
        """测试中等可信度纪录片评分"""
        data = {
            'producer': 'Independent Producer',
            'duration': '45:00',
            'release_date': '2020-01-01'
        }
        url = "https://example.com/documentary"
        
        score = crawler._calculate_documentary_credibility(data, url)
        
        assert isinstance(score, float)
        assert 0.5 <= score <= 0.8  # 应该是中等分数
    
    def test_calculate_documentary_credibility_low_score(self, crawler):
        """测试低可信度纪录片评分"""
        data = {
            'producer': '',
            'duration': '',
            'release_date': ''
        }
        url = "https://unknown-site.com/video"
        
        score = crawler._calculate_documentary_credibility(data, url)
        
        assert isinstance(score, float)
        assert score == 0.6  # 基础分数
    
    def test_reputable_producers_recognition(self, crawler):
        """测试知名制作方识别"""
        reputable_producers = [
            "National Geographic",
            "Discovery Channel",
            "History Channel",
            "BBC Documentary",
            "PBS Nova",
            "Netflix Original"
        ]
        
        for producer in reputable_producers:
            data = {'producer': producer, 'duration': '', 'release_date': ''}
            score = crawler._calculate_documentary_credibility(data, "https://example.com")
            assert score >= 0.9, f"Producer {producer} should get high score"
    
    def test_reputable_domains_recognition(self, crawler):
        """测试知名域名识别"""
        reputable_urls = [
            "https://nationalgeographic.com/doc",
            "https://discovery.com/show",
            "https://history.com/documentary",
            "https://bbc.com/programme",
            "https://pbs.org/nova"
        ]
        
        for url in reputable_urls:
            data = {'producer': '', 'duration': '', 'release_date': ''}
            score = crawler._calculate_documentary_credibility(data, url)
            assert score >= 0.8, f"URL {url} should get high score"
    
    def test_duration_scoring(self, crawler):
        """测试时长评分"""
        test_cases = [
            ("1:30:00", True),   # 90分钟，应该加分
            ("45:00", True),     # 45分钟，应该加分
            ("25:00", False),    # 25分钟，不应该加分
            ("invalid", False)   # 无效格式，不应该加分
        ]
        
        for duration, should_boost in test_cases:
            data = {'producer': '', 'duration': duration, 'release_date': ''}
            base_score = crawler._calculate_documentary_credibility(
                {'producer': '', 'duration': '', 'release_date': ''}, 
                "https://example.com"
            )
            test_score = crawler._calculate_documentary_credibility(data, "https://example.com")
            
            if should_boost:
                assert test_score > base_score, f"Duration {duration} should boost score"
            else:
                assert test_score == base_score, f"Duration {duration} should not boost score"
    
    def test_release_date_scoring(self, crawler):
        """测试发布日期评分"""
        current_year = datetime.now().year
        recent_date = f"{current_year - 1}-01-01"  # 去年
        old_date = f"{current_year - 10}-01-01"    # 10年前
        
        data_recent = {'producer': '', 'duration': '', 'release_date': recent_date}
        data_old = {'producer': '', 'duration': '', 'release_date': old_date}
        
        score_recent = crawler._calculate_documentary_credibility(data_recent, "https://example.com")
        score_old = crawler._calculate_documentary_credibility(data_old, "https://example.com")
        
        assert score_recent > score_old, "Recent documentaries should score higher"
    
    def test_mystery_keyword_detection(self, crawler):
        """测试神秘关键词检测"""
        test_cases = [
            ("UFO sightings and alien encounters", MysteryEventType.UFO),
            ("Bigfoot and Sasquatch evidence", MysteryEventType.CRYPTID),
            ("Ghost stories and haunted houses", MysteryEventType.PARANORMAL),
            ("Ancient pyramids and lost civilizations", MysteryEventType.ANCIENT_MYSTERY),
            ("Missing persons and disappearances", MysteryEventType.DISAPPEARANCE),
            ("Strange weather anomalies", MysteryEventType.NATURAL_ANOMALY),
            ("Regular documentary content", MysteryEventType.UNKNOWN)
        ]
        
        for content, expected_type in test_cases:
            html = f"<html><head><title>{content}</title></head><body><p>{content}</p></body></html>"
            
            # 直接测试关键词检测逻辑
            content_text = content.lower()
            detected_type = MysteryEventType.UNKNOWN
            
            for event_type, keywords in crawler.mystery_keywords.items():
                if any(keyword in content_text for keyword in keywords):
                    detected_type = event_type
                    break
            
            assert detected_type == expected_type, f"Content '{content}' should be classified as {expected_type}"
    
    def test_pattern_extraction(self, crawler):
        """测试模式提取"""
        html = """
        <html>
            <head>
                <title>Test Documentary</title>
                <meta name="description" content="Test description">
            </head>
            <body>
                <span class="duration">1:20:30</span>
                <time datetime="2023-06-01">June 1, 2023</time>
                <p>Producer: Test Producer</p>
            </body>
        </html>
        """
        
        # 测试各个字段的提取
        import re
        
        # 测试标题提取
        title_patterns = crawler.documentary_patterns['title']
        title_found = False
        for pattern in title_patterns:
            match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
            if match and "Test Documentary" in match.group(1):
                title_found = True
                break
        assert title_found, "Title should be extracted"
        
        # 测试描述提取
        desc_patterns = crawler.documentary_patterns['description']
        desc_found = False
        for pattern in desc_patterns:
            match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
            if match and "Test description" in match.group(1):
                desc_found = True
                break
        assert desc_found, "Description should be extracted"
    
    @pytest.mark.asyncio
    async def test_empty_html_handling(self, crawler):
        """测试空HTML处理"""
        result = await crawler.parse_documentary_html("", "https://example.com")
        
        assert isinstance(result, dict)
        assert result['title'] == ""
        assert result['description'] == ""
        assert result['mystery_type'] == MysteryEventType.UNKNOWN
        assert result['credibility_score'] == 0.6  # 基础分数
    
    @pytest.mark.asyncio
    async def test_malformed_html_handling(self, crawler):
        """测试格式错误HTML处理"""
        malformed_html = "<html><head><title>Broken HTML</head><body><p>Missing closing tags"
        
        result = await crawler.parse_documentary_html(malformed_html, "https://example.com")
        
        assert isinstance(result, dict)
        assert "Broken HTML" in result['title']
        assert result['mystery_type'] == MysteryEventType.UNKNOWN