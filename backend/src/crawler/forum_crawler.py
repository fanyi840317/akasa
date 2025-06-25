# Copyright (c) 2024 Lingjing
# SPDX-License-Identifier: MIT

import hashlib
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import quote, urljoin

from bs4 import BeautifulSoup

from src.crawler.crawler import Crawler
from src.rag.retriever import Document, Chunk
from config.config import DataSourceConfig


class ForumCrawler(Crawler):
    """论坛爬虫"""

    def __init__(self, config: DataSourceConfig):
        super().__init__(config)
        self._initialize_selectors()

    def _initialize_selectors(self):
        """初始化论坛网站的CSS选择器"""
        super()._initialize_selectors()
        forum_selectors = {
            'post_title': ['h1.post-title', '.thread-title'],
            'post_content': ['.post-body', '.post-content', '.main-post'],
            'author': ['.author-name', '.user-name', 'a.author'],
            'post_date': ['.post-date', '.message-date'],
            'replies_container': ['#replies', '.post-replies', '.reply-list'],
            'reply_item': ['.reply', '.post', '.message'],
            'reply_content': ['.reply-content', '.message-body', '.post-text'],
            'reply_author': ['.reply-author', '.user-info .username', '.author']
        }
        for key, value in forum_selectors.items():
            self.selectors.setdefault(key, []).extend(value)

    async def search(self, query: str, limit: int = 10) -> List[Document]:
        """在论坛搜索帖子"""
        if not self.config.search_url:
            self.logger.warning("Search URL is not configured for this forum.")
            return []

        search_query = quote(query)
        # 假设搜索URL使用 {query} 作为占位符
        full_search_url = self.config.search_url.format(query=search_query)

        try:
            html = await self.fetch_html(full_search_url)
            if not html:
                return []

            soup = BeautifulSoup(html, 'html.parser')
            
            # 子类需要定义 'search_result_link' 选择器
            link_selector = self.selectors.get('search_result_link', ['a[href*="thread-"]'])
            links = soup.select(', '.join(link_selector))
            
            post_urls = []
            for link in links[:limit]:
                href = link.get('href')
                if href:
                    full_url = urljoin(full_search_url, href)
                    post_urls.append(full_url)

            return await self.batch_crawl(post_urls)

        except Exception as e:
            self.logger.error(f"Error during forum search: {e}", exc_info=True)
            return []

    def _is_forum_page(self, html: str) -> bool:
        """判断页面是否为论坛帖子页面"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        return soup.select_one(', '.join(self.selectors.get('post_content', []))) is not None

    def _parse_html(self, html: str, url: str) -> Optional[Dict[str, Any]]:
        """解析论坛HTML"""
        parsed_data = super()._parse_html(html, url)
        if not parsed_data or not self._is_forum_page(html):
            self.logger.info(f"Skipping non-forum page: {url}")
            return None

        soup = BeautifulSoup(html, 'html.parser')

        # 论坛标题和内容通常更特定
        parsed_data['title'] = self._extract_text_by_selectors(soup, self.selectors['post_title']) or parsed_data.get('title')
        parsed_data['content'] = self._extract_text_by_selectors(soup, self.selectors['post_content']) or parsed_data.get('content')

        if not parsed_data['title']:
            return None

        author = self._extract_text_by_selectors(soup, self.selectors['author'])
        post_date_str = self._extract_text_by_selectors(soup, self.selectors['post_date'])
        post_date = self._parse_date(post_date_str)
        replies = self._extract_replies(soup)

        credibility_score = self._calculate_forum_credibility(parsed_data['content'], replies)

        parsed_data['metadata'].update({
            'author': author,
            'post_date': post_date.isoformat() if post_date else None,
            'reply_count': len(replies),
            'credibility_score': credibility_score
        })
        parsed_data['replies'] = replies

        if not parsed_data.get('publication_date') and post_date:
            parsed_data['publication_date'] = post_date.isoformat()

        return parsed_data

    def _extract_replies(self, soup: Any) -> List[Dict[str, str]]:
        """提取回复"""
        replies = []
        container_selector = ', '.join(self.selectors.get('replies_container', []))
        item_selector = ', '.join(self.selectors.get('reply_item', []))
        
        replies_container = soup.select_one(container_selector)
        if not replies_container:
            return []

        for reply_element in replies_container.select(item_selector):
            content = self._extract_text_by_selectors(reply_element, ['reply_content'])
            author = self._extract_text_by_selectors(reply_element, ['reply_author'])
            if content:
                replies.append({'author': author or 'Anonymous', 'content': content})
        return replies

    def _calculate_forum_credibility(self, content: str, replies: List[Dict]) -> float:
        """计算论坛内容可信度"""
        score = self.config.reliability_score
        if len(replies) > 5:
            score = min(1.0, score + 0.1)
        if len(content) < 100:
            score *= 0.9
        # 可以在这里加入更多基于作者信誉、回复质量等的逻辑
        return round(score, 2)

    def _create_document(self, parsed_data: Dict[str, Any]) -> Document:
        """创建论坛文档对象"""
        document = super()._create_document(parsed_data)
        if not document:
            return None
        metadata = parsed_data['metadata']

        # 替换基类创建的content chunk，使用更结构化的主楼内容
        document.chunks = [c for c in document.chunks if c.metadata.get('type') != 'content']
        document.chunks.append(Chunk(content=parsed_data['content'], similarity=0.8, metadata={'type': 'post_content'}))

        if metadata.get('author'):
            document.chunks.insert(1, Chunk(content=f"Author: {metadata['author']}", similarity=0.9, metadata={'type': 'author'}))

        for i, reply in enumerate(parsed_data.get('replies', [])):
            document.chunks.append(Chunk(
                content=f"Reply by {reply['author']}: {reply['content']}",
                similarity=0.7,
                metadata={'type': 'reply', 'reply_index': i, 'author': reply['author']}
            ))

        return document