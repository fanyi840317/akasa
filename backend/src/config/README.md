# Configuration Module

这个模块提供了神秘事件研究系统的统一配置管理功能。

## 模块结构

### 核心模块

- **`base.py`** - 基础配置类和工具
  - `BaseConfig`: 所有配置类的基类
  - `ConfigLoader`: YAML配置文件加载器
  - `ConfigRegistry`: 配置注册表
  - 通用配置类: `APIConfig`, `DatabaseConfig`, `CacheConfig`

- **`system_config.py`** - 系统配置
  - 神秘事件类型和数据源配置
  - 系统性能和安全配置
  - 统一的系统配置管理

- **`components.py`** - 组件配置
  - 工具和代理配置
  - 搜索引擎、RAG提供商等枚举
  - 组件间依赖关系管理

- **`llms/`** - LLM配置模块
  - `types.py`: LLM类型定义
  - `llm.py`: LLM配置管理
  - `__init__.py`: 模块导出

- **`validator.py`** - 配置验证器
  - 多级别验证支持
  - 详细的验证报告
  - 配置完整性检查

## 使用方法

### 基本使用

```python
from config import (
    SystemConfig, ComponentsConfig, LLMConfig,
    load_system_config, ConfigValidator
)

# 加载系统配置
system_config = load_system_config("config/default.yaml")

# 加载组件配置
components_config = ComponentsConfig.from_dict(config_data)

# 验证配置
validator = ConfigValidator()
reports = validator.validate_system_config(system_config)
```

### 配置验证

```python
from config import validate_all_configs, print_validation_results

# 验证所有配置文件
reports = validate_all_configs("config/")
print_validation_results(reports)
```

### LLM配置

```python
from config import get_llm_by_type, LLMType

# 获取特定类型的LLM
llm = get_llm_by_type(LLMType.REASONING)
```

## 配置文件结构

### 统一配置 (default.yaml)

所有配置都已合并到default.yaml中，包括：
- 系统基本信息（名称、版本、调试模式等）
- AI模型配置（OpenAI、Anthropic、Google等）
- 搜索引擎配置（Tavily、Google、DuckDuckGo等）
- 数据库配置（Neo4j、Elasticsearch、PostgreSQL）
- 神秘事件类型定义
- 数据源配置
- 组件配置（RAG、分析引擎、数据提取器）
- 智能体配置
- 工作流配置
- 性能参数
- 缓存设置
- 安全配置
- 监控设置

```yaml
system:
  name: "Akasa Mystery Research System"
  version: "1.0.0"
  debug: false
  environment: "development"

ai:
  openai:
    api_key: ${OPENAI_API_KEY}
    models:
      basic: gpt-3.5-turbo
      reasoning: gpt-4

mystery_events:
  ufo:
    keywords: ["UFO", "不明飞行物", "飞碟"]
    credibility_factors:
      witness_count: 0.3
      evidence_quality: 0.4
```

## 迁移指南

### 从旧配置迁移

如果你之前使用的是旧的配置文件，需要进行以下迁移：

1. **`configuration.py` → `system_config.py`**
   - `Configuration` 类 → `SystemConfig` 类
   - 配置加载函数已统一

2. **`mystery_config.py` → `system_config.py`**
   - 神秘事件配置合并到系统配置中
   - 枚举类型保持不变

3. **`agents.py` + `tools.py` → `components.py`**
   - 代理和工具配置统一管理
   - 配置结构更加清晰

4. **`validator.py`**
   - 新的验证器支持多级别验证
   - 更详细的验证报告

### 代码更新示例

**旧代码:**
```python
from config.configuration import Configuration
from config.agents import AGENT_CONFIGS
from config.tools import SELECTED_SEARCH_ENGINE

config = Configuration.from_runnable_config(runnable_config)
agent_config = AGENT_CONFIGS["mystery_researcher"]
search_engine = SELECTED_SEARCH_ENGINE
```

**新代码:**
```python
from config import SystemConfig, ComponentsConfig
from config import SearchEngine, AgentType

system_config = SystemConfig.from_dict(config_data)
components_config = ComponentsConfig.from_dict(config_data)

agent_config = components_config.agents[AgentType.MYSTERY_RESEARCHER]
search_engine = components_config.search_engine
```

## 最佳实践

1. **使用环境变量**: 敏感信息如API密钥应使用环境变量
2. **配置验证**: 在系统启动前验证所有配置
3. **模块化配置**: 将不同类型的配置分离到不同文件
4. **版本控制**: 配置文件应纳入版本控制，但排除敏感信息
5. **文档更新**: 配置变更时及时更新文档

## 故障排除

### 常见问题

1. **导入错误**: 确保使用新的导入路径
2. **配置验证失败**: 检查配置文件格式和必需字段
3. **环境变量未设置**: 确保所有必需的环境变量已设置
4. **文件路径错误**: 使用绝对路径或正确的相对路径

### 调试技巧

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 验证配置
from config import ConfigValidator, ValidationLevel
validator = ConfigValidator(ValidationLevel.STRICT)
reports = validator.validate_config_file("config.yaml")
for report in reports:
    print(f"{report.result.value}: {report.message}")
```

## 贡献指南

1. 添加新配置类时，继承 `BaseConfig`
2. 实现 `validate()` 方法
3. 添加相应的测试用例
4. 更新文档和类型注解
5. 确保向后兼容性