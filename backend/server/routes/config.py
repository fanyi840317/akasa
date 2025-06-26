# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

import logging

from fastapi import APIRouter
from src.config.tools import SELECTED_RAG_PROVIDER
from src.llms.llm import get_configured_llm_models
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
async def config():
    """Get the config of the server."""
    return ConfigResponse(
        rag=RAGConfigResponse(provider=SELECTED_RAG_PROVIDER),
        models=get_configured_llm_models(),
    )