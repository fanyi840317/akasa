#!/usr/bin/env python3
"""
Akasa Backend API

RESTful API for the Akasa mystery research system.
"""

from .app import create_app

__all__ = ['create_app']