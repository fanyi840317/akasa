# -*- coding: utf-8 -*-
# Copyright (c) 2024 Lingjing
# SPDX-License-Identifier: MIT

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from src.tools.search import (
    AcademicSearch,
    MysterySearch,
    get_web_search_tool,
    get_academic_search_tool,
    get_mystery_search_tool,
    search_academic_databases,
    search_mystery_sources
)
from src.config import SearchEngine


class TestAcademicSearch:
    """Test cases for AcademicSearch class."""
    
    def test_academic_search_initialization(self):
        """Test AcademicSearch initialization."""
        search = AcademicSearch(max_results=10, databases=["arxiv", "cnki"])
        assert search.max_results == 10
        assert search.databases == ["arxiv", "cnki"]
        assert search.name == "academic_search"
        assert "scholarly articles" in search.description
    
    def test_academic_search_default_params(self):
        """Test AcademicSearch with default parameters."""
        search = AcademicSearch()
        assert search.max_results == 5
        assert "arxiv" in search.databases
        assert "cnki" in search.databases
        assert "wanfang" in search.databases
    
    @patch('src.tools.search.LoggedArxivSearch')
    def test_academic_search_run_arxiv(self, mock_arxiv):
        """Test AcademicSearch._run with arxiv database."""
        # Mock arxiv search results
        mock_tool = Mock()
        mock_tool.invoke.return_value = json.dumps([
            {
                "title": "Test Paper",
                "authors": "Test Author",
                "summary": "Test summary",
                "published": "2024-01-01",
                "entry_id": "http://arxiv.org/abs/2401.00001"
            }
        ])
        mock_arxiv.return_value = mock_tool
        
        search = AcademicSearch(databases=["arxiv"])
        results = search.invoke("quantum computing")
        
        assert len(results) > 0
        assert results[0]["source"] == "arxiv"
        assert results[0]["source_type"] == "academic"
        assert "Test Paper" in results[0]["title"]
    
    def test_academic_search_run_other_databases(self):
        """Test AcademicSearch._run with other databases."""
        with patch.dict('os.environ', {'CNKI_API_KEY': 'test_key'}):
            search = AcademicSearch(databases=["cnki"])
            results = search.invoke("machine learning")
            
            assert len(results) > 0
            assert any(result["source"] == "cnki" for result in results)
    
    def test_academic_search_error_handling(self):
        """Test AcademicSearch error handling."""
        with patch('src.tools.search.LoggedArxivSearch') as mock_arxiv:
            mock_arxiv.side_effect = Exception("API Error")
            
            search = AcademicSearch(databases=["arxiv"])
            results = search.invoke("test query")
            
            # Should handle error gracefully
            assert isinstance(results, list)


class TestMysterySearch:
    """Test cases for MysterySearch class."""
    
    def test_mystery_search_initialization(self):
        """Test MysterySearch initialization."""
        search = MysterySearch(max_results=8, event_types=["UFO"])
        assert search.max_results == 8
        assert search.event_types == ["UFO"]
        assert search.name == "mystery_search"
        assert "mysterious events" in search.description
    
    def test_mystery_search_default_params(self):
        """Test MysterySearch with default parameters."""
        search = MysterySearch()
        assert search.max_results == 5
        assert isinstance(search.event_types, list)
        assert len(search.event_types) > 0
    
    @patch('src.tools.search.get_web_search_tool')
    def test_mystery_search_run(self, mock_web_search):
        """Test MysterySearch._run method."""
        # Mock web search tool
        mock_tool = Mock()
        mock_tool.invoke.return_value = json.dumps([
            {
                "title": "UFO Sighting Report",
                "content": "Strange lights in the sky",
                "url": "http://example.com/ufo"
            }
        ])
        mock_web_search.return_value = mock_tool
        
        search = MysterySearch()
        results = search.invoke("UFO sighting")
        
        assert len(results) > 0
        assert any("UFO" in str(result) for result in results)
    
    def test_mystery_search_enhance_query(self):
        """Test query enhancement functionality."""
        search = MysterySearch()
        
        # Test with UFO-related query
        enhanced = search._enhance_query("strange lights")
        assert "strange lights" in enhanced
        
        # Test with non-mystery query
        enhanced = search._enhance_query("weather forecast")
        assert enhanced == "weather forecast"
    
    @patch('src.tools.search.get_web_search_tool')
    def test_mystery_search_specialized_databases(self, mock_web_search):
        """Test specialized database integration."""
        mock_tool = Mock()
        mock_tool.invoke.return_value = "[]"
        mock_web_search.return_value = mock_tool
        
        with patch.dict('os.environ', {'MUFON_API_KEY': 'test_key'}):
            search = MysterySearch()
            results = search.invoke("UFO encounter")
            
            # Should include MUFON results for UFO queries
            assert any(result.get("source") == "mufon" for result in results)


