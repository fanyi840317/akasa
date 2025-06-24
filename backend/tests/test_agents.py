# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys
from config.llm import LLMType

src_path = str((Path(__file__).parent.parent / "src").resolve())
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from agents.agents import (
    create_agent,
    create_mystery_agent,
    create_mystery_researcher_agent,
    create_academic_researcher_agent,
    create_credibility_analyzer_agent,
    create_correlation_analyzer_agent,
    create_mystery_planner_agent,
    create_mystery_reporter_agent
)


class TestCreateAgent:
    """Test the basic create_agent function."""
    
    @patch('agents.agents.create_react_agent')
    @patch('agents.agents.get_llm_by_type')
    @patch('agents.agents.apply_prompt_template')
    @patch('config.agents.AGENT_LLM_MAP', {'researcher': LLMType.RESEARCH})
    def test_create_agent_basic(self, mock_apply_prompt, mock_get_llm, mock_create_react):
        """Test basic agent creation."""
        # Setup mocks
        mock_llm = Mock()
        mock_get_llm.return_value = mock_llm
        mock_agent = Mock()
        mock_create_react.return_value = mock_agent
        mock_tools = [Mock(), Mock()]
        
        # Call function
        result = create_agent(
            agent_name="test_agent",
            agent_type="researcher",
            tools=mock_tools,
            prompt_template="test_template"
        )
        
        # Verify calls
        mock_get_llm.assert_called_once_with(LLMType.RESEARCH)
        mock_create_react.assert_called_once()
        
        # Check create_react_agent arguments
        call_args = mock_create_react.call_args
        assert call_args.kwargs['name'] == "test_agent"
        assert call_args.kwargs['model'] == mock_llm
        assert call_args.kwargs['tools'] == mock_tools
        assert callable(call_args.kwargs['prompt'])
        
        # Test prompt function
        test_state = {"test": "data"}
        prompt_func = call_args.kwargs['prompt']
        prompt_func(test_state)
        mock_apply_prompt.assert_called_once_with("test_template", test_state)
        
        assert result == mock_agent
    
    @patch('agents.agents.create_react_agent')
    @patch('agents.agents.get_llm_by_type')
    @patch('config.agents.AGENT_LLM_MAP', {})
    def test_create_agent_missing_type(self, mock_get_llm, mock_create_react):
        """Test agent creation with missing agent type."""
        with pytest.raises(KeyError):
            create_agent(
                agent_name="test_agent",
                agent_type="nonexistent_type",
                tools=[],
                prompt_template="test_template"
            )


