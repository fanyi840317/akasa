# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT

from .config import AgentType
from ..llm import LLMType

# Agent to LLM type mapping
AGENT_LLM_MAP = {
    AgentType.MYSTERY_RESEARCHER: LLMType.RESEARCH,
    AgentType.ACADEMIC_RESEARCHER: LLMType.RESEARCH,
    AgentType.CREDIBILITY_ANALYZER: LLMType.ANALYSIS,
    AgentType.CORRELATION_ANALYZER: LLMType.ANALYSIS,
    AgentType.DATA_COLLECTOR: LLMType.REASONING,
    AgentType.REPORT_GENERATOR: LLMType.BASIC,
    AgentType.TIMELINE_BUILDER: LLMType.REASONING,
    AgentType.EVIDENCE_EVALUATOR: LLMType.ANALYSIS,
}

__all__ = ["AGENT_LLM_MAP"]