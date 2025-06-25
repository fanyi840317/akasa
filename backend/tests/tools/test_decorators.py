# -*- coding: utf-8 -*-
# Copyright (c) 2024 Lingjing
# SPDX-License-Identifier: MIT

import json
import time
import logging
from unittest.mock import patch, MagicMock, call
import pytest
from src.tools.decorators import (
    log_io, performance_monitor, retry_on_failure, rate_limit, cache_result, mystery_tool
)
from src.config import MysteryEventType, DataSourceType

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)


class TestDecorators:
    """Test suite for all decorators."""

    def test_log_io(self):
        """Test the log_io decorator for input/output logging."""
        @log_io
        def sample_tool(a, b):
            return {"result": a + b}

        with patch('src.tools.decorators.logger') as mock_logger:
            result_json = sample_tool(1, 2)
            result = json.loads(result_json)
            assert result == {"result": 3}
            assert mock_logger.info.call_count >= 2
            assert mock_logger.debug.call_count >= 2

    def test_performance_monitor(self):
        """Test the performance_monitor decorator."""
        @performance_monitor(threshold_seconds=0.01)
        def fast_tool():
            return "fast"

        @performance_monitor(threshold_seconds=0.01)
        def slow_tool():
            time.sleep(0.02)
            return "slow"

        with patch('src.tools.decorators.logger') as mock_logger:
            fast_tool()
            mock_logger.warning.assert_not_called()
            slow_tool()
            mock_logger.warning.assert_called_once()

    def test_retry_on_failure(self):
        """Test the retry_on_failure decorator."""
        mock_func = MagicMock()
        mock_func.side_effect = [ValueError("fail"), ValueError("fail"), "success"]
        
        @retry_on_failure(max_retries=3, delay_seconds=0.01)
        def retry_tool():
            return mock_func()

        result = retry_tool()
        assert result == "success"
        assert mock_func.call_count == 3

    def test_retry_all_retries_fail(self):
        """Test when all retries fail in retry_on_failure."""
        mock_func = MagicMock(side_effect=ValueError("persistent failure"))

        @retry_on_failure(max_retries=3, delay_seconds=0.01)
        def failing_tool():
            return mock_func()

        with pytest.raises(ValueError, match="persistent failure"):
            failing_tool()
        assert mock_func.call_count == 4 # 1 initial + 3 retries

    @patch('time.sleep', return_value=None)
    def test_rate_limit(self, mock_sleep):
        """Test the rate_limit decorator."""
        @rate_limit(calls=2, period=1)
        def limited_tool():
            return "called"

        # First two calls should not sleep
        limited_tool()
        limited_tool()
        mock_sleep.assert_not_called()

        # Third call should sleep
        limited_tool()
        mock_sleep.assert_called_once()
        assert mock_sleep.call_args[0][0] > 0

    def test_cache_result(self):
        """Test the cache_result decorator."""
        mock_func = MagicMock(return_value="cached_result")

        @cache_result(duration=10)
        def cached_tool(param):
            return mock_func(param)

        # First call should execute the function
        result1 = cached_tool("A")
        assert result1 == "cached_result"
        mock_func.assert_called_once_with("A")

        # Second call with same param should return cached result
        result2 = cached_tool("A")
        assert result2 == "cached_result"
        mock_func.assert_called_once_with("A") # Not called again

        # Call with different param should execute again
        cached_tool("B")
        assert mock_func.call_count == 2

    def test_mystery_tool_decorator(self):
        """Test the mystery_tool decorator for query enhancement and Enum handling."""
        mock_config = {
            'keywords': {
                'UFO': ['sighting', 'alien']
            }
        }

        @mystery_tool(tool_config=mock_config)
        def sample_tool(query: str, event_type: str):
            return {"processed_query": query, "event": event_type}

        # Pass the Enum member as a keyword argument
        result_json = sample_tool(query="test query", event_type=MysteryEventType.UFO)
        result = json.loads(result_json)

        # The query passed to the original function is the *enhanced* one
        assert 'sighting' in result['processed_query']
        assert 'alien' in result['processed_query']
        assert 'test query' in result['processed_query']
        assert result['event'] == 'UFO'


@patch('time.sleep', return_value=None)
@patch('time.time', side_effect=list(range(20)))
def test_all_decorators_combined(_, __):
    """Test that all decorators work together correctly."""
    mock_config = {
        'keywords': {
            'UFO': ['haunting', 'spirit'] # Changed to UFO to match available Enum
        }
    }

    # Define a simple function to be decorated
    def base_tool(query, event_type):
        return {"final_query": query, "event": event_type}

    # Apply decorators in a more readable way
    @log_io
    @retry_on_failure(max_retries=1, delay_seconds=0)
    @cache_result(duration=10)
    @rate_limit(calls=5, period=10)
    @performance_monitor(threshold_seconds=0.5)
    @mystery_tool(tool_config=mock_config)
    def decorated_tool(query, event_type):
        return base_tool(query, event_type)

    # First call
    result1_json = decorated_tool(query="old house", event_type=MysteryEventType.UFO)
    result1 = json.loads(result1_json)
    assert 'haunting' in result1['final_query']
    assert 'spirit' in result1['final_query']
    assert result1['event'] == 'UFO'

    # Second call (should be cached)
    result2_json = decorated_tool(query="old house", event_type=MysteryEventType.UFO)
    result2 = json.loads(result2_json)
    assert result1 == result2