class TestCreateMysteryAgent:
    """Test the create_mystery_agent function."""
    
    @patch('agents.agents.create_react_agent')
    @patch('agents.agents.get_llm_by_type')
    @patch('agents.agents.apply_prompt_template')
    @patch('config.agents.AGENT_LLM_MAP', {'researcher': LLMType.RESEARCH})
    def test_create_mystery_agent_basic(self, mock_apply_prompt, mock_get_llm, mock_create_react):
        """Test basic mystery agent creation."""
        # Setup mocks
        mock_llm = Mock()
        mock_get_llm.return_value = mock_llm
        mock_agent = Mock()
        mock_create_react.return_value = mock_agent
        mock_tools = [Mock()]
        mock_apply_prompt.return_value = "base prompt"
        
        # Call function
        result = create_mystery_agent(
            agent_name="mystery_agent",
            agent_type="researcher",
            tools=mock_tools,
            prompt_template="mystery_template"
        )
        
        # Verify basic calls
        mock_get_llm.assert_called_once_with(LLMType.RESEARCH)
        mock_create_react.assert_called_once()
        
        # Check create_react_agent arguments
        call_args = mock_create_react.call_args
        assert call_args.kwargs['name'] == "mystery_agent"
        assert call_args.kwargs['model'] == mock_llm
        assert call_args.kwargs['tools'] == mock_tools
        assert callable(call_args.kwargs['prompt'])
        
        assert result == mock_agent
    
    @patch('agents.agents.create_react_agent')
    @patch('agents.agents.get_llm_by_type')
    @patch('agents.agents.apply_prompt_template')
    @patch('agents.agents.AGENT_LLM_MAP', {'researcher': 'research_llm'})
    def test_create_mystery_agent_with_config(self, mock_apply_prompt, mock_get_llm, mock_create_react):
        """Test mystery agent creation with mystery config."""
        # Setup mocks
        mock_llm = Mock()
        mock_get_llm.return_value = mock_llm
        mock_agent = Mock()
        mock_create_react.return_value = mock_agent
        mock_apply_prompt.return_value = "base prompt"
        
        mystery_config = {
            "event_types": ["UFO", "Bigfoot"],
            "credibility_threshold": 0.7,
            "correlation_enabled": True
        }
        
        # Call function
        result = create_mystery_agent(
            agent_name="mystery_agent",
            agent_type="researcher",
            tools=[],
            prompt_template="mystery_template",
            mystery_config=mystery_config
        )
        
        # Test enhanced prompt function
        call_args = mock_create_react.call_args
        prompt_func = call_args.kwargs['prompt']
        
        test_state = {"test": "data"}
        result_prompt = prompt_func(test_state)
        
        # Verify base prompt was called
        mock_apply_prompt.assert_called_once_with("mystery_template", test_state)
        
        # Check that mystery context was added
        assert "神秘事件研究配置" in result_prompt
        assert "UFO, Bigfoot" in result_prompt
        assert "0.7" in result_prompt
        assert "启用" in result_prompt
    
    @patch('agents.agents.create_react_agent')
    @patch('agents.agents.get_llm_by_type')
    @patch('agents.agents.apply_prompt_template')
    @patch('agents.agents.AGENT_LLM_MAP', {'researcher': 'research_llm'})
    def test_create_mystery_agent_with_state_data(self, mock_apply_prompt, mock_get_llm, mock_create_react):
        """Test mystery agent with various state data."""
        # Setup mocks
        mock_llm = Mock()
        mock_get_llm.return_value = mock_llm
        mock_agent = Mock()
        mock_create_react.return_value = mock_agent
        mock_apply_prompt.return_value = "base prompt"
        
        # Call function
        result = create_mystery_agent(
            agent_name="mystery_agent",
            agent_type="researcher",
            tools=[],
            prompt_template="mystery_template"
        )
        
        # Test enhanced prompt function with state data
        call_args = mock_create_react.call_args
        prompt_func = call_args.kwargs['prompt']
        
        test_state = {
            "mystery_events": [
                Mock(title="Event 1", credibility_score=0.8),
                Mock(title="Event 2", credibility_score=0.6),
                Mock(title="Event 3", credibility_score=0.9),
                Mock(title="Event 4", credibility_score=0.7),
            ],
            "academic_sources": [Mock(), Mock(), Mock()],
            "credibility_scores": {"source1": 0.8, "source2": 0.6},
            "correlation_results": {"corr1": "data1", "corr2": "data2"}
        }
        
        result_prompt = prompt_func(test_state)
        
        # Check that all context was added
        assert "已收集神秘事件" in result_prompt
        assert "Event 1" in result_prompt
        assert "Event 2" in result_prompt
        assert "Event 3" in result_prompt
        assert "还有 1 个事件" in result_prompt  # Should show only first 3
        assert "学术资源" in result_prompt
        assert "已收集 3 个学术资源" in result_prompt
        assert "可信度分析" in result_prompt
        assert "平均可信度: 0.70" in result_prompt
        assert "关联分析" in result_prompt
        assert "发现 2 个关联关系" in result_prompt
    
    @patch('agents.agents.create_react_agent')
    @patch('agents.agents.get_llm_by_type')
    @patch('agents.agents.apply_prompt_template')
    @patch('agents.agents.AGENT_LLM_MAP', {'researcher': 'research_llm'})
    def test_create_mystery_agent_list_prompt(self, mock_apply_prompt, mock_get_llm, mock_create_react):
        """Test mystery agent with list-based prompt."""
        # Setup mocks
        mock_llm = Mock()
        mock_get_llm.return_value = mock_llm
        mock_agent = Mock()
        mock_create_react.return_value = mock_agent
        mock_apply_prompt.return_value = [{"role": "user", "content": "base prompt"}]
        
        mystery_config = {"event_types": ["UFO"]}
        
        # Call function
        result = create_mystery_agent(
            agent_name="mystery_agent",
            agent_type="researcher",
            tools=[],
            prompt_template="mystery_template",
            mystery_config=mystery_config
        )
        
        # Test enhanced prompt function with list prompt
        call_args = mock_create_react.call_args
        prompt_func = call_args.kwargs['prompt']
        
        test_state = {"test": "data"}
        result_prompt = prompt_func(test_state)
        
        # Should return list with additional message
        assert isinstance(result_prompt, list)
        assert len(result_prompt) == 2
        assert result_prompt[0] == {"role": "user", "content": "base prompt"}
        assert result_prompt[1]["role"] == "user"
        assert "神秘事件研究配置" in result_prompt[1]["content"]


