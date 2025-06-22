"""API routes for agent management."""

import json
import yaml
from pathlib import Path
from flask import Blueprint, request, jsonify, current_app
from typing import Dict, Any

# Import agent types and configurations
from src.config.agents import AgentType, AgentConfig
from src.config.components import load_components_config
from src.config.llm import LLMType
from src.config.agents.mapping import AGENT_LLM_MAP
from src.agents.agents import (
    create_agent,
    create_mystery_agent,
    create_mystery_researcher_agent,
    create_academic_researcher_agent,
    create_credibility_analyzer_agent,
    create_correlation_analyzer_agent,
    create_mystery_planner_agent,
    create_mystery_reporter_agent
)

# Configuration file path
USER_CONFIG_FILE = Path.home() / '.akasa' / 'config.yaml'

# Create blueprint
agents_bp = Blueprint('agents', __name__)

# Agent creation function mapping
AGENT_CREATORS = {
    AgentType.MYSTERY_RESEARCHER: create_mystery_researcher_agent,
    AgentType.ACADEMIC_RESEARCHER: create_academic_researcher_agent,
    AgentType.CREDIBILITY_ANALYZER: create_credibility_analyzer_agent,
    AgentType.CORRELATION_ANALYZER: create_correlation_analyzer_agent,
    AgentType.DATA_COLLECTOR: create_mystery_planner_agent,  # Map to available function
    AgentType.REPORT_GENERATOR: create_mystery_reporter_agent,  # Map to available function
}


