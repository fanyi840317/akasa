# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT

from .components import AgentType
from .llm import LLMType

# Agent to LLM type mapping
AGENT_LLM_MAP = {
    "researcher": LLMType.RESEARCH,
    "analyzer": LLMType.ANALYSIS,
    "planner": LLMType.REASONING,
    "reporter": LLMType.BASIC,
    "mystery_researcher": LLMType.RESEARCH,
    "academic_researcher": LLMType.RESEARCH,
    "credibility_analyzer": LLMType.ANALYSIS,
    "correlation_analyzer": LLMType.ANALYSIS,
    "mystery_planner": LLMType.REASONING,
    "mystery_reporter": LLMType.BASIC,
}

__all__ = ["AGENT_LLM_MAP"]