class TestSpecializedAgents:
    """Test specialized agent creation functions."""
    
    @patch('agents.agents.create_mystery_agent')
    def test_create_mystery_researcher_agent(self, mock_create_mystery):
        """Test mystery researcher agent creation."""
        mock_tools = [Mock()]
        mock_config = {"test": "config"}
        mock_agent = Mock()
        mock_create_mystery.return_value = mock_agent
        
        result = create_mystery_researcher_agent(mock_tools, mock_config)
        
        mock_create_mystery.assert_called_once_with(
            agent_name="mystery_researcher",
            agent_type="researcher",
            tools=mock_tools,
            prompt_template="mystery_researcher",
            mystery_config=mock_config
        )
        assert result == mock_agent
    
    @patch('agents.agents.create_mystery_agent')
    def test_create_academic_researcher_agent(self, mock_create_mystery):
        """Test academic researcher agent creation."""
        mock_tools = [Mock()]
        mock_config = {"test": "config"}
        mock_agent = Mock()
        mock_create_mystery.return_value = mock_agent
        
        result = create_academic_researcher_agent(mock_tools, mock_config)
        
        mock_create_mystery.assert_called_once_with(
            agent_name="academic_researcher",
            agent_type="researcher",
            tools=mock_tools,
            prompt_template="academic_researcher",
            mystery_config=mock_config
        )
        assert result == mock_agent
    
    @patch('agents.agents.create_mystery_agent')
    def test_create_credibility_analyzer_agent(self, mock_create_mystery):
        """Test credibility analyzer agent creation."""
        mock_tools = [Mock()]
        mock_config = {"test": "config"}
        mock_agent = Mock()
        mock_create_mystery.return_value = mock_agent
        
        result = create_credibility_analyzer_agent(mock_tools, mock_config)
        
        mock_create_mystery.assert_called_once_with(
            agent_name="credibility_analyzer",
            agent_type="analyzer",
            tools=mock_tools,
            prompt_template="credibility_analyzer",
            mystery_config=mock_config
        )
        assert result == mock_agent
    
    @patch('agents.agents.create_mystery_agent')
    def test_create_correlation_analyzer_agent(self, mock_create_mystery):
        """Test correlation analyzer agent creation."""
        mock_tools = [Mock()]
        mock_config = {"test": "config"}
        mock_agent = Mock()
        mock_create_mystery.return_value = mock_agent
        
        result = create_correlation_analyzer_agent(mock_tools, mock_config)
        
        mock_create_mystery.assert_called_once_with(
            agent_name="correlation_analyzer",
            agent_type="analyzer",
            tools=mock_tools,
            prompt_template="correlation_analyzer",
            mystery_config=mock_config
        )
        assert result == mock_agent
    
    @patch('agents.agents.create_mystery_agent')
    def test_create_mystery_planner_agent(self, mock_create_mystery):
        """Test mystery planner agent creation."""
        mock_tools = [Mock()]
        mock_config = {"test": "config"}
        mock_agent = Mock()
        mock_create_mystery.return_value = mock_agent
        
        result = create_mystery_planner_agent(mock_tools, mock_config)
        
        mock_create_mystery.assert_called_once_with(
            agent_name="mystery_planner",
            agent_type="planner",
            tools=mock_tools,
            prompt_template="mystery_planner",
            mystery_config=mock_config
        )
        assert result == mock_agent
    
    @patch('agents.agents.create_mystery_agent')
    def test_create_mystery_reporter_agent(self, mock_create_mystery):
        """Test mystery reporter agent creation."""
        mock_tools = [Mock()]
        mock_config = {"test": "config"}
        mock_agent = Mock()
        mock_create_mystery.return_value = mock_agent
        
        result = create_mystery_reporter_agent(mock_tools, mock_config)
        
        mock_create_mystery.assert_called_once_with(
            agent_name="mystery_reporter",
            agent_type="reporter",
            tools=mock_tools,
            prompt_template="mystery_reporter",
            mystery_config=mock_config
        )
        assert result == mock_agent
    
    @patch('agents.agents.create_mystery_agent')
    def test_specialized_agents_with_none_config(self, mock_create_mystery):
        """Test specialized agents with None config."""
        mock_tools = [Mock()]
        mock_agent = Mock()
        mock_create_mystery.return_value = mock_agent
        
        # Test all specialized agents with None config
        agents_to_test = [
            create_mystery_researcher_agent,
            create_academic_researcher_agent,
            create_credibility_analyzer_agent,
            create_correlation_analyzer_agent,
            create_mystery_planner_agent,
            create_mystery_reporter_agent
        ]
        
        for agent_func in agents_to_test:
            mock_create_mystery.reset_mock()
            result = agent_func(mock_tools, None)
            
            # Verify create_mystery_agent was called with None config
            call_args = mock_create_mystery.call_args
            assert call_args.kwargs['mystery_config'] is None
            assert result == mock_agent


