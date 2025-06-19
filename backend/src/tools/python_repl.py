#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT

"""
Python REPL tool for mysterious event research.
Provides code execution capabilities for data analysis and processing.
"""
import io
import json
import math
import logging
import traceback
import statistics
import multiprocessing
from datetime import datetime
from typing import Dict, Any, Optional, TYPE_CHECKING
from contextlib import redirect_stdout, redirect_stderr
from langchain_core.tools import BaseTool, tool

from .decorators import mystery_tool

logger = logging.getLogger(__name__)


class SafePythonREPL:
    """Safe Python REPL for mystery research data analysis."""
    
    def __init__(self):
        self._globals = {
            '__builtins__': {
                'len': len,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'range': range,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter,
                'sorted': sorted,
                'sum': sum,
                'min': min,
                'max': max,
                'abs': abs,
                'round': round,
                'print': print,
            }
        }
        
        # Add safe modules for data analysis
        try:
            safe_modules = {
                'json': json,
                'math': math,
                'datetime': datetime,
                'statistics': statistics,
            }
            for name, module in safe_modules.items():
                self._globals[name] = module
        except ImportError as e:
            logger.error(f"Failed to import required module: {str(e)}")
    
    def execute(self, code: str, timeout: int = 30) -> Dict[str, Any]:
        """Execute Python code safely.
        
        Args:
            code: Python code to execute
            timeout: Execution timeout in seconds
            
        Returns:
            Dict containing execution results
        """
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        result = {
            "success": False,
            "output": "",
            "error": None,
            "traceback": None
        }

        try:
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                # Run code with timeout
                with multiprocessing.Pool(1) as pool:
                    exec_result = pool.apply_async(exec, (code, self._globals))
                    exec_result.get(timeout=timeout)
                
            result["success"] = True
            result["output"] = stdout_capture.getvalue()
            
        except Exception as e:
            result["error"] = str(e)
            result["traceback"] = traceback.format_exc()
            logger.error(f"Code execution error: {str(e)}")
            
        finally:
            result["stderr"] = stderr_capture.getvalue()
            
        return result


# Global REPL instance
_repl = SafePythonREPL()


@tool
@mystery_tool(max_retries=3)
def python_repl_tool(
    code: str,
    timeout: Optional[int] = 30
) -> Dict[str, Any]:
    """Execute Python code safely in a restricted environment.
    
    Args:
        code: Python code to execute
        timeout: Execution timeout in seconds
        
    Returns:
        Dict containing execution results
    """
    try:
        return _repl.execute(code, timeout=timeout or 30)
    except Exception as e:
        logger.error(f"REPL tool error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@tool
@mystery_tool(max_retries=3)
def data_analysis_tool(
    data: str,
    analysis_type: str = "basic_stats"
) -> Dict[str, Any]:
    """Analyze data using Python statistical tools.
    
    Args:
        data: JSON string containing data to analyze
        analysis_type: Type of analysis to perform
        
    Returns:
        Dict containing analysis results
    """
    try:
        parsed_data = json.loads(data)
        result = {
            "analysis_type": analysis_type,
            "results": {},
            "errors": []
        }
        
        # Add analysis code here based on analysis_type
        
        return result
        
    except json.JSONDecodeError:
        return {"error": "Invalid JSON data"}
    except Exception as e:
        logger.error(f"Data analysis error: {str(e)}")
        return {"error": str(e)}


@tool
@mystery_tool(max_retries=3)
def mystery_data_processor(
    events: str,
    processing_type: str = "summary"
) -> Dict[str, Any]:
    """Process mystery event data using specific analysis routines.
    
    Args:
        events: JSON string containing event data
        processing_type: Type of processing to perform
        
    Returns:
        Dict containing processing results
    """
    try:
        parsed_events = json.loads(events)
        result = {
            "processing_type": processing_type,
            "results": {},
            "errors": []
        }
        
        # Add processing code here based on processing_type
        
        return result
        
    except json.JSONDecodeError:
        return {"error": "Invalid JSON data"}
    except Exception as e:
        logger.error(f"Data processing error: {str(e)}")
        return {"error": str(e)}