# Copyright (c) 2024 Lingjing
# SPDX-License-Identifier: MIT

import os
import logging
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from pathlib import Path
from functools import lru_cache

# Create logger
logger = logging.getLogger(__name__)

from enum import Enum
from ..base import BaseConfig, ConfigType, ConfigLoader, APIConfig

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

# Default LLM configurations for different providers and types
DEFAULT_LLM_CONFIGS: Dict[str, Dict[str, Dict[str, Any]]] = {
    "openai": {
        "basic": {"model": "gpt-3.5-turbo", "temperature": 0.7},
        "reasoning": {"model": "gpt-4", "temperature": 0.3},
        "vision": {"model": "gpt-4-vision-preview", "temperature": 0.7},
        "fast": {"model": "gpt-3.5-turbo", "temperature": 0.5},
        "embedding": {"model": "text-embedding-ada-002"},
        "code": {"model": "gpt-4", "temperature": 0.1},
        "research": {"model": "gpt-4", "temperature": 0.3},
        "analysis": {"model": "gpt-4", "temperature": 0.2}
    },
    "anthropic": {
        "basic": {"model": "claude-3-haiku-20240307", "temperature": 0.7},
        "reasoning": {"model": "claude-3-opus-20240229", "temperature": 0.3},
        "vision": {"model": "claude-3-opus-20240229", "temperature": 0.7},
        "fast": {"model": "claude-3-haiku-20240307", "temperature": 0.5},
        "code": {"model": "claude-3-opus-20240229", "temperature": 0.1},
        "research": {"model": "claude-3-opus-20240229", "temperature": 0.3},
        "analysis": {"model": "claude-3-opus-20240229", "temperature": 0.2}
    },
    "google": {
        "basic": {"model": "gemini-pro", "temperature": 0.7},
        "reasoning": {"model": "gemini-pro", "temperature": 0.3},
        "vision": {"model": "gemini-pro-vision", "temperature": 0.7},
        "fast": {"model": "gemini-pro", "temperature": 0.5},
        "code": {"model": "gemini-pro", "temperature": 0.1},
        "research": {"model": "gemini-pro", "temperature": 0.3},
        "analysis": {"model": "gemini-pro", "temperature": 0.2}
    },
    "ollama": {
        "basic": {"model": "llama2", "temperature": 0.7},
        "reasoning": {"model": "llama2", "temperature": 0.3},
        "fast": {"model": "llama2", "temperature": 0.5},
        "code": {"model": "codellama", "temperature": 0.1},
        "research": {"model": "llama2", "temperature": 0.3},
        "analysis": {"model": "llama2", "temperature": 0.2}
    }
}


class LLMType(Enum):
    """Types of LLM models for different use cases."""
    BASIC = "basic"
    REASONING = "reasoning"
    VISION = "vision"
    FAST = "fast"
    EMBEDDING = "embedding"
    CODE = "code"
    RESEARCH = "research"
    ANALYSIS = "analysis"


