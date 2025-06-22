# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from enum import Enum
from pathlib import Path

from ..base import BaseConfig, ConfigType, ConfigLoader
from ..llm import LLMType


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


def load_agents_config(config_path: Optional[str] = None) -> Dict[str, AgentConfig]:
    """Load agents configuration from YAML file."""
    if config_path is None:
        config_path = Path(__file__).parent / "agents.yaml"
    
    loader = ConfigLoader()
    data = loader.load_yaml(config_path)
    
    agents = {}
    if 'agents' in data:
        for agent_name, agent_data in data['agents'].items():
            agents[agent_name] = AgentConfig.from_dict(agent_data)
    
    return agents