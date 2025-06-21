# Akasa Backend API

神秘事件研究系统的后端API服务，提供配置管理和系统控制接口。

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥
```

### 3. 启动API服务器

```bash
python run_api.py
```

服务器将在 `http://localhost:8000` 启动。

## API 端点

### 健康检查

```http
GET /api/health
```

返回服务器状态信息。

### 配置管理

#### 获取所有配置

```http
GET /api/config/
```

返回系统、组件和LLM的所有配置信息。

#### 获取系统配置

```http
GET /api/config/system
```

返回系统基本配置信息。

#### 获取组件配置

```http
GET /api/config/components
```

返回组件配置信息。

#### 获取LLM配置

```http
GET /api/config/llm
```

返回AI模型配置信息。

#### 获取原始配置

```http
GET /api/config/raw
```

返回原始YAML配置文件内容，包括默认配置、用户配置和合并后的配置。

#### 更新配置

```http
POST /api/config/update
Content-Type: application/json

{
  "system": {
    "debug": true,
    "verbose": true
  },
  "ai": {
    "openai": {
      "api_key": "your-new-api-key"
    }
  }
}
```

更新配置信息。只需要提供要更改的字段，其他字段保持不变。

#### 重置配置

```http
POST /api/config/reset
```

重置配置到默认值。

#### 验证配置

```http
POST /api/config/validate
Content-Type: application/json

{
  "system": {
    "name": "Test System"
  }
}
```

验证提供的配置是否有效。如果不提供请求体，则验证当前配置。

#### 获取配置模式

```http
GET /api/config/schema
```

返回配置的JSON Schema，用于前端表单验证。

## 响应格式

### 成功响应

```json
{
  "success": true,
  "data": {
    // 响应数据
  }
}
```

### 错误响应

```json
{
  "success": false,
  "error": "错误信息",
  "status_code": 400
}
```

## 配置文件结构

系统使用两个配置文件：

- `src/config/default.yaml` - 默认配置（不应修改）
- `src/config/user.yaml` - 用户自定义配置（通过API创建和修改）

用户配置会覆盖默认配置中的相应字段。

## 开发

### 添加新的API端点

1. 在 `api/routes/` 目录下创建新的路由文件
2. 在 `api/routes/__init__.py` 中导入新的蓝图
3. 在 `api/app.py` 中注册新的蓝图

### 错误处理

所有API端点都应该使用统一的错误处理格式。错误处理器在 `api/middleware.py` 中定义。

### 日志记录

使用Flask的内置日志记录功能。日志配置在 `api/middleware.py` 中设置。

## 部署

### 生产环境

建议使用WSGI服务器（如Gunicorn）来部署：

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "api.app:create_app()"
```

### Docker部署

可以创建Dockerfile来容器化部署：

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "run_api.py"]
```

## 安全注意事项

1. 在生产环境中设置 `API_DEBUG=false`
2. 使用强密码作为 `SECRET_KEY`
3. 限制CORS允许的源
4. 考虑添加API认证和授权
5. 定期更新依赖包

## 故障排除

### 常见问题

1. **端口被占用**：修改 `.env` 文件中的 `API_PORT`
2. **配置验证失败**：检查配置文件格式和必需字段
3. **API密钥错误**：确认 `.env` 文件中的API密钥正确

### 日志查看

开发模式下，日志会输出到控制台。生产环境建议配置日志文件。