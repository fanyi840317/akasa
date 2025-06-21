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

# Components configuration
from .components import (
    SearchEngine, RAGProvider, AnalysisEngine, DataExtractor, AgentType,
    ToolConfig, AgentConfig, ComponentsConfig,
    load_components_config
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
from typing import Optional

@dataclass
class Config:
    """Unified configuration container."""
    system: Optional[SystemConfig] = None
    components: Optional[ComponentsConfig] = None
    llm: Optional[LLMConfig] = None

def load_config() -> Config:
    """Load all configurations."""
    return Config(
        system=load_system_config(),
        components=load_components_config(),
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
    
    # Components
    'SearchEngine',
    'RAGProvider',
    'AnalysisEngine',
    'DataExtractor',
    'AgentType',
    'ToolConfig',
    'AgentConfig',
    'ComponentsConfig',
    'load_components_config',
    
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