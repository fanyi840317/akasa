# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from prompts.planner_model import StepType

from .types import State, GraphNodes
from prompts.planner_model import STEP_TYPE_TO_NODE_MAP
from .nodes import (
    coordinator_node,
    planner_node,
    reporter_node,
    mystery_researcher_node,
    academic_researcher_node,
    credibility_analyzer_node,
    correlation_analyzer_node,
    graph_storage_node,
    human_feedback_node,
    background_investigation_node,
)


def continue_to_running_research_team(state: State):
    """Determine the next node based on the current plan."""
    current_plan = state.get("current_plan")
    if not current_plan or not current_plan.get_next_step():
        # If there is no plan or all steps are completed, go to analysis
        return GraphNodes.CORRELATION_ANALYZER

    next_step = current_plan.get_next_step()

    # Route based on the step type using the map
    if next_step.step_type in STEP_TYPE_TO_NODE_MAP:
        return STEP_TYPE_TO_NODE_MAP[next_step.step_type].value
    
    # Fallback to a default researcher if no specific mapping is found
    return GraphNodes.MYSTERY_RESEARCHER.value


def should_continue_analysis(state: State):
    """Determine if additional analysis steps are needed."""
    current_plan = state.get("current_plan")
    if not current_plan:
        return GraphNodes.REPORTER
    
    # Check if credibility analysis is needed and enabled
    if (state.get("enable_credibility_filter") and 
        not state.get("credibility_scores") and 
        state.get("mystery_events")):
        return GraphNodes.CREDIBILITY_ANALYZER
    
    # Check if correlation analysis is needed and enabled
    if (state.get("enable_correlation_analysis") and 
        not state.get("correlation_results") and 
        len(state.get("mystery_events", [])) > 1):
        return GraphNodes.CORRELATION_ANALYZER
    
    # Check if graph storage is needed and enabled
    if (state.get("enable_graph_storage") and 
        not state.get("graph_relationships") and 
        state.get("mystery_events")):
        return GraphNodes.GRAPH_STORAGE
    
    return GraphNodes.REPORTER


def _build_base_graph():
    """Build and return the base state graph with all nodes and edges for mystery research."""
    builder = StateGraph(State)
    
    # Add all nodes
    builder.add_edge(START, GraphNodes.COORDINATOR)
    builder.add_node(GraphNodes.COORDINATOR, coordinator_node)
    builder.add_node(GraphNodes.BACKGROUND_INVESTIGATION, background_investigation_node)
    builder.add_node(GraphNodes.PLANNER, planner_node)
    builder.add_node(GraphNodes.REPORTER, reporter_node)
    builder.add_node(GraphNodes.MYSTERY_RESEARCHER, mystery_researcher_node)
    builder.add_node(GraphNodes.ACADEMIC_RESEARCHER, academic_researcher_node)
    builder.add_node(GraphNodes.CREDIBILITY_ANALYZER, credibility_analyzer_node)
    builder.add_node(GraphNodes.CORRELATION_ANALYZER, correlation_analyzer_node)
    builder.add_node(GraphNodes.GRAPH_STORAGE, graph_storage_node)
    builder.add_node(GraphNodes.HUMAN_FEEDBACK, human_feedback_node)
    
    # Add edges
    builder.add_edge(GraphNodes.BACKGROUND_INVESTIGATION, GraphNodes.PLANNER)
    
    # Conditional edges from coordinator
    builder.add_conditional_edges(
        GraphNodes.COORDINATOR,
        lambda state: GraphNodes.BACKGROUND_INVESTIGATION if state.get("enable_background_investigation") else GraphNodes.PLANNER,
        [GraphNodes.BACKGROUND_INVESTIGATION, GraphNodes.PLANNER]
    )
    
    # Conditional edges from planner
    builder.add_conditional_edges(
        GraphNodes.PLANNER,
        continue_to_running_research_team,
        {
            GraphNodes.MYSTERY_RESEARCHER: GraphNodes.MYSTERY_RESEARCHER,
            GraphNodes.ACADEMIC_RESEARCHER: GraphNodes.ACADEMIC_RESEARCHER,
            GraphNodes.CREDIBILITY_ANALYZER: GraphNodes.CREDIBILITY_ANALYZER,
            GraphNodes.CORRELATION_ANALYZER: GraphNodes.CORRELATION_ANALYZER,
            GraphNodes.GRAPH_STORAGE: GraphNodes.GRAPH_STORAGE,
            GraphNodes.HUMAN_FEEDBACK: GraphNodes.HUMAN_FEEDBACK,
            GraphNodes.REPORTER: GraphNodes.REPORTER,
            GraphNodes.PLANNER: GraphNodes.PLANNER,
        },
    )
    
    # Research nodes back to planner or analysis
    builder.add_conditional_edges(
        GraphNodes.MYSTERY_RESEARCHER,
        should_continue_analysis,
        {
            GraphNodes.PLANNER: GraphNodes.PLANNER,
            GraphNodes.CREDIBILITY_ANALYZER: GraphNodes.CREDIBILITY_ANALYZER,
            GraphNodes.CORRELATION_ANALYZER: GraphNodes.CORRELATION_ANALYZER,
            GraphNodes.GRAPH_STORAGE: GraphNodes.GRAPH_STORAGE,
            GraphNodes.REPORTER: GraphNodes.REPORTER,
        }
    )
    
    builder.add_conditional_edges(
        GraphNodes.ACADEMIC_RESEARCHER,
        should_continue_analysis,
        {
            GraphNodes.PLANNER: GraphNodes.PLANNER,
            GraphNodes.CREDIBILITY_ANALYZER: GraphNodes.CREDIBILITY_ANALYZER,
            GraphNodes.CORRELATION_ANALYZER: GraphNodes.CORRELATION_ANALYZER,
            GraphNodes.GRAPH_STORAGE: GraphNodes.GRAPH_STORAGE,
            GraphNodes.REPORTER: GraphNodes.REPORTER,
        }
    )
    
    # Analysis nodes
    builder.add_conditional_edges(
        GraphNodes.CREDIBILITY_ANALYZER,
        should_continue_analysis,
        {
            GraphNodes.CORRELATION_ANALYZER: GraphNodes.CORRELATION_ANALYZER,
            GraphNodes.GRAPH_STORAGE: GraphNodes.GRAPH_STORAGE,
            GraphNodes.REPORTER: GraphNodes.REPORTER,
        }
    )
    
    builder.add_conditional_edges(
        GraphNodes.CORRELATION_ANALYZER,
        should_continue_analysis,
        {
            GraphNodes.GRAPH_STORAGE: GraphNodes.GRAPH_STORAGE,
            GraphNodes.REPORTER: GraphNodes.REPORTER,
        }
    )
    
    builder.add_edge(GraphNodes.GRAPH_STORAGE, GraphNodes.REPORTER)
    
    # Human feedback and reporter
    builder.add_edge(GraphNodes.HUMAN_FEEDBACK, GraphNodes.PLANNER)
    builder.add_edge(GraphNodes.REPORTER, END)
    
    return builder


def build_graph():
    """Build and compile the mystery research graph."""
    builder = _build_base_graph()
    return builder.compile()


def build_graph_with_memory():
    """Build and compile the mystery research graph with memory."""
    builder = _build_base_graph()
    memory = MemorySaver()
    return builder.compile(checkpointer=memory)