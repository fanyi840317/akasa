# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT

import re
import logging
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from src.crawler.crawler import Crawler
from src.rag.retriever import Document, Chunk
from config.config import DataSourceConfig

logger = logging.getLogger(__name__)


class DocumentaryCrawler(Crawler):
    """纪录片和视频爬虫"""

    def __init__(self, config: DataSourceConfig):
        super().__init__(config)
        self._initialize_selectors()

    def _initialize_selectors(self):
        """初始化纪录片网站的CSS选择器"""
        super()._initialize_selectors()
        doc_selectors = {
            'video_container': ['#video-player', '.video-container', 'div[data-video-id]'],
            'video_url': ['video > source[src]', 'iframe[src]'],
            'mystery_type': ['.tags a', '.category', 'meta[name="keywords"]']
        }
        for key, value in doc_selectors.items():
            self.selectors.setdefault(key, []).extend(value)

    async def search(self, query: str, limit: int = 10) -> List[Document]:
        """在视频网站搜索纪录片"""
        from urllib.parse import quote
        if not self.config.search_url:
            self.logger.warning("Search URL is not configured for this documentary source.")
            return []

        search_query = quote(query)
        full_search_url = self.config.search_url.format(query=search_query)

        try:
            html = await self.fetch_html(full_search_url)
            if not html:
                return []

            soup = BeautifulSoup(html, 'html.parser')
            
            # 子类需要定义 'search_result_link' 选择器
            link_selector = self.selectors.get('search_result_link', ['a[href*="/video/"]', 'a[href*="/watch?"]'])
            links = soup.select(', '.join(link_selector))
            
            video_urls = []
            for link in links[:limit]:
                href = link.get('href')
                if href:
                    full_url = urljoin(full_search_url, href)
                    video_urls.append(full_url)

            return await self.batch_crawl(video_urls)

        except Exception as e:
            self.logger.error(f"Error during documentary search: {e}", exc_info=True)
            return []

    def _is_documentary_page(self, html: str) -> bool:
        """判断页面是否为纪录片或视频页面"""
        soup = BeautifulSoup(html, 'html.parser')
        return soup.select_one('video, iframe[src*="youtube"], iframe[src*="vimeo"]') is not None

    def _parse_html(self, html: str, url: str) -> Optional[Dict[str, Any]]:
        """解析纪录片HTML"""
        if not self._is_documentary_page(html):
            self.logger.info(f"Skipping non-documentary page: {url}")
            return None

        parsed_data = super()._parse_html(html, url)
        if not parsed_data:
            return None

        soup = BeautifulSoup(html, 'html.parser')
        video_url = self._extract_video_url(soup, url)
        mystery_type = self._extract_mystery_type(soup)
        credibility_score = self._calculate_documentary_credibility(soup, video_url)

        parsed_data['metadata'].update({
            'video_url': video_url,
            'mystery_type': mystery_type,
            'credibility_score': credibility_score
        })

        return parsed_data

    def _extract_video_url(self, soup: BeautifulSoup, base_url: str) -> Optional[str]:
        """提取视频URL"""
        for selector in self.selectors.get('video_url', []):
            element = soup.select_one(selector)
            if element:
                src = element.get('src')
                if src:
                    # 将相对URL转换为绝对URL
                    return urljoin(base_url, src)
        return None

    def _extract_mystery_type(self, soup: BeautifulSoup) -> Optional[str]:
        """提取神秘事件类型"""
        text_content = self._extract_text_by_selectors(soup, ['mystery_type'])
        if not text_content:
            # 如果选择器找不到，从整个页面文本中查找
            text_content = soup.get_text()

        text_content = text_content.upper()
        # 简单的关键词匹配
        if 'UFO' in text_content or 'ALIEN' in text_content: return 'UFO'
        if 'GHOST' in text_content or 'PARANORMAL' in text_content: return 'Ghost'
        if 'CONSPIRACY' in text_content: return 'Conspiracy'
        if 'CRYPTOZOOLOGY' in text_content or 'BIGFOOT' in text_content: return 'Cryptozoology'
        return None

    def _calculate_documentary_credibility(self, soup: BeautifulSoup, video_url: Optional[str]) -> float:
        """计算纪录片可信度"""
        score = self._analyze_source(soup)
        if not video_url:
            score *= 0.7
        # 检查来源是否为知名平台
        if video_url and any(domain in video_url for domain in ['youtube.com', 'vimeo.com', 'dailymotion.com']):
            score = min(1.0, score + 0.1)
        
        # 检查是否有对专家的引用或采访
        text = soup.get_text().lower()
        if any(keyword in text for keyword in ['expert', 'scientist', 'researcher', 'interview with']):
            score = min(1.0, score + 0.15)

        return round(score, 2)

    def _create_document(self, parsed_data: Dict[str, Any]) -> Document:
        """创建纪录片文档对象"""
        document = super()._create_document(parsed_data)
        metadata = parsed_data['metadata']

        if metadata.get('video_url'):
            document.chunks.append(Chunk(
                content=f"Video available at: {metadata['video_url']}",
                similarity=0.9,
                metadata={'type': 'video_link'}
            ))
        if metadata.get('mystery_type'):
            document.chunks.append(Chunk(
                content=f"Mystery Type: {metadata['mystery_type']}",
                similarity=0.8,
                metadata={'type': 'mystery_type'}
            ))

        return document