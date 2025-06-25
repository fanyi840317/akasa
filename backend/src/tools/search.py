# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT

import json
import logging
import os
from typing import Dict, List, Any, Optional

from langchain_community.tools import BraveSearch, DuckDuckGoSearchResults
from langchain_community.tools.arxiv import ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper, BraveSearchWrapper
from langchain_core.tools import BaseTool, tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

# Add src directory to Python path if not already added
import sys
from pathlib import Path

src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config import SearchEngine, RAGProvider
from src.config import MysteryEventType, DataSourceType, MysteryEventConfig, config
# from tools.tavily_search.tavily_search_results_with_images import (
#     tavily_search_results_with_images
# )
from .decorators import create_logged_tool, log_io

logger = logging.getLogger(__name__)

# Create logged versions of the search tools
# LoggedTavilySearch = create_logged_tool(TavilySearchResultsWithImages)
LoggedDuckDuckGoSearch = create_logged_tool(DuckDuckGoSearchResults)
LoggedBraveSearch = create_logged_tool(BraveSearch)
LoggedArxivSearch = create_logged_tool(ArxivQueryRun)


class AcademicSearch(BaseTool):
    """An academic search tool that searches across multiple databases."""
    name: str = "academic_search"
    description: str = "Searches academic databases like Arxiv, CNKI, etc."
    max_results: int = 5
    databases: List[str] = []
    api_keys: Dict[str, str] = {}

    def __init__(self, **kwargs):
        """Initialize the academic search tool."""
        super().__init__(**kwargs)
        self.databases = self.databases or config.mystery.academic_search_types
        self.api_keys = {
            "cnki": config.api.cnki_api_key or "",
            "wanfang": config.api.wanfang_api_key or "",
            "webofscience": config.api.webofscience_api_key or "",
        }
    
    def _run(self, query: str) -> List[Dict[str, Any]]:
        """Run the academic search.

        Args:
            query: The search query

        Returns:
            List of academic search results
        """
        logger.info(f"Searching academic databases: {self.databases} for: {query}")

        results = []

        # Use ArxivQueryRun for arxiv searches
        if "arxiv" in self.databases:
            try:
                arxiv_tool = LoggedArxivSearch(
                    api_wrapper=ArxivAPIWrapper(
                        top_k_results=self.max_results,
                        load_max_docs=self.max_results,
                        load_all_available_meta=True,
                    ),
                )
                arxiv_results_str = arxiv_tool.invoke(query)

                # The result from ArxivQueryRun is a string, not a list of dicts.
                # We'll wrap it in a result dictionary.
                if isinstance(arxiv_results_str, str) and arxiv_results_str:
                    results.append({
                        "title": f"Arxiv Search Results for {query}",
                        "content": arxiv_results_str,
                        "source": "arxiv",
                        "source_type": "academic"
                    })

            except Exception as e:
                logger.error(f"Error searching arxiv: {e}")

        # Simulate other academic database searches
        # In a real implementation, these would connect to actual APIs
        for db in self.databases:
            if db == "arxiv":
                continue  # Already handled above

            if db == "cnki" and self.api_keys["cnki"]:
                # Simulated CNKI search
                results.append({
                    "title": f"CNKI Search Results for {query}",
                    "content": f"Simulated CNKI academic search results for: {query}",
                    "source": "cnki",
                    "source_type": "academic"
                })

            if db == "wanfang" and self.api_keys["wanfang"]:
                # Simulated Wanfang search
                results.append({
                    "title": f"Wanfang Search Results for {query}",
                    "content": f"Simulated Wanfang academic search results for: {query}",
                    "source": "wanfang",
                    "source_type": "academic"
                })

            if db == "webofscience" and self.api_keys["webofscience"]:
                # Simulated Web of Science search
                results.append({
                    "title": f"Web of Science Search Results for {query}",
                    "content": f"Simulated Web of Science academic search results for: {query}",
                    "source": "webofscience",
                    "source_type": "academic"
                })

        return results[:self.max_results]


