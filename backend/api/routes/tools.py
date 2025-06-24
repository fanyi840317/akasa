#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tools API Routes for Akasa Backend.

Provides endpoints for browsing and testing available tools.
"""

import json
import logging
from pathlib import Path
from flask import Blueprint, request, jsonify
from typing import Dict, Any, List

# Import unified API response class
from ..response import APIResponse
from config.tools import  load_tools_config

# Create blueprint
tools_bp = Blueprint('tools', __name__)
logger = logging.getLogger(__name__)


@tools_bp.route('/', methods=['GET'])
def list_tools():
    """
    List all available tools with their configurations.
    
    Returns:
        JSON response with tools list and metadata
    """
    try:
        tools_config =  load_tools_config()
        tools_list = []
        for tool_name, config in tools_config.items():
            tools_list.append({
                'name': config.name,
                'type': config.type,
                'description': config.description,
                'enabled': config.enabled,
                'parameters': list(config.parameters.keys()) if config.parameters else []
            })
        
        return APIResponse.success({
                'tools': tools_list,
                'total': len(tools_list),
                'enabled_count': sum(1 for t in tools_list if t['enabled'])
            })
        
    except Exception as e:
        logger.error(f"Error listing tools: {str(e)}")
        return APIResponse.error(f"Failed to list tools: {str(e)}")


    """
    Health check for tools API.
    
    Returns:
        JSON response with health status
    """
    return jsonify({
        'success': True,
        'data': {
            'status': 'healthy',
            'service': 'tools-api',
            'available_tools': len(MOCK_TOOLS_CONFIG),
            'enabled_tools': sum(1 for config in MOCK_TOOLS_CONFIG.values() if config['enabled'])
        }
    })