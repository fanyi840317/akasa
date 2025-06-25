# Copyright (c) 2025 Lingjing Project
# SPDX-License-Identifier: MIT

import os
import yaml
from dataclasses import dataclass, field, fields
from typing import Any, Optional
from pathlib import Path

from langchain_core.runnables import RunnableConfig

from .config import config
from src.rag.retriever import Resource


@dataclass(kw_only=True)
class Configuration:
    """神秘事件研究系统的可配置字段"""

    # 基础配置
    resources: list[Resource] = field(
        default_factory=list
    )  # 用于研究的资源
    max_plan_iterations: int = 1  # 最大计划迭代次数
    max_step_num: int = 5  # 计划中的最大步骤数（神秘事件研究需要更多步骤）
    max_search_results: int = 10  # 最大搜索结果数（神秘事件需要更多信息）
    mcp_settings: Optional[dict] = None  # MCP设置，包括动态加载的工具
    


    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """从RunnableConfig创建Configuration实例"""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})
    

    



def load_yaml_config(config_path: str) -> dict:
    """加载YAML配置文件"""
    config_file = Path(config_path)
    if not config_file.is_file():
        return {}

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except (yaml.YAMLError, IOError) as e:
        print(f"Warning: Failed to load or parse config from {config_path}: {e}")
        return {}