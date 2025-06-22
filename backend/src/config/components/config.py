# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from pathlib import Path

from ..base import BaseConfig, ConfigLoader
from ..tools import ToolConfig, load_tools_config
from ..agents import AgentConfig, load_agents_config


# Agent-related enums



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
    
    # Load main components config
    loader = ConfigLoader()
    data = loader.load_yaml(config_path)
    
    # Load tools and agents from their respective modules
    tools = load_tools_config()
    agents = load_agents_config()
    
    # Merge configurations
    if 'tools' not in data:
        data['tools'] = {}
    if 'agents' not in data:
        data['agents'] = {}
    
    # Add tools and agents to the main config
    for tool_name, tool_config in tools.items():
        if tool_name not in data['tools']:
            data['tools'][tool_name] = tool_config.to_dict()
    
    for agent_name, agent_config in agents.items():
        if agent_name not in data['agents']:
            data['agents'][agent_name] = agent_config.to_dict()
    
    return ComponentsConfig.from_dict(data)


# Removed duplicate ComponentsConfig class - using the new YAML-compatible version above