class MysterySearch(BaseTool):
    """Tool for searching mystery-specific sources and databases."""
    name: str = "mystery_search"
    description: str = "Search for information about mysterious events from specialized sources."
    max_results: int = 5
    event_types: List[MysteryEventType] = []
    api_keys: Dict[str, str] = {}
    tool_config: Dict[str, Any] = {}
    
    def __init__(self, **kwargs):
        """Initialize the mystery search tool."""
        super().__init__(**kwargs)
        self.event_types = self.event_types or list(config.mystery.mystery_search_types.keys())
        self.api_keys = {
            "mufon": config.api.mufon_api_key or "",
            "paranormal_db": config.api.paranormal_db_api_key or "",
            "nuforc": "", # NUFORC doesn't require an API key for basic search
        }
        self.tool_config = {
            "keywords": config.mystery.mystery_keywords
        }
    
    def _run(self, query: str) -> List[Dict[str, Any]]:
        """Run the mystery search.
        
        Args:
            query: The search query
            
        Returns:
            List of mystery search results
        """
        logger.info(f"Searching mystery sources for: {query}")
        
        results = []
        
        # Enhance query with mystery keywords based on detected event type
        enhanced_query = self._enhance_query(query)
        
        # First use regular web search as fallback
        web_results = get_web_search_tool(self.max_results).invoke(enhanced_query)
        
        # Parse web results
        if isinstance(web_results, str):
            try:
                parsed_results = json.loads(web_results)
                if isinstance(parsed_results, list):
                    for result in parsed_results:
                        results.append({
                            "title": result.get("title", ""),
                            "content": result.get("content", ""),
                            "url": result.get("url", ""),
                            "source": "web_search",
                            "source_type": "web"
                        })
            except json.JSONDecodeError:
                # Handle as text
                results.append({
                    "title": "Web Search Results",
                    "content": web_results,
                    "source": "web_search",
                    "source_type": "web"
                })
        
        # Simulate specialized mystery database searches
        # In a real implementation, these would connect to actual APIs
        event_type = self._detect_event_type(query)
        if event_type and event_type in config.mystery.mystery_search_types:
            search_sources = config.mystery.mystery_search_types[event_type]
            for source in search_sources:
                if source == "mufon" and self.api_keys.get("mufon"):
                    results.append(self._simulated_search(query, "mufon", "MUFON UFO Sighting Report"))
                elif source == "nuforc": # No API key needed
                    results.append(self._simulated_search(query, "nuforc", "NUFORC UFO Sighting Report"))
                elif source == "paranormal_db" and self.api_keys.get("paranormal_db"):
                    results.append(self._simulated_search(query, "paranormal_db", "Paranormal Activity Database Report"))

        return results[:self.max_results]
    
    def _simulated_search(self, query: str, source: str, title_prefix: str) -> Dict[str, str]:
        """Simulate a search to a specialized database."""
        return {
            "title": f"{title_prefix} for {query}",
            "content": f"Simulated {source} database search results for: {query}",
            "source": source,
            "source_type": "specialized_database"
        }

    def _detect_event_type(self, query: str) -> Optional[str]:
        """Detect event type from query and return its string name."""
        query_lower = query.lower()
        for event_name, keywords in self.tool_config.get("keywords", {}).items():
            if any(keyword.lower() in query_lower for keyword in keywords):
                return event_name
        return None

    def _enhance_query(self, query: str) -> str:
        """Enhance the query with mystery-specific keywords."""
        event_type = self._detect_event_type(query)
        
        if not event_type:
            return query
        
        # Add relevant keywords to the query
        enhanced_terms = []
        keywords_dict = self.tool_config.get("keywords", {})
        if event_type in keywords_dict:
            # Add up to 2 additional keywords
            enhanced_terms = keywords_dict[event_type][:2]
        
        enhanced_query = f"{query} {' '.join(enhanced_terms)}".strip()
        logger.info(f"Enhanced query: {enhanced_query}")
        return enhanced_query


# Get the selected search tool
def get_web_search_tool(max_search_results: int, engine: SearchEngine = SearchEngine.DUCKDUCKGO):
    """Get the configured web search tool."""
    if engine == SearchEngine.TAVILY:
        # Tavily search not available, fallback to DuckDuckGo
        return LoggedDuckDuckGoSearch(name="web_search", max_results=max_search_results)
    elif engine == SearchEngine.DUCKDUCKGO:
        return LoggedDuckDuckGoSearch(name="web_search", max_results=max_search_results)
    elif engine == SearchEngine.BRAVE_SEARCH:
        from pydantic import SecretStr
        return LoggedBraveSearch(
            name="web_search",
            search_wrapper=BraveSearchWrapper(
                api_key=SecretStr(config.api.brave_search_api_key or ""),
                search_kwargs={"count": max_search_results},
            ),
        )
    # elif engine == SearchEngine.BAIDU:
    #     # BAIDU search not implemented or not available in SearchEngine
    #     return LoggedDuckDuckGoSearch(name="web_search", max_results=max_search_results)
    else:
        # Default to DuckDuckGo for unsupported engines
        return LoggedDuckDuckGoSearch(name="web_search", max_results=max_search_results)


def get_academic_search_tool(max_search_results: int = 5, databases: Optional[List[str]] = None):
    """Get the academic search tool."""
    return AcademicSearch(max_results=max_search_results, databases=databases)


def get_mystery_search_tool(max_search_results: int = 5, event_types: Optional[List[str]] = None):
    """Get the mystery search tool."""
    return MysterySearch(max_results=max_search_results, event_types=event_types)


@tool
@log_io
def search_academic_databases(
    query: str,
    databases: Optional[List[str]] = None,
    max_results: int = 5
) -> str:
    """Search academic databases for scholarly articles and papers."""
    try:
        academic_search = AcademicSearch(max_results=max_results, databases=databases)
        results = academic_search.invoke(query)
        return json.dumps(results, ensure_ascii=False)
    except Exception as e:
        error_msg = f"Failed to search academic databases. Error: {repr(e)}"
        logger.error(error_msg)
        return error_msg


@tool
@log_io
def search_mystery_sources(
    query: str,
    event_types: Optional[List[str]] = None,
    max_results: int = 5
) -> str:
    """Search mystery-specific sources and databases."""
    try:
        mystery_search = MysterySearch(max_results=max_results, event_types=event_types)
        results = mystery_search.invoke(query)
        return json.dumps(results, ensure_ascii=False)
    except Exception as e:
        error_msg = f"Failed to search mystery sources. Error: {repr(e)}"
        logger.error(error_msg)
        return error_msg