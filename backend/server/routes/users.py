# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query

from src.services.appwrite_service import appwrite_service
from server.middleware.auth import get_current_user_id, require_user_id, get_user_id_or_default
from server.user_request import (
    CreateUserRequest,
    UserResponse,
    UserConfigRequest,
    UserConfigResponse,
    ToolConfigRequest,
    ToolConfigResponse,
    UserListResponse,
    ApiResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/", response_model=ApiResponse)
async def create_user(request: CreateUserRequest):
    """Create a new user with default configuration."""
    try:
        if not appwrite_service.is_available():
            raise HTTPException(
                status_code=503,
                detail="User management service is not available. Please configure Appwrite."
            )
        
        user = await appwrite_service.create_user(
            user_id=request.user_id,
            email=request.email,
            name=request.name,
            password=request.password
        )
        
        return ApiResponse(
            success=True,
            data={
                "user_id": user["$id"],
                "email": user["email"],
                "name": user["name"],
                "created_at": user["$createdAt"],
                "updated_at": user["$updatedAt"]
            },
            message="User created successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to create user: {e}")
        return ApiResponse(
            success=False,
            error=str(e),
            message="Failed to create user"
        )


@router.get("/me", response_model=ApiResponse)
async def get_current_user(user_id: str = Depends(require_user_id)):
    """Get current user information."""
    try:
        if not appwrite_service.is_available():
            raise HTTPException(
                status_code=503,
                detail="User management service is not available. Please configure Appwrite."
            )
        
        user = await appwrite_service.get_user(user_id)
        
        return ApiResponse(
            success=True,
            data={
                "user_id": user["$id"],
                "email": user["email"],
                "name": user["name"],
                "created_at": user["$createdAt"],
                "updated_at": user["$updatedAt"]
            },
            message="User information retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to get user {user_id}: {e}")
        return ApiResponse(
            success=False,
            error=str(e),
            message="Failed to retrieve user information"
        )


@router.get("/config", response_model=ApiResponse)
async def get_user_config(user_id: str = Depends(get_user_id_or_default)):
    """Get user configuration."""
    try:
        if not appwrite_service.is_available():
            # Return default configuration if Appwrite is not available
            from src.config.tools import SearchEngine, RAGProvider
            from src.config.report_style import ReportStyle
            
            default_config = {
                "user_id": user_id,
                "search_engine": SearchEngine.TAVILY.value,
                "rag_provider": RAGProvider.RAGFLOW.value,
                "max_plan_iterations": 1,
                "max_step_num": 3,
                "max_search_results": 3,
                "report_style": ReportStyle.ACADEMIC.value,
                "enable_deep_thinking": False,
                "tools_config": {},
                "created_at": "2025-01-01T00:00:00Z",
                "updated_at": "2025-01-01T00:00:00Z"
            }
            
            return ApiResponse(
                success=True,
                data=default_config,
                message="Default configuration returned (Appwrite not configured)"
            )
        
        config = await appwrite_service.get_user_config(user_id)
        
        return ApiResponse(
            success=True,
            data=config,
            message="User configuration retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to get config for user {user_id}: {e}")
        return ApiResponse(
            success=False,
            error=str(e),
            message="Failed to retrieve user configuration"
        )


@router.put("/config", response_model=ApiResponse)
async def update_user_config(
    request: UserConfigRequest,
    user_id: str = Depends(get_user_id_or_default)
):
    """Update user configuration."""
    try:
        if not appwrite_service.is_available():
            return ApiResponse(
                success=False,
                error="User management service is not available",
                message="Please configure Appwrite to enable user configuration management"
            )
        
        # Convert request to dict, excluding None values
        config_updates = {k: v for k, v in request.dict().items() if v is not None}
        
        updated_config = await appwrite_service.update_user_config(user_id, config_updates)
        
        return ApiResponse(
            success=True,
            data=updated_config,
            message="User configuration updated successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to update config for user {user_id}: {e}")
        return ApiResponse(
            success=False,
            error=str(e),
            message="Failed to update user configuration"
        )


@router.get("/tools/{tool_name}/config", response_model=ApiResponse)
async def get_tool_config(
    tool_name: str,
    user_id: str = Depends(get_user_id_or_default)
):
    """Get specific tool configuration for user."""
    try:
        if not appwrite_service.is_available():
            return ApiResponse(
                success=False,
                error="User management service is not available",
                message="Please configure Appwrite to enable tool configuration management"
            )
        
        tool_config = await appwrite_service.get_tool_config(user_id, tool_name)
        
        if tool_config is None:
            return ApiResponse(
                success=False,
                error="Tool configuration not found",
                message=f"No configuration found for tool {tool_name}"
            )
        
        return ApiResponse(
            success=True,
            data={
                "tool_name": tool_name,
                "config": tool_config
            },
            message="Tool configuration retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to get tool config for user {user_id}, tool {tool_name}: {e}")
        return ApiResponse(
            success=False,
            error=str(e),
            message="Failed to retrieve tool configuration"
        )


@router.put("/tools/{tool_name}/config", response_model=ApiResponse)
async def update_tool_config(
    tool_name: str,
    request: ToolConfigRequest,
    user_id: str = Depends(get_user_id_or_default)
):
    """Update specific tool configuration for user."""
    try:
        if not appwrite_service.is_available():
            return ApiResponse(
                success=False,
                error="User management service is not available",
                message="Please configure Appwrite to enable tool configuration management"
            )
        
        # Prepare tool config
        tool_config = request.config.copy()
        if request.enabled is not None:
            tool_config["enabled"] = request.enabled
        
        updated_config = await appwrite_service.update_tool_config(user_id, tool_name, tool_config)
        
        return ApiResponse(
            success=True,
            data={
                "tool_name": tool_name,
                "config": tool_config,
                "updated_at": updated_config["updated_at"]
            },
            message=f"Tool {tool_name} configuration updated successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to update tool config for user {user_id}, tool {tool_name}: {e}")
        return ApiResponse(
            success=False,
            error=str(e),
            message="Failed to update tool configuration"
        )


@router.get("/list", response_model=ApiResponse)
async def list_users(
    limit: int = Query(25, ge=1, le=100, description="Number of users to return"),
    offset: int = Query(0, ge=0, description="Number of users to skip")
):
    """List users with their configurations (admin endpoint)."""
    try:
        if not appwrite_service.is_available():
            return ApiResponse(
                success=False,
                error="User management service is not available",
                message="Please configure Appwrite to enable user management"
            )
        
        users = await appwrite_service.list_users_with_configs(limit=limit, offset=offset)
        
        return ApiResponse(
            success=True,
            data={
                "users": users,
                "total": len(users),
                "limit": limit,
                "offset": offset
            },
            message="Users retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to list users: {e}")
        return ApiResponse(
            success=False,
            error=str(e),
            message="Failed to retrieve users"
        )


@router.get("/health", response_model=ApiResponse)
async def user_service_health():
    """Check user service health."""
    try:
        is_available = appwrite_service.is_available()
        
        return ApiResponse(
            success=True,
            data={
                "service": "users",
                "appwrite_configured": is_available,
                "status": "operational" if is_available else "degraded",
                "message": "Appwrite is configured and available" if is_available else "Appwrite is not configured, using fallback mode"
            },
            message="User service health check completed"
        )
        
    except Exception as e:
        logger.error(f"User service health check failed: {e}")
        return ApiResponse(
            success=False,
            error=str(e),
            message="User service health check failed"
        )