"""Tests for configuration modules."""

import os
import tempfile
import pytest
from pathlib import Path
from typing import Dict, Any

import sys
sys.path.append(str(Path(__file__).parent.parent / "src"))

from config.base import BaseConfig, ConfigLoader, APIConfig
from config.system import (
    SystemConfig, DataSourceConfig, MysteryEventConfig,
    PerformanceConfig, SecurityConfig, load_system_config
)
from config.components import (
    ComponentsConfig, ToolConfig, AgentConfig,
    SearchEngine, RAGProvider, AnalysisEngine, DataExtractor,
    AgentType, load_components_config
)
from config.llm import LLMConfig, LLMProviderConfig, LLMType, LLMProvider


class TestConfigLoader:
    """Test ConfigLoader functionality."""
    
    def test_load_yaml_basic(self):
        """Test basic YAML loading."""
        yaml_content = """
test_key: test_value
nested:
  key1: value1
  key2: value2
list_items:
  - item1
  - item2
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            f.write(yaml_content)
            f.flush()
            
            loader = ConfigLoader()
            data = loader.load_yaml(f.name)
            
            assert data['test_key'] == 'test_value'
            assert data['nested']['key1'] == 'value1'
            assert data['list_items'] == ['item1', 'item2']
            
        os.unlink(f.name)
    
    def test_environment_variable_expansion(self):
        """Test environment variable expansion."""
        os.environ['TEST_VAR'] = 'test_value'
        
        yaml_content = """
api_key: ${TEST_VAR}
base_url: https://api.example.com
timeout: ${TEST_TIMEOUT:30}
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            f.write(yaml_content)
            f.flush()
            
            loader = ConfigLoader()
            data = loader.load_yaml(f.name)
            
            assert data['api_key'] == 'test_value'
            assert data['timeout'] == '30'  # Default value
            
        os.unlink(f.name)
        del os.environ['TEST_VAR']
    
    def test_deep_merge(self):
        """Test deep merge functionality."""
        loader = ConfigLoader()
        
        base = {
            'level1': {
                'key1': 'value1',
                'key2': 'value2'
            },
            'simple': 'base_value'
        }
        
        override = {
            'level1': {
                'key2': 'new_value2',
                'key3': 'value3'
            },
            'simple': 'override_value'
        }
        
        result = loader.deep_merge(base, override)
        
        assert result['level1']['key1'] == 'value1'
        assert result['level1']['key2'] == 'new_value2'
        assert result['level1']['key3'] == 'value3'
        assert result['simple'] == 'override_value'


class TestAPIConfig:
    """Test APIConfig functionality."""
    
    def test_api_config_creation(self):
        """Test APIConfig creation and validation."""
        config = APIConfig(
            api_key='test_key',
            base_url='https://api.example.com',
            timeout=30,
            max_retries=3
        )
        
        assert config.api_key == 'test_key'
        assert config.base_url == 'https://api.example.com'
        assert config.timeout == 30
        assert config.max_retries == 3


