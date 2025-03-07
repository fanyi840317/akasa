# Shell 组件使用指南

Shell 组件是一个灵活的控制台布局组件，提供了完整的布局骨架，支持各种布局配置。

## 基本用法

```svelte
<script>
  import Shell from "$lib/components/console/layout/shell.svelte";
</script>

<Shell>
  <svelte:fragment slot="child">
    <div>这里是主内容区域</div>
  </svelte:fragment>
</Shell>
```

## 完整示例

```svelte
<script>
  import Shell from "$lib/components/console/layout/shell.svelte";
  
  // 示例标题路径
  const titles = [
    { name: "控制台", path: "/console" },
    { name: "用户管理", path: "/console/users" }
  ];
</script>

<Shell
  {titles}
  showLeftSidebar={true}
  showRightSidebar={true}
  leftSidebarMode="icon"
  rightSidebarMode="offcanvas"
  contentClass="bg-gray-50 p-4"
  showHeader={true}
  showFooter={true}
>
  <!-- 主内容区域 -->
  <svelte:fragment slot="child">
    <div class="bg-white p-4 rounded-lg shadow">
      <h1 class="text-2xl font-bold">用户管理</h1>
      <p>这里是主要内容...</p>
    </div>
  </svelte:fragment>

  <!-- 左侧内容区域 -->
  <svelte:fragment slot="leftView">
    <div class="p-4">
      <h2 class="text-lg font-semibold mb-4">过滤器</h2>
      <div class="space-y-4">
        <!-- 过滤器内容 -->
        <div>过滤选项1</div>
        <div>过滤选项2</div>
      </div>
    </div>
  </svelte:fragment>

  <!-- 右侧内容区域 -->
  <svelte:fragment slot="rightView">
    <div class="p-4">
      <h2 class="text-lg font-semibold mb-4">详情</h2>
      <div>
        <!-- 详情内容 -->
        <p>这里显示选定项目的详情</p>
      </div>
    </div>
  </svelte:fragment>

  <!-- 操作区域 -->
  <svelte:fragment slot="actions">
    <button class="btn btn-primary">新增</button>
    <button class="btn btn-secondary">导出</button>
  </svelte:fragment>

  <!-- 底部区域 -->
  <svelte:fragment slot="footer">
    <div class="p-4 flex justify-between items-center">
      <div>总计: 100 项</div>
      <div>
        <!-- 分页控件 -->
        <button class="btn btn-sm">上一页</button>
        <span class="mx-2">1 / 10</span>
        <button class="btn btn-sm">下一页</button>
      </div>
    </div>
  </svelte:fragment>
</Shell>
```

## 属性说明

| 属性名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| titles | `{ name: string; path: string; }[]` | `[]` | 页面标题数组，用于面包屑导航 |
| showLeftSidebar | `boolean` | `true` | 是否显示左侧导航栏 |
| showRightSidebar | `boolean` | `false` | 是否显示右侧边栏 |
| leftSidebarMode | `'none' \| 'icon' \| 'offcanvas'` | `'icon'` | 左侧边栏模式 |
| rightSidebarMode | `'none' \| 'icon' \| 'offcanvas'` | `'icon'` | 右侧边栏模式 |
| contentClass | `string` | `''` | 主内容区域额外的样式类 |
| showHeader | `boolean` | `true` | 是否显示头部区域 |
| showFooter | `boolean` | `false` | 是否显示底部区域 |

## 插槽

| 插槽名 | 说明 |
|--------|------|
| child | 主内容区域 |
| leftView | 左侧内容区域 |
| rightView | 右侧内容区域 |
| actions | 右上角操作区域 |
| footer | 底部区域 |

## 常见布局模式

### 只有主内容区域

```svelte
<Shell showLeftSidebar={false} showRightSidebar={false}>
  <svelte:fragment slot="child">
    <!-- 内容 -->
  </svelte:fragment>
</Shell>
```

### 带导航栏和主内容

```svelte
<Shell showLeftSidebar={true} showRightSidebar={false}>
  <svelte:fragment slot="child">
    <!-- 内容 -->
  </svelte:fragment>
</Shell>
```

### 三栏布局

```svelte
<Shell 
  showLeftSidebar={true} 
  showRightSidebar={true}
  leftSidebarMode="icon"
  rightSidebarMode="icon"
>
  <svelte:fragment slot="child">
    <!-- 主内容 -->
  </svelte:fragment>
  <svelte:fragment slot="leftView">
    <!-- 左侧内容 -->
  </svelte:fragment>
  <svelte:fragment slot="rightView">
    <!-- 右侧内容 -->
  </svelte:fragment>
</Shell>
```

### 带底部内容

```svelte
<Shell showFooter={true}>
  <svelte:fragment slot="child">
    <!-- 主内容 -->
  </svelte:fragment>
  <svelte:fragment slot="footer">
    <!-- 底部内容，如分页或状态栏 -->
  </svelte:fragment>
</Shell>
``` 