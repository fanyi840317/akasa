#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for tools API endpoints."""

import pytest
import json
from pathlib import Path
import sys

# Add src directory to path
backend_dir = Path(__file__).parent.parent
src_dir = backend_dir / 'src'
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from api.app import create_app


@pytest.fixture
def app():
    """Create test Flask app."""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestToolsAPI:
    """Test cases for tools API endpoints."""
    
    def test_list_tools(self, client):
        """Test listing all available tools."""
        response = client.get('/api/tools/')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'data' in data
        assert 'tools' in data['data']
        assert 'total' in data['data']
        assert isinstance(data['data']['tools'], list)
        assert data['data']['total'] >= 0
    
    def test_get_tool_info_existing(self, client):
        """Test getting info for an existing tool."""
        # First get the list of tools to find an existing one
        response = client.get('/api/tools/')
        data = json.loads(response.data)
        
        if data['data']['tools']:
            tool_name = data['data']['tools'][0]['name']
            
            response = client.get(f'/api/tools/{tool_name}')
            assert response.status_code == 200
            
            tool_data = json.loads(response.data)
            assert tool_data['success'] is True
            assert 'data' in tool_data
            assert tool_data['data']['name'] == tool_name
    
    def test_get_tool_info_nonexistent(self, client):
        """Test getting info for a non-existent tool."""
        response = client.get('/api/tools/nonexistent_tool')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data
    
    def test_get_tool_types(self, client):
        """Test getting available tool types."""
        response = client.get('/api/tools/types')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'data' in data
        assert 'tool_types' in data['data']
        assert 'categories' in data['data']
        assert isinstance(data['data']['tool_types'], dict)
        assert isinstance(data['data']['categories'], list)
    
    def test_tool_test_nonexistent(self, client):
        """Test testing a non-existent tool."""
        response = client.post('/api/tools/nonexistent_tool/test',
                             json={'query': 'test'})
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data
    
    def test_tool_test_with_params(self, client):
        """Test testing a tool with parameters."""
        # First get the list of tools to find an enabled one
        response = client.get('/api/tools/')
        data = json.loads(response.data)
        
        enabled_tools = [t for t in data['data']['tools'] if t['enabled']]
        
        if enabled_tools:
            tool_name = enabled_tools[0]['name']
            tool_type = enabled_tools[0]['type']
            
            # Prepare test parameters based on tool type
            test_params = {}
            if tool_type in ['duckduckgo', 'tavily', 'google']:
                test_params = {'query': 'test search'}
            elif tool_type == 'arxiv':
                test_params = {'query': 'machine learning'}
            elif tool_type == 'crawl':
                test_params = {'url': 'https://example.com'}
            
            response = client.post(f'/api/tools/{tool_name}/test',
                                 json=test_params)
            
            # The test might fail due to missing API keys or network issues,
            # but it should return a proper response structure
            data = json.loads(response.data)
            assert 'success' in data
            
            if data['success']:
                assert 'data' in data
                assert 'result' in data['data']
            else:
                assert 'error' in data
    
    def test_tool_test_disabled_tool(self, client):
        """Test testing a disabled tool."""
        # First get the list of tools to find a disabled one
        response = client.get('/api/tools/')
        data = json.loads(response.data)
        
        disabled_tools = [t for t in data['data']['tools'] if not t['enabled']]
        
        if disabled_tools:
            tool_name = disabled_tools[0]['name']
            
            response = client.post(f'/api/tools/{tool_name}/test',
                                 json={'query': 'test'})
            assert response.status_code == 400
            
            data = json.loads(response.data)
            assert data['success'] is False
            assert 'disabled' in data['error'].lower()


if __name__ == '__main__':
    pytest.main([__file__])