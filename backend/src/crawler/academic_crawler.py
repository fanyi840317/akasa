# Copyright (c) 2024 Lingjing
# SPDX-License-Identifier: MIT

import hashlib
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import quote, urljoin

from config.config import DataSourceConfig
from config.types import DataSourceType
from crawler.crawler import Crawler
from rag.retriever import Document, Chunk


class AcademicCrawler(Crawler):
    """学术数据库爬虫"""

    def __init__(self, config: DataSourceConfig):
        """初始化并覆盖学术网站的CSS选择器"""
        super().__init__(config)
        academic_selectors = {
            'title': [
                'h1.article-title', '.article-title', 'h1.title',
                '.paper-title', 'h1', 'title'
            ],
            'abstract': [
                '.abstract', '#abstract', '.summary', '[data-testid="abstract"]',
                '.article-abstract'
            ],
            'author': ['.author', '.authors', '.author-name', '.contributor'],
            'journal': ['.journal-title', '.publication-title', '.source'],
            'doi': ['a[href^="https://doi.org"]', 'a[href^="http://dx.doi.org"]'],
            'keywords': ['.keywords', '.tags', '.subjects']
        }
        for key, value in academic_selectors.items():
            self.selectors.setdefault(key, []).extend(value)



    async def search(self, query: str, limit: int = 10) -> List[Document]:
        """搜索学术论文，使用 Semantic Scholar API。"""
        self.logger.info(f"Performing academic search for: {query}")
        base_url = self.config.api_url
        if not base_url:
            self.logger.error("Semantic Scholar API URL is not configured.")
            return []
        api_url = f"{base_url}/graph/v1/paper/search?query={quote(query)}&limit={limit}&fields=title,abstract,authors,journal,year,url,doi"

        try:
            async with self.session.get(api_url, timeout=30) as response:
                if response.status != 200:
                    self.logger.error(f"Failed to fetch from Semantic Scholar API: {response.status} {await response.text()}")
                    return []
                data = await response.json()
        except Exception as e:
            self.logger.error(f"Error during Semantic Scholar API call: {e}")
            return []

        documents = []
        results = data.get('data', [])
        for item in results:
            url = item.get('url')
            if not url:
                continue

            doc_id = hashlib.md5(url.encode()).hexdigest()
            publication_year = item.get('year')
            
            metadata = {
                'source_type': self.config.source_type.value,
                'reliability_score': self.config.reliability_score,
                'authors': [author['name'] for author in item.get('authors', [])],
                'journal': item.get('journal', {}).get('name') if item.get('journal') else None,
                'publication_year': publication_year,
                'doi': item.get('doi'),
                'keywords': [],  # API不直接提供关键词，可留空或后续处理
                'abstract': item.get('abstract'),
                'url': url
            }

            parsed_data = {
                'title': item.get('title'),
                'content': item.get('abstract', ''),
                'metadata': metadata
            }

            doc = self._create_document(parsed_data, doc_id)
            documents.append(doc)

        return documents

    def _parse_html(self, html: str, url: str) -> Optional[Dict[str, Any]]:
        """
        解析学术论文HTML，在基类解析结果的基础上添加学术特有字段。
        """
        parsed_data = super()._parse_html(html, url)
        if not parsed_data:
            return None

        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取学术特定元数据
        abstract = self._extract_text_by_selectors(soup, self.selectors['abstract'])
        authors = self._extract_all_texts_by_selectors(soup, self.selectors['author'])
        journal_name = self._extract_text_by_selectors(soup, self.selectors['journal'])
        doi = self._extract_text_by_selectors(soup, self.selectors['doi'])
        keywords = self._extract_text_by_selectors(soup, self.selectors['keywords'])
        
        # 尝试从内容中提取年份
        publication_year = None
        date_text = parsed_data.get('publication_date', '') or parsed_data.get('content', '')
        if date_text:
            year_match = re.search(r'\b(19|20)\d{2}\b', str(date_text))
            if year_match:
                publication_year = int(year_match.group())

        # 更新元数据
        parsed_data['metadata'].update({
            'authors': authors,
            'journal': journal_name,
            'publication_year': publication_year,
            'doi': doi,
            'keywords': keywords.split(',') if keywords else [],
            'abstract': abstract
        })
        
        # 将摘要作为主要内容（如果内容为空）
        if not parsed_data.get('content') and abstract:
            parsed_data['content'] = abstract

        return parsed_data

    def _create_document(self, parsed_data: Dict[str, Any]) -> Document:
        """创建学术文档对象"""
        document = super()._create_document(parsed_data)

        metadata = parsed_data['metadata']
        
        # 创建并添加特定于学术的文档块
        academic_chunks = []
        
        # 摘要作为一个独立的、高权重的块
        abstract = metadata.get('abstract')
        if abstract:
            academic_chunks.append(Chunk(
                content=abstract,
                similarity=1.0,
                metadata={'type': 'abstract'}
            ))
        
        document.chunks.extend(academic_chunks)

        # 更新文档元数据
        document.author = ",".join(metadata.get('authors', []))
        document.publication_date = self._parse_date(str(metadata.get('publication_year'))) if metadata.get('publication_year') else None
        document.metadata.update(metadata)

        return document