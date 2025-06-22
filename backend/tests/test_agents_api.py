"""Tests for agents API routes."""

import json
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from api.app import create_app
from config.agents import AgentType, AgentConfig
from config.llm import LLMType


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


@pytest.fixture
def mock_config():
    """Mock components config."""
    mock_agent_config = AgentConfig(
        name="Test Agent",
        type=AgentType.MYSTERY_RESEARCHER,
        llm_type=LLMType.RESEARCH,
        description="Test description",
        prompt_template="Test prompt",
        parameters={"temperature": 0.7, "max_tokens": 2000}
    )
    
    mock_config = MagicMock()
    mock_config.agents = {
        AgentType.MYSTERY_RESEARCHER: mock_agent_config,
        AgentType.ACADEMIC_RESEARCHER: mock_agent_config
    }
    return mock_config


class TestAgentsAPI:
    """Test cases for agents API."""
    
    @patch('api.routes.agents.load_components_config')
    def test_get_all_agents(self, mock_load_config, client, mock_config):
        """Test getting all agents."""
        mock_load_config.return_value = mock_config
        
        response = client.get('/api/agents/')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'agents' in data['data']
        assert 'agent_llm_mapping' in data['data']
        assert 'available_types' in data['data']
    
    @patch('api.routes.agents.load_components_config')
    def test_get_specific_agent(self, mock_load_config, client, mock_config):
        """Test getting specific agent."""
        mock_load_config.return_value = mock_config
        
        response = client.get('/api/agents/mystery_researcher')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['agent_type'] == 'mystery_researcher'
        assert 'config' in data['data']
        assert 'llm_type' in data['data']
    
    def test_get_invalid_agent(self, client):
        """Test getting invalid agent type."""
        response = client.get('/api/agents/invalid_agent')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'Invalid agent type' in data['error']
    
    @patch('api.routes.agents.load_components_config')
    def test_get_nonexistent_agent(self, mock_load_config, client):
        """Test getting non-existent agent."""
        mock_config = MagicMock()
        mock_config.agents = {}
        mock_load_config.return_value = mock_config
        
        response = client.get('/api/agents/mystery_researcher')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'not found' in data['error']
    
    @patch('builtins.open')
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.mkdir')
    @patch('yaml.dump')
    @patch('yaml.safe_load')
    def test_update_agent(self, mock_yaml_load, mock_yaml_dump, mock_mkdir, mock_exists, mock_open, client):
        """Test updating agent configuration."""
        mock_exists.return_value = False
        mock_yaml_load.return_value = {}
        
        update_data = {
            'name': 'Updated Agent',
            'description': 'Updated description',
            'system_prompt': 'Updated prompt',
            'temperature': 0.8,
            'max_tokens': 3000
        }
        
        response = client.put('/api/agents/mystery_researcher', 
                            data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'updated successfully' in data['message']
    
    def test_update_agent_no_data(self, client):
        """Test updating agent with no data."""
        response = client.put('/api/agents/mystery_researcher')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'No data provided' in data['error']
    
    def test_update_agent_missing_fields(self, client):
        """Test updating agent with missing required fields."""
        update_data = {
            'name': 'Test Agent'
            # Missing other required fields
        }
        
        response = client.put('/api/agents/mystery_researcher',
                            data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'Missing required field' in data['error']
    
    def test_update_agent_invalid_data(self, client):
        """Test updating agent with invalid data types."""
        update_data = {
            'name': 'Test Agent',
            'description': 'Test description',
            'system_prompt': 'Test prompt',
            'temperature': 'invalid',  # Should be number
            'max_tokens': 2000
        }
        
        response = client.put('/api/agents/mystery_researcher',
                            data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'temperature must be a number' in data['error']
    
    def test_update_invalid_agent_type(self, client):
        """Test updating invalid agent type."""
        update_data = {
            'name': 'Test Agent',
            'description': 'Test description',
            'system_prompt': 'Test prompt',
            'temperature': 0.7,
            'max_tokens': 2000
        }
        
        response = client.put('/api/agents/invalid_agent',
                            data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'Invalid agent type' in data['error']
    
    @patch('builtins.open')
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.unlink')
    @patch('yaml.dump')
    @patch('yaml.safe_load')
    def test_delete_agent_config(self, mock_yaml_load, mock_yaml_dump, mock_unlink, mock_exists, mock_open, client):
        """Test deleting agent configuration."""
        mock_exists.return_value = True
        mock_yaml_load.return_value = {
            'components': {
                'agents': {
                    'mystery_researcher': {
                        'name': 'Test Agent'
                    }
                }
            }
        }
        
        response = client.delete('/api/agents/mystery_researcher',
                                content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'reset to default' in data['message']
    
    @patch('api.routes.agents.create_mystery_researcher_agent')
    def test_create_agent_instance(self, mock_create_agent, client):
        """Test creating agent instance."""
        mock_agent = MagicMock()
        mock_create_agent.return_value = mock_agent
        
        create_data = {
            'agent_type': 'mystery_researcher'
        }
        
        response = client.post('/api/agents/create',
                             data=json.dumps(create_data),
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'created successfully' in data['message']
        assert 'agent_id' in data
    
    def test_create_agent_missing_type(self, client):
        """Test creating agent without type."""
        response = client.post('/api/agents/create',
                             data=json.dumps({}),
                             content_type='application/json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'agent_type is required' in data['error']
    
    def test_get_agent_types(self, client):
        """Test getting agent types."""
        response = client.get('/api/agents/types',
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'agent_types' in data['data']
        assert 'llm_types' in data['data']
        assert 'agent_llm_mapping' in data['data']
    
    def test_validate_agent_config(self, client):
        """Test validating agent configuration."""
        valid_config = {
            'name': 'Test Agent',
            'description': 'Test description',
            'system_prompt': 'Test prompt',
            'temperature': 0.7,
            'max_tokens': 2000
        }
        
        response = client.post('/api/agents/validate',
                             data=json.dumps(valid_config),
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'valid' in data['message']
    
    def test_validate_invalid_agent_config(self, client):
        """Test validating invalid agent configuration."""
        # Test with no data
        response = client.post('/api/agents/validate',
                             data=json.dumps({}),
                             content_type='application/json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'No data provided' in data['error']