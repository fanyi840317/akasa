# SPDX-License-Identifier: MIT

# Base configuration
from .base import (
    ConfigType, BaseConfig, ConfigLoader, ConfigRegistry,
    APIConfig, DatabaseConfig, CacheConfig
)

# System configuration
from .system import (
    MysteryEventType, DataSourceType, DataSourceConfig, MysteryEventConfig,
    PerformanceConfig, SecurityConfig, SystemConfig,
    load_system_config
)

# Agents configuration
from .agents import (
    AgentType, AgentConfig, load_agents_config
)

# Tools configuration
from .tools import (
    SearchEngine, RAGProvider, AnalysisEngine, DataExtractor,
    ToolConfig, load_tools_config
)

# LLM configuration
from .llm import (
    LLMType, LLMProvider, LLMProviderConfig, LLMConfig,
    get_llm_by_type, create_llm_from_config, load_llm_config
)

# Validation
from .validator import (
    ValidationLevel, ValidationResult, ValidationReport, ConfigValidator,
    validate_all_configs, print_validation_results
)

# Unified configuration loader
from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class Config:
    """Unified configuration container."""
    system: Optional[SystemConfig] = None
    agents: Optional[Dict[str, AgentConfig]] = None
    tools: Optional[ToolConfig] = None
    llm: Optional[LLMConfig] = None

def load_config() -> Config:
    """Load all configurations."""
    return Config(
        system=load_system_config(),
        agents=load_agents_config(),
        tools=load_tools_config(),
        llm=load_llm_config()
    )

__all__ = [
    # Base
    'ConfigType',
    'BaseConfig',
    'ConfigLoader',
    'ConfigRegistry',
    'APIConfig',
    'DatabaseConfig',
    'CacheConfig',
    
    # System
    'MysteryEventType',
    'DataSourceType',
    'DataSourceConfig',
    'MysteryEventConfig',
    'PerformanceConfig',
    'SecurityConfig',
    'SystemConfig',
    'load_system_config',
    
    # Agents
    'AgentType',
    'AgentConfig',
    'load_agents_config',
    
    # Tools
    'SearchEngine',
    'RAGProvider',
    'AnalysisEngine',
    'DataExtractor',
    'ToolConfig',
    'load_tools_config',
    
    # LLMs
    'LLMType',
    'LLMProvider',
    'LLMProviderConfig',
    'LLMConfig',
    'get_llm_by_type',
    'create_llm_from_config',
    'load_llm_config',
    
    # Validation
    'ValidationLevel',
    'ValidationResult',
    'ValidationReport',
    'ConfigValidator',
    'validate_all_configs',
    'print_validation_results',
    
    # Unified config
    'Config',
    'load_config',
]