class TestIntegration:
    """Integration tests for agent creation."""
    
    @patch('agents.agents.create_react_agent')
    @patch('agents.agents.get_llm_by_type')
    @patch('agents.agents.apply_prompt_template')
    @patch('agents.agents.AGENT_LLM_MAP', {
        'researcher': 'research_llm',
        'analyzer': 'analysis_llm',
        'planner': 'planning_llm',
        'reporter': 'basic_llm'
    })
    def test_end_to_end_agent_creation(self, mock_apply_prompt, mock_get_llm, mock_create_react):
        """Test end-to-end agent creation workflow."""
        # Setup mocks
        mock_llm = Mock()
        mock_get_llm.return_value = mock_llm
        mock_agent = Mock()
        mock_create_react.return_value = mock_agent
        mock_apply_prompt.return_value = "test prompt"
        
        # Test tools
        mock_tools = [Mock(name="tool1"), Mock(name="tool2")]
        
        # Test mystery config
        mystery_config = {
            "event_types": ["UFO", "Cryptid"],
            "credibility_threshold": 0.8,
            "correlation_enabled": True
        }
        
        # Create different types of agents
        researcher = create_mystery_researcher_agent(mock_tools, mystery_config)
        analyzer = create_credibility_analyzer_agent(mock_tools, mystery_config)
        planner = create_mystery_planner_agent(mock_tools, mystery_config)
        reporter = create_mystery_reporter_agent(mock_tools, mystery_config)
        
        # Verify all agents were created
        assert researcher == mock_agent
        assert analyzer == mock_agent
        assert planner == mock_agent
        assert reporter == mock_agent
        
        # Verify correct LLM types were requested
        expected_llm_calls = ['research_llm', 'analysis_llm', 'planning_llm', 'basic_llm']
        actual_llm_calls = [call[0][0] for call in mock_get_llm.call_args_list]
        assert actual_llm_calls == expected_llm_calls
        
        # Verify create_react_agent was called 4 times
        assert mock_create_react.call_count == 4
    
    def test_agent_prompt_enhancement_edge_cases(self):
        """Test edge cases in prompt enhancement."""
        with patch('agents.agents.create_react_agent') as mock_create_react, \
             patch('agents.agents.get_llm_by_type') as mock_get_llm, \
             patch('agents.agents.apply_prompt_template') as mock_apply_prompt, \
             patch('agents.agents.AGENT_LLM_MAP', {'researcher': 'research_llm'}):
            
            mock_llm = Mock()
            mock_get_llm.return_value = mock_llm
            mock_agent = Mock()
            mock_create_react.return_value = mock_agent
            mock_apply_prompt.return_value = "base prompt"
            
            # Create agent
            agent = create_mystery_agent(
                agent_name="test_agent",
                agent_type="researcher",
                tools=[],
                prompt_template="test_template"
            )
            
            # Get prompt function
            prompt_func = mock_create_react.call_args.kwargs['prompt']
            
            # Test with empty state
            result = prompt_func({})
            assert result == "base prompt"
            
            # Test with empty lists/dicts
            result = prompt_func({
                "mystery_events": [],
                "academic_sources": [],
                "credibility_scores": {},
                "correlation_results": {}
            })
            assert result == "base prompt"
            
            # Test with single item lists
            result = prompt_func({
                "mystery_events": [Mock(title="Single Event", credibility_score=0.5)],
                "academic_sources": [Mock()],
                "credibility_scores": {"single": 0.5},
                "correlation_results": {"single": "data"}
            })
            
            assert "已收集神秘事件" in result
            assert "Single Event" in result
            assert "已收集 1 个学术资源" in result
            assert "平均可信度: 0.50" in result
            assert "发现 1 个关联关系" in result