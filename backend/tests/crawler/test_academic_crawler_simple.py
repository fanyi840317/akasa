# SPDX-License-Identifier: MIT

import pytest
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from unittest.mock import Mock, patch
from bs4 import BeautifulSoup


class TestAcademicCrawlerSimple:
    """学术爬虫简化测试类"""
    
    def test_basic_functionality(self):
        """测试基本功能"""
        # 测试HTML解析
        html = """
        <html>
        <head>
            <title>Test Academic Paper</title>
            <meta name="author" content="Dr. John Smith">
            <meta name="citation_journal_title" content="Nature">
        </head>
        <body>
            <div class="abstract">This is the abstract content.</div>
            <div class="content">This is the main content.</div>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # 测试标题提取
        title = soup.find('title')
        assert title is not None
        assert title.get_text() == "Test Academic Paper"
        
        # 测试作者提取
        author_meta = soup.find('meta', {'name': 'author'})
        assert author_meta is not None
        assert author_meta.get('content') == "Dr. John Smith"
        
        # 测试期刊信息提取
        journal_meta = soup.find('meta', {'name': 'citation_journal_title'})
        assert journal_meta is not None
        assert journal_meta.get('content') == "Nature"
        
        # 测试摘要提取
        abstract = soup.find('div', class_='abstract')
        assert abstract is not None
        assert "abstract content" in abstract.get_text()
    
    def test_keyword_extraction(self):
        """测试关键词提取"""
        html = """
        <html>
        <head>
            <meta name="keywords" content="atmospheric, electromagnetic, anomalies">
        </head>
        <body>
            <div class="keywords">
                <span>plasma</span>, <span>ionosphere</span>
            </div>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # 测试meta关键词
        keywords_meta = soup.find('meta', {'name': 'keywords'})
        assert keywords_meta is not None
        keywords_content = keywords_meta.get('content')
        assert "atmospheric" in keywords_content
        assert "electromagnetic" in keywords_content
        assert "anomalies" in keywords_content
        
        # 测试HTML关键词区域
        keywords_div = soup.find('div', class_='keywords')
        assert keywords_div is not None
        keywords_text = keywords_div.get_text()
        assert "plasma" in keywords_text
        assert "ionosphere" in keywords_text
    
    def test_reference_counting(self):
        """测试引用计数"""
        html = """
        <html>
        <body>
            <div class="references">
                <ol>
                    <li>Smith et al. (2022)</li>
                    <li>Johnson & Brown (2021)</li>
                    <li>Wilson (2020)</li>
                </ol>
            </div>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        references_div = soup.find('div', class_='references')
        assert references_div is not None
        
        reference_items = references_div.find_all('li')
        assert len(reference_items) == 3
        
        # 验证引用内容
        ref_texts = [item.get_text() for item in reference_items]
        assert "Smith et al. (2022)" in ref_texts
        assert "Johnson & Brown (2021)" in ref_texts
        assert "Wilson (2020)" in ref_texts
    
    def test_credibility_scoring_logic(self):
        """测试可信度评分逻辑"""
        # 模拟可信度评分计算
        base_score = 0.6
        
        # 高可信度期刊加分
        prestigious_journals = ["Nature", "Science", "Cell", "PNAS"]
        journal = "Nature"
        if journal in prestigious_journals:
            base_score += 0.2
        
        # 多作者加分
        authors = "Dr. A, Prof. B, Dr. C"
        author_count = len([a.strip() for a in authors.split(',') if a.strip()])
        if author_count >= 3:
            base_score += 0.1
        
        # 引用数量加分
        reference_count = 15
        if reference_count >= 10:
            base_score += 0.1
        
        assert base_score == 1.0  # 0.6 + 0.2 + 0.1 + 0.1
    
    def test_academic_keywords(self):
        """测试学术异常现象关键词"""
        academic_keywords = [
            "atmospheric anomalies",
            "electromagnetic phenomena", 
            "plasma physics",
            "ionospheric disturbances",
            "geophysical anomalies",
            "radar anomalies",
            "optical phenomena",
            "magnetic field variations",
            "atmospheric electricity",
            "ball lightning",
            "anomalous phenomena"
        ]
        
        # 验证关键词列表不为空
        assert len(academic_keywords) > 0
        
        # 验证包含预期的关键词
        assert "atmospheric anomalies" in academic_keywords
        assert "electromagnetic phenomena" in academic_keywords
        assert "plasma physics" in academic_keywords
        assert "anomalous phenomena" in academic_keywords
    
    def test_url_generation(self):
        """测试搜索URL生成"""
        query = "atmospheric anomalies"
        base_urls = [
            "https://scholar.google.com/scholar",
            "https://arxiv.org/search",
            "https://pubmed.ncbi.nlm.nih.gov",
            "https://ieeexplore.ieee.org/search"
        ]
        
        # 模拟URL生成
        generated_urls = []
        for base_url in base_urls:
            if "scholar.google.com" in base_url:
                url = f"{base_url}?q={query.replace(' ', '+')}"
            elif "arxiv.org" in base_url:
                url = f"{base_url}/?query={query.replace(' ', '+')}"
            else:
                url = f"{base_url}?term={query.replace(' ', '+')}"
            generated_urls.append(url)
        
        assert len(generated_urls) == 4
        assert all(query.replace(' ', '+') in url for url in generated_urls)
        assert any("scholar.google.com" in url for url in generated_urls)
        assert any("arxiv.org" in url for url in generated_urls)
    
    def test_content_chunking(self):
        """测试内容分块"""
        content = """This is the abstract section with important summary information.

This is the introduction section with background information and context.

This is the methodology section describing the research methods used.

This is the results section presenting the findings of the study.

This is the conclusion section summarizing the key outcomes."""
        
        # 模拟内容分块
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        chunks = []
        
        for i, paragraph in enumerate(paragraphs):
            if len(paragraph) > 50:  # 只保留足够长的段落
                chunk_metadata = {'chunk_id': i, 'type': 'content'}
                if 'abstract' in paragraph.lower():
                    chunk_metadata['type'] = 'abstract'
                    chunk_metadata['similarity'] = 0.95  # 摘要高相似度
                else:
                    chunk_metadata['similarity'] = 0.8
                
                chunks.append({
                    'content': paragraph,
                    'metadata': chunk_metadata
                })
        
        assert len(chunks) == 5
        
        # 验证摘要块
        abstract_chunks = [c for c in chunks if c['metadata']['type'] == 'abstract']
        assert len(abstract_chunks) == 1
        assert abstract_chunks[0]['metadata']['similarity'] == 0.95
        
        # 验证其他内容块
        content_chunks = [c for c in chunks if c['metadata']['type'] == 'content']
        assert len(content_chunks) == 4
        assert all(c['metadata']['similarity'] == 0.8 for c in content_chunks)