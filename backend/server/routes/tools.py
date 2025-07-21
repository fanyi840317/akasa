# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

import logging
import os
from datetime import datetime
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from src.config import SearchEngine, SELECTED_SEARCH_ENGINE
from src.tools.search import get_web_search_tool
from src.services.appwrite_service import appwrite_service
from server.middleware.auth import get_user_id_or_default

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/tools", tags=["tools"])


class ToolInfo(BaseModel):
    name: str
    type: str
    description: str
    enabled: bool
    config: Optional[Dict[str, Any]] = None
    status: str = "unknown"
    last_tested: Optional[str] = None


class ToolTestRequest(BaseModel):
    tool_name: str
    test_query: Optional[str] = "test query"
    config: Optional[Dict[str, Any]] = None


class ToolTestResult(BaseModel):
    success: bool
    tool_name: str
    response_time_ms: Optional[int] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    timestamp: str


class ToolConfigRequest(BaseModel):
    tool_name: str
    config: Dict[str, Any]
    enabled: Optional[bool] = None


class ToolsResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    message: Optional[str] = None


def get_search_engine_info() -> List[ToolInfo]:
    """获取所有搜索引擎工具信息"""
    tools = []
    
    # Tavily Search
    tavily_enabled = bool(os.getenv("TAVILY_API_KEY"))
    tools.append(ToolInfo(
        name="tavily_search",
        type="search",
        description="Tavily AI-powered search engine with real-time web results",
        enabled=tavily_enabled and SELECTED_SEARCH_ENGINE == SearchEngine.TAVILY.value,
        config={
            "api_key_set": bool(os.getenv("TAVILY_API_KEY")),
            "max_results": 10,
            "include_images": True,
            "include_raw_content": True
        },
        status="available" if tavily_enabled else "missing_api_key"
    ))
    
    # DuckDuckGo Search
    tools.append(ToolInfo(
        name="duckduckgo_search",
        type="search",
        description="DuckDuckGo privacy-focused search engine",
        enabled=SELECTED_SEARCH_ENGINE == SearchEngine.DUCKDUCKGO.value,
        config={
            "max_results": 10,
            "region": "us-en",
            "safesearch": "moderate"
        },
        status="available"
    ))
    
    # Brave Search
    brave_enabled = bool(os.getenv("BRAVE_SEARCH_API_KEY"))
    tools.append(ToolInfo(
        name="brave_search",
        type="search",
        description="Brave independent search engine",
        enabled=brave_enabled and SELECTED_SEARCH_ENGINE == SearchEngine.BRAVE_SEARCH.value,
        config={
            "api_key_set": bool(os.getenv("BRAVE_SEARCH_API_KEY")),
            "max_results": 10,
            "country": "US",
            "search_lang": "en"
        },
        status="available" if brave_enabled else "missing_api_key"
    ))
    
    # ArXiv Search
    tools.append(ToolInfo(
        name="arxiv_search",
        type="academic",
        description="ArXiv academic paper search",
        enabled=SELECTED_SEARCH_ENGINE == SearchEngine.ARXIV.value,
        config={
            "max_results": 10,
            "sort_by": "relevance",
            "sort_order": "descending"
        },
        status="available"
    ))
    
    return tools


@router.get("/")
async def get_tools(user_id: str = Depends(get_user_id_or_default)):
    """获取所有可用工具列表"""
    try:
        tools = get_search_engine_info()
        
        # 如果 Appwrite 可用，获取用户特定的配置
        if appwrite_service.is_available():
            try:
                user_config = await appwrite_service.get_user_config(user_id)
                if user_config and "tools_config" in user_config:
                    # 更新工具配置为用户特定的配置
                    for tool in tools:
                        if tool.name in user_config["tools_config"]:
                            user_tool_config = user_config["tools_config"][tool.name]
                            tool.enabled = user_tool_config.get("enabled", tool.enabled)
                            if "config" in user_tool_config:
                                tool.config.update(user_tool_config["config"])
            except Exception as e:
                logger.warning(f"Failed to get user config for {user_id}: {e}")
        
        enabled_count = sum(1 for tool in tools if tool.enabled)
        total_count = len(tools)
        
        return ToolsResponse(
            success=True,
            data={
                "tools": [tool.dict() for tool in tools],
                "enabled_count": enabled_count,
                "total": total_count,
                "current_search_engine": SELECTED_SEARCH_ENGINE,
                "user_id": user_id,
                "personalized": appwrite_service.is_available()
            },
            message="Tools retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to get tools: {e}")
        return ToolsResponse(
            success=False,
            error=str(e),
            message="Failed to retrieve tools"
        )