class TestSearchToolFactories:
    """Test cases for search tool factory functions."""
    
    def test_get_web_search_tool_default(self):
        """Test get_web_search_tool with default engine."""
        tool = get_web_search_tool(5)
        assert tool is not None
        assert hasattr(tool, 'invoke')
    
    def test_get_web_search_tool_different_engines(self):
        """Test get_web_search_tool with different engines."""
        # Test DuckDuckGo
        tool_ddg = get_web_search_tool(5, SearchEngine.DUCKDUCKGO)
        assert tool_ddg is not None
        
        # Test Tavily (should fallback to DuckDuckGo)
        tool_tavily = get_web_search_tool(5, SearchEngine.TAVILY)
        assert tool_tavily is not None
        
        # Test Brave Search
        tool_brave = get_web_search_tool(5, SearchEngine.BRAVE_SEARCH)
        assert tool_brave is not None
    
    def test_get_academic_search_tool(self):
        """Test get_academic_search_tool factory."""
        tool = get_academic_search_tool(10, ["arxiv"])
        assert isinstance(tool, AcademicSearch)
        assert tool.max_results == 10
        assert tool.databases == ["arxiv"]
    
    def test_get_mystery_search_tool(self):
        """Test get_mystery_search_tool factory."""
        tool = get_mystery_search_tool(8, ["UFO"])
        assert isinstance(tool, MysterySearch)
        assert tool.max_results == 8
        assert tool.event_types == ["UFO"]


class TestSearchToolDecorators:
    """Test cases for decorated search tool functions."""
    
    @patch('src.tools.search.AcademicSearch')
    def test_search_academic_databases_success(self, mock_academic):
        """Test search_academic_databases function success case."""
        # Mock AcademicSearch instance
        mock_instance = Mock()
        mock_instance.invoke.return_value = [
            {"title": "Test Paper", "source": "arxiv"}
        ]
        mock_academic.return_value = mock_instance
        
        result = search_academic_databases.invoke({"query": "quantum physics", "databases": ["arxiv"], "max_results": 5})
        
        # Should return JSON string
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert len(parsed) > 0
        assert parsed[0]["title"] == "Test Paper"
    
    @patch('src.tools.search.AcademicSearch')
    def test_search_academic_databases_error(self, mock_academic):
        """Test search_academic_databases function error handling."""
        mock_academic.side_effect = Exception("Database error")
        
        result = search_academic_databases.invoke({"query": "test query"})
        
        # Should return error message
        assert "Failed to search academic databases" in result
        assert "Database error" in result
    
    @patch('src.tools.search.MysterySearch')
    def test_search_mystery_sources_success(self, mock_mystery):
        """Test search_mystery_sources function success case."""
        # Mock MysterySearch instance
        mock_instance = Mock()
        mock_instance.invoke.return_value = [
            {"title": "UFO Report", "source": "mufon"}
        ]
        mock_mystery.return_value = mock_instance
        
        result = search_mystery_sources.invoke({"query": "UFO sighting", "event_types": ["UFO"], "max_results": 3})
        
        # Should return JSON string
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert len(parsed) > 0
        assert parsed[0]["title"] == "UFO Report"
    
    @patch('src.tools.search.MysterySearch')
    def test_search_mystery_sources_error(self, mock_mystery):
        """Test search_mystery_sources function error handling."""
        mock_mystery.side_effect = Exception("Mystery database error")
        
        result = search_mystery_sources.invoke({"query": "test query"})
        
        # Should return error message
        assert "Failed to search mystery sources" in result
        assert "Mystery database error" in result


class TestSearchIntegration:
    """Integration tests for search functionality."""
    
    @patch('src.tools.search.LoggedDuckDuckGoSearch')
    def test_full_search_workflow(self, mock_ddg):
        """Test complete search workflow."""
        # Mock DuckDuckGo search
        mock_tool = Mock()
        mock_tool.invoke.return_value = json.dumps([
            {
                "title": "Search Result",
                "content": "Test content",
                "url": "http://example.com"
            }
        ])
        mock_ddg.return_value = mock_tool
        
        # Test web search
        web_tool = get_web_search_tool(5)
        web_results = web_tool.invoke("test query")
        assert web_results is not None
        
        # Test academic search
        academic_tool = get_academic_search_tool(3)
        academic_results = academic_tool.invoke("research topic")
        assert isinstance(academic_results, list)
        
        # Test mystery search
        mystery_tool = get_mystery_search_tool(3)
        mystery_results = mystery_tool.invoke("paranormal activity")
        assert isinstance(mystery_results, list)
    
    def test_search_result_consistency(self):
        """Test that search results have consistent structure."""
        academic_tool = get_academic_search_tool(1, ["cnki"])
        academic_results = academic_tool.invoke("test")
        
        mystery_tool = get_mystery_search_tool(1)
        mystery_results = mystery_tool.invoke("test")
        
        # Both should return lists
        assert isinstance(academic_results, list)
        assert isinstance(mystery_results, list)
        
        # Results should have consistent fields
        for results in [academic_results, mystery_results]:
            if results:
                result = results[0]
                assert "source" in result
                assert "source_type" in result or "title" in result
    
    def test_error_recovery(self):
        """Test error recovery in search operations."""
        # Test with invalid parameters
        academic_tool = get_academic_search_tool(0, [])
        results = academic_tool.invoke("")
        assert isinstance(results, list)
        
        mystery_tool = get_mystery_search_tool(0, [])
        results = mystery_tool.invoke("")
        assert isinstance(results, list)
    
    @patch('src.tools.search.logger')
    def test_logging_integration(self, mock_logger):
        """Test that search operations are properly logged."""
        academic_tool = get_academic_search_tool(1)
        academic_tool.invoke("test query")
        
        mystery_tool = get_mystery_search_tool(1)
        mystery_tool.invoke("test query")
        
        # Verify logging calls were made
        assert mock_logger.info.called