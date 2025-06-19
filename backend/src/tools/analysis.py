#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT

"""
Analysis tools for mysterious event research.
Provides credibility analysis, correlation analysis, timeline analysis, and location analysis tools.
"""

import logging
from typing import Dict, List, Any, Optional
from langchain_core.tools import tool
import json

from .credibility import analyze_information_credibility, filter_reliable_information
from .correlation import analyze_event_correlations, build_correlation_timeline, analyze_location_patterns
from .timeline import analyze_timeline_patterns, generate_timeline_report
from .location import analyze_location_patterns as location_patterns, find_location_clusters, generate_location_heatmap_data
from .decorators import mystery_tool

logger = logging.getLogger(__name__)


@tool
@mystery_tool(max_retries=3)
def get_credibility_analyzer_tool(
    tool_input: str
) -> Dict[str, Any]:
    """Get credibility analysis tool for analyzing information reliability.
    
    Args:
        tool_input: JSON string containing {content: str, source_info?: Dict, context?: Dict}
        
    Returns:
        Dict containing credibility analysis results
    """
    try:
        data = json.loads(tool_input)
        content = data['content']
        source_info = data.get('source_info')
        context = data.get('context')
        result = analyze_information_credibility(content, source_info)
        result_dict = json.loads(result)
        logger.info(f"Credibility analysis completed with score: {result_dict.get('overall_score', 0)}")
        return result_dict
    except Exception as e:
        logger.error(f"Error in credibility analysis: {str(e)}")
        return {"error": str(e), "overall_score": 0.0}


@tool
@mystery_tool(max_retries=3)
def get_correlation_analyzer_tool(tool_input: str) -> Dict[str, Any]:
    """Get correlation analysis tool for analyzing relationships between events.
    
    Args:
        tool_input: JSON string containing list of events
        
    Returns:
        Dict containing correlation analysis results
    """
    try:
        events = json.loads(tool_input)
        result = {}
        
        result["timeline"] = build_correlation_timeline(json.dumps(events))
        result["locations"] = analyze_location_patterns(json.dumps(events))
        result["correlations"] = analyze_event_correlations(json.dumps(events))
        
        return result
    except Exception as e:
        logger.error(f"Error in correlation analysis: {str(e)}")
        return {"error": str(e)}


@tool
@mystery_tool(max_retries=3)
def get_timeline_analyzer_tool(tool_input: str) -> Dict[str, Any]:
    """Get timeline analysis tool for analyzing temporal patterns.
    
    Args:
        tool_input: JSON string containing {events: List[Dict], analysis_period?: str}
        
    Returns:
        Dict containing timeline analysis results
    """
    try:
        data = json.loads(tool_input)
        events = data["events"]
        analysis_period = data.get("analysis_period")
        
        result = analyze_timeline_patterns(json.dumps(events))
        return json.loads(result)
    except Exception as e:
        logger.error(f"Error in timeline analysis: {str(e)}")
        return {"error": str(e)}


@tool
@mystery_tool(max_retries=3)
def get_location_analyzer_tool(tool_input: str) -> Dict[str, Any]:
    """Get location analysis tool for analyzing spatial patterns.
    
    Args:
        tool_input: JSON string containing list of events
        
    Returns:
        Dict containing location analysis results
    """
    try:
        events = json.loads(tool_input)
        result = {}
        
        result["clusters"] = json.loads(find_location_clusters(json.dumps(events)))
        result["heatmap"] = json.loads(generate_location_heatmap_data(json.dumps(events)))
        result["patterns"] = json.loads(location_patterns(json.dumps(events)))
        
        return result
    except Exception as e:
        logger.error(f"Error in location analysis: {str(e)}")
        return {"error": str(e)}

@tool
@mystery_tool(max_retries=3)
def comprehensive_analysis_tool(
    events: List[Dict[str, Any]],
    enable_credibility: bool = True,
    enable_correlation: bool = True,
    enable_timeline: bool = True,
    enable_location: bool = True
) -> Dict[str, Any]:
    """Perform comprehensive analysis on mystery events.
    
    Args:
        events: List of mystery events to analyze
        enable_credibility: Whether to perform credibility analysis
        enable_correlation: Whether to perform correlation analysis
        enable_timeline: Whether to perform timeline analysis
        enable_location: Whether to perform location analysis
        
    Returns:
        Dict containing comprehensive analysis results
    """
    results = {
        "total_events": len(events),
        "analysis_timestamp": None,
        "credibility_analysis": None,
        "correlation_analysis": None,
        "timeline_analysis": None,
        "location_analysis": None,
        "summary": {}
    }
    
    try:
        from datetime import datetime
        results["analysis_timestamp"] = datetime.now().isoformat()
        
        # Credibility analysis
        if enable_credibility and events:
            credibility_scores = []
            for event in events:
                content = event.get("description", "")
                source_info = event.get("source", {})
                input_data = {
                    "content": content,
                    "source_info": source_info
                }
                score_result = json.loads(get_credibility_analyzer_tool(json.dumps(input_data)))
                if isinstance(score_result, dict):
                    credibility_scores.append(score_result.get("overall_score", 0.0))
            
            results["credibility_analysis"] = {
                "average_score": sum(credibility_scores) / len(credibility_scores) if credibility_scores else 0.0,
                "high_credibility_count": sum(1 for score in credibility_scores if score >= 0.7),
                "low_credibility_count": sum(1 for score in credibility_scores if score < 0.3),
                "scores": credibility_scores
            }
        
        # Correlation analysis
        if enable_correlation and events:
            results["correlation_analysis"] = json.loads(get_correlation_analyzer_tool(json.dumps(events)))
        
        # Timeline analysis
        if enable_timeline and events:
            results["timeline_analysis"] = json.loads(get_timeline_analyzer_tool(json.dumps({
                "events": events,
                "analysis_period": "auto"
            })))
        
        # Location analysis
        if enable_location and events:
            results["location_analysis"] = json.loads(get_location_analyzer_tool(json.dumps(events)))
        
        # Generate summary
        results["summary"] = {
            "high_credibility_events": results.get("credibility_analysis", {}).get("high_credibility_count", 0),
            "correlation_count": len(results.get("correlation_analysis", {}).get("correlations", [])),
            "timeline_patterns": len(results.get("timeline_analysis", {}).get("patterns", [])),
            "location_clusters": len(results.get("location_analysis", {}).get("clusters", []))
        }
        
        logger.info(f"Comprehensive analysis completed for {len(events)} events")
        return results
        
    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {str(e)}")
        results["error"] = str(e)
        return results