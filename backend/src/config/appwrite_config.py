# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class AppwriteConfig:
    """Appwrite configuration settings."""
    
    def __init__(self):
        self.endpoint = os.getenv("APPWRITE_ENDPOINT", "https://cloud.appwrite.io/v1")
        self.project_id = os.getenv("APPWRITE_PROJECT_ID")
        self.api_key = os.getenv("APPWRITE_API_KEY")
        self.database_id = os.getenv("APPWRITE_DATABASE_ID", "akasa_db")
        self.users_collection_id = os.getenv("APPWRITE_USERS_COLLECTION_ID", "users")
        self.configs_collection_id = os.getenv("APPWRITE_CONFIGS_COLLECTION_ID", "user_configs")
        
    def is_configured(self) -> bool:
        """Check if Appwrite is properly configured."""
        return bool(self.project_id and self.api_key)
    
    def validate(self) -> Optional[str]:
        """Validate configuration and return error message if invalid."""
        if not self.project_id:
            return "APPWRITE_PROJECT_ID is required"
        if not self.api_key:
            return "APPWRITE_API_KEY is required"
        return None


# Global instance
appwrite_config = AppwriteConfig()