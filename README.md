# akasa

## 项目概述
基于SvelteKit和Appwrite后端构建的现代Web应用，提供高效的数据管理能力。

## 技术栈
- **前端**: SvelteKit + Tailwind CSS
- **后端**: Appwrite BaaS
- **数据库**: Appwrite Database（JSON格式）

## 快速开始
```bash
# 安装依赖
pnpm install

# 初始化数据库（需要Appwrite终端和API密钥）
node db/setup_database.js

# 启动开发服务器
cd web.app && pnpm run dev
```

## 项目结构
`web.app/` 包含：
- `src/routes/` - 页面组件
- `src/lib/` - 公共工具
- `static/` - CSS/字体资源

## 贡献指南
1. Fork本仓库
2. 创建功能分支
3. 提交PR并描述变更
