# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

import logging
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["research", "health"])


class ResearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 10
    sources: Optional[List[str]] = None


class ResearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    source: str
    timestamp: Optional[str] = None


class ResearchResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
    message: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    services: dict


@router.get("/health")
async def health_check():
    """健康检查端点"""
    try:
        return HealthResponse(
            status="healthy",
            timestamp=datetime.now().isoformat(),
            version="0.1.0",
            services={
                "api": "running",
                "database": "connected",
                "search": "available"
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Service unhealthy")


@router.post("/research")
async def research_query(request: ResearchRequest):
    """研究查询端点"""
    try:
        # 模拟搜索结果
        mock_results = [
            ResearchResult(
                title=f"Research Result for '{request.query}'",
                url="https://example.com/research",
                snippet=f"This is a mock research result for the query: {request.query}. In a real implementation, this would contain actual search results from various sources.",
                source="web",
                timestamp=datetime.now().isoformat()
            ),
            ResearchResult(
                title=f"Academic Paper on {request.query}",
                url="https://scholar.google.com/example",
                snippet=f"Academic research findings related to {request.query}. This would typically come from scholarly databases and research papers.",
                source="academic",
                timestamp=datetime.now().isoformat()
            ),
            ResearchResult(
                title=f"News Article: {request.query}",
                url="https://news.example.com/article",
                snippet=f"Latest news and developments regarding {request.query}. This would be sourced from news APIs and current events.",
                source="news",
                timestamp=datetime.now().isoformat()
            )
        ]
        
        # 限制结果数量
        limited_results = mock_results[:request.max_results]
        
        return ResearchResponse(
            success=True,
            data={
                "query": request.query,
                "results": [result.dict() for result in limited_results],
                "total_results": len(limited_results),
                "sources_used": request.sources or ["web", "academic", "news"]
            },
            message="Research completed successfully"
        )
        
    except Exception as e:
        logger.error(f"Research query failed: {e}")
        return ResearchResponse(
            success=False,
            error=str(e),
            message="Research query failed"
        )


@router.get("/research/sources")
async def get_available_sources():
    """获取可用的搜索源"""
    try:
        sources = {
            "web": {
                "name": "Web Search",
                "description": "General web search results",
                "enabled": True
            },
            "academic": {
                "name": "Academic Papers",
                "description": "Scholarly articles and research papers",
                "enabled": True
            },
            "news": {
                "name": "News Articles",
                "description": "Current news and events",
                "enabled": True
            },
            "github": {
                "name": "GitHub Repositories",
                "description": "Code repositories and documentation",
                "enabled": True
            }
        }
        
        return ResearchResponse(
            success=True,
            data={"sources": sources},
            message="Available sources retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to get sources: {e}")
        return ResearchResponse(
            success=False,
            error=str(e),
            message="Failed to retrieve available sources"
        )


@router.get("/research/status")
async def get_research_status():
    """获取研究服务状态"""
    try:
        return ResearchResponse(
            success=True,
            data={
                "service": "research",
                "status": "operational",
                "last_updated": datetime.now().isoformat(),
                "endpoints": {
                    "/api/research": "POST - Submit research query",
                    "/api/research/sources": "GET - Get available sources",
                    "/api/research/status": "GET - Get service status"
                }
            },
            message="Research service is operational"
        )
        
    except Exception as e:
        logger.error(f"Failed to get research status: {e}")
        return ResearchResponse(
            success=False,
            error=str(e),
            message="Failed to retrieve research status"
        )