# Copyright (c) 2024 Lingjing
# SPDX-License-Identifier: MIT

import hashlib
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import quote, urljoin

from src.crawler.crawler import Crawler
from src.rag.retriever import Document, Chunk
from config.config import DataSourceConfig


class NewsCrawler(Crawler):
    """新闻网站爬虫"""

    def __init__(self, config: DataSourceConfig):
        super().__init__(config)
        self._initialize_selectors()

    def _initialize_selectors(self):
        """初始化新闻网站的CSS选择器"""
        super()._initialize_selectors()
        news_selectors = {
            'title': ['h1.story-title', '.article-title', 'h1'],
            'content': ['.story-content', '.article-body', 'article'],
            'publish_date': ['.timestamp', '.published-date', 'time'],
            'author': ['.author-name', '.byline', 'a[rel="author"]'],
            'source': ['.source', '.credit', 'span.source'],
            'summary': ['.summary', '.dek', '.article-summary'],
            'tags': ['.tags a', '.keywords a', '.topics a']
        }
        for key, value in news_selectors.items():
            self.selectors.setdefault(key, []).extend(value)



    async def search(self, query: str, limit: int = 10) -> List[Document]:
        """使用 NewsAPI 搜索新闻。"""
        self.logger.info(f"Performing news search for: {query}")
        # 注意：您需要一个 NewsAPI 的密钥才能使用此功能。
        # 您可以从 https://newsapi.org/ 免费获取。
        api_key = self.config.api_key
        if not api_key:
            self.logger.error("NewsAPI key is not configured. Please add it to the data source configuration.")
            return []

        base_url = self.config.api_url
        if not base_url:
            self.logger.error("NewsAPI URL is not configured.")
            return []
        api_url = f"{base_url}/v2/everything?q={quote(query)}&pageSize={limit}&apiKey={api_key}"

        try:
            async with self.session.get(api_url, timeout=20) as response:
                if response.status != 200:
                    self.logger.error(f"Failed to fetch from NewsAPI: {response.status} {await response.text()}")
                    return []
                data = await response.json()
        except Exception as e:
            self.logger.error(f"Error during NewsAPI call: {e}")
            return []

        documents = []
        articles = data.get('articles', [])
        for article in articles:
            url = article.get('url')
            if not url:
                continue

            # NewsAPI 的结果可以直接用于创建文档，因为它们已经包含了所需的大部分信息
            # 但为了保持一致性，我们仍然可以走一遍 crawl_url 流程来获取最新内容和标准化数据
            # 这里为了效率，我们直接使用API返回的数据创建文档
            doc = await self.crawl_url(url)
            if doc:
                documents.append(doc)

        return documents

    def _parse_html(self, html: str, url: str) -> Optional[Dict[str, Any]]:
        """解析新闻HTML，在基类解析结果的基础上添加新闻特有字段。"""
        parsed_data = super()._parse_html(html, url)
        if not parsed_data:
            return None

        soup = BeautifulSoup(html, 'html.parser')

        # 提取新闻特定元数据
        source = self._extract_text_by_selectors(soup, self.selectors['source'])
        summary = self._extract_text_by_selectors(soup, self.selectors['summary'])
        tags = self._extract_all_texts_by_selectors(soup, self.selectors['tags'])

        # 使用基类的可信度分析
        credibility_score = self._analyze_source(source, parsed_data.get('author'))

        # 更新元数据
        parsed_data['metadata'].update({
            'source': source,
            'summary': summary,
            'tags': tags,
            'credibility_score': credibility_score
        })

        # 如果没有摘要，从内容中生成一个
        if not summary and parsed_data.get('content'):
            parsed_data['metadata']['summary'] = parsed_data['content'][:200] + '...'

        return parsed_data

    def _create_document(self, parsed_data: Dict[str, Any]) -> Document:
        """创建新闻文档对象"""
        document = super()._create_document(parsed_data)
        metadata = parsed_data['metadata']
        
        # 创建并添加特定于新闻的文档块
        news_chunks = []
        summary = metadata.get('summary')
        if summary:
            news_chunks.append(Chunk(content=summary, similarity=0.9, metadata={'type': 'summary'}))
        
        document.chunks.extend(news_chunks)

        # 更新文档元数据
        document.metadata.update(metadata)

        return document