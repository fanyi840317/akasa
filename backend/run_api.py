#!/usr/bin/env python3
"""
Akasa API Server Launcher

This script starts the Flask API server for the Akasa mystery research system.
"""

import os
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from api.app import create_app


def main():
    """Main entry point for the API server."""
    # Load environment variables from .env file if it exists
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)
    
    # Create Flask app
    app = create_app()
    
    # Get configuration from environment
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', 8000))
    debug = os.getenv('API_DEBUG', 'true').lower() == 'true'
    
    print(f"Starting Akasa API server on {host}:{port}")
    print(f"Debug mode: {debug}")
    print(f"API endpoints available at: http://{host}:{port}/api/")
    
    # Start the server
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )


if __name__ == '__main__':
    main()