# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Union
from enum import Enum
from pathlib import Path

from ..base import BaseConfig, ConfigType, ConfigLoader, APIConfig
from ..llm import LLMType


# Tool-related enums
class SearchEngine(str, Enum):
    """Available search engines."""
    TAVILY = "tavily"
    GOOGLE = "google"
    BING = "bing"
    DUCKDUCKGO = "duckduckgo"
    BAIDU = "baidu"
    YANDEX = "yandex"


class RAGProvider(str, Enum):
    """Available RAG providers."""
    CHROMA = "chroma"
    PINECONE = "pinecone"
    WEAVIATE = "weaviate"
    QDRANT = "qdrant"
    FAISS = "faiss"
    ELASTICSEARCH = "elasticsearch"


class AnalysisEngine(str, Enum):
    """Available analysis engines."""
    SPACY = "spacy"
    NLTK = "nltk"
    TRANSFORMERS = "transformers"
    OPENAI = "openai"
    CUSTOM = "custom"


class DataExtractor(str, Enum):
    """Available data extractors."""
    BEAUTIFULSOUP = "beautifulsoup"
    SCRAPY = "scrapy"
    SELENIUM = "selenium"
    PLAYWRIGHT = "playwright"
    REQUESTS = "requests"


# Agent-related enums
class AgentType(str, Enum):
    """Types of agents in the system."""
    MYSTERY_RESEARCHER = "mystery_researcher"
    ACADEMIC_RESEARCHER = "academic_researcher"
    CREDIBILITY_ANALYZER = "credibility_analyzer"
    DATA_COLLECTOR = "data_collector"
    REPORT_GENERATOR = "report_generator"
    CORRELATION_ANALYZER = "correlation_analyzer"
    TIMELINE_BUILDER = "timeline_builder"
    EVIDENCE_EVALUATOR = "evidence_evaluator"


@dataclass
class ToolConfig:
    """Configuration for a specific tool."""
    name: str
    type: str
    enabled: bool = True
    api_config: Optional[APIConfig] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ToolConfig':
        """Create ToolConfig from dictionary."""
        api_config = None
        if 'api_config' in data and data['api_config']:
            api_config = APIConfig(
                api_key=data['api_config']['api_key'],
                base_url=data['api_config'].get('base_url', ''),
                timeout=data['api_config'].get('timeout', 30),
                max_retries=data['api_config'].get('max_retries', 3),
                rate_limit=data['api_config'].get('rate_limit')
            )
        
        return cls(
            name=data['name'],
            type=data['type'],
            enabled=data.get('enabled', True),
            api_config=api_config,
            parameters=data.get('parameters', {})
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            'name': self.name,
            'type': self.type,
            'enabled': self.enabled,
            'parameters': self.parameters
        }
        
        if self.api_config:
            result['api_config'] = {
                'api_key': self.api_config.api_key,
                'base_url': self.api_config.base_url,
                'timeout': self.api_config.timeout,
                'max_retries': self.api_config.max_retries,
                'rate_limit': self.api_config.rate_limit
            }
        
        return result
    
    def validate(self) -> bool:
        """Validate tool configuration."""
        if not self.name:
            return False
        if self.api_config and not self.api_config.api_key:
            return False
        return True


@dataclass
class AgentConfig:
    """Configuration for a specific agent."""
    name: str
    type: AgentType
    llm_type: LLMType
    description: str = ""
    capabilities: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    prompt_template: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentConfig':
        """Create AgentConfig from dictionary."""
        return cls(
            name=data['name'],
            type=AgentType(data['type']),
            llm_type=LLMType(data['llm_type']),
            description=data.get('description', ''),
            capabilities=data.get('capabilities', []),
            tools=data.get('tools', []),
            prompt_template=data.get('prompt_template', ''),
            parameters=data.get('parameters', {}),
            enabled=data.get('enabled', True)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'type': self.type.value,
            'llm_type': self.llm_type.value,
            'description': self.description,
            'capabilities': self.capabilities,
            'tools': self.tools,
            'prompt_template': self.prompt_template,
            'parameters': self.parameters,
            'enabled': self.enabled
        }
    
    def validate(self) -> bool:
        """Validate agent configuration."""
        return bool(self.name and self.type and self.llm_type)


@dataclass
class ComponentsConfig(BaseConfig):
    """Main components configuration."""
    tools: Dict[str, ToolConfig] = field(default_factory=dict)
    agents: Dict[str, AgentConfig] = field(default_factory=dict)
    defaults: Dict[str, Any] = field(default_factory=dict)
    workflows: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ComponentsConfig':
        """Create ComponentsConfig from dictionary."""
        tools = {}
        if 'tools' in data:
            for tool_name, tool_data in data['tools'].items():
                tools[tool_name] = ToolConfig.from_dict(tool_data)
        
        agents = {}
        if 'agents' in data:
            for agent_name, agent_data in data['agents'].items():
                agents[agent_name] = AgentConfig.from_dict(agent_data)
        
        return cls(
            tools=tools,
            agents=agents,
            defaults=data.get('defaults', {}),
            workflows=data.get('workflows', {})
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'tools': {name: tool.to_dict() for name, tool in self.tools.items()},
            'agents': {name: agent.to_dict() for name, agent in self.agents.items()},
            'defaults': self.defaults,
            'workflows': self.workflows
        }
    
    def validate(self) -> bool:
        """Validate components configuration."""
        # Validate all tools
        for tool in self.tools.values():
            if not tool.validate():
                return False
        
        # Validate all agents
        for agent in self.agents.values():
            if not agent.validate():
                return False
        
        return True
    
    def get_tool(self, name: str) -> Optional[ToolConfig]:
        """Get tool configuration by name."""
        return self.tools.get(name)
    
    def get_agent(self, name: str) -> Optional[AgentConfig]:
        """Get agent configuration by name."""
        return self.agents.get(name)
    
    def get_enabled_tools(self) -> Dict[str, ToolConfig]:
        """Get all enabled tools."""
        return {name: tool for name, tool in self.tools.items() if tool.enabled}
    
    def get_enabled_agents(self) -> Dict[str, AgentConfig]:
        """Get all enabled agents."""
        return {name: agent for name, agent in self.agents.items() if agent.enabled}


def load_components_config(config_path: Optional[str] = None) -> ComponentsConfig:
    """Load components configuration from YAML file."""
    if config_path is None:
        config_path = Path(__file__).parent / "components.yaml"
    
    loader = ConfigLoader()
    data = loader.load_yaml(config_path)
    return ComponentsConfig.from_dict(data)


# Removed duplicate ComponentsConfig class - using the new YAML-compatible version above