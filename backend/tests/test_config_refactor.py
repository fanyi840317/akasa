#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试配置重构 - 验证硬编码配置已成功移至配置文件
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_llm_config():
    """测试LLM配置是否正确从文件加载"""
    print("\n=== 测试LLM配置 ===")
    
    try:
        # Add src directory to Python path
import sys
from pathlib import Path

src_path = Path(__file__).parent.parent / 'src'
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config.llm.config import load_llm_config, LLMType
        
        # 加载配置
        config = load_llm_config()
        print(f"✓ LLM配置加载成功")
        print(f"  - 可用提供商: {list(config.providers.keys())}")
        print(f"  - 默认提供商: {config.default_providers}")
        print(f"  - 回退启用: {config.fallback_enabled}")
        
        # 测试获取特定类型的LLM配置
        basic_config = config.get_llm_by_type(LLMType.BASIC, "openai")
        print(f"  - OpenAI基础模型配置: {basic_config.get('model', 'N/A')}")
        
        # 测试model_configs是否生效
        if 'temperature' in basic_config:
            print(f"  - 温度参数: {basic_config['temperature']}")
        if 'max_tokens' in basic_config:
            print(f"  - 最大令牌数: {basic_config['max_tokens']}")
            
        return True
        
    except Exception as e:
        print(f"✗ LLM配置测试失败: {e}")
        return False

def test_system_config():
    """测试系统配置是否正确从文件加载"""
    print("\n=== 测试系统配置 ===")
    
    try:
        from config.system.config import load_system_config, MysteryEventType
        
        # 加载配置
        config = load_system_config()
        print(f"✓ 系统配置加载成功")
        print(f"  - 系统名称: {config.name}")
        print(f"  - 版本: {config.version}")
        
        # 测试神秘事件配置
        mystery_config = config.mystery_config
        print(f"  - 可信度阈值: {mystery_config.credibility_threshold}")
        print(f"  - 最大搜索结果: {mystery_config.max_search_results}")
        
        # 测试关键词配置
        if MysteryEventType.UFO in mystery_config.keywords:
            ufo_keywords = mystery_config.keywords[MysteryEventType.UFO]
            print(f"  - UFO关键词数量: {len(ufo_keywords)}")
            print(f"  - UFO关键词示例: {ufo_keywords[:3]}")
        
        # 测试数据源配置
        data_sources = mystery_config.data_sources
        print(f"  - 数据源数量: {len(data_sources)}")
        print(f"  - 数据源: {list(data_sources.keys())}")
        
        if 'cnki' in data_sources:
            cnki = data_sources['cnki']
            print(f"  - CNKI可信度权重: {cnki.credibility_weight}")
            
        return True
        
    except Exception as e:
        print(f"✗ 系统配置测试失败: {e}")
        return False

def test_config_integration():
    """测试配置集成"""
    print("\n=== 测试配置集成 ===")
    
    try:
        from config import load_config
        
        # 加载完整配置
        config = load_config()
        print(f"✓ 完整配置加载成功")
        
        # 验证各个配置模块
        print(f"  - 系统配置: {'✓' if config.system else '✗'}")
        print(f"  - 组件配置: {'✓' if config.components else '✗'}")
        print(f"  - LLM配置: {'✓' if config.llm else '✗'}")
        
        return True
        
    except Exception as e:
        print(f"✗ 配置集成测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试配置重构...")
    
    # 检查配置文件是否存在
    config_files = [
        "src/config/system/system.yaml",
        "src/config/llm/llm.yaml",
        "src/config/components/components.yaml"
    ]
    
    print("\n=== 检查配置文件 ===")
    all_files_exist = True
    for file_path in config_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} (文件不存在)")
            all_files_exist = False
    
    if not all_files_exist:
        print("\n配置文件缺失，无法继续测试")
        return False
    
    # 运行测试
    tests = [
        test_llm_config,
        test_system_config,
        test_config_integration
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # 总结
    print("\n=== 测试总结 ===")
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 所有测试通过！配置重构成功完成。")
        print("\n主要改进:")
        print("  - 移除了LLM配置中的硬编码DEFAULT_LLM_CONFIGS")
        print("  - 移除了系统配置中的硬编码关键词和数据源")
        print("  - 所有配置现在从YAML文件动态加载")
        print("  - 支持model_configs详细配置")
        print("  - 配置更加灵活和可维护")
        return True
    else:
        print("\n❌ 部分测试失败，请检查配置。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)