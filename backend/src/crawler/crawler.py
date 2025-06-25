# Copyright (c) 2024 Lingjing
# SPDX-License-Identifier: MIT

import abc
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup
from readabilipy import simple_json_from_html_string

from rag.retriever import Document, MysteryEvent
from src.config import DataSourceConfig, DataSourceType


class Crawler(abc.ABC):
    """基础爬虫抽象类"""

    def __init__(self, config: DataSourceConfig):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session: Optional[aiohttp.ClientSession] = None
        self._initialize_selectors()



    def _initialize_selectors(self):
        """从配置初始化CSS选择器"""
        self.selectors = {}
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession(
            headers=self.config.headers,
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
            
    async def crawl_url(self, url: str) -> Optional[Document]:
        """爬取单个URL"""
        try:
            html = await self.fetch_html(url)
            if not html:
                return None
            
            parsed_data = self._parse_html(html, url)
            if not parsed_data or not parsed_data.get('title') or not parsed_data.get('content'):
                self.logger.warning(f"Failed to parse essential data from {url}")
                return None

            return self._create_document(parsed_data)

        except aiohttp.ClientError as e:
            self.logger.error(f"An error occurred while crawling {url}: {e}", exc_info=True)
            return None
        
    @abc.abstractmethod
    async def search(self, query: str, limit: int = 10) -> List[Document]:
        """搜索相关内容"""
        pass
        
    async def batch_crawl(self, urls: List[str]) -> List[Document]:
        """批量爬取URL"""
        tasks = [self.crawl_url(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        documents = []
        for result in results:
            if isinstance(result, Document):
                documents.append(result)
            elif isinstance(result, Exception):
                self.logger.error(f"Crawling failed: {result}")
                
        return documents
        
    async def fetch_html(self, url: str) -> str:
        """获取HTML内容"""
        if hasattr(self.config, 'use_jina') and self.config.use_jina:
            return await self._fetch_with_jina(url)
        else:
            return await self._fetch_with_aiohttp(url)

    async def _fetch_with_aiohttp(self, url: str) -> str:
        """使用aiohttp获取HTML"""
        if not self.session:
            raise RuntimeError("Session not started. Use 'async with crawler:' syntax.")
        
        try:
            timeout = getattr(self.config, 'timeout', 30)
            async with self.session.get(url, timeout=timeout) as response:
                response.raise_for_status()
                return await response.text()
        except aiohttp.ClientError as e:
            self.logger.error(f"Error fetching {url} with aiohttp: {e}")
            return ""

    async def _fetch_with_jina(self, url: str) -> str:
        """使用Jina AI Reader获取内容"""
        import os
        if not self.session:
            raise RuntimeError("Session not started. Use 'async with crawler:' syntax.")

        jina_url = "https://r.jina.ai/"
        headers = {
            "Content-Type": "application/json",
            "X-Return-Format": "html",
        }
        api_key = self.config.jina_api_key
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        data = {"url": url}

        try:
            timeout = getattr(self.config, 'timeout', 60) # Jina might take longer
            async with self.session.post(jina_url, headers=headers, json=data, timeout=timeout) as response:
                response.raise_for_status()
                return await response.text()
        except aiohttp.ClientError as e:
            self.logger.error(f"Error fetching {url} with Jina: {e}")
            return ""
            
    def _parse_html(self, html: str, url: str) -> Dict[str, Any]:
        """解析HTML内容，子类可以覆盖此方法以实现更复杂的解析逻辑"""
        try:
            article_data = simple_json_from_html_string(html, use_readability=True)
        except Exception as e:
            self.logger.warning(f"Readability extraction failed for {url}: {e}")
            article_data = {}

        soup = BeautifulSoup(html, 'html.parser')

        # 提取基本信息
        title = self._extract_title(soup, article_data)
        content = self._extract_content(soup, article_data)
        metadata = self._extract_metadata(soup, url, article_data)

        return {
            'title': title,
            'content': content,
            'metadata': metadata,
        }

    def _create_document(self, parsed_data: Dict[str, Any]) -> Document:
        """创建基础文档对象，子类可以扩展此方法以添加特定的chunks"""
        metadata = parsed_data['metadata']
        publication_date = self._parse_date(metadata.get('publication_date'))
        doc_id = f"{self.config.source_type.value}-{metadata['url']}"

        # 基础的 title 和 content chunks
        chunks = [
            Chunk(content=parsed_data['title'], similarity=1.0, metadata={'type': 'title'}),
            Chunk(content=parsed_data['content'], similarity=0.8, metadata={'type': 'content'})
        ]

        return Document(
            id=doc_id,
            url=metadata['url'],
            title=parsed_data['title'],
            chunks=chunks,
            credibility_score=metadata.get('credibility_score', self.config.reliability_score),
            source_type=metadata.get('source_type', self.config.source_type.value),
            publication_date=publication_date,
            metadata=metadata
        )

    def _parse_date(self, date_text: Optional[str]) -> Optional[datetime]:
        """解析日期字符串"""
        if not date_text:
            return None
        try:
            # 尝试使用dateutil解析，它能处理多种格式
            from dateutil.parser import parse
            return parse(date_text)
        except (ValueError, TypeError):
            self.logger.warning(f"Could not parse date: {date_text}")
            return None

    def _analyze_source(self, soup: BeautifulSoup) -> float:
        """分析来源可信度"""
        # 默认可信度
        score = self.config.reliability_score

        # 可以在这里添加更多通用的可信度分析逻辑
        # 例如，检查SSL证书、域名年龄等（需要额外库）

        return score
        
    def _extract_text_by_selectors(self, soup: BeautifulSoup, selector_keys: List[str]) -> Optional[str]:
        """根据选择器列表提取文本"""
        for key in selector_keys:
            selectors = self.selectors.get(key, [])
            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    return element.get_text(separator='\n', strip=True)
        return None

    def _extract_title(self, soup: BeautifulSoup, article_data: Optional[Dict] = None) -> str:
        """提取标题"""
        if article_data and article_data.get('title'):
            return article_data['title']
        title = self._extract_text_by_selectors(soup, ['title'])
        return title or "Untitled"
    def _extract_content(self, soup: BeautifulSoup, article_data: Optional[Dict] = None) -> str:
        """提取正文内容"""
        if article_data and article_data.get('content'):
            # 使用BeautifulSoup从HTML内容中提取纯文本
            content_soup = BeautifulSoup(article_data['content'], 'html.parser')
            return content_soup.get_text(separator='\n', strip=True)

        # 移除脚本和样式标签
        for script in soup(["script", "style"]):
            script.decompose()

        content = self._extract_text_by_selectors(soup, ['content'])
        if content:
            return content

        # 如果没有找到特定内容区域，返回body内容
        body = soup.find('body')
        if body:
            return body.get_text(separator='\n', strip=True)

        return soup.get_text(separator='\n', strip=True)
        
    def _extract_metadata(self, soup: BeautifulSoup, url: str, article_data: Optional[Dict] = None) -> Dict[str, Any]:
        """提取元数据"""
        # 分析来源可信度
        source_info = self._analyze_source(url)
        
        metadata = {
            'url': url,
            'crawled_at': datetime.now().isoformat(),
            'source_type': source_info['type'],
            'reliability_score': source_info['score']
        }
        
        # 提取meta标签信息
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            name = tag.get('name') or tag.get('property')
            content = tag.get('content')
            if name and content:
                metadata[f'meta_{name}'] = content
                
        # 从readabilipy结果中提取作者和日期
        if article_data:
            if article_data.get('byline'):
                metadata['author'] = article_data['byline']
            if article_data.get('date'):
                metadata['publication_date'] = article_data['date']

        # 如果readabilipy没有提供，则尝试从HTML中提取
        if 'publication_date' not in metadata:
            publication_date = self._extract_text_by_selectors(soup, ['date'])
            if publication_date:
                metadata['publication_date'] = publication_date

        if 'author' not in metadata:
            author = self._extract_text_by_selectors(soup, ['author'])
            if author:
                metadata['author'] = author
                
        return metadata
        
    def _create_document(self, parsed_data: Dict[str, Any], doc_id: str) -> Document:
        """创建文档对象"""
        return Document(
            id=doc_id,
            url=parsed_data['metadata']['url'],
            title=parsed_data['title'],
            chunks=[],  # 将在后续处理中分块
            credibility_score=self.config.reliability_score,
            source_type=self.config.source_type.value,
            metadata=parsed_data['metadata']
        )
        
    def _analyze_source(self, url: str) -> Dict[str, Any]:
        """分析来源可信度"""
        if not url:
            return {"type": "unknown", "score": 0.1}
        
        url_lower = url.lower()
        parsed = urlparse(url_lower)
        domain = parsed.netloc
        
        # 检查已知来源
        for known_domain, info in self.source_credibility_map.items():
            if known_domain in domain:
                return info
        
        # 基于域名特征进行基本判断
        if any(ext in domain for ext in [".edu", ".gov"]):
            return {"type": "institutional", "score": 0.8}
        elif ".org" in domain:
            return {"type": "organization", "score": 0.6}
        elif any(keyword in domain for keyword in ["news", "press", "media"]):
            return {"type": "news", "score": 0.5}
        elif any(keyword in domain for keyword in ["blog", "personal"]):
            return {"type": "blog", "score": 0.2}
        elif any(keyword in domain for keyword in ["forum", "discussion", "community"]):
            return {"type": "forum", "score": 0.3}
        else:
            return {"type": "unknown", "score": 0.3}

    def _should_crawl_url(self, url: str) -> bool:
        """判断是否应该爬取该URL"""
        parsed = urlparse(url)
        
        # 检查域名是否在允许列表中
        if hasattr(self.config, 'allowed_domains'):
            if parsed.netloc not in self.config.allowed_domains:
                return False
                
        # 检查URL模式
        if hasattr(self.config, 'url_patterns'):
            import re
            for pattern in self.config.url_patterns:
                if re.match(pattern, url):
                    return True
            return False
            
        return True