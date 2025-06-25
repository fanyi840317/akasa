# Copyright (c) 2025 Lingjing Project
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from pathlib import Path

from .configuration import load_yaml_config
from .types import LLMType

CONFIG_FILE = Path(__file__).parent / "llm_config.yaml"

@dataclass
class LLMModelConfig:
    """Configuration for a single LLM model."""
    basic: str = ""
    reasoning: str = ""
    vision: str = ""
    fast: str = ""
    embedding: Optional[str] = None
    code: str = ""
    research: str = ""
    analysis: str = ""

@dataclass
class LLMProviderDetails:
    """Details for an LLM provider."""
    api_key: Optional[str]
    base_url: Optional[str]
    organization: Optional[str] = None
    secret_key: Optional[str] = None  # For Baidu
    models: LLMModelConfig = field(default_factory=LLMModelConfig)
    default_params: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LLMProviderDetails":
        models_data = data.get("models", {})
        models = LLMModelConfig(**models_data)
        return cls(
            api_key=data.get("api_key"),
            base_url=data.get("base_url"),
            organization=data.get("organization"),
            secret_key=data.get("secret_key"),
            models=models,
            default_params=data.get("default_params", {}),
        )

@dataclass
class LLMConfig:
    """Complete LLM configuration."""
    providers: Dict[str, LLMProviderDetails] = field(default_factory=dict)
    default_providers: List[str] = field(default_factory=list)
    type_provider_mapping: Dict[str, List[str]] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, file_path: Path = CONFIG_FILE) -> "LLMConfig":
        data = load_yaml_config(file_path)
        providers = {k: LLMProviderDetails.from_dict(v) for k, v in data.items() if isinstance(v, dict) and "models" in v}
        return cls(
            providers=providers,
            default_providers=data.get("default_providers", []),
            type_provider_mapping=data.get("type_provider_mapping", {}),
        )

    def get_provider_for_type(self, llm_type: LLMType) -> Optional[LLMProviderDetails]:
        """Get the best available provider for a given LLM type."""
        provider_names = self.type_provider_mapping.get(llm_type.value, self.default_providers)
        for provider_name in provider_names:
            if provider_name in self.providers:
                return self.providers[provider_name]
        return None

# Global instance
llm_config = LLMConfig.from_yaml()