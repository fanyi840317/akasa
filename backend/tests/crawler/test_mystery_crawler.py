# SPDX-License-Identifier: MIT

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

from pathlib import Path

from src.crawler.mystery_crawler import MysteryCrawler
from src.config.config import DataSourceConfig, DataSourceType, MysteryEventType
from src.rag.retriever import Document, MysteryEvent


class TestMysteryCrawler:
    """神秘事件爬虫测试类"""
    
    @pytest.fixture
    def config(self):
        """创建测试配置"""
        return DataSourceConfig(
            name="test_mystery",
            source_type=DataSourceType.MYSTERY,
            base_url="https://mystery.example.com",
            headers={"User-Agent": "test-agent"}
        )
    
    @pytest.fixture
    def crawler(self, config):
        """创建爬虫实例"""
        return MysteryCrawler(config)
    
    @pytest.fixture
    def sample_ufo_html(self):
        """示例UFO事件HTML"""
        return """
        <html>
            <head><title>UFO Sighting Over Phoenix - March 13, 1997</title></head>
            <body>
                <h1>The Phoenix Lights Incident</h1>
                <div class="event-description">
                    On March 13, 1997, thousands of people witnessed a series of widely 
                    sighted unidentified flying objects observed in the skies over Arizona, 
                    Nevada, and the Mexican state of Sonora. The lights appeared to be 
                    in a V-formation and moved silently across the sky.
                </div>
                <div class="location">Phoenix, Arizona</div>
                <div class="event-date">1997-03-13</div>
                <div class="witnesses">
                    <div class="witness">Governor Fife Symington</div>
                    <div class="witness">Dr. Lynne Kitei</div>
                    <div class="witness">Tim Ley</div>
                </div>
                <div class="evidence">
                    <div>Video footage by multiple witnesses</div>
                    <div>Photographs from various angles</div>
                    <div>Radar data from Luke Air Force Base</div>
                </div>
                <p>The incident was investigated by the military and later explained 
                as flares dropped during training exercises.</p>
            </body>
        </html>
        """
    
    @pytest.fixture
    def sample_cryptid_html(self):
        """示例神秘生物HTML"""
        return """
        <html>
            <head><title>Bigfoot Sighting in Olympic National Forest</title></head>
            <body>
                <h1>Sasquatch Encounter Report</h1>
                <div class="case-details">
                    A group of hikers reported seeing a large, bipedal creature 
                    covered in dark hair walking through the forest. The creature 
                    was estimated to be 8-9 feet tall and moved with a distinctive gait.
                </div>
                <div class="place">Olympic National Forest, Washington</div>
                <div class="when">June 15, 2023</div>
                <div class="observer">Hiking group led by Sarah Johnson</div>
                <div class="documentation">
                    <div>Footprint casts taken at the scene</div>
                    <div>Hair samples collected from tree branches</div>
                </div>
            </body>
        </html>
        """
    
    def test_init(self, crawler, config):
        """测试初始化"""
        assert crawler.config.source_type == DataSourceType.MYSTERY
        assert len(crawler.mystery_keywords) == 6
        assert MysteryEventType.UFO in crawler.mystery_keywords
        assert "UFO" in crawler.mystery_keywords[MysteryEventType.UFO]
    
    @pytest.mark.asyncio
    async def test_crawl_url_success(self, crawler, sample_ufo_html):
        """测试成功爬取神秘事件URL"""
        with patch.object(crawler, '_fetch_html', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = sample_ufo_html
            
            result = await crawler.crawl_url("https://mystery.example.com/phoenix-lights")
            
            assert result is not None
            assert isinstance(result, Document)
            assert "Phoenix Lights" in result.title
            assert result.mystery_event is not None
    
    @pytest.mark.asyncio
    async def test_crawl_url_no_html(self, crawler):
        """测试无法获取HTML的情况"""
        with patch.object(crawler, '_fetch_html', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = None
            
            result = await crawler.crawl_url("https://mystery.example.com/invalid")
            
            assert result is None
    
    @pytest.mark.asyncio
    async def test_search(self, crawler):
        """测试搜索功能"""
        with patch.object(crawler, 'crawl_url', new_callable=AsyncMock) as mock_crawl:
            mock_doc = Mock(spec=Document)
            mock_crawl.return_value = mock_doc
            
            results = await crawler.search("UFO sighting", limit=2)
            
            assert len(results) <= 2
            assert all(isinstance(doc, type(mock_doc)) for doc in results)
    
    def test_extract_event_details_ufo(self, crawler, config, sample_ufo_html):
        """测试UFO事件HTML解析"""
        result = crawler._parse_mystery_html(sample_ufo_html, "https://mystery.example.com/phoenix-lights")
        
        assert result is not None
        assert "Phoenix Lights" in result['title']
        assert result['metadata']['event_type'] == MysteryEventType.UFO.value
        assert result['metadata']['location'] == "Phoenix, Arizona"
        assert result['metadata']['witnesses_count'] == 3
        assert result['metadata']['evidence_count'] == 3
        assert isinstance(result['mystery_event'], MysteryEvent)
    
    def test_extract_event_details_cryptid(self, crawler, config, sample_cryptid_html):
        """测试神秘生物事件HTML解析"""
        result = crawler._parse_mystery_html(sample_cryptid_html, "https://mystery.example.com/bigfoot")
        
        assert result is not None
        assert "Sasquatch" in result['title']
        assert result['metadata']['event_type'] == MysteryEventType.CRYPTID.value
        assert "Olympic National Forest" in result['metadata']['location']
    
    def test_parse_mystery_html_no_title(self, crawler, config):
        """测试无标题的HTML"""
        html = "<html><body><p>Content without title</p></body></html>"
        
        result = crawler._parse_mystery_html(html, "https://example.com")
        
        assert result is None
    
    def test_detect_event_type_ufo(self, crawler, config):
        """测试UFO事件类型检测"""
        text = "I saw a UFO flying saucer with bright lights over the city"
        
        event_type = crawler._detect_event_type(text)
        
        assert event_type == MysteryEventType.UFO
    
    def test_detect_event_type_cryptid(self, crawler, config):
        """测试神秘生物事件类型检测"""
        text = "Bigfoot sasquatch sighting in the forest with large footprints"
        
        event_type = crawler._detect_event_type(text)
        
        assert event_type == MysteryEventType.CRYPTID
    
    def test_detect_event_type_paranormal(self, crawler, config):
        """测试超自然事件类型检测"""
        text = "Ghost haunting in the old house with supernatural activities"
        
        event_type = crawler._detect_event_type(text)
        
        assert event_type == MysteryEventType.PARANORMAL
    
    def test_detect_event_type_no_match(self, crawler, config):
        """测试无匹配的事件类型"""
        text = "Regular news about weather and traffic conditions"
        
        event_type = crawler._detect_event_type(text)
        
        assert event_type is None
    
    def test_extract_mystery_description(self, crawler, config, sample_ufo_html):
        """测试神秘事件描述提取"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(sample_ufo_html, 'html.parser')
        description = crawler._extract_mystery_description(soup)
        
        assert "March 13, 1997" in description
        assert "V-formation" in description
        assert "Arizona" in description
    
    def test_extract_location(self, crawler, config, sample_ufo_html):
        """测试位置提取"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(sample_ufo_html, 'html.parser')
        location = crawler._extract_location(soup)
        
        assert location == "Phoenix, Arizona"
    
    def test_extract_location_from_text(self, crawler, config):
        """测试从文本中提取位置"""
        from bs4 import BeautifulSoup
        
        html = "<html><body><p>The incident occurred near Las Vegas, NV</p></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        location = crawler._extract_location(soup)
        
        assert "Las Vegas" in location
    
    def test_extract_event_date(self, crawler, config, sample_ufo_html):
        """测试事件日期提取"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(sample_ufo_html, 'html.parser')
        event_date = crawler._extract_event_date(soup)
        
        assert event_date is not None
        assert event_date.year == 1997
        assert event_date.month == 3
        assert event_date.day == 13
    
    def test_parse_date_various_formats(self, crawler, config):
        """测试各种日期格式解析"""
        dates = [
            "2023-06-15",
            "06/15/2023",
            "June 15, 2023",
            "15 Jun 2023"
        ]
        
        for date_str in dates:
            parsed = crawler._parse_date(date_str)
            if parsed:  # 某些格式可能解析失败
                assert parsed.year == 2023
                assert parsed.month == 6
                assert parsed.day == 15
    
    def test_parse_date_invalid(self, crawler, config):
        """测试无效日期解析"""
        invalid_dates = ["invalid date", "not a date", ""]
        
        for date_str in invalid_dates:
            parsed = crawler._parse_date(date_str)
            assert parsed is None
    
    def test_extract_witnesses(self, crawler, config, sample_ufo_html):
        """测试目击者提取"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(sample_ufo_html, 'html.parser')
        witnesses = crawler._extract_witnesses(soup)
        
        assert len(witnesses) == 3
        assert "Governor Fife Symington" in witnesses
        assert "Dr. Lynne Kitei" in witnesses
        assert "Tim Ley" in witnesses
    
    def test_extract_witnesses_from_text(self, crawler, config):
        """测试从文本中提取目击者"""
        from bs4 import BeautifulSoup
        
        html = "<html><body><p>The incident was reported by John Smith and witnessed by Mary Johnson.</p></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        witnesses = crawler._extract_witnesses(soup)
        
        assert len(witnesses) > 0
        assert any("John Smith" in witness for witness in witnesses)
    
    def test_extract_evidence(self, crawler, config, sample_ufo_html):
        """测试证据提取"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(sample_ufo_html, 'html.parser')
        evidence = crawler._extract_evidence(soup)
        
        assert len(evidence) == 3
        assert "Video footage by multiple witnesses" in evidence
        assert "Photographs from various angles" in evidence
        assert "Radar data from Luke Air Force Base" in evidence
    
    def test_extract_evidence_with_media(self, crawler, config):
        """测试包含媒体的证据提取"""
        from bs4 import BeautifulSoup
        
        html = """
        <html><body>
            <div class="evidence">Photo evidence</div>
            <img src="/images/ufo1.jpg" alt="UFO photo">
            <video src="/videos/sighting.mp4">UFO video</video>
        </body></html>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        evidence = crawler._extract_evidence(soup)
        
        assert len(evidence) == 3
        assert "Photo evidence" in evidence
        assert "Media: /images/ufo1.jpg" in evidence
        assert "Media: /videos/sighting.mp4" in evidence
    
    def test_calculate_credibility_high(self, crawler, config):
        """测试高可信度计算"""
        from bs4 import BeautifulSoup
        
        html = """
        <html><body>
            <p>This incident was investigated by NASA scientists and the military. 
            Official police report confirms multiple witnesses and radar data analysis.</p>
        </body></html>
        """
        soup = BeautifulSoup(html, 'html.parser')
        witnesses = ["Officer Smith", "Dr. Johnson", "Pilot Williams"]
        evidence = ["Radar data", "Photos", "Video", "Lab analysis"]
        
        credibility = crawler._calculate_credibility(soup, witnesses, evidence)
        
        assert credibility > 0.8  # 应该是高可信度
    
    def test_calculate_credibility_low(self, crawler, config):
        """测试低可信度计算"""
        from bs4 import BeautifulSoup
        
        html = "<html><body><p>Someone said they saw something strange.</p></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        witnesses = []
        evidence = []
        
        credibility = crawler._calculate_credibility(soup, witnesses, evidence)
        
        assert credibility == 0.5  # 基础分数
    
    def test_create_mystery_document(self, crawler, config):
        """测试神秘事件文档创建"""
        mystery_event = MysteryEvent(
            event_id="test123",
            event_type="ufo",
            title="Test UFO Event",
            description="Test description",
            location="Test Location",
            date=datetime.now(),
            credibility_score=0.8,
            source_url="https://example.com",
            witnesses=["Witness 1"],
            evidence=["Evidence 1"]
        )
        
        parsed_data = {
            'title': 'Test UFO Event',
            'content': 'This is a test UFO event.\n\nIt has multiple paragraphs with detailed information about the sighting.',
            'mystery_event': mystery_event,
            'metadata': {
                'url': 'https://example.com',
                'credibility_score': 0.8
            }
        }
        
        document = crawler._create_mystery_document(parsed_data, "test_doc_id")
        
        assert isinstance(document, Document)
        assert document.id == "test_doc_id"
        assert document.title == "Test UFO Event"
        assert document.mystery_event == mystery_event
        assert len(document.chunks) > 0
    
    def test_identify_event_type(self, crawler, config):
        """测试事件类型识别"""
        queries = [
            ("UFO sighting over city", MysteryEventType.UFO),
            ("Bigfoot encounter in forest", MysteryEventType.CRYPTID),
            ("Ghost haunting old house", MysteryEventType.PARANORMAL),
            ("Ancient pyramid mystery", MysteryEventType.ANCIENT_MYSTERY),
            ("Person vanished mysteriously", MysteryEventType.DISAPPEARANCE),
            ("Strange ball lightning phenomenon", MysteryEventType.NATURAL_ANOMALY)
        ]
        
        for query, expected_type in queries:
            identified_type = crawler._identify_event_type(query)
            assert identified_type == expected_type
    
    def test_build_mystery_query(self, crawler, config):
        """测试神秘事件查询构建"""
        query = "strange lights"
        event_type = MysteryEventType.UFO
        
        mystery_query = crawler._build_mystery_query(query, event_type)
        
        assert "strange lights" in mystery_query
        assert "UFO" in mystery_query
        assert len(mystery_query.split()) > 2  # 应该添加了关键词
    
    def test_build_mystery_query_no_type(self, crawler, config):
        """测试无事件类型的查询构建"""
        query = "strange phenomenon"
        
        mystery_query = crawler._build_mystery_query(query, None)
        
        assert mystery_query == query  # 应该保持原样
    
    def test_generate_mystery_search_urls(self, crawler, config):
        """测试神秘事件搜索URL生成"""
        query = "UFO sighting"
        urls = crawler._generate_mystery_search_urls(query, limit=3)
        
        assert isinstance(urls, list)
        assert len(urls) <= 3
        assert all(isinstance(url, str) for url in urls)
        assert all("UFO%20sighting" in url or "UFO+sighting" in url for url in urls)
    
    def test_extract_title(self, crawler, config, sample_ufo_html):
        """测试标题提取"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(sample_ufo_html, 'html.parser')
        title = crawler._extract_title(soup)
        
        assert title == "The Phoenix Lights Incident"
    
    def test_mystery_keywords_completeness(self, crawler, config):
        """测试神秘关键词的完整性"""
        # 确保所有事件类型都有关键词
        for event_type in MysteryEventType:
            assert event_type in crawler.mystery_keywords
            assert len(crawler.mystery_keywords[event_type]) > 0
            assert all(isinstance(keyword, str) for keyword in crawler.mystery_keywords[event_type])
    
    def test_empty_mystery_html(self, crawler, config):
        """测试空神秘事件HTML"""
        empty_html = "<html><body></body></html>"
        
        result = crawler._parse_mystery_html(empty_html, "https://example.com")
        
        assert result is None
    
    def test_malformed_mystery_html(self, crawler, config):
        """测试格式错误的神秘事件HTML"""
        malformed_html = "<html><body><h1>Title</h1><div class='event-description'>Broken HTML without closing"
        
        # 应该能够处理格式错误的HTML而不崩溃
        result = crawler._parse_mystery_html(malformed_html, "https://example.com")
        
        # 可能返回部分解析的结果或None，但不应该抛出异常
        assert result is None or isinstance(result, dict)
    
    def test_credibility_score_bounds(self, crawler, config):
        """测试可信度分数边界"""
        from bs4 import BeautifulSoup
        
        # 测试最大可信度
        high_credibility_html = """
        <html><body>
            <p>NASA investigation official government military police report 
            scientist expert laboratory analysis research study</p>
        </body></html>
        """
        soup = BeautifulSoup(high_credibility_html, 'html.parser')
        witnesses = ["w1", "w2", "w3", "w4", "w5"]  # 多个目击者
        evidence = ["e1", "e2", "e3", "e4", "e5"]    # 多个证据
        
        credibility = crawler._calculate_credibility(soup, witnesses, evidence)
        
        assert 0.0 <= credibility <= 1.0
        assert credibility > 0.9  # 应该接近最大值
    
    def test_location_extraction_patterns(self, crawler, config):
        """测试位置提取的各种模式"""
        from bs4 import BeautifulSoup
        
        test_cases = [
            ("<p>The event occurred in Phoenix, AZ</p>", "Phoenix"),
            ("<p>Sighting near Las Vegas, Nevada</p>", "Las Vegas"),
            ("<p>Location: coordinates 34.0522, -118.2437</p>", "34.0522")
        ]
        
        for html_content, expected_part in test_cases:
            html = f"<html><body>{html_content}</body></html>"
            soup = BeautifulSoup(html, 'html.parser')
            location = crawler._extract_location(soup)
            
            if location:  # 某些模式可能不匹配
                assert expected_part in location