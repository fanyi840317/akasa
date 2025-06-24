# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Union, List, Type, TypeVar, cast
from pathlib import Path
import yaml
import os
import re
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ConfigType(str, Enum):
    """Configuration types for different components."""
    SYSTEM = "system"
    LLM = "llm"
    MYSTERY = "mystery"
    AGENT = "agent"
    TOOL = "tool"
    VALIDATOR = "validator"


T = TypeVar('T', bound='BaseConfig')

@dataclass
class BaseConfig(ABC):
    """Base configuration class with common functionality."""
    
    config_type: ConfigType = field(init=False)
    
    @classmethod
    @abstractmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create configuration from dictionary."""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate configuration."""
        pass
        
    @classmethod
    def from_yaml(cls: Type[T], file_path: Union[str, Path], environment: Optional[str] = None) -> T:
        """Create configuration from YAML file.
        
        Args:
            file_path: Path to YAML configuration file
            environment: Optional environment name to apply environment-specific overrides
            
        Returns:
            Configuration instance
        """
        config_data = ConfigLoader.load_yaml(file_path)
        
        # Apply environment-specific overrides if specified
        if environment and "environments" in config_data and environment in config_data["environments"]:
            env_config = config_data["environments"][environment]
            config_data = ConfigLoader.deep_merge(config_data, env_config)
            # Remove the environments section to avoid confusion
            if "environments" in config_data:
                del config_data["environments"]
                
        return cls.from_dict(config_data)
        
    @classmethod
    def from_yaml_files(cls: Type[T], *file_paths: Union[str, Path], environment: Optional[str] = None) -> T:
        """Create configuration from multiple YAML files.
        
        Args:
            *file_paths: Paths to YAML configuration files
            environment: Optional environment name to apply environment-specific overrides
            
        Returns:
            Configuration instance
        """
        config_data = ConfigLoader.load_config_files(*file_paths, environment=environment)
        return cls.from_dict(config_data)


class ConfigLoader:
    """Unified configuration loader with environment variable expansion."""
    
    ENV_VAR_PATTERN = re.compile(r'\${([^}^{]+)}') 
    
    @staticmethod
    def expand_env_vars(value: Any) -> Any:
        """Recursively expand environment variables in configuration values."""
        if isinstance(value, str):
            # Handle ${VAR:default} syntax
            if value.startswith('${') and value.endswith('}'):
                var_expr = value[2:-1]
                if ':' in var_expr:
                    var_name, default_value = var_expr.split(':', 1)
                    return os.getenv(var_name, default_value)
                else:
                    return os.getenv(var_expr, '')
            # Handle ${VAR} within a string
            matches = ConfigLoader.ENV_VAR_PATTERN.findall(value)
            if matches:
                for match in matches:
                    if ':' in match:
                        var_name, default_value = match.split(':', 1)
                        env_value = os.getenv(var_name, default_value)
                    else:
                        env_value = os.getenv(match, '')
                    value = value.replace(f'${{{match}}}', env_value)
            return value
        elif isinstance(value, dict):
            return {k: ConfigLoader.expand_env_vars(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [ConfigLoader.expand_env_vars(item) for item in value]
        return value
    
    @staticmethod
    def load_yaml(file_path: Union[str, Path]) -> Dict[str, Any]:
        """Load and expand YAML configuration file."""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if data is None:
            logger.warning(f"Empty YAML file: {file_path}")
            return {}
            
        return ConfigLoader.expand_env_vars(data)
    
    @staticmethod
    def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries recursively."""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = ConfigLoader.deep_merge(result[key], value)
            else:
                result[key] = value
                
        return result
    
    @staticmethod
    def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
        """Merge multiple configuration dictionaries with deep merging."""
        if not configs:
            return {}
            
        result = configs[0].copy()
        for config in configs[1:]:
            result = ConfigLoader.deep_merge(result, config)
            
        return result
        
    @staticmethod
    def load_config_files(*file_paths: Union[str, Path], environment: Optional[str] = None) -> Dict[str, Any]:
        """Load and merge multiple YAML configuration files.
        
        Args:
            *file_paths: Paths to YAML configuration files
            environment: Optional environment name to apply environment-specific overrides
            
        Returns:
            Merged configuration dictionary
        """
        configs = []
        
        for file_path in file_paths:
            try:
                config = ConfigLoader.load_yaml(file_path)
                configs.append(config)
                logger.info(f"Loaded configuration from {file_path}")
            except FileNotFoundError:
                logger.warning(f"Configuration file not found: {file_path}")
            except Exception as e:
                logger.error(f"Error loading configuration from {file_path}: {e}")
                
        merged_config = ConfigLoader.merge_configs(*configs)
        
        # Apply environment-specific overrides if specified
        if environment and "environments" in merged_config and environment in merged_config["environments"]:
            env_config = merged_config["environments"][environment]
            merged_config = ConfigLoader.deep_merge(merged_config, env_config)
            # Remove the environments section to avoid confusion
            if "environments" in merged_config:
                del merged_config["environments"]
                
        return merged_config


@dataclass
class APIConfig:
    """Common API configuration structure."""
    api_key: str
    base_url: str = ""
    timeout: int = 30
    max_retries: int = 3
    rate_limit: Optional[int] = None
    
    def __post_init__(self):
        if not self.api_key:
            raise ValueError("API key is required")


@dataclass
class DatabaseConfig:
    """Common database configuration structure."""
    host: str
    port: int
    database: str
    username: Optional[str] = None
    password: Optional[str] = None
    timeout: int = 30
    max_connections: int = 10
    
    @property
    def connection_string(self) -> str:
        """Generate connection string based on database type."""
        if self.username and self.password:
            return f"{self.host}:{self.port}/{self.database}"
        return f"{self.host}:{self.port}/{self.database}"


@dataclass
class CacheConfig:
    """Common cache configuration structure."""
    enabled: bool = True
    backend: str = "memory"  # memory, redis, file
    ttl: int = 3600  # seconds
    max_size: int = 1000
    
    def validate(self) -> bool:
        """Validate cache configuration."""
        valid_backends = ["memory", "redis", "file"]
        return self.backend in valid_backends and self.ttl > 0 and self.max_size > 0


class ConfigRegistry:
    """Registry for managing different configuration types."""
    
    _configs: Dict[ConfigType, BaseConfig] = {}
    _config_files: Dict[ConfigType, Path] = {}
    
    @classmethod
    def register(cls, config_type: ConfigType, config: BaseConfig, file_path: Optional[Path] = None):
        """Register a configuration."""
        cls._configs[config_type] = config
        if file_path:
            cls._config_files[config_type] = file_path
    
    @classmethod
    def get(cls, config_type: ConfigType) -> Optional[BaseConfig]:
        """Get a registered configuration."""
        return cls._configs.get(config_type)
    
    @classmethod
    def reload(cls, config_type: ConfigType) -> bool:
        """Reload configuration from file."""
        if config_type not in cls._config_files:
            return False
        
        try:
            file_path = cls._config_files[config_type]
            data = ConfigLoader.load_yaml(file_path)
            # This would need to be implemented by specific config classes
            return True
        except Exception:
            return False
    
    @classmethod
    def validate_all(cls) -> Dict[ConfigType, bool]:
        """Validate all registered configurations."""
        return {config_type: config.validate() for config_type, config in cls._configs.items()}