#!/usr/bin/env python3
"""
API Routes for Akasa Backend.
"""

from .config import config_bp
from .agents import agents_bp

__all__ = ['config_bp', 'agents_bp']