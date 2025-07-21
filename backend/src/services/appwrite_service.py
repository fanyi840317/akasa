# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.users import Users
from appwrite.exception import AppwriteException
from appwrite.query import Query

from src.config.appwrite_config import appwrite_config
from src.config.tools import SearchEngine, RAGProvider
from src.config.report_style import ReportStyle

logger = logging.getLogger(__name__)


class AppwriteService:
    """Service for managing user configurations with Appwrite."""
    
    def __init__(self):
        if not appwrite_config.is_configured():
            logger.warning("Appwrite is not configured. Service will be disabled.")
            self.client = None
            self.databases = None
            self.users = None
            return
            
        self.client = Client()
        self.client.set_endpoint(appwrite_config.endpoint)
        self.client.set_project(appwrite_config.project_id)
        self.client.set_key(appwrite_config.api_key)
        
        self.databases = Databases(self.client)
        self.users = Users(self.client)
    
    def is_available(self) -> bool:
        """Check if Appwrite service is available."""
        return self.client is not None
    
    async def create_user(self, user_id: str, email: str, name: str, password: str) -> Dict[str, Any]:
        """Create a new user."""
        if not self.is_available():
            raise Exception("Appwrite service is not available")
            
        try:
            user = self.users.create(
                user_id=user_id,
                email=email,
                name=name,
                password=password
            )
            
            # Create default configuration for the user
            await self.create_default_config(user_id)
            
            return user
        except AppwriteException as e:
            logger.error(f"Failed to create user: {e}")
            raise
    
    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user by ID."""
        if not self.is_available():
            raise Exception("Appwrite service is not available")
            
        try:
            return self.users.get(user_id)
        except AppwriteException as e:
            logger.error(f"Failed to get user {user_id}: {e}")
            raise
    
    async def create_default_config(self, user_id: str) -> Dict[str, Any]:
        """Create default configuration for a user."""
        if not self.is_available():
            raise Exception("Appwrite service is not available")
            
        default_config = {
            "user_id": user_id,
            "search_engine": SearchEngine.TAVILY.value,
            "rag_provider": RAGProvider.RAGFLOW.value,
            "max_plan_iterations": 1,
            "max_step_num": 3,
            "max_search_results": 3,
            "report_style": ReportStyle.ACADEMIC.value,
            "enable_deep_thinking": False,
            "tools_config": {
                "tavily_search": {
                    "enabled": True,
                    "max_results": 10,
                    "include_images": True,
                    "include_raw_content": True
                },
                "duckduckgo_search": {
                    "enabled": False,
                    "max_results": 10,
                    "region": "us-en",
                    "safesearch": "moderate"
                },
                "brave_search": {
                    "enabled": False,
                    "max_results": 10,
                    "country": "US",
                    "search_lang": "en"
                },
                "arxiv_search": {
                    "enabled": False,
                    "max_results": 10,
                    "sort_by": "relevance",
                    "sort_order": "descending"
                }
            },
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        try:
            return self.databases.create_document(
                database_id=appwrite_config.database_id,
                collection_id=appwrite_config.configs_collection_id,
                document_id=user_id,  # Use user_id as document_id for easy lookup
                data=default_config
            )
        except AppwriteException as e:
            logger.error(f"Failed to create default config for user {user_id}: {e}")
            raise
    
    async def get_user_config(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user configuration."""
        if not self.is_available():
            raise Exception("Appwrite service is not available")
            
        try:
            document = self.databases.get_document(
                database_id=appwrite_config.database_id,
                collection_id=appwrite_config.configs_collection_id,
                document_id=user_id
            )
            return document
        except AppwriteException as e:
            if e.code == 404:  # Document not found
                logger.info(f"Config not found for user {user_id}, creating default")
                return await self.create_default_config(user_id)
            logger.error(f"Failed to get config for user {user_id}: {e}")
            raise
    
    async def update_user_config(self, user_id: str, config_updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update user configuration."""
        if not self.is_available():
            raise Exception("Appwrite service is not available")
            
        # Add updated timestamp
        config_updates["updated_at"] = datetime.now().isoformat()
        
        try:
            return self.databases.update_document(
                database_id=appwrite_config.database_id,
                collection_id=appwrite_config.configs_collection_id,
                document_id=user_id,
                data=config_updates
            )
        except AppwriteException as e:
            logger.error(f"Failed to update config for user {user_id}: {e}")
            raise
    
    async def update_tool_config(self, user_id: str, tool_name: str, tool_config: Dict[str, Any]) -> Dict[str, Any]:
        """Update specific tool configuration for a user."""
        if not self.is_available():
            raise Exception("Appwrite service is not available")
            
        # Get current config
        current_config = await self.get_user_config(user_id)
        
        # Update tool config
        if "tools_config" not in current_config:
            current_config["tools_config"] = {}
        
        current_config["tools_config"][tool_name] = tool_config
        current_config["updated_at"] = datetime.now().isoformat()
        
        try:
            return self.databases.update_document(
                database_id=appwrite_config.database_id,
                collection_id=appwrite_config.configs_collection_id,
                document_id=user_id,
                data={"tools_config": current_config["tools_config"], "updated_at": current_config["updated_at"]}
            )
        except AppwriteException as e:
            logger.error(f"Failed to update tool config for user {user_id}: {e}")
            raise
    
    async def get_tool_config(self, user_id: str, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get specific tool configuration for a user."""
        config = await self.get_user_config(user_id)
        if config and "tools_config" in config:
            return config["tools_config"].get(tool_name)
        return None
    
    async def list_users_with_configs(self, limit: int = 25, offset: int = 0) -> List[Dict[str, Any]]:
        """List users with their configurations."""
        if not self.is_available():
            raise Exception("Appwrite service is not available")
            
        try:
            response = self.databases.list_documents(
                database_id=appwrite_config.database_id,
                collection_id=appwrite_config.configs_collection_id,
                queries=[
                    Query.limit(limit),
                    Query.offset(offset),
                    Query.order_desc("updated_at")
                ]
            )
            return response["documents"]
        except AppwriteException as e:
            logger.error(f"Failed to list users with configs: {e}")
            raise


# Global instance
appwrite_service = AppwriteService()