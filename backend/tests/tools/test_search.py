# -*- coding: utf-8 -*-
# Copyright (c) 2024 Lingjing
# SPDX-License-Identifier: MIT

import pytest
import json
from unittest.mock import patch, MagicMock
from src.tools.search import AcademicSearch, MysterySearch
from src.config import MysteryEventType

class TestSearchTools:
    """Test suite for search tools."""

    @pytest.fixture
    def mock_arxiv_tool(self):
        """Fixture to mock the LoggedArxivSearch tool."""
        with patch('src.tools.search.LoggedArxivSearch') as mock_tool:
            mock_instance = MagicMock()
            # Arxiv tool returns a list of dicts, not a JSON string
            mock_instance.invoke.return_value = [
                {
                    'title': 'Mock Arxiv Paper',
                    'authors': 'Mock Author',
                    'summary': 'A summary of the mock paper.',
                    'published': '2024-01-01',
                    'entry_id': 'http://arxiv.org/abs/2401.00001'
                }
            ]
            mock_tool.return_value = mock_instance
            yield mock_tool

    @patch('src.tools.search.LoggedArxivSearch')
    def test_academic_search_arxiv(self, mock_arxiv_tool_class):
        """Test academic search with Arxiv."""
        mock_arxiv_tool = MagicMock()
        mock_arxiv_tool.invoke.return_value = "Published: 2023-10-26\nTitle: Test Arxiv Paper\nAuthors: Test Author\nSummary: A summary of the test paper."
        mock_arxiv_tool_class.return_value = mock_arxiv_tool

        search_tool = AcademicSearch(databases=["arxiv"])
        results = search_tool.invoke("test query")

        assert len(results) == 1, "Expected 1 result from Arxiv search"
        assert results[0]['source'] == 'arxiv'
        assert "Test Arxiv Paper" in results[0]['content']
        mock_arxiv_tool.invoke.assert_called_once_with("test query")

    def test_academic_search_simulated_db(self):
        """Test the AcademicSearch tool with a simulated database like CNKI."""
        search_tool = AcademicSearch(databases=["cnki"], max_results=1)
        # Manually set the API key for the test to simulate it being available
        search_tool.api_keys['cnki'] = 'fake_key'
        results = search_tool.invoke("AI ethics")
        assert len(results) == 1, "Expected 1 result from simulated CNKI search"
        result = results[0]
        assert result['source'] == 'cnki'
        assert "Simulated CNKI academic search results" in result['content']

    def test_mystery_search_enhancement(self):
        """Test that mystery search enhances the query with keywords."""
        search_tool = MysterySearch()
        search_tool.tool_config = {
            'keywords': {
                'UFO': ['sighting', 'unidentified']
            }
        }

        # Mock the internal search tool to avoid actual web requests
        with patch.object(search_tool, '_get_search_tool') as mock_get_tool:
            mock_search_instance = MagicMock()
            mock_search_instance.invoke.return_value = json.dumps([{"title": "Test Result", "content": "..."}])
            mock_get_tool.return_value = mock_search_instance

            search_tool.invoke("ufo over area 51")

            # Check that the query was enhanced before being passed to the search tool
            mock_search_instance.invoke.assert_called_once()
            called_query = mock_search_instance.invoke.call_args[0][0]
            assert "sighting" in called_query
            assert "unidentified" in called_query
            assert "ufo over area 51" in called_query