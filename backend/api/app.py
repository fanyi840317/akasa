#!/usr/bin/env python3
"""
Flask application factory for Akasa API.
"""

from flask import Flask
from flask_cors import CORS
import logging
from typing import Optional

from .routes import config_bp
from .middleware import setup_error_handlers, setup_logging


def create_app(config_name: Optional[str] = None) -> Flask:
    """Create and configure Flask application.
    
    Args:
        config_name: Configuration name (development, production, testing)
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Enable CORS for frontend communication
    CORS(app, origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative dev port
        "http://localhost:8080",  # Alternative dev port
    ])
    
    # Setup logging
    setup_logging(app)
    
    # Setup error handlers
    setup_error_handlers(app)
    
    # Register blueprints
    app.register_blueprint(config_bp, url_prefix='/api/config')
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint."""
        return {'status': 'healthy', 'service': 'akasa-api'}
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8000)