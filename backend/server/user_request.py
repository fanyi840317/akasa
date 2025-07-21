# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class CreateUserRequest(BaseModel):
    """Request model for creating a new user."""
    
    user_id: str = Field(..., description="Unique user identifier")
    email: EmailStr = Field(..., description="User email address")
    name: str = Field(..., description="User display name")
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")


class UserResponse(BaseModel):
    """Response model for user information."""
    
    user_id: str = Field(..., description="User identifier")
    email: str = Field(..., description="User email")
    name: str = Field(..., description="User name")
    created_at: str = Field(..., description="User creation timestamp")
    updated_at: str = Field(..., description="User last update timestamp")


class UserConfigRequest(BaseModel):
    """Request model for updating user configuration."""
    
    search_engine: Optional[str] = Field(None, description="Preferred search engine")
    rag_provider: Optional[str] = Field(None, description="RAG provider")
    max_plan_iterations: Optional[int] = Field(None, ge=1, le=10, description="Maximum plan iterations")
    max_step_num: Optional[int] = Field(None, ge=1, le=20, description="Maximum steps in plan")
    max_search_results: Optional[int] = Field(None, ge=1, le=50, description="Maximum search results")
    report_style: Optional[str] = Field(None, description="Report style preference")
    enable_deep_thinking: Optional[bool] = Field(None, description="Enable deep thinking mode")
    tools_config: Optional[Dict[str, Any]] = Field(None, description="Tools configuration")


class UserConfigResponse(BaseModel):
    """Response model for user configuration."""
    
    user_id: str = Field(..., description="User identifier")
    search_engine: str = Field(..., description="Current search engine")
    rag_provider: str = Field(..., description="Current RAG provider")
    max_plan_iterations: int = Field(..., description="Maximum plan iterations")
    max_step_num: int = Field(..., description="Maximum steps in plan")
    max_search_results: int = Field(..., description="Maximum search results")
    report_style: str = Field(..., description="Report style")
    enable_deep_thinking: bool = Field(..., description="Deep thinking enabled")
    tools_config: Dict[str, Any] = Field(..., description="Tools configuration")
    created_at: str = Field(..., description="Configuration creation timestamp")
    updated_at: str = Field(..., description="Configuration last update timestamp")


class ToolConfigRequest(BaseModel):
    """Request model for updating tool configuration."""
    
    tool_name: str = Field(..., description="Tool name")
    enabled: Optional[bool] = Field(None, description="Whether tool is enabled")
    config: Dict[str, Any] = Field(..., description="Tool configuration parameters")


class ToolConfigResponse(BaseModel):
    """Response model for tool configuration."""
    
    tool_name: str = Field(..., description="Tool name")
    enabled: bool = Field(..., description="Whether tool is enabled")
    config: Dict[str, Any] = Field(..., description="Tool configuration")
    updated_at: str = Field(..., description="Last update timestamp")


class UserListResponse(BaseModel):
    """Response model for user list."""
    
    users: List[UserConfigResponse] = Field(..., description="List of users with configurations")
    total: int = Field(..., description="Total number of users")
    limit: int = Field(..., description="Limit used for pagination")
    offset: int = Field(..., description="Offset used for pagination")


class ApiResponse(BaseModel):
    """Generic API response model."""
    
    success: bool = Field(..., description="Whether the operation was successful")
    data: Optional[Any] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if operation failed")
    message: Optional[str] = Field(None, description="Human-readable message")