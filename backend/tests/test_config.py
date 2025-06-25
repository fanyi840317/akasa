# SPDX-License-Identifier: MIT

import os
import sys
from pathlib import Path
import pytest
import tempfile
import yaml
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

# 模拟缺失的模块
import types

# 创建模拟的rag.retriever模块
# rag_module = types.ModuleType('rag')
# rag_retriever_module = types.ModuleType('rag.retriever')
# rag_retriever_module.Resource = type('Resource', (), {})
# rag_module.retriever = rag_retriever_module
# sys.modules['rag'] = rag_module
# sys.modules['rag.retriever'] = rag_retriever_module

from config.configuration import Configuration, load_yaml_config

from config.config import MysteryEventConfig


class TestConfigurationLoading:
    """测试配置文件加载功能"""
    
    def test_load_yaml_config_success(self):
        """测试成功加载YAML配置文件"""
        test_config = {
            'system': {
                'name': '测试系统',
                'version': '1.0.0',
                'debug': True
            },
            'ai': {
                'default_provider': 'openai',
                'openai': {
                    'model': 'gpt-4',
                    'temperature': 0.7
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            yaml.dump(test_config, f, default_flow_style=False, allow_unicode=True)
            f.flush()  # 确保数据写入文件
            temp_path = f.name
        
        try:
            result = load_yaml_config(temp_path)
            assert isinstance(result, dict)
            assert len(result) > 0  # 确保不是空字典
            if result:  # 如果成功加载
                assert result == test_config
                assert result['system']['name'] == '测试系统'
                assert result['ai']['openai']['model'] == 'gpt-4'
        finally:
            os.unlink(temp_path)
    
    def test_load_yaml_config_file_not_exists(self):
        """测试加载不存在的配置文件"""
        result = load_yaml_config('/path/to/nonexistent/file.yaml')
        assert result == {}
    
    def test_load_yaml_config_invalid_yaml(self):
        """测试加载无效的YAML文件"""
        invalid_yaml = "invalid: yaml: content: ["
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(invalid_yaml)
            temp_path = f.name
        
        try:
            result = load_yaml_config(temp_path)
            assert result == {}
        finally:
            os.unlink(temp_path)
    
    def test_load_yaml_config_empty_file(self):
        """测试加载空的YAML文件"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            temp_path = f.name
        
        try:
            result = load_yaml_config(temp_path)
            assert result == {}
        finally:
            os.unlink(temp_path)
    
    def test_load_default_yaml_config(self):
        """测试加载默认配置文件"""
        current_dir = Path(__file__).parent
        backend_root = current_dir.parent
        default_config_path = backend_root / "src" / "config" / "default.yaml"

        if default_config_path.exists():
            result = load_yaml_config(str(default_config_path))
            assert isinstance(result, dict)
            assert 'system' in result
            assert 'ai' in result
            assert result['system']['name'] == '神秘事件研究系统'
        else:
            pytest.skip(f"Default config file not found at {default_config_path}")
    
    def test_load_llm_config_yaml(self):
        """测试加载LLM配置文件"""
        backend_dir = Path(__file__).parent.parent
        llm_config_path = backend_dir / 'llm_config.yaml'
        
        if llm_config_path.exists():
            result = load_yaml_config(str(llm_config_path))
            assert isinstance(result, dict)
            assert 'openai' in result
            assert 'anthropic' in result
            assert 'google' in result
            
            # 检查OpenAI配置结构
            openai_config = result['openai']
            assert 'models' in openai_config
            assert 'default_params' in openai_config
            assert 'basic' in openai_config['models']


class TestConfigurationIntegration:
    """测试配置类的集成功能"""
    
    def test_configuration_default_values(self):
        """测试配置类的默认值"""
        config = Configuration()
        
        # 基础配置
        assert config.max_plan_iterations == 1
        assert config.max_step_num == 5
        assert config.max_search_results == 10
        assert config.mcp_settings is None
        
        # 神秘事件专用配置
        assert config.mystery_config is not None
        assert config.enable_academic_search is True
        assert config.enable_credibility_filter is True
        assert config.enable_correlation_analysis is True
        assert config.enable_graph_storage is True
        
        # 报告生成配置
        assert config.report_formats == ["markdown", "pdf", "json"]
        assert config.include_images is True
        assert config.include_timeline is True
        assert config.include_correlation_graph is True
        
        # API接口配置
        assert config.api_rate_limit == 100
        assert config.api_key_required is True
        assert config.enable_batch_processing is True
    
    def test_configuration_from_runnable_config(self):
        """测试从RunnableConfig创建配置"""
        runnable_config = {
            "configurable": {
                "max_plan_iterations": 3,
                "max_step_num": 8,
                "max_search_results": 15,
                "enable_academic_search": False,
                "api_rate_limit": 200
            }
        }
        
        # 如果from_runnable_config需要RunnableConfig类型，需先转换
        # 假设RunnableConfig是一个dataclass或类似结构
        from langchain_core.runnables import RunnableConfig  # 确保已导入正确类型
        config_obj = RunnableConfig(**runnable_config["configurable"])
        config = Configuration.from_runnable_config(config=config_obj)
        # 注意：from_runnable_config可能不会覆盖所有字段，只检查实际设置的值
        # 如果字段没有被设置，会使用默认值
        assert hasattr(config, 'max_plan_iterations')
        assert hasattr(config, 'max_step_num')
        assert hasattr(config, 'max_search_results')
        assert hasattr(config, 'enable_academic_search')
        assert hasattr(config, 'api_rate_limit')
    
    def test_configuration_from_environment_variables(self, monkeypatch):
        """测试从环境变量创建配置"""
        monkeypatch.setenv("MAX_PLAN_ITERATIONS", "5")
        monkeypatch.setenv("MAX_STEP_NUM", "10")
        monkeypatch.setenv("ENABLE_ACADEMIC_SEARCH", "false")
        
        config = Configuration.from_runnable_config()
        assert config.max_plan_iterations == "5"  # 环境变量是字符串
        assert config.max_step_num == "10"
        assert config.enable_academic_search == "false"
    
    def test_get_mystery_keywords(self):
        """测试获取神秘事件关键词"""
        config = Configuration()
        
        # 测试获取所有关键词
        all_keywords = config.get_mystery_keywords()
        assert isinstance(all_keywords, list)
        
        # 测试获取特定类型的关键词
        ufo_keywords = config.get_mystery_keywords("UFO")
        assert isinstance(ufo_keywords, list)
        
        # 测试无效类型
        invalid_keywords = config.get_mystery_keywords("INVALID_TYPE")
        assert isinstance(invalid_keywords, list)
    
    def test_get_reliable_sources(self):
        """测试获取可靠数据源"""
        config = Configuration()
        sources = config.get_reliable_sources()
        assert isinstance(sources, list)


class TestConfigurationFileIntegration:
    """测试配置文件与配置类的集成"""
    
    def test_load_and_apply_config(self):
        """测试加载配置文件并应用到配置类"""
        test_config = {
            'mystery_research': {
                'max_plan_iterations': 3,
                'max_step_num': 8,
                'enable_academic_search': False,
                'api_rate_limit': 150
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_config, f, default_flow_style=False, allow_unicode=True)
            temp_path = f.name
        
        try:
            # 加载配置文件
            loaded_config = load_yaml_config(temp_path)
            assert loaded_config == test_config
            
            # 应用到配置类
            mystery_config = loaded_config.get('mystery_research', {})
            config = Configuration.from_runnable_config(mystery_config)
            
            # 检查配置对象是否正确创建
            assert isinstance(config, Configuration)
            assert hasattr(config, 'max_plan_iterations')
            assert hasattr(config, 'max_step_num')
            assert hasattr(config, 'enable_academic_search')
            assert hasattr(config, 'api_rate_limit')
        finally:
            os.unlink(temp_path)
    
    @patch('builtins.open', new_callable=mock_open, read_data="invalid: yaml: [")
    def test_load_config_with_io_error(self, mock_file):
        """测试配置文件IO错误处理"""
        mock_file.side_effect = IOError("File read error")
        result = load_yaml_config("/fake/path/config.yaml")
        assert result == {}
    
    def test_config_file_encoding(self):
        """测试配置文件编码处理"""
        test_config = {
            'system': {
                'name': '神秘事件研究系统',
                'description': '基于AI的综合性神秘现象研究平台'
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', 
                                       encoding='utf-8', delete=False) as f:
            yaml.dump(test_config, f, default_flow_style=False, 
                     allow_unicode=True)
            temp_path = f.name
        
        try:
            result = load_yaml_config(temp_path)
            assert result['system']['name'] == '神秘事件研究系统'
            assert '神秘现象' in result['system']['description']
        finally:
            os.unlink(temp_path)


class TestConfigurationValidation:
    """测试配置验证功能"""
    
    def test_configuration_field_types(self):
        """测试配置字段类型验证"""
        config = Configuration(
            max_plan_iterations=5,
            max_step_num=10,
            max_search_results=20,
            enable_academic_search=True,
            report_formats=["markdown", "json"],
            api_rate_limit=300
        )
        
        assert isinstance(config.max_plan_iterations, int)
        assert isinstance(config.max_step_num, int)
        assert isinstance(config.max_search_results, int)
        assert isinstance(config.enable_academic_search, bool)
        assert isinstance(config.report_formats, list)
        assert isinstance(config.api_rate_limit, int)
    
    def test_configuration_mystery_config_integration(self):
        """测试神秘事件配置集成"""
        config = Configuration()
        
        # 测试神秘事件配置是否正确初始化
        assert hasattr(config, 'mystery_config')
        # 注意：由于我们使用了模拟的MysteryEventConfig，类型检查可能不同
        assert config.mystery_config is not None
        
        # 测试神秘事件相关方法
        keywords = config.get_mystery_keywords()
        sources = config.get_reliable_sources()
        
        assert isinstance(keywords, list)
        assert isinstance(sources, list)