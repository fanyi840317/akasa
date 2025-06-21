#!/usr/bin/env python3
"""
Configuration API routes.
"""

import os
import yaml
from flask import Blueprint, request, jsonify, current_app
from pathlib import Path
from typing import Dict, Any, Optional

# Import config modules
import sys
sys.path.append(str(Path(__file__).parent.parent.parent / 'src'))

from config import (
    load_config, Config, SystemConfig, ComponentsConfig, LLMConfig,
    load_system_config, load_components_config, load_llm_config,
    validate_all_configs, ConfigValidator
)
from config.base import ConfigLoader

config_bp = Blueprint('config', __name__)

# Configuration file paths
CONFIG_DIR = Path(__file__).parent.parent.parent / 'src' / 'config'
DEFAULT_CONFIG_FILE = CONFIG_DIR / 'default.yaml'
USER_CONFIG_FILE = CONFIG_DIR / 'user.yaml'


@config_bp.route('/', methods=['GET'])
def get_all_configs():
    """Get all configuration sections.
    
    Returns:
        JSON response with all configuration data
    """
    try:
        config = load_config()
        
        result = {
            'system': config.system.to_dict() if config.system else None,
            'components': config.components.to_dict() if config.components else None,
            'llm': config.llm.to_dict() if config.llm else None
        }
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        current_app.logger.error(f"Error loading configs: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@config_bp.route('/system', methods=['GET'])
def get_system_config():
    """Get system configuration.
    
    Returns:
        JSON response with system configuration
    """
    try:
        config = load_system_config()
        return jsonify({
            'success': True,
            'data': config.to_dict()
        })
        
    except Exception as e:
        current_app.logger.error(f"Error loading system config: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@config_bp.route('/components', methods=['GET'])
def get_components_config():
    """Get components configuration.
    
    Returns:
        JSON response with components configuration
    """
    try:
        config = load_components_config()
        return jsonify({
            'success': True,
            'data': config.to_dict()
        })
        
    except Exception as e:
        current_app.logger.error(f"Error loading components config: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@config_bp.route('/llm', methods=['GET'])
def get_llm_config():
    """Get LLM configuration.
    
    Returns:
        JSON response with LLM configuration
    """
    try:
        config = load_llm_config()
        return jsonify({
            'success': True,
            'data': config.to_dict()
        })
        
    except Exception as e:
        current_app.logger.error(f"Error loading LLM config: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@config_bp.route('/raw', methods=['GET'])
def get_raw_config():
    """Get raw configuration from YAML files.
    
    Returns:
        JSON response with raw configuration data
    """
    try:
        # Load default config
        default_config = {}
        if DEFAULT_CONFIG_FILE.exists():
            with open(DEFAULT_CONFIG_FILE, 'r', encoding='utf-8') as f:
                default_config = yaml.safe_load(f) or {}
        
        # Load user config if exists
        user_config = {}
        if USER_CONFIG_FILE.exists():
            with open(USER_CONFIG_FILE, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f) or {}
        
        # Merge configs
        merged_config = ConfigLoader.deep_merge(default_config, user_config)
        
        return jsonify({
            'success': True,
            'data': {
                'default': default_config,
                'user': user_config,
                'merged': merged_config
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Error loading raw config: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@config_bp.route('/update', methods=['POST'])
def update_config():
    """Update configuration.
    
    Expects JSON payload with configuration updates.
    
    Returns:
        JSON response indicating success or failure
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Load existing user config or create new
        user_config = {}
        if USER_CONFIG_FILE.exists():
            with open(USER_CONFIG_FILE, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f) or {}
        
        # Merge with new data
        updated_config = ConfigLoader.deep_merge(user_config, data)
        
        # Validate the updated configuration
        try:
            # Create temporary merged config for validation
            default_config = {}
            if DEFAULT_CONFIG_FILE.exists():
                with open(DEFAULT_CONFIG_FILE, 'r', encoding='utf-8') as f:
                    default_config = yaml.safe_load(f) or {}
            
            merged_for_validation = ConfigLoader.deep_merge(default_config, updated_config)
            
            # Basic validation - try to load configs
            if 'system' in merged_for_validation:
                SystemConfig.from_dict(merged_for_validation)
            if 'components' in merged_for_validation:
                ComponentsConfig.from_dict(merged_for_validation)
            if 'llm' in merged_for_validation or 'ai' in merged_for_validation:
                LLMConfig.from_dict(merged_for_validation)
                
        except Exception as validation_error:
            return jsonify({
                'success': False,
                'error': f'Configuration validation failed: {str(validation_error)}'
            }), 400
        
        # Save updated config
        USER_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(USER_CONFIG_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(updated_config, f, default_flow_style=False, allow_unicode=True)
        
        return jsonify({
            'success': True,
            'message': 'Configuration updated successfully'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error updating config: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@config_bp.route('/reset', methods=['POST'])
def reset_config():
    """Reset configuration to defaults.
    
    Returns:
        JSON response indicating success or failure
    """
    try:
        # Remove user config file if it exists
        if USER_CONFIG_FILE.exists():
            USER_CONFIG_FILE.unlink()
        
        return jsonify({
            'success': True,
            'message': 'Configuration reset to defaults'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error resetting config: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@config_bp.route('/validate', methods=['POST'])
def validate_config():
    """Validate configuration.
    
    Optionally accepts JSON payload with configuration to validate.
    If no payload provided, validates current configuration.
    
    Returns:
        JSON response with validation results
    """
    try:
        data = request.get_json()
        
        if data:
            # Validate provided configuration
            try:
                # Merge with defaults for complete validation
                default_config = {}
                if DEFAULT_CONFIG_FILE.exists():
                    with open(DEFAULT_CONFIG_FILE, 'r', encoding='utf-8') as f:
                        default_config = yaml.safe_load(f) or {}
                
                merged_config = ConfigLoader.deep_merge(default_config, data)
                
                # Validate each section
                validation_results = []
                
                if 'system' in merged_config:
                    try:
                        SystemConfig.from_dict(merged_config)
                        validation_results.append({
                            'section': 'system',
                            'valid': True,
                            'message': 'System configuration is valid'
                        })
                    except Exception as e:
                        validation_results.append({
                            'section': 'system',
                            'valid': False,
                            'message': str(e)
                        })
                
                if 'components' in merged_config:
                    try:
                        ComponentsConfig.from_dict(merged_config)
                        validation_results.append({
                            'section': 'components',
                            'valid': True,
                            'message': 'Components configuration is valid'
                        })
                    except Exception as e:
                        validation_results.append({
                            'section': 'components',
                            'valid': False,
                            'message': str(e)
                        })
                
                if 'llm' in merged_config or 'ai' in merged_config:
                    try:
                        LLMConfig.from_dict(merged_config)
                        validation_results.append({
                            'section': 'llm',
                            'valid': True,
                            'message': 'LLM configuration is valid'
                        })
                    except Exception as e:
                        validation_results.append({
                            'section': 'llm',
                            'valid': False,
                            'message': str(e)
                        })
                
                all_valid = all(result['valid'] for result in validation_results)
                
                return jsonify({
                    'success': True,
                    'valid': all_valid,
                    'results': validation_results
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'valid': False,
                    'error': str(e)
                }), 400
        
        else:
            # Validate current configuration
            validation_report = validate_all_configs()
            
            return jsonify({
                'success': True,
                'valid': validation_report.is_valid,
                'results': [
                    {
                        'section': result.config_type,
                        'valid': result.is_valid,
                        'message': result.message,
                        'errors': result.errors
                    }
                    for result in validation_report.results
                ]
            })
        
    except Exception as e:
        current_app.logger.error(f"Error validating config: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@config_bp.route('/schema', methods=['GET'])
def get_config_schema():
    """Get configuration schema for frontend validation.
    
    Returns:
        JSON response with configuration schema
    """
    try:
        # This is a simplified schema - in a real implementation,
        # you might want to generate this from the actual config classes
        schema = {
            'system': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'version': {'type': 'string'},
                    'description': {'type': 'string'},
                    'locale': {'type': 'string'},
                    'timezone': {'type': 'string'},
                    'debug': {'type': 'boolean'},
                    'verbose': {'type': 'boolean'},
                    'environment': {'type': 'string'}
                }
            },
            'ai': {
                'type': 'object',
                'properties': {
                    'openai': {
                        'type': 'object',
                        'properties': {
                            'api_key': {'type': 'string'},
                            'base_url': {'type': 'string'},
                            'organization': {'type': 'string'},
                            'models': {'type': 'object'},
                            'default_params': {'type': 'object'}
                        }
                    },
                    'anthropic': {
                        'type': 'object',
                        'properties': {
                            'api_key': {'type': 'string'},
                            'base_url': {'type': 'string'},
                            'models': {'type': 'object'},
                            'default_params': {'type': 'object'}
                        }
                    }
                }
            }
        }
        
        return jsonify({
            'success': True,
            'data': schema
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting config schema: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500