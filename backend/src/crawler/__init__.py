# Copyright (c) 2025 Lingjing Project
# SPDX-License-Identifier: MIT

from src.config import config
from .crawler import Crawler
from .academic_crawler import AcademicCrawler
from .mystery_crawler import MysteryCrawler
from .news_crawler import NewsCrawler
from .forum_crawler import ForumCrawler
from .documentary_crawler import DocumentaryCrawler


def build_crawler(crawler_type: str = "mystery"):
    """Build a crawler based on the specified type."""
    config = get_config()
    crawler_map = {
        "mystery": MysteryCrawler,
        "academic": AcademicCrawler,
        "news": NewsCrawler,
        "forum": ForumCrawler,
        "documentary": DocumentaryCrawler,
    }
    
    crawler_class = crawler_map.get(crawler_type.lower())
    if not crawler_class:
        raise ValueError(f"Unknown crawler type: {crawler_type}")

    data_source_config = next((ds for ds in config.data_sources if ds.name == crawler_type), None)
    if not data_source_config:
        raise ValueError(f"No config found for crawler type: {crawler_type}")

    return crawler_class(data_source_config)


def build_specialized_crawlers():
    """Build all specialized crawlers for mystery research."""
    config = get_config()
    crawlers = {}
    for data_source in config.data_sources:
        crawler_type = data_source.name
        crawler_class = {
            "mystery": MysteryCrawler,
            "academic": AcademicCrawler,
            "news": NewsCrawler,
            "forum": ForumCrawler,
            "documentary": DocumentaryCrawler,
        }.get(crawler_type)

        if crawler_class:
            crawlers[crawler_type] = crawler_class(data_source)
            
    return crawlers


__all__ = [
    "Crawler",
    "AcademicCrawler", 
    "MysteryCrawler",
    "NewsCrawler",
    "ForumCrawler",
    "DocumentaryCrawler",
    "build_crawler",
    "build_specialized_crawlers",
]