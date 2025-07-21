# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

import logging

from fastapi import APIRouter, Depends, HTTPException
from src.config.tools import SELECTED_RAG_PROVIDER
from src.llms.llm import get_configured_llm_models
from src.services.appwrite_service import appwrite_service
from server.middleware.auth import get_user_id_or_default
from server.config_request import ConfigResponse
from server.rag_request import RAGConfigResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["config"])


@router.get("/rag/config", response_model=RAGConfigResponse)
async def rag_config():
    """Get the config of the RAG."""
    return RAGConfigResponse(provider=SELECTED_RAG_PROVIDER)


# @router.get("/rag/resources", response_model=RAGResourcesResponse)
# async def rag_resources(request: Annotated[RAGResourceRequest, Query()]):
#     """Get the resources of the RAG."""
#     retriever = build_retriever()
#     if retriever:
#         return RAGResourcesResponse(resources=retriever.list_resources(request.query))
#     return RAGResourcesResponse(resources=[])


@router.get("/config", response_model=ConfigResponse)
async def config(user_id: str = Depends(get_user_id_or_default)):
    """Get the config of the server."""
    try:
        # 获取已配置的 LLM 模型
        llm_models = get_configured_llm_models()
        
        config_data = {
            "llm_models": llm_models,
            "rag_provider": SELECTED_RAG_PROVIDER,
            "version": "1.0.0",
            "environment": "development",
            "user_id": user_id,
            "appwrite_enabled": appwrite_service.is_available()
        }
        
        # 如果 Appwrite 可用，获取用户特定的配置
        if appwrite_service.is_available():
            try:
                user_config = await appwrite_service.get_user_config(user_id)
                if user_config:
                    config_data["user_config"] = user_config
                    config_data["personalized"] = True
                else:
                    config_data["personalized"] = False
            except Exception as e:
                logger.warning(f"Failed to get user config for {user_id}: {e}")
                config_data["personalized"] = False
        else:
            config_data["personalized"] = False
        
        return ConfigResponse(
            success=True,
            data=config_data,
            message="Configuration retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Failed to get config: {e}")
        raise HTTPException(status_code=500, detail=str(e))