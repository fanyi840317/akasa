# Akasa - 神秘事件记录平台

Akasa 是一个现代化的神秘事件记录平台，让用户能够以优雅的方式记录和分享他们的神秘经历。

## 项目结构

```
akasa/
├── web.app/                          # 前端应用
│   ├── src/                          # 源代码目录
│   │   ├── lib/                      # 共享库和组件
│   │   │   ├── components/          # UI 组件
│   │   │   │   ├── ui/             # 基础 UI 组件
│   │   │   │   ├── events/         # 事件相关组件
│   │   │   │   ├── map/            # 地图相关组件
│   │   │   │   └── editor/         # 编辑器相关组件
│   │   │   ├── stores/             # 状态管理
│   │   │   │   ├── auth.store.ts   # 认证状态
│   │   │   │   ├── event.store.ts  # 事件状态
│   │   │   │   └── ui.store.ts     # UI 状态
│   │   │   ├── types/              # TypeScript 类型定义
│   │   │   │   ├── event.types.ts  # 事件相关类型
│   │   │   │   ├── user.types.ts   # 用户相关类型
│   │   │   │   └── map.types.ts    # 地图相关类型
│   │   │   ├── utils/              # 工具函数
│   │   │   │   ├── date.ts         # 日期处理
│   │   │   │   ├── format.ts       # 格式化工具
│   │   │   │   └── validation.ts   # 验证工具
│   │   │   └── i18n/               # 国际化
│   │   │       ├── locales/        # 翻译文件
│   │   │       └── index.ts        # 国际化配置
│   │   ├── routes/                 # 页面路由
│   │   │   ├── (auth)/            # 认证相关页面
│   │   │   ├── (main)/            # 主要页面
│   │   │   └── +layout.svelte     # 根布局
│   │   ├── app.css                 # 全局样式
│   │   └── app.d.ts                # 全局类型声明
│   ├── static/                     # 静态资源
│   │   ├── images/                 # 图片资源
│   │   ├── fonts/                  # 字体文件
│   │   └── icons/                  # 图标资源
│   ├── tests/                      # 测试文件
│   │   ├── unit/                   # 单元测试
│   │   └── integration/            # 集成测试
│   ├── tailwind.config.ts          # Tailwind 配置
│   ├── svelte.config.js            # Svelte 配置
│   ├── vite.config.ts              # Vite 配置
│   └── package.json                # 项目依赖
├── db/                             # 数据库相关
│   ├── migrations/                 # 数据库迁移
│   ├── seeds/                      # 数据库种子
│   └── schema/                     # 数据库模式
└── package.json                    # 根项目依赖
```

### 目录说明

#### web.app/
前端应用主目录，包含所有前端相关代码和配置。

