# SPDX-License-Identifier: MIT

import sys
from pathlib import Path

# Add the project root directory to the Python path
# This allows for absolute imports from 'src' (e.g., from src.config.configuration import Configuration)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from src.config.config import Config

@pytest.fixture(scope="session")
def config():
    """全局测试配置"""
    return Config()