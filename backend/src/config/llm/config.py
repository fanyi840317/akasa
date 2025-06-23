# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT

import os
import logging
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from pathlib import Path
from functools import lru_cache
from enum import Enum

from ..base import BaseConfig, ConfigType, ConfigLoader, APIConfig

# Create logger
logger = logging.getLogger(__name__)

# Try to import LangChain LLM classes
try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None

try:
    from langchain_anthropic import ChatAnthropic
except ImportError:
    ChatAnthropic = None

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

try:
    from langchain_community.llms import Ollama
except ImportError:
    Ollama = None

# Global LLM cache
_llm_cache: Dict[str, Any] = {}


class LLMType(str, Enum):
    """Types of LLM models for different use cases."""
    BASIC = "basic"
    REASONING = "reasoning"
    VISION = "vision"
    FAST = "fast"
    EMBEDDING = "embedding"
    CODE = "code"
    RESEARCH = "research"
    ANALYSIS = "analysis"


class LLMProvider(str, Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OLLAMA = "ollama"
    QWEN = "qwen"
    ZHIPU = "zhipu"
    BAIDU = "baidu"


@dataclass
class LLMProviderConfig:
    """Configuration for a specific LLM provider."""
    api_key: str = ""
    base_url: str = ""
    organization: str = ""
    timeout: float = 30.0
    max_retries: int = 3
    models: Dict[str, str] = field(default_factory=dict)
    model_configs: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    default_params: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LLMProviderConfig':
        """Create LLMProviderConfig from dictionary."""
        return cls(
            api_key=data.get('api_key', ''),
            base_url=data.get('base_url', ''),
            organization=data.get('organization', ''),
            timeout=data.get('timeout', 30.0),
            max_retries=data.get('max_retries', 3),
            models=data.get('models', {}),
            model_configs=data.get('model_configs', {}),
            default_params=data.get('default_params', {})
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'api_key': self.api_key,
            'base_url': self.base_url,
            'organization': self.organization,
            'timeout': self.timeout,
            'max_retries': self.max_retries,
            'models': self.models,
            'model_configs': self.model_configs,
            'default_params': self.default_params
        }
    
    def get_model(self, llm_type: LLMType) -> Optional[str]:
        """Get model name for specific LLM type."""
        return self.models.get(llm_type.value)
    
    def validate(self) -> bool:
        """Validate provider configuration."""
        # For Ollama, API key is not required
        if 'ollama' in self.base_url.lower():
            return bool(self.base_url and self.models)
        # For Baidu, both api_key and secret_key are required
        if any(key in self.default_params for key in ['secret_key']):
            return bool(self.api_key and self.default_params.get('secret_key') and self.models)
        return bool(self.api_key and self.models)


@dataclass
class LLMConfig(BaseConfig):
    """Unified LLM configuration."""
    
    config_type: ConfigType = field(default=ConfigType.LLM, init=False)
    providers: Dict[str, LLMProviderConfig] = field(default_factory=dict)
    type_provider_mapping: Dict[str, List[str]] = field(default_factory=dict)
    fallback_enabled: bool = True
    max_retries: int = 3
    retry_delay: float = 1.0
    timeout: float = 30.0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LLMConfig':
        """Create LLM configuration from dictionary."""
        providers = {}
        
        # Extract provider configurations
        providers_data = data.get('providers', {})
        for provider_name, provider_data in providers_data.items():
            providers[provider_name] = LLMProviderConfig.from_dict(provider_data)
        
        # Extract global settings
        fallback_config = data.get('fallback', {})
        
        return cls(
            providers=providers,
            type_provider_mapping=data.get('type_provider_mapping', {}),
            fallback_enabled=fallback_config.get('enabled', True),
            max_retries=fallback_config.get('max_retries', 3),
            retry_delay=fallback_config.get('retry_delay', 1.0),
            timeout=fallback_config.get('timeout', 30.0)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'providers': {name: provider.to_dict() for name, provider in self.providers.items()},
            'type_provider_mapping': self.type_provider_mapping,
            'fallback': {
                'enabled': self.fallback_enabled,
                'max_retries': self.max_retries,
                'retry_delay': self.retry_delay,
                'timeout': self.timeout
            }
        }
    
    def validate(self) -> bool:
        """Validate LLM configuration."""
        # Check if at least one provider is configured
        if not self.providers:
            return False
        
        # Validate each provider
        for provider in self.providers.values():
            if not provider.validate():
                return False
        
        return True
    
    def get_provider(self, provider_name: str) -> Optional[LLMProviderConfig]:
        """Get provider configuration by name."""
        return self.providers.get(provider_name)
    
    def get_llm_by_type(self, llm_type: LLMType, provider: Optional[str] = None) -> Dict[str, Any]:
        """Get LLM configuration by type and optional provider."""
        # If no provider specified, use the first available provider for this type
        if provider is None:
            providers_for_type = self.type_provider_mapping.get(llm_type.value, [])
            if providers_for_type:
                provider = providers_for_type[0]
            else:
                # Fallback to first available provider
                provider = next(iter(self.providers.keys())) if self.providers else None
        
        if not provider or provider not in self.providers:
            raise ValueError(f"Provider '{provider}' not found in configuration")
        
        provider_config = self.providers[provider]
        model = provider_config.get_model(llm_type)
        
        if not model:
            raise ValueError(f"Model for type '{llm_type.value}' not found for provider '{provider}'")
        
        # Start with base configuration
        config = {
            'provider': provider,
            'model': model,
            'api_key': provider_config.api_key,
            'base_url': provider_config.base_url,
            **provider_config.default_params
        }
        
        # Add organization if available
        if provider_config.organization:
            config['organization'] = provider_config.organization
        
        # Override with specific model configuration
        type_config = provider_config.model_configs.get(llm_type.value, {})
        if type_config:
            config.update(type_config)
        
        return config
    
    def create_llm_from_config(self, llm_type: LLMType, provider: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Create LLM configuration with optional parameter overrides."""
        config = self.get_llm_by_type(llm_type, provider)
        config.update(kwargs)
        return config


def load_llm_config(config_path: Optional[str] = None) -> LLMConfig:
    """Load LLM configuration from YAML file."""
    if config_path is None:
        config_path = str(Path(__file__).parent / "llm.yaml")
    
    loader = ConfigLoader()
    data = loader.load_yaml(config_path)
    return LLMConfig.from_dict(data)


# LLM creation functions
def _create_openai_llm(llm_type: LLMType, config: Dict[str, Any]) -> Optional[Any]:
    """Create OpenAI LLM instance."""
    if ChatOpenAI is None:
        raise ImportError("langchain_openai is required for OpenAI models. Install with: pip install langchain-openai")
    
    # Remove provider-specific keys that ChatOpenAI doesn't accept
    clean_config = {k: v for k, v in config.items() if k not in ['provider']}
    return ChatOpenAI(**clean_config)


def _create_anthropic_llm(llm_type: LLMType, config: Dict[str, Any]) -> Optional[Any]:
    """Create Anthropic LLM instance."""
    if ChatAnthropic is None:
        raise ImportError("langchain_anthropic is required for Anthropic models. Install with: pip install langchain-anthropic")
    
    # Remove provider-specific keys that ChatAnthropic doesn't accept
    clean_config = {k: v for k, v in config.items() if k not in ['provider']}
    return ChatAnthropic(**clean_config)


def _create_google_llm(llm_type: LLMType, config: Dict[str, Any]) -> Optional[Any]:
    """Create Google LLM instance."""
    if ChatGoogleGenerativeAI is None:
        raise ImportError("langchain_google_genai is required for Google models. Install with: pip install langchain-google-genai")
    
    # Remove provider-specific keys that ChatGoogleGenerativeAI doesn't accept
    clean_config = {k: v for k, v in config.items() if k not in ['provider']}
    return ChatGoogleGenerativeAI(**clean_config)


def _create_ollama_llm(llm_type: LLMType, config: Dict[str, Any]) -> Optional[Any]:
    """Create Ollama LLM instance."""
    if Ollama is None:
        raise ImportError("langchain_community is required for Ollama models. Install with: pip install langchain-community")
    
    # Remove provider-specific keys that Ollama doesn't accept
    clean_config = {k: v for k, v in config.items() if k not in ['provider', 'api_key']}
    return Ollama(**clean_config)


def _create_qwen_llm(config: Dict[str, Any]) -> Any:
    """Create Qwen LLM instance."""
    try:
        logger.info("Creating Qwen LLM instance")
        # This is a placeholder - actual implementation would depend on Qwen SDK
        class MockQwenLLM:
            def __init__(self, config):
                self.config = config
                self.model = config.get("model", "qwen-turbo")
                self.api_key = config.get("api_key")
                self.base_url = config.get("base_url", "https://dashscope.aliyuncs.com/api/v1")
            
            def generate(self, prompt: str, **kwargs) -> str:
                return f"Mock Qwen response for: {prompt[:50]}..."
        
        return MockQwenLLM(config)
    except Exception as e:
        logger.error(f"Failed to create Qwen LLM: {e}")
        raise


def _create_zhipu_llm(config: Dict[str, Any]) -> Any:
    """Create Zhipu AI LLM instance."""
    try:
        logger.info("Creating Zhipu AI LLM instance")
        # This is a placeholder - actual implementation would depend on Zhipu SDK
        class MockZhipuLLM:
            def __init__(self, config):
                self.config = config
                self.model = config.get("model", "glm-3-turbo")
                self.api_key = config.get("api_key")
                self.base_url = config.get("base_url", "https://open.bigmodel.cn/api/paas/v4")
            
            def generate(self, prompt: str, **kwargs) -> str:
                return f"Mock Zhipu response for: {prompt[:50]}..."
        
        return MockZhipuLLM(config)
    except Exception as e:
        logger.error(f"Failed to create Zhipu LLM: {e}")
        raise


def _create_baidu_llm(config: Dict[str, Any]) -> Any:
    """Create Baidu ERNIE LLM instance."""
    try:
        logger.info("Creating Baidu ERNIE LLM instance")
        # This is a placeholder - actual implementation would depend on Baidu SDK
        class MockBaiduLLM:
            def __init__(self, config):
                self.config = config
                self.model = config.get("model", "ernie-bot-turbo")
                self.api_key = config.get("api_key")
                self.secret_key = config.get("secret_key")
                self.base_url = config.get("base_url", "https://aip.baidubce.com")
            
            def generate(self, prompt: str, **kwargs) -> str:
                return f"Mock Baidu ERNIE response for: {prompt[:50]}..."
        
        return MockBaiduLLM(config)
    except Exception as e:
        logger.error(f"Failed to create Baidu LLM: {e}")
        raise


def _create_llm_from_provider(provider: str, llm_type: LLMType, config: Dict[str, Any]) -> Any:
    """Create LLM instance based on provider."""
    creators = {
        "openai": _create_openai_llm,
        "anthropic": _create_anthropic_llm,
        "google": _create_google_llm,
        "ollama": _create_ollama_llm,
        "qwen": _create_qwen_llm,
        "zhipu": _create_zhipu_llm,
        "baidu": _create_baidu_llm,
    }
    
    creator = creators.get(provider.lower())
    if not creator:
        raise ValueError(f"Unsupported LLM provider: {provider}")
    
    if provider in ["qwen", "zhipu", "baidu"]:
        return creator(config)
    else:
        return creator(llm_type, config)


def _get_env_llm_conf(llm_type: str, provider: str = "openai") -> Dict[str, Any]:
    """
    Get LLM configuration from environment variables.
    Environment variables should follow the format: {PROVIDER}_{KEY}
    e.g., OPENAI_API_KEY, ANTHROPIC_API_KEY
    """
    prefix = f"{provider.upper()}_"
    conf = {}
    for key, value in os.environ.items():
        if key.startswith(prefix):
            conf_key = key[len(prefix):].lower()
            conf[conf_key] = value
    
    return conf


def create_llm_from_config(
    llm_type: LLMType,
    provider: Optional[str] = None,
    config_override: Optional[Dict[str, Any]] = None
) -> Any:
    """
    Create LLM instance from configuration.
    
    Args:
        llm_type: Type of LLM to create
        provider: LLM provider (if None, will auto-detect)
        config_override: Override configuration parameters
    
    Returns:
        LLM instance
    """
    # Load configuration from YAML
    llm_config = load_llm_config()
    
    # Get configuration for the specified type and provider
    config = llm_config.get_llm_by_type(llm_type, provider)
    
    # Get configuration from environment variables
    env_config = _get_env_llm_conf(llm_type.value, config['provider'])
    
    # Merge configurations (priority: override > env > yaml)
    config.update(env_config)
    if config_override:
        config.update(config_override)
    
    try:
        return _create_llm_from_provider(config['provider'], llm_type, config)
    except Exception as e:
        logger.error(f"Failed to create LLM with provider {config['provider']}: {e}")
        
        # Try fallback if enabled
        if llm_config.fallback_enabled:
            # Try other providers for this type
            providers_for_type = llm_config.type_provider_mapping.get(llm_type.value, [])
            for fallback_provider in providers_for_type:
                if fallback_provider != config['provider']:
                    try:
                        logger.info(f"Trying fallback provider: {fallback_provider}")
                        return create_llm_from_config(llm_type, fallback_provider, config_override)
                    except Exception as fallback_error:
                        logger.warning(f"Fallback provider {fallback_provider} also failed: {fallback_error}")
                        continue
        
        raise RuntimeError(f"All LLM providers failed. Last error: {e}")


@lru_cache(maxsize=32)
def get_llm_by_type(
    llm_type: LLMType,
    provider: Optional[str] = None,
    use_cache: bool = True
) -> Any:
    """
    Get LLM instance by type. Returns cached instance if available.
    
    Args:
        llm_type: Type of LLM to get
        provider: LLM provider (if None, will auto-detect)
        use_cache: Whether to use cached instances
    
    Returns:
        LLM instance
    """
    cache_key = f"{provider or 'auto'}_{llm_type.value}"
    
    if use_cache and cache_key in _llm_cache:
        return _llm_cache[cache_key]
    
    llm = create_llm_from_config(llm_type, provider)
    
    if use_cache:
        _llm_cache[cache_key] = llm
    
    return llm


def list_available_providers() -> Dict[str, bool]:
    """List available LLM providers and their installation status."""
    providers = {
        "openai": ChatOpenAI is not None,
        "anthropic": ChatAnthropic is not None,
        "google": ChatGoogleGenerativeAI is not None,
        "ollama": Ollama is not None,
        "qwen": True,  # Mock implementation available
        "zhipu": True,  # Mock implementation available
        "baidu": True,  # Mock implementation available
    }
    return providers


def clear_llm_cache():
    """Clear the LLM instance cache."""
    global _llm_cache
    _llm_cache.clear()
    # Also clear the lru_cache
    get_llm_by_type.cache_clear()


def get_llm_info(llm_type: LLMType, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get information about an LLM configuration."""
    llm_config = load_llm_config()
    
    if provider is None:
        providers_for_type = llm_config.type_provider_mapping.get(llm_type.value, [])
        provider = providers_for_type[0] if providers_for_type else next(iter(llm_config.providers.keys()), None)
    
    if not provider:
        return {"error": "No provider available"}
    
    config = llm_config.get_llm_by_type(llm_type, provider)
    env_config = _get_env_llm_conf(llm_type.value, provider)
    
    return {
        "provider": provider,
        "type": llm_type.value,
        "config": {k: "***" if "key" in k.lower() else v for k, v in config.items()},
        "env_config": {k: "***" if "key" in k.lower() else v for k, v in env_config.items()},
        "available": provider in list_available_providers() and list_available_providers()[provider],
    }