- **src/**: 源代码目录
  - **lib/**: 共享库和组件
    - **components/**: UI 组件目录
      - **ui/**: 基础 UI 组件，如按钮、输入框等
      - **events/**: 事件相关组件，如事件卡片、事件表单等
      - **map/**: 地图相关组件，如地图选择器、位置标记等
      - **editor/**: 编辑器相关组件，如富文本编辑器等
    - **stores/**: 状态管理目录
      - **auth.store.ts**: 用户认证状态管理
      - **event.store.ts**: 事件数据状态管理
      - **ui.store.ts**: UI 状态管理
    - **types/**: TypeScript 类型定义目录
      - **event.types.ts**: 事件相关类型定义
      - **user.types.ts**: 用户相关类型定义
      - **map.types.ts**: 地图相关类型定义
    - **utils/**: 工具函数目录
      - **date.ts**: 日期处理工具
      - **format.ts**: 数据格式化工具
      - **validation.ts**: 数据验证工具
    - **i18n/**: 国际化目录
      - **locales/**: 多语言翻译文件
      - **index.ts**: 国际化配置
  - **routes/**: 页面路由目录
    - **(auth)/**: 认证相关页面
    - **(main)/**: 主要功能页面
    - **+layout.svelte**: 根布局组件
  - **app.css**: 全局样式文件
  - **app.d.ts**: 全局类型声明文件

- **static/**: 静态资源目录
  - **images/**: 图片资源
  - **fonts/**: 字体文件
  - **icons/**: 图标资源

- **tests/**: 测试文件目录
  - **unit/**: 单元测试
  - **integration/**: 集成测试

#### db/
数据库相关目录，包含数据库迁移、种子数据和模式定义。

- **migrations/**: 数据库迁移文件
- **seeds/**: 数据库种子数据
- **schema/**: 数据库模式定义

## 技术栈

### 核心框架
- **前端框架**: SvelteKit 2.0
- **样式框架**: Tailwind CSS 3.4
- **UI 组件**: shadcn-svelte
- **编辑器**: Affine Editor (基于 BlockSuite)
- **状态管理**: Svelte Stores
- **类型系统**: TypeScript 5.0
- **国际化**: svelte-i18n 4.0

### 地图相关
- **地图引擎**: Cesium.js
- **地图服务**: Mapbox GL
- **地图组件**: Leaflet

### 开发工具
- **构建工具**: Vite
- **包管理器**: pnpm
- **代码检查**: svelte-check
- **动画库**: tailwindcss-animate
- **UI 组件库**: bits-ui, vaul-svelte
- **图标库**: Lucide Icons

### 后端服务
- **BaaS**: Appwrite 14.0
- **分析**: Vercel Analytics

## 开发规范

### 代码规范

1. **文件组织**
   - 组件文件放在 `src/lib/components` 目录下
   - 页面文件放在 `src/routes` 目录下
   - 类型定义放在 `src/lib/types` 目录下
   - Store 文件放在 `src/lib/stores` 目录下

2. **命名规范**
   - 文件命名:
     - 组件文件: `re-component-name.svelte` (例如: `re-event-card.svelte`)
     - 工具文件: `re-utils-name.ts` (例如: `re-format-date.ts`)
     - 类型文件: `re-types-name.ts` (例如: `re-event-types.ts`)
     - Store 文件: `re-store-name.ts` (例如: `re-user-store.ts`)
     - 测试文件: `re-test-name.test.ts` (例如: `re-event-card.test.ts`)
     - 样式文件: `re-style-name.css` (例如: `re-event-card.css`)
     - 布局文件: `+layout.svelte` (SvelteKit 约定)
     - 页面文件: `+page.svelte` (SvelteKit 约定)
     - 加载文件: `+loading.svelte` (SvelteKit 约定)
     - 错误文件: `+error.svelte` (SvelteKit 约定)

   - 变量命名：
     - 组件变量：`PascalCase` (如 `EventCard`, `UserProfile`)
     - 普通变量：`camelCase` (如 `userName`, `eventDate`)
     - 常量：`UPPER_SNAKE_CASE` (如 `MAX_EVENTS`, `API_ENDPOINT`)
     - 类型和接口：`PascalCase` (如 `User`, `EventData`)
     - 枚举：`PascalCase` (如 `EventStatus`, `UserRole`)
     - 布尔变量：使用 `is`, `has`, `should` 等前缀 (如 `isLoading`, `hasError`)
     - 事件处理函数：使用 `handle` 前缀 (如 `handleClick`, `handleSubmit`)
     - 异步函数：使用 `fetch`, `load`, `save` 等动词 (如 `fetchUserData`, `saveEvent`)
     - Store 变量：使用 `Store` 后缀 (如 `userStore`, `eventStore`)
     - 派生状态：使用 `$` 前缀 (如 `$user`, `$event`)

   - 目录命名：
     - 组件目录：`PascalCase` (如 `EventCard/`)
     - 功能目录：`camelCase` (如 `userProfile/`)
     - 工具目录：`camelCase` (如 `utils/`)
     - 类型目录：`types/`
     - 测试目录：`__tests__/`
     - 样式目录：`styles/`
     - 资源目录：`assets/`

   - 导入命名：
     ```typescript
     // 组件导入
     import EventCard from '$lib/components/EventCard.svelte';
     
     // 类型导入
     import type { Event, User } from '$lib/types';
     
     // Store 导入
     import { userStore } from '$lib/stores/user.store';
     
     // 工具函数导入
     import { formatDate } from '$lib/utils/date';
     ```

   - CSS 类命名：
     - 使用 Tailwind 类名
     - 自定义类名使用 `camelCase`
     - 组件特定类名使用 `component-name-class` 格式
     - 状态类名使用 `is-` 前缀 (如 `is-active`, `is-disabled`)
     - 主题类名使用 `theme-` 前缀 (如 `theme-dark`, `theme-light`)

### 组件开发规范

1. **组件设计原则**
   - 单一职责
   - 可复用性
   - 可测试性
   - 可维护性

2. **组件文档**
   ```svelte
   <!-- EventCard.svelte -->
   <script lang="ts">
     /**
      * @component EventCard
      * @description 事件卡片组件，用于展示事件的基本信息
      * 
      * @prop {string} title - 事件标题
      * @prop {string} description - 事件描述
      * @prop {Date} date - 事件日期
      * @prop {string} location - 事件地点
      * 
      * @event {CustomEvent} click - 点击事件
      */
     
     interface Props {
       title: string;
       description?: string;
       date: Date;
       location: string;
     }
     
     let { title, description, date, location }: Props = $props();
   </script>
   ```

3. **组件测试**
   ```typescript
   // EventCard.test.ts
   import { render, screen } from '@testing-library/svelte';
   import EventCard from './EventCard.svelte';
   
   describe('EventCard', () => {
     it('renders event title', () => {
       render(EventCard, {
         props: {
           title: 'Test Event',
           date: new Date(),
           location: 'Test Location'
         }
       });
       
       expect(screen.getByText('Test Event')).toBeInTheDocument();
     });
   });
   ```

### 性能优化规范

1. **组件优化**
   - 使用 `$:reactive` 声明
   - 避免不必要的计算
   - 使用 `svelte:component` 动态加载
   - 合理使用 `bind:this`

2. **状态管理优化**
   - 避免过度使用全局状态
   - 使用派生状态
   - 合理使用订阅

3. **资源优化**
   - 图片懒加载
   - 组件懒加载
   - 合理使用缓存

## 开发流程

1. **环境设置**
   ```bash
   # 安装依赖
   pnpm install

   # 启动开发服务器
   pnpm dev

   # 构建生产版本
   pnpm build

   # 代码检查
   pnpm check
   ```

2. **开发流程**
   ```bash
   # 1. 创建功能分支
   git checkout -b feature/new-feature

   # 2. 开发功能
   # 3. 提交代码
   git add .
   git commit -m "feat: add new feature"

   # 4. 推送到远程
   git push origin feature/new-feature

   # 5. 创建 Pull Request
   ```

3. **代码审查**
   - 遵循代码规范
   - 确保测试通过
   - 检查性能影响
   - 更新文档

## 部署指南

1. **环境要求**
   - Node.js 18+
   - pnpm 8+
   - Appwrite 14.0+

2. **部署步骤**
   ```bash
   # 1. 安装依赖
   pnpm install

   # 2. 构建项目
   pnpm build

   # 3. 预览构建结果
   pnpm preview
   ```

3. **环境变量配置**
   - 创建 `.env` 文件
   - 配置必要的环境变量：
     ```
     PUBLIC_APPWRITE_ENDPOINT=
     PUBLIC_APPWRITE_PROJECT_ID=
     PUBLIC_MAPBOX_TOKEN=
     ```

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

### 错误处理规范

1. **错误类型**
   ```typescript
   // 自定义错误类
   class AppError extends Error {
     constructor(
       message: string,
       public code: string,
       public status: number = 500
     ) {
       super(message);
       this.name = 'AppError';
     }
   }

   // 错误类型定义
   type ErrorType = 
     | 'VALIDATION_ERROR'
     | 'AUTH_ERROR'
     | 'NETWORK_ERROR'
     | 'SERVER_ERROR';
   ```

2. **错误处理**
   ```typescript
   try {
     // 业务逻辑
   } catch (error) {
     if (error instanceof AppError) {
       // 处理应用错误
       toast.error(error.message);
     } else {
       // 处理未知错误
       console.error('Unexpected error:', error);
       toast.error('发生未知错误，请重试');
     }
   }
   ```

3. **错误边界**
   ```svelte
   <ErrorBoundary>
     <slot />
   </ErrorBoundary>
   ```

### 国际化规范

1. **翻译文件组织**
   ```
   src/
   ├── lib/
   │   └── i18n/
   │       ├── locales/
   │       │   ├── en.json
   │       │   └── zh.json
   │       └── index.ts
   ```

2. **翻译键命名**
   ```json
   {
     "common": {
       "buttons": {
         "submit": "提交",
         "cancel": "取消"
       },
       "errors": {
         "required": "此项为必填",
         "invalid": "输入无效"
       }
     },
     "events": {
       "create": {
         "title": "创建事件",
         "form": {
           "name": "事件名称",
           "date": "事件日期"
         }
       }
     }
   }
   ```

3. **使用示例**
   ```svelte
   <script>
     import { _ } from 'svelte-i18n';
   </script>

   <h1>{$_('events.create.title')}</h1>
   <label>{$_('events.create.form.name')}</label>
   ```

### 测试规范

1. **测试文件组织**
   ```
   src/
   ├── lib/
   │   └── components/
   │       └── EventCard/
   │           ├── EventCard.svelte
   │           ├── EventCard.test.ts
   │           └── EventCard.stories.ts
   ```

2. **测试命名**
   ```typescript
   describe('EventCard', () => {
     it('should render event title correctly', () => {
       // 测试代码
     });

     it('should handle click event', () => {
       // 测试代码
     });

     it('should display error state', () => {
       // 测试代码
     });
   });
   ```

3. **测试覆盖率要求**
   - 组件测试覆盖率 > 80%
   - 工具函数测试覆盖率 > 90%
   - Store 测试覆盖率 > 85%
