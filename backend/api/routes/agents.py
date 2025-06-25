"""API routes for agent management."""

import json
import yaml
from pathlib import Path
from flask import Blueprint, request, current_app
from typing import Dict, Any

# Import unified API response class
from ..response import APIResponse

# Add src directory to Python path if not already added
import sys
from pathlib import Path

src_path = Path(__file__).parent.parent.parent / 'src'
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import agent types and configurations
from src.config.agents import AGENT_LLM_MAP, AgentConfig, AgentType, load_agents_config
from src.config.types import LLMType

# Configuration file path
USER_CONFIG_FILE = Path.home() / '.akasa' / 'config.yaml'

# Create blueprint
agents_bp = Blueprint('agents', __name__)



@agents_bp.route('/', methods=['GET'])
def get_all_agents():
    """Get all agent configurations."""
    try:
        agents_config = load_agents_config()
        
        # Convert agents to serializable format
        agents_data = []
        i = 0
        for agent_name, agent_config in agents_config.items():
            agents_data.append({
                "$id": agent_config.name,
                'name': agent_config.name,
                'description': agent_config.description,
                'prompt': agent_config.prompt_template,
                'temperature': agent_config.parameters.get('temperature', 0.7),
                'maxTokens': agent_config.parameters.get('max_tokens', 2000)
            })
            i+=1
        
        # Convert LLM mapping to serializable format
        llm_mapping = {}
        for agent_type_key, llm_type in AGENT_LLM_MAP.items():
            llm_mapping[str(agent_type_key)] = str(llm_type)
        
        return APIResponse.success({
            'agents': agents_data,
            'total': i,
            'agent_llm_mapping': llm_mapping,
            'available_types': [str(t) for t in AgentType]
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting agents: {str(e)}")
        return APIResponse.error(str(e))


@agents_bp.route('/validate', methods=['POST'])
def validate_agent_config():
    """Validate agent configuration."""
    try:
        data = request.get_json()
        if not data:
            return APIResponse.validation_error('No data provided')
        
        # Validate agent configuration
        try:
            # Create AgentConfig instance to validate
            agent_config = AgentConfig(
                name=data.get('name', ''),
                type=AgentType.MYSTERY_RESEARCHER,  # Default type for validation
                llm_type=LLMType.RESEARCH,  # Default LLM type for validation
                description=data.get('description', ''),
                prompt_template=data.get('system_prompt', ''),
                parameters={
                    'temperature': data.get('temperature', 0.7),
                    'max_tokens': data.get('max_tokens', 2000)
                }
            )
            
            return APIResponse.success(message='Agent configuration is valid')
            
        except (TypeError, ValueError) as validation_error:
            return APIResponse.validation_error(
                'Invalid agent configuration',
                str(validation_error)
            )
        
    except Exception as e:
        current_app.logger.error(f"Error validating agent config: {str(e)}")
        return APIResponse.error(str(e))