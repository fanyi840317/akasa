from flask import Blueprint, jsonify, request
from pathlib import Path
import sys
import os

# Add src directory to path
backend_dir = Path(__file__).parent.parent.parent
src_dir = backend_dir / 'src'
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from config import load_config, load_agents_config, load_tools_config
from config.validator import ConfigValidator, ValidationLevel

config_bp = Blueprint('config', __name__, url_prefix='/config')

@config_bp.route('/', methods=['GET'])
def get_config():
    """Get current configuration."""
    try:
        config = load_config()
        return jsonify({
            'success': True,
            'data': {
                'system': config.system.to_dict() if hasattr(config.system, 'to_dict') else config.system.__dict__,
                'llm': config.llm.to_dict() if hasattr(config.llm, 'to_dict') else config.llm.__dict__
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@config_bp.route('/agents', methods=['GET'])
def get_agents_config():
    """Get agents configuration."""
    try:
        agents_config = load_agents_config()
        return jsonify({
            'success': True,
            'data': {name: config.to_dict() if hasattr(config, 'to_dict') else config.__dict__ 
                    for name, config in agents_config.items()}
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@config_bp.route('/tools', methods=['GET'])
def get_tools_config():
    """Get tools configuration."""
    try:
        tools_config = load_tools_config()
        return jsonify({
            'success': True,
            'data': tools_config.to_dict() if hasattr(tools_config, 'to_dict') else tools_config.__dict__
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@config_bp.route('/validate', methods=['POST'])
def validate_config():
    """Validate configuration."""
    try:
        data = request.get_json() or {}
        validation_level = ValidationLevel(data.get('level', 'WARNING'))
        
        validator = ConfigValidator(validation_level)
        config = load_config()
        
        # Convert config to dict for validation
        config_dict = {
            'system': config.system.to_dict() if hasattr(config.system, 'to_dict') else config.system.__dict__,
            'llm': config.llm.to_dict() if hasattr(config.llm, 'to_dict') else config.llm.__dict__,
            'agents': {name: cfg.to_dict() if hasattr(cfg, 'to_dict') else cfg.__dict__ 
                      for name, cfg in config.agents.items()},
            'tools': config.tools.to_dict() if hasattr(config.tools, 'to_dict') else config.tools.__dict__
        }
        
        reports = validator.validate_config(config_dict)
        
        return jsonify({
            'success': True,
            'data': {
                'valid': len([r for r in reports if r.result.value == 'FAILED']) == 0,
                'reports': [{
                    'level': report.level.value,
                    'result': report.result.value,
                    'message': report.message,
                    'suggestions': report.suggestions
                } for report in reports]
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500