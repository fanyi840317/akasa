# 控制台元素组件

该目录包含控制台界面中使用的常见UI元素，这些组件都遵循Notion简洁、现代的设计风格，使用Inter字体和简约交互效果。

## 组件列表

### SearchBox

一个Notion风格的搜索框组件，提供标准的搜索界面和位置搜索功能。

**特性：**
- 简洁的搜索图标
- 可选的位置搜索按钮
- 符合Notion设计规范的输入样式
- 事件分发：`search` 和 `locationSearch`

**用法示例：**
```svelte
<SearchBox 
  placeholder="搜索位置..." 
  bind:value={searchQuery} 
  on:search={handleSearch}
  on:locationSearch={handleLocationSearch}
/>
```

### NotionCard

符合Notion风格的卡片容器组件，提供一致的卡片布局和样式。

**特性：**
- 可选的毛玻璃背景效果
- 标题和副标题区域
- 自定义页脚插槽
- 支持透明背景选项
- 符合Notion设计规范的间距和字体样式

**用法示例：**
```svelte
<NotionCard 
  title="最新活动" 
  subtitle="查看周边最新发生的事件"
  withBlur={true}
>
  <!-- 卡片内容 -->
  <EventList />
  
  <!-- 卡片页脚 -->
  <svelte:fragment slot="footer">
    <Button>查看全部</Button>
  </svelte:fragment>
</NotionCard>
```

## 设计规范

所有元素组件遵循以下设计规范：

1. **字体**: 使用Inter字体，权重范围300-700
2. **交互**: 微妙且平滑的过渡动画，通常为200ms左右
3. **颜色**: 使用低饱和度的中性色调，强调内容而非界面
4. **阴影**: 轻微且柔和的阴影效果，增强层次感
5. **间距**: 一致且有节奏的内边距和外边距
6. **圆角**: 轻微的圆角，通常为4-6px

这些组件旨在提供一致的用户体验，便于构建复杂的控制台界面。