class LLMProvider(Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OLLAMA = "ollama"
    QWEN = "qwen"
    ZHIPU = "zhipu"
    BAIDU = "baidu"


# Available LLM types
AVAILABLE_LLM_TYPES = [
    "basic",
    "reasoning",
    "vision",
    "fast",
    "embedding",
    "code",
    "research",
    "analysis"
]


# Default LLM configurations will be loaded from llm.yaml
# This allows for dynamic configuration without code changes


# Available LLM providers
AVAILABLE_PROVIDERS = [
    "openai",
    "anthropic", 
    "google",
    "ollama",
    "qwen",
    "zhipu",
    "baidu"
]


@dataclass
class LLMProviderConfig(APIConfig):
    """Configuration for a specific LLM provider."""
    models: Dict[str, str] = field(default_factory=dict)
    default_params: Dict[str, Any] = field(default_factory=dict)
    model_configs: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    def get_model(self, llm_type: LLMType) -> Optional[str]:
        """Get model name for specific LLM type."""
        return self.models.get(llm_type.value)
    
    def validate(self) -> bool:
        """Validate provider configuration."""
        return bool(self.api_key and self.models)


@dataclass
class LLMConfig(BaseConfig):
    """Unified LLM configuration."""
    
    config_type: ConfigType = field(default=ConfigType.LLM, init=False)
    providers: Dict[str, LLMProviderConfig] = field(default_factory=dict)
    default_providers: List[str] = field(default_factory=list)
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
        for provider_name in AVAILABLE_PROVIDERS:
            if provider_name in data:
                provider_data = data[provider_name]
                providers[provider_name] = LLMProviderConfig(
                    api_key=provider_data.get('api_key', ''),
                    base_url=provider_data.get('base_url', ''),
                    timeout=provider_data.get('timeout', 30),
                    max_retries=provider_data.get('max_retries', 3),
                    models=provider_data.get('models', {}),
                    default_params=provider_data.get('default_params', {}),
                    model_configs=provider_data.get('model_configs', {})
                )
        
        # Extract global settings
        fallback_config = data.get('fallback', {})
        
        return cls(
            providers=providers,
            default_providers=data.get('default_providers', AVAILABLE_PROVIDERS),
            type_provider_mapping=data.get('type_provider_mapping', {}),
            fallback_enabled=fallback_config.get('enabled', True),
            max_retries=fallback_config.get('max_retries', 3),
            retry_delay=fallback_config.get('retry_delay', 1.0),
            timeout=fallback_config.get('timeout', 30.0)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        result = {
            'default_providers': self.default_providers,
            'type_provider_mapping': self.type_provider_mapping,
            'fallback': {
                'enabled': self.fallback_enabled,
                'max_retries': self.max_retries,
                'retry_delay': self.retry_delay,
                'timeout': self.timeout
            }
        }
        
        # Add provider configurations
        for name, provider in self.providers.items():
            result[name] = {
                'api_key': provider.api_key,
                'base_url': provider.base_url,
                'timeout': provider.timeout,
                'max_retries': provider.max_retries,
                'models': provider.models,
                'default_params': provider.default_params
            }
        
        return result
    
    def validate(self) -> bool:
        """Validate LLM configuration."""
        # Check if at least one provider is configured
        if not self.providers:
            return False
        
        # Validate each provider
        for provider in self.providers.values():
            if not provider.validate():
                return False
        
        # Check if default providers exist
        for provider_name in self.default_providers:
            if provider_name not in self.providers:
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
                # Fallback to default providers
                provider = self.default_providers[0] if self.default_providers else None
        
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
        
        # Check if provider has model_configs for this type
        if hasattr(provider_config, 'model_configs') and provider_config.model_configs:
            type_config = provider_config.model_configs.get(llm_type.value)
            if type_config:
                # Override with specific model configuration
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
        config_path = Path(__file__).parent / "llm.yaml"
    
    data = ConfigLoader.load_yaml(config_path)
    return LLMConfig.from_dict(data)


# Backward compatibility functions
def get_llm_by_type(llm_type: LLMType, provider: Optional[str] = None) -> Dict[str, Any]:
    """Get LLM configuration by type and optional provider."""
    config = load_llm_config()
    return config.get_llm_by_type(llm_type, provider)


def create_llm_from_config(llm_type: LLMType, provider: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    """Create LLM configuration with optional parameter overrides."""
    config = load_llm_config()
    return config.create_llm_from_config(llm_type, provider, **kwargs)


def _get_env_llm_conf(llm_type: str, provider: str = "openai") -> Dict[str, Any]:
    """
    Get LLM configuration from environment variables.
    Environment variables should follow the format: {PROVIDER}_{LLM_TYPE}__{KEY}
    e.g., OPENAI_BASIC__api_key, ANTHROPIC_REASONING__api_key
    """
    prefix = f"{provider.upper()}_{llm_type.upper()}__"
    conf = {}
    for key, value in os.environ.items():
        if key.startswith(prefix):
            conf_key = key[len(prefix):].lower()
            conf[conf_key] = value
    
    # Also check for general provider config
    general_prefix = f"{provider.upper()}__"
    for key, value in os.environ.items():
        if key.startswith(general_prefix) and key not in conf:
            conf_key = key[len(general_prefix):].lower()
            conf[conf_key] = value
    
    return conf


def _create_openai_llm(llm_type: LLMType, config: Dict[str, Any]) -> Optional[Any]:
    """Create OpenAI LLM instance."""
    if ChatOpenAI is None:
        raise ImportError("langchain_openai is required for OpenAI models. Install with: pip install langchain-openai")
    
    return ChatOpenAI(**config)


def _create_anthropic_llm(llm_type: LLMType, config: Dict[str, Any]) -> Optional[Any]:
    """Create Anthropic LLM instance."""
    if ChatAnthropic is None:
        raise ImportError("langchain_anthropic is required for Anthropic models. Install with: pip install langchain-anthropic")
    
    return ChatAnthropic(**config)


def _create_google_llm(llm_type: LLMType, config: Dict[str, Any]) -> Optional[Any]:
    """Create Google LLM instance."""
    if ChatGoogleGenerativeAI is None:
        raise ImportError("langchain_google_genai is required for Google models. Install with: pip install langchain-google-genai")
    
    return ChatGoogleGenerativeAI(**config)


def _create_ollama_llm(llm_type: LLMType, config: Dict[str, Any]) -> Optional[Any]:
    """Create Ollama LLM instance."""
    if Ollama is None:
        raise ImportError("langchain_community is required for Ollama models. Install with: pip install langchain-community")
    
    return Ollama(**config)


def _create_qwen_llm(config: Dict[str, Any]) -> Any:
    """Create Qwen LLM instance."""
    try:
        # This is a placeholder - actual implementation would depend on Qwen SDK
        logger.info("Creating Qwen LLM instance")
        # For now, return a mock object
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


def _load_config_file() -> Dict[str, Any]:
    """Load configuration from YAML file."""
    config_path = Path(__file__).parent / "llm.yaml"
    if config_path.exists():
        return ConfigLoader.load_yaml(str(config_path))
    return {}


def load_llm_config() -> LLMConfig:
    """Load LLM configuration from llm.yaml."""
    config_data = _load_config_file()
    return LLMConfig.from_dict(config_data)


def create_llm_from_config(
    llm_type: LLMType,
    provider: str = "openai",
    config_override: Optional[Dict[str, Any]] = None
) -> Any:
    """
    Create LLM instance from configuration.
    
    Args:
        llm_type: Type of LLM to create
        provider: LLM provider (openai, anthropic, google, ollama, qwen, zhipu, baidu)
        config_override: Override configuration parameters
    
    Returns:
        LLM instance
    """
    # Load base configuration
    file_config = _load_config_file()
    
    # Get default configuration for provider and type
    default_config = DEFAULT_LLM_CONFIGS.get(provider, {}).get(llm_type.value, {})
    
    # Get configuration from file
    provider_config = file_config.get("llm", {}).get(provider, {})
    type_config = provider_config.get(llm_type.value, {})
    
    # Get configuration from environment variables
    env_config = _get_env_llm_conf(llm_type.value, provider)
    
    # Merge configurations (priority: override > env > file > default)
    merged_config = {}
    merged_config.update(default_config)
    merged_config.update(type_config)
    merged_config.update(env_config)
    if config_override:
        merged_config.update(config_override)
    
    if not merged_config:
        raise ValueError(f"No configuration found for {provider} {llm_type}")
    
    try:
        return _create_llm_from_provider(provider, llm_type, merged_config)
    except Exception as e:
        logger.error(f"Failed to create LLM with provider {provider}: {e}")
        
        # Try fallback providers
        llm_config = load_llm_config()
        fallback_enabled = llm_config.get("fallback", {}).get("enabled", True)
        
        if fallback_enabled:
            fallback_providers = llm_config.get("default_providers", list(AVAILABLE_PROVIDERS.keys()))
            for fallback_provider in fallback_providers:
                if fallback_provider != provider:
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
        provider: LLM provider (if None, will try to detect from config)
        use_cache: Whether to use cached instances
    
    Returns:
        LLM instance
    """
    # Auto-detect provider if not specified
    if provider is None:
        provider = _detect_default_provider()
    
    cache_key = f"{provider}_{llm_type.value}"
    
    if use_cache and cache_key in _llm_cache:
        return _llm_cache[cache_key]
    
    llm = create_llm_from_config(llm_type, provider)
    
    if use_cache:
        _llm_cache[cache_key] = llm
    
    return llm


def _detect_default_provider() -> str:
    """Detect the default LLM provider from environment or config."""
    # Check environment variable
    default_provider = os.getenv("DEFAULT_LLM_PROVIDER")
    if default_provider:
        return default_provider.lower()
    
    # Check config file
    config = _load_config_file()
    llm_config = config.get("llm", {})
    if "default_provider" in llm_config:
        return llm_config["default_provider"].lower()
    
    # Load LLM config and check provider priority
    llm_config_data = load_llm_config()
    default_providers = llm_config_data.get("default_providers", ["openai", "anthropic", "qwen", "google", "zhipu", "baidu", "ollama"])
    
    # Check providers in order of preference
    for provider in default_providers:
        if provider in llm_config_data and _is_provider_available(provider, llm_config_data[provider]):
            return provider
    
    # Check which provider has API keys configured
    providers = ["openai", "anthropic", "google", "qwen", "zhipu", "baidu"]
    for provider in providers:
        env_vars = [
            f"{provider.upper()}_API_KEY",
            f"{provider.upper()}__api_key",
        ]
        if any(os.getenv(var) for var in env_vars):
            return provider
    
    # Default to OpenAI
    return "openai"


def _is_provider_available(provider: str, provider_config: Dict[str, Any]) -> bool:
    """Check if a provider is available (has required credentials)."""
    if provider == "ollama":
        # Ollama doesn't require API key, just check if base_url is accessible
        return "base_url" in provider_config
    elif provider in ["openai", "anthropic", "google", "qwen", "zhipu"]:
        return "api_key" in provider_config and provider_config["api_key"]
    elif provider == "baidu":
        return ("api_key" in provider_config and provider_config["api_key"] and
                "secret_key" in provider_config and provider_config["secret_key"])
    
    return False


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
    if provider is None:
        provider = _detect_default_provider()
    
    config = _load_config_file()
    default_config = DEFAULT_LLM_CONFIGS.get(provider, {}).get(llm_type.value, {})
    env_config = _get_env_llm_conf(llm_type.value, provider)
    
    return {
        "provider": provider,
        "type": llm_type.value,
        "default_config": default_config,
        "env_config": {k: "***" if "key" in k.lower() else v for k, v in env_config.items()},
        "available": provider in list_available_providers() and list_available_providers()[provider],
    }