@agents_bp.route('/', methods=['GET'])
def get_all_agents():
    """Get all agent configurations."""
    try:
        config = load_components_config()
        
        # Convert agents to serializable format
        agents_data = {}
        for agent_type, agent_config in config.agents.items():
            agents_data[str(agent_type)] = {
                'name': agent_config.name,
            'description': agent_config.description,
            'system_prompt': agent_config.prompt_template,
            'temperature': agent_config.parameters.get('temperature', 0.7),
            'max_tokens': agent_config.parameters.get('max_tokens', 2000)
            }
        
        # Convert LLM mapping to serializable format
        llm_mapping = {}
        for agent_type, llm_type in AGENT_LLM_MAP.items():
            llm_mapping[str(agent_type)] = str(llm_type)
        
        return jsonify({
            'success': True,
            'data': {
                'agents': agents_data,
                'agent_llm_mapping': llm_mapping,
                'available_types': [str(t) for t in AgentType]
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting agents: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@agents_bp.route('/<agent_type>', methods=['GET'])
def get_agent(agent_type: str):
    """Get specific agent configuration."""
    try:
        # Validate agent type
        try:
            agent_enum = AgentType(agent_type)
        except ValueError:
            return jsonify({
                'success': False,
                'error': f'Invalid agent type: {agent_type}'
            }), 400
        
        config = load_components_config()
        
        if agent_enum not in config.agents:
            return jsonify({
                'success': False,
                'error': f'Agent {agent_type} not found'
            }), 404
        
        agent_config = config.agents[agent_enum]
        
        return jsonify({
            'success': True,
            'data': {
                'agent_type': agent_type,
                'config': {
                    'name': agent_config.name,
                    'description': agent_config.description,
                    'system_prompt': agent_config.prompt_template,
                    'temperature': agent_config.parameters.get('temperature', 0.7),
                    'max_tokens': agent_config.parameters.get('max_tokens', 2000)
                },
                'llm_type': str(AGENT_LLM_MAP.get(agent_enum, LLMType.RESEARCH))
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting agent {agent_type}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@agents_bp.route('/<agent_type>', methods=['PUT'])
def update_agent(agent_type: str):
    """Update agent configuration."""
    try:
        # Validate agent type
        try:
            agent_enum = AgentType(agent_type)
        except ValueError:
            return jsonify({
                'success': False,
                'error': f'Invalid agent type: {agent_type}'
            }), 400
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['name', 'description', 'system_prompt', 'temperature', 'max_tokens']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Validate data types
        if not isinstance(data['temperature'], (int, float)):
            return jsonify({
                'success': False,
                'error': 'temperature must be a number'
            }), 400
        
        if not isinstance(data['max_tokens'], int):
            return jsonify({
                'success': False,
                'error': 'max_tokens must be an integer'
            }), 400
        
        # Load or create user config
        user_config = {}
        if USER_CONFIG_FILE.exists():
            with open(USER_CONFIG_FILE, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f) or {}
        
        # Ensure structure exists
        if 'components' not in user_config:
            user_config['components'] = {}
        if 'agents' not in user_config['components']:
            user_config['components']['agents'] = {}
        
        # Update agent configuration
        user_config['components']['agents'][agent_type] = {
            'name': data['name'],
            'description': data['description'],
            'prompt_template': data['system_prompt'],
            'parameters': {
                'temperature': data['temperature'],
                'max_tokens': data['max_tokens']
            }
        }
        
        # Save configuration
        USER_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(USER_CONFIG_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(user_config, f, default_flow_style=False, allow_unicode=True)
        
        return jsonify({
            'success': True,
            'message': f'Agent {agent_type} updated successfully'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error updating agent {agent_type}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@agents_bp.route('/<agent_type>', methods=['DELETE'])
def delete_agent(agent_type: str):
    """Delete agent configuration (reset to default)."""
    try:
        # Validate agent type
        try:
            agent_enum = AgentType(agent_type)
        except ValueError:
            return jsonify({
                'success': False,
                'error': f'Invalid agent type: {agent_type}'
            }), 400
        
        # Load user config
        if not USER_CONFIG_FILE.exists():
            return jsonify({
                'success': True,
                'message': f'Agent {agent_type} already at default configuration'
            })
        
        with open(USER_CONFIG_FILE, 'r', encoding='utf-8') as f:
            user_config = yaml.safe_load(f) or {}
        
        # Remove agent configuration
        if ('components' in user_config and 
            'agents' in user_config['components'] and 
            agent_type in user_config['components']['agents']):
            
            del user_config['components']['agents'][agent_type]
            
            # Clean up empty structures
            if not user_config['components']['agents']:
                del user_config['components']['agents']
            if not user_config['components']:
                del user_config['components']
            
            # Save updated configuration
            if user_config:
                with open(USER_CONFIG_FILE, 'w', encoding='utf-8') as f:
                    yaml.dump(user_config, f, default_flow_style=False, allow_unicode=True)
            else:
                USER_CONFIG_FILE.unlink()  # Delete empty config file
        
        return jsonify({
            'success': True,
            'message': f'Agent {agent_type} reset to default configuration'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error deleting agent {agent_type}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@agents_bp.route('/create', methods=['POST'])
def create_agent_instance():
    """Create an agent instance for testing."""
    try:
        data = request.get_json()
        if not data or 'agent_type' not in data:
            return jsonify({
                'success': False,
                'error': 'agent_type is required'
            }), 400
        
        agent_type_str = data['agent_type']
        
        # Validate agent type
        try:
            agent_enum = AgentType(agent_type_str)
        except ValueError:
            return jsonify({
                'success': False,
                'error': f'Invalid agent type: {agent_type_str}'
            }), 400
        
        # Get agent creator function
        if agent_enum not in AGENT_CREATORS:
            return jsonify({
                'success': False,
                'error': f'No creator function for agent type: {agent_type_str}'
            }), 400
        
        # Create agent instance
        creator_func = AGENT_CREATORS[agent_enum]
        # Provide empty tools list for now - in real implementation, 
        # tools would be loaded based on agent configuration
        agent = creator_func(tools=[])
        
        return jsonify({
            'success': True,
            'message': f'Agent {agent_type_str} created successfully',
            'agent_id': str(id(agent))  # Simple ID for testing
        })
        
    except Exception as e:
        current_app.logger.error(f"Error creating agent: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@agents_bp.route('/types', methods=['GET'])
def get_agent_types():
    """Get available agent and LLM types."""
    try:
        # Convert LLM mapping to serializable format
        llm_mapping = {}
        for agent_type, llm_type in AGENT_LLM_MAP.items():
            llm_mapping[str(agent_type)] = str(llm_type)
        
        return jsonify({
            'success': True,
            'data': {
                'agent_types': [str(t) for t in AgentType],
                'llm_types': [str(t) for t in LLMType],
                'agent_llm_mapping': llm_mapping
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting agent types: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@agents_bp.route('/validate', methods=['POST'])
def validate_agent_config():
    """Validate agent configuration."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
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
            
            return jsonify({
                'success': True,
                'message': 'Agent configuration is valid'
            })
            
        except (TypeError, ValueError) as validation_error:
            return jsonify({
                'success': False,
                'error': 'Invalid agent configuration',
                'details': str(validation_error)
            }), 400
        
    except Exception as e:
        current_app.logger.error(f"Error validating agent config: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500