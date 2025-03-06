# Console 组件库

该目录包含应用控制台界面的核心组件，遵循Notion简洁、现代的设计风格，并基于组件化和关注点分离原则进行组织。

## 目录结构

```
console/
├── index.ts                   # 统一导出入口
├── types.ts                   # 组件类型定义
│
├── layout/                    # 布局相关组件
│   ├── shell.svelte           # 控制台主外壳
│   ├── header.svelte          # 页面头部组件
│   ├── page-container.svelte  # 页面容器
│   ├── page-content.svelte    # 页面内容区
│   └── map-view.svelte        # 地图视图容器
│
├── navigation/                # 导航相关组件
│   ├── sidebar.svelte         # 侧边栏容器
│   ├── nav-main.svelte        # 主导航菜单
│   ├── nav-projects.svelte    # 项目导航
│   ├── nav-secondary.svelte   # 次要导航
│   └── nav-user.svelte        # 用户信息
│
├── elements/                  # UI元素组件
│   ├── search-box.svelte      # 搜索框组件
│   └── notion-card.svelte     # Notion风格卡片
│
└── styles/                    # 样式资源
    ├── index.ts               # 样式工具导出
    ├── notion-typography.css  # 文本排版样式
    └── notion-animations.css  # 动画效果
```

## 设计原则

- **组件化**：每个组件都有明确的职责和边界
- **一致性**：整体遵循Notion的UI设计语言
- **可扩展性**：组件设计易于扩展和重用
- **Inter字体**：使用Notion的标准字体
- **最小化组件层级**：优化渲染性能

## 使用方式

### 基础组件导入

通过索引文件统一导入，简化导入路径：

```svelte
import { Shell, Header, PageContent } from "$lib/components/console";
```

### 布局结构示例

```svelte
<Shell {child} title="Console">
  <!-- 通过child插槽渲染内容 -->
</Shell>

<!-- 在子页面中 -->
<Header title="Event Page" />
<PageContent>
  <!-- 页面内容 -->
</PageContent>
```

### 导航数据配置

导航数据结构定义在 `$lib/data/navigation-data.ts` 中，遵循类型定义：

```typescript
import type { NavItem, Project, User } from "$lib/components/console/types";

// 使用类型安全的数据结构
const navData = {
  navMain: [] as NavItem[],
  // 其他导航项...
};
```

### 样式使用

可以直接使用定义好的样式类，或通过helper函数生成类名：

```svelte
<script>
import { notionClass } from "$lib/components/console/styles";
</script>

<!-- 直接使用类名 -->
<h1 class="notion-h1">标题内容</h1>

<!-- 使用helper函数 -->
<div class={notionClass('container', 'p-4')}>
  <p class={notionClass('text')}>段落内容</p>
</div>
```

## 字体与颜色

- **字体**: Inter (300-400-500-600-700)
- **主色**: 标准Notion文本色 rgb(55, 53, 47)
- **辅助色**: 低饱和度的中性色和功能色
- **过渡**: 简洁的微动效，通常150-200ms

## 兼容性与性能

- 组件设计考虑了移动端和桌面端的不同交互需求
- 优化了样式和渲染性能，避免不必要的重绘
- 尽可能减少DOM嵌套层级，提升性能