class TestSystemConfig:
    """Test SystemConfig functionality."""
    
    def test_data_source_config(self):
        """Test DataSourceConfig creation and validation."""
        from config.system import DataSourceType
        config = DataSourceConfig(
            name='test_source',
            type=DataSourceType.ACADEMIC,
            base_url='https://example.com',
            api_key='test_key',
            enabled=True
        )
        
        assert config.name == 'test_source'
        
        # Test from_dict
        data = {
            'name': 'dict_source',
            'type': 'academic',
            'base_url': 'https://dict.com',
            'enabled': False
        }
        
        dict_config = DataSourceConfig.from_dict(data)
        assert dict_config.name == 'dict_source'
        assert dict_config.enabled is False
    
    def test_mystery_event_config(self):
        """Test MysteryEventConfig functionality."""
        from config.system import MysteryEventType
        
        # Create config with test data
        config = MysteryEventConfig(
            keywords={MysteryEventType.UFO: ["UFO", "飞碟"]},
            credibility_threshold=0.5
        )
        
        # Test keyword retrieval
        ufo_keywords = config.get_keywords_for_type(MysteryEventType.UFO)
        assert isinstance(ufo_keywords, list)
        assert len(ufo_keywords) > 0
        assert "UFO" in ufo_keywords
        
        # Test validation
        assert config.validate()
    
    def test_system_config_yaml_loading(self):
        """Test SystemConfig loading from YAML."""
        yaml_content = """
system:
  name: "Test System"
  version: "1.0.0"
  debug: true

mystery:
  keywords:
    ufo: ["UFO", "飞碟", "不明飞行物"]
  credibility_threshold: 0.5
  data_sources:
    cnki:
      name: "CNKI"
      type: "academic"
      base_url: "https://cnki.net"
      enabled: true

performance:
  max_memory_mb: 1024
  max_concurrent_requests: 10

security:
  api_rate_limit: 1000
  max_file_size_mb: 100
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            f.write(yaml_content)
            f.flush()
            
            config = load_system_config(f.name)
            
            assert config.name == 'Test System'
            assert config.debug is True
            assert len(config.mystery_config.data_sources) > 0
            assert 'cnki' in config.mystery_config.data_sources
            
        os.unlink(f.name)


class TestComponentsConfig:
    """Test ComponentsConfig functionality."""
    
    def test_tool_config(self):
        """Test ToolConfig creation and validation."""
        api_config = APIConfig(
            api_key='test_key',
            base_url='https://api.example.com'
        )
        
        tool = ToolConfig(
            name='Test Tool',
            type='search',
            enabled=True,
            api_config=api_config,
            parameters={'max_results': 10}
        )
        
        assert tool.validate()
        assert tool.name == 'Test Tool'
        
        # Test to_dict and from_dict
        tool_dict = tool.to_dict()
        recreated_tool = ToolConfig.from_dict(tool_dict)
        
        assert recreated_tool.name == tool.name
        assert recreated_tool.type == tool.type
        assert recreated_tool.api_config.api_key == tool.api_config.api_key
    
    def test_agent_config(self):
        """Test AgentConfig creation and validation."""
        agent = AgentConfig(
            name='Test Agent',
            type=AgentType.MYSTERY_RESEARCHER,
            llm_type=LLMType.RESEARCH,
            description='Test agent description',
            capabilities=['analysis', 'research'],
            tools=['tool1', 'tool2'],
            enabled=True
        )
        
        assert agent.validate()
        assert agent.name == 'Test Agent'
        
        # Test to_dict and from_dict
        agent_dict = agent.to_dict()
        recreated_agent = AgentConfig.from_dict(agent_dict)
        
        assert recreated_agent.name == agent.name
        assert recreated_agent.type == agent.type
        assert recreated_agent.llm_type == agent.llm_type
    
    def test_components_config_yaml_loading(self):
        """Test ComponentsConfig loading from YAML."""
        yaml_content = """
tools:
  search_tool:
    name: "Search Tool"
    type: "search"
    enabled: true
    parameters:
      max_results: 10
      timeout: 30

agents:
  researcher:
    name: "Researcher Agent"
    type: "mystery_researcher"
    llm_type: "research"
    description: "Research agent"
    capabilities:
      - "analysis"
      - "research"
    tools:
      - "search_tool"
    enabled: true

defaults:
  timeout: 30
  max_retries: 3

workflows:
  research_workflow:
    steps:
      - "search"
      - "analyze"
      - "report"
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            f.write(yaml_content)
            f.flush()
            
            config = load_components_config(f.name)
            
            assert 'search_tool' in config.tools
            assert config.tools['search_tool'].name == 'Search Tool'
            
            assert 'researcher' in config.agents
            assert config.agents['researcher'].name == 'Researcher Agent'
            
            assert config.validate()
            
        os.unlink(f.name)
    
    def test_components_config_methods(self):
        """Test ComponentsConfig utility methods."""
        # Create test configuration
        tool = ToolConfig(
            name='Test Tool',
            type='search',
            enabled=True
        )
        
        agent = AgentConfig(
            name='Test Agent',
            type=AgentType.MYSTERY_RESEARCHER,
            llm_type=LLMType.RESEARCH,
            enabled=True
        )
        
        config = ComponentsConfig(
            tools={'test_tool': tool},
            agents={'test_agent': agent}
        )
        
        # Test get methods
        assert config.get_tool('test_tool') == tool
        assert config.get_agent('test_agent') == agent
        
        # Test enabled methods
        enabled_tools = config.get_enabled_tools()
        enabled_agents = config.get_enabled_agents()
        
        assert 'test_tool' in enabled_tools
        assert 'test_agent' in enabled_agents
        
        # Test validation
        assert config.validate()


class TestLLMConfig:
    """Test LLM configuration functionality."""
    
    def test_llm_provider_config(self):
        """Test LLMProviderConfig creation."""
        config = LLMProviderConfig(
            api_key='test_key',
            base_url='https://api.openai.com/v1',
            models={
                LLMType.BASIC.value: 'gpt-3.5-turbo',
                LLMType.RESEARCH.value: 'gpt-4'
            }
        )
        
        assert config.api_key == 'test_key'
        assert config.models[LLMType.BASIC.value] == 'gpt-3.5-turbo'
    
    def test_llm_config(self):
        """Test LLMConfig creation and validation."""
        provider_config = LLMProviderConfig(
            api_key='test_key',
            models={LLMType.BASIC.value: 'gpt-3.5-turbo'}
        )
        
        config = LLMConfig(
            providers={'openai': provider_config},
            default_providers=['openai'],
            type_provider_mapping={
                LLMType.BASIC.value: ['openai']
            }
        )
        
        assert config.validate()
        assert config.providers['openai'] == provider_config


if __name__ == '__main__':
    pytest.main([__file__])