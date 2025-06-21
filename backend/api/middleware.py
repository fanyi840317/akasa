#!/usr/bin/env python3
"""
Middleware for Flask application.
"""

import logging
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from typing import Dict, Any


def setup_logging(app: Flask) -> None:
    """Setup application logging.
    
    Args:
        app: Flask application instance
    """
    if not app.debug:
        # Production logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s: %(message)s'
        )
    else:
        # Development logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(name)s: %(message)s'
        )
    
    # Request logging
    @app.before_request
    def log_request_info():
        app.logger.debug('Request: %s %s', request.method, request.url)
        if request.get_json():
            app.logger.debug('Request body: %s', request.get_json())


def setup_error_handlers(app: Flask) -> None:
    """Setup error handlers for the application.
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(400)
    def bad_request(error) -> tuple[Dict[str, Any], int]:
        """Handle bad request errors."""
        return jsonify({
            'error': 'Bad Request',
            'message': 'The request could not be understood by the server.',
            'status_code': 400
        }), 400
    
    @app.errorhandler(404)
    def not_found(error) -> tuple[Dict[str, Any], int]:
        """Handle not found errors."""
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found.',
            'status_code': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error) -> tuple[Dict[str, Any], int]:
        """Handle internal server errors."""
        app.logger.error('Internal server error: %s', str(error))
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred.',
            'status_code': 500
        }), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException) -> tuple[Dict[str, Any], int]:
        """Handle HTTP exceptions."""
        return jsonify({
            'error': error.name,
            'message': error.description,
            'status_code': error.code
        }), error.code
    
    @app.errorhandler(Exception)
    def handle_exception(error: Exception) -> tuple[Dict[str, Any], int]:
        """Handle unexpected exceptions."""
        app.logger.error('Unexpected error: %s', str(error), exc_info=True)
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred.',
            'status_code': 500
        }), 500