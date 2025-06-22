# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from enum import Enum
from pathlib import Path

from ..base import BaseConfig, ConfigType, ConfigLoader, APIConfig


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


def load_tools_config(config_path: Optional[str] = None) -> Dict[str, ToolConfig]:
    """Load tools configuration from YAML file."""
    if config_path is None:
        config_path = Path(__file__).parent / "tools.yaml"
    
    loader = ConfigLoader()
    data = loader.load_yaml(config_path)
    
    tools = {}
    if 'tools' in data:
        for tool_name, tool_data in data['tools'].items():
            tools[tool_name] = ToolConfig.from_dict(tool_data)
    
    return tools