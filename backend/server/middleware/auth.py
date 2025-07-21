# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

import logging
from typing import Optional
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)


def get_current_user_id(request: Request, credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[str]:
    """Extract user ID from request.
    
    This function tries multiple methods to get user ID:
    1. From Authorization header (JWT token)
    2. From X-User-ID header (for development/testing)
    3. From query parameter user_id
    4. Returns None if no user ID found (anonymous user)
    """
    
    # Method 1: Extract from JWT token (if using JWT authentication)
    if credentials and credentials.credentials:
        try:
            # Here you would decode the JWT token and extract user_id
            # For now, we'll assume the token itself is the user_id for simplicity
            # In production, you should properly decode and validate JWT
            token = credentials.credentials
            # TODO: Implement proper JWT decoding
            # decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # return decoded.get("user_id")
            logger.debug(f"JWT token received: {token[:10]}...")
        except Exception as e:
            logger.warning(f"Failed to decode JWT token: {e}")
    
    # Method 2: From X-User-ID header (for development/testing)
    user_id = request.headers.get("X-User-ID")
    if user_id:
        logger.debug(f"User ID from header: {user_id}")
        return user_id
    
    # Method 3: From query parameter
    user_id = request.query_params.get("user_id")
    if user_id:
        logger.debug(f"User ID from query: {user_id}")
        return user_id
    
    # Method 4: No user ID found - anonymous user
    logger.debug("No user ID found, treating as anonymous user")
    return None


def require_user_id(user_id: Optional[str] = Depends(get_current_user_id)) -> str:
    """Require user ID to be present, raise 401 if not found."""
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="User authentication required. Please provide user ID via Authorization header, X-User-ID header, or user_id query parameter."
        )
    return user_id


def get_user_id_or_default(user_id: Optional[str] = Depends(get_current_user_id)) -> str:
    """Get user ID or return default for anonymous users."""
    return user_id or "anonymous"