/**
 * Console 组件库导出索引
 * 提供统一的导入路径，使用方式更简洁
 */

// 布局组件
export { default as Shell } from './shell.svelte';
export { default as Header } from './header.svelte';

// 导航组件
export { default as Sidebar } from './sidebar.svelte';
export { default as NavUser } from './nav-user.svelte';
export { default as Nav } from './nav.svelte';

// 元素组件
export { default as SearchBox } from '../../../lib/components/search-box.svelte';

// 事件组件
export { default as EventList } from './event-list.svelte';
export { default as EventCard } from './event-card.svelte';
export { default as CategoryList } from './category-list.svelte';

// Notion 风格组件
export { default as NotionPanel } from './notion-panel.svelte';

// 类型导出
export * from './types';
