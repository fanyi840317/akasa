# Copyright (c) 2024 Lingjing
# SPDX-License-Identifier: MIT

from enum import Enum
from typing import Literal


class DataSourceType(str, Enum):
    """数据源类型"""
    ACADEMIC = "academic"
    NEWS = "news"
    FORUM = "forum"
    DOCUMENTARY = "documentary"
    RESEARCH_INSTITUTE = "research_institute"
    MYSTERY = "mystery"


class SearchEngine(str, Enum):
    """搜索引擎类型"""
    TAVILY = "tavily"
    GOOGLE = "google"
    DUCKDUCKGO = "duckduckgo"
    BRAVE_SEARCH = "brave_search"


class RAGProvider(str, Enum):
    """RAG提供商类型"""
    NEO4J = "neo4j"
    DEFAULT = "default"


class MysteryEventType(str, Enum):
    """神秘事件类型"""
    UFO = "ufo"
    CRYPTID = "cryptid"
    PARANORMAL = "paranormal"
    ANCIENT_MYSTERY = "ancient_mystery"
    DISAPPEARANCE = "disappearance"
    NATURAL_ANOMALY = "natural_anomaly"


class ConfigType(str, Enum):
    """配置类型"""
    MYSTERY = "mystery"
    LLM = "llm"


class DataExtractor(str, Enum):
    """数据提取器类型"""
    DEFAULT = "default"


class AnalysisEngine(str, Enum):
    """Supported analysis engines."""
    CORRELATION_ANALYZER = "correlation_analyzer"


class LLMType(str, Enum):
    """Supported LLM types for different tasks."""
    
    # Basic models for general tasks
    BASIC = "basic"
    
    # Advanced reasoning models for complex analysis
    REASONING = "reasoning"
    
    # Vision models for image/video analysis
    VISION = "vision"
    
    # Fast models for quick responses
    FAST = "fast"
    
    # Embedding models for vector representations
    EMBEDDING = "embedding"
    
    # Code generation models
    CODE = "code"
    
    # Research-specific models
    RESEARCH = "research"
    
    # Analysis-specific models
    ANALYSIS = "analysis"