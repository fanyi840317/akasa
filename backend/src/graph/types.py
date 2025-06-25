# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT

from langgraph.graph import MessagesState
from typing import TypedDict, List, Optional, Dict, Any
from enum import Enum
from langgraph.graph import START, END

from prompts.planner_model import Plan
from rag import Resource, MysteryEvent


class GraphNodes(str, Enum):
    START = START
    END = END
    COORDINATOR = "coordinator"
    PLANNER = "planner"
    REPORTER = "reporter"
    MYSTERY_RESEARCHER = "mystery_researcher"
    ACADEMIC_RESEARCHER = "academic_researcher"
    CREDIBILITY_ANALYZER = "credibility_analyzer"
    CORRELATION_ANALYZER = "correlation_analyzer"
    GRAPH_STORAGE = "graph_storage"
    HUMAN_FEEDBACK = "human_feedback"
    BACKGROUND_INVESTIGATION = "background_investigator"


class State(TypedDict, total=False):
    """State for the mystery research agent system, extends MessagesState with mystery-specific fields."""

    # Runtime Variables (inherited from deer-flow)
    locale: str = "zh-CN"  # Default to Chinese for mystery research
    observations: list[str] = []
    resources: list[Resource] = []
    plan_iterations: int = 0
    current_plan: Plan | str = None
    final_report: str = ""
    auto_accepted_plan: bool = False
    enable_background_investigation: bool = True
    background_investigation_results: str = None
    
    # Mystery Research Specific Variables
    mystery_events: List[MysteryEvent] = []  # Collected mystery events
    correlation_results: Dict[str, Any] = {}  # Event correlation analysis results
    credibility_scores: Dict[str, float] = {}  # Source credibility scores
    academic_sources: List[Dict[str, Any]] = []  # Academic database sources
    graph_relationships: List[Dict[str, Any]] = []  # Neo4j graph relationships
    
    # Feature Flags
    enable_academic_search: bool = True
    enable_credibility_filter: bool = True
    enable_correlation_analysis: bool = True
    enable_graph_storage: bool = True
    
    # Analysis Results
    timeline_analysis: Dict[str, Any] = {}
    location_analysis: Dict[str, Any] = {}
    pattern_analysis: Dict[str, Any] = {}
    witness_analysis: Dict[str, Any] = {}
    evidence_analysis: Dict[str, Any] = {}
    
    # Report Generation
    report_sections: Dict[str, str] = {}
    report_images: List[str] = []
    report_timeline: List[Dict[str, Any]] = []
    report_correlation_graph: Dict[str, Any] = {}
    
    # API Interface
    api_request_id: str = ""
    api_user_id: str = ""
    api_permissions: List[str] = []
    
    # Processing Status
    processing_status: str = "initialized"  # initialized, processing, completed, error
    error_messages: List[str] = []
    warnings: List[str] = []