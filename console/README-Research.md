# Research Page API Configuration

Research页面集成了多个真实API来提供全面的搜索功能，包括神秘现象、新闻、学术论文和开源项目。

## 支持的API

### 1. Wikipedia API (免费)
- **用途**: 搜索神秘现象和百科知识
- **配置**: 无需配置，开箱即用
- **限制**: 合理使用，无严格限制

### 2. arXiv API (免费)
- **用途**: 搜索学术论文和研究
- **配置**: 无需配置，开箱即用
- **限制**: 合理使用，无严格限制

### 3. News API (需要密钥)
- **用途**: 搜索实时新闻和媒体报道
- **获取密钥**: https://newsapi.org (免费计划每月1000次请求)
- **配置**: 在`.env.local`中设置`VITE_NEWS_API_KEY`

### 4. GitHub API (可选密钥)
- **用途**: 搜索开源项目和代码仓库
- **无密钥**: 每小时60次请求
- **有密钥**: 每小时5000次请求
- **获取密钥**: https://github.com/settings/tokens
- **配置**: 在`.env.local`中设置`VITE_GITHUB_TOKEN`

## 配置步骤

### 1. 创建环境变量文件
```bash
cp .env.example .env.local
```

### 2. 配置API密钥
编辑`.env.local`文件：

```env
# News API - 必需（用于新闻搜索）
VITE_NEWS_API_KEY=your_actual_news_api_key

# GitHub Token - 可选（提高请求限制）
VITE_GITHUB_TOKEN=your_actual_github_token
```

### 3. 获取News API密钥
1. 访问 https://newsapi.org
2. 点击"Get API Key"
3. 注册账户
4. 复制API密钥到`.env.local`

### 4. 获取GitHub Token（可选）
1. 访问 https://github.com/settings/tokens
2. 点击"Generate new token (classic)"
3. 选择适当的权限（public_repo即可）
4. 复制token到`.env.local`

## API状态指示器

页面右上角显示各API的状态：
- 🟢 绿色：API工作正常
- 🟡 黄色：API有限制或需要配置
- 🔴 红色：API出现错误
- ⚪ 灰色：API未使用

## 功能特性

### 多源搜索
- 同时搜索Wikipedia、arXiv、News API和GitHub
- 结果按类型分类显示
- 支持不同类型的内容标识

### 神秘事件专区
- 自动加载Wikipedia上的神秘现象内容
- 严重程度分级显示
- 地理位置信息
- 验证状态标识

### 搜索历史
- 自动保存搜索记录
- 快速重复搜索
- 本地存储持久化

### 资源收藏
- 保存感兴趣的搜索结果
- 分类管理
- 快速访问链接

## 故障排除

### News API不工作
- 检查`.env.local`中的`VITE_NEWS_API_KEY`是否正确
- 确认API密钥有效且未超出限制
- 重启开发服务器

### GitHub API限制
- 无token时每小时限制60次请求
- 配置`VITE_GITHUB_TOKEN`提高限制
- 等待限制重置（每小时）

### 网络问题
- 检查网络连接
- 确认防火墙设置
- 尝试使用VPN（如果API被屏蔽）

## 开发说明

### 添加新API
1. 在`API_CONFIG`中添加配置
2. 在`searchAPIs`中实现搜索函数
3. 在`apiStatus`中添加状态跟踪
4. 更新UI显示新API状态

### 错误处理
- 所有API调用都有try-catch包装
- 状态更新反映API健康状况
- 用户友好的错误提示

### 性能优化
- 并行API调用减少等待时间
- 结果缓存避免重复请求
- 合理的请求限制和重试机制