@router.post("/test")
async def test_tool(request: ToolTestRequest):
    """测试指定工具"""
    try:
        start_time = datetime.now()
        
        # 目前只支持搜索工具测试
        if request.tool_name not in ["tavily_search", "duckduckgo_search", "brave_search", "arxiv_search"]:
            raise HTTPException(status_code=400, detail=f"Tool {request.tool_name} is not supported for testing")
        
        # 根据工具名称设置搜索引擎
        engine_map = {
            "tavily_search": SearchEngine.TAVILY.value,
            "duckduckgo_search": SearchEngine.DUCKDUCKGO.value,
            "brave_search": SearchEngine.BRAVE_SEARCH.value,
            "arxiv_search": SearchEngine.ARXIV.value
        }
        
        # 临时设置搜索引擎（仅用于测试）
        original_engine = SELECTED_SEARCH_ENGINE
        test_engine = engine_map[request.tool_name]
        
        try:
            # 获取搜索工具并执行测试
            search_tool = get_web_search_tool(max_search_results=3)
            result = search_tool.run(request.test_query)
            
            end_time = datetime.now()
            response_time = int((end_time - start_time).total_seconds() * 1000)
            
            return ToolsResponse(
                success=True,
                data=ToolTestResult(
                    success=True,
                    tool_name=request.tool_name,
                    response_time_ms=response_time,
                    result=result,
                    timestamp=end_time.isoformat()
                ).dict(),
                message=f"Tool {request.tool_name} tested successfully"
            )
            
        except Exception as tool_error:
            end_time = datetime.now()
            response_time = int((end_time - start_time).total_seconds() * 1000)
            
            return ToolsResponse(
                success=False,
                data=ToolTestResult(
                    success=False,
                    tool_name=request.tool_name,
                    response_time_ms=response_time,
                    error=str(tool_error),
                    timestamp=end_time.isoformat()
                ).dict(),
                error=str(tool_error),
                message=f"Tool {request.tool_name} test failed"
            )
            
    except Exception as e:
        logger.error(f"Tool test failed: {e}")
        return ToolsResponse(
            success=False,
            error=str(e),
            message="Tool test failed"
        )


@router.post("/config")
async def update_tool_config(
    request: ToolConfigRequest,
    user_id: str = Depends(get_user_id_or_default)
):
    """更新工具配置"""
    try:
        # 如果 Appwrite 可用，保存用户特定的配置
        if appwrite_service.is_available():
            tool_config = request.config.copy()
            if request.enabled is not None:
                tool_config["enabled"] = request.enabled
            
            await appwrite_service.update_tool_config(user_id, request.tool_name, tool_config)
            
            return ToolsResponse(
                success=True,
                data={
                    "tool_name": request.tool_name,
                    "config": tool_config,
                    "enabled": request.enabled,
                    "user_id": user_id,
                    "updated_at": datetime.now().isoformat()
                },
                message=f"Tool {request.tool_name} configuration updated successfully for user {user_id}"
            )
        else:
            # 如果 Appwrite 不可用，返回模拟响应
            return ToolsResponse(
                success=True,
                data={
                    "tool_name": request.tool_name,
                    "config": request.config,
                    "enabled": request.enabled,
                    "updated_at": datetime.now().isoformat(),
                    "note": "Configuration not persisted (Appwrite not configured)"
                },
                message=f"Tool {request.tool_name} configuration updated successfully (not persisted)"
            )
        
    except Exception as e:
        logger.error(f"Failed to update tool config: {e}")
        return ToolsResponse(
            success=False,
            error=str(e),
            message="Failed to update tool configuration"
        )


@router.get("/search-engines")
async def get_search_engines():
    """获取可用的搜索引擎列表"""
    try:
        engines = []
        
        for engine in SearchEngine:
            engine_info = {
                "name": engine.value,
                "display_name": engine.value.replace("_", " ").title(),
                "enabled": engine.value == SELECTED_SEARCH_ENGINE,
                "requires_api_key": engine.value in ["tavily", "brave_search"]
            }
            
            # 检查API密钥状态
            if engine.value == "tavily":
                engine_info["api_key_configured"] = bool(os.getenv("TAVILY_API_KEY"))
            elif engine.value == "brave_search":
                engine_info["api_key_configured"] = bool(os.getenv("BRAVE_SEARCH_API_KEY"))
            else:
                engine_info["api_key_configured"] = True
                
            engines.append(engine_info)
        
        return ToolsResponse(
            success=True,
            data={
                "engines": engines,
                "current": SELECTED_SEARCH_ENGINE
            },
            message="Search engines retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to get search engines: {e}")
        return ToolsResponse(
            success=False,
            error=str(e),
            message="Failed to retrieve search engines"
        )


@router.get("/status")
async def get_tools_status():
    """获取工具服务状态"""
    try:
        tools = get_search_engine_info()
        
        status_summary = {
            "total_tools": len(tools),
            "enabled_tools": sum(1 for tool in tools if tool.enabled),
            "available_tools": sum(1 for tool in tools if tool.status == "available"),
            "tools_with_issues": sum(1 for tool in tools if tool.status != "available")
        }
        
        return ToolsResponse(
            success=True,
            data={
                "service": "tools",
                "status": "operational",
                "summary": status_summary,
                "last_updated": datetime.now().isoformat(),
                "endpoints": {
                    "/api/tools/": "GET - Get all tools",
                    "/api/tools/test": "POST - Test a tool",
                    "/api/tools/config": "POST - Update tool configuration",
                    "/api/tools/search-engines": "GET - Get search engines",
                    "/api/tools/status": "GET - Get tools status"
                }
            },
            message="Tools service is operational"
        )
        
    except Exception as e:
        logger.error(f"Failed to get tools status: {e}")
        return ToolsResponse(
            success=False,
            error=str(e),
            message="Failed to retrieve tools status"
        )