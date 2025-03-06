/**
 * Console 组件库导出索引
 * 提供统一的导入路径，使用方式更简洁
 */

// 布局组件
export { default as Shell } from './layout/shell.svelte';
export { default as Header } from './layout/header.svelte';
export { default as PageContainer } from './layout/page-container.svelte';
export { default as PageContent } from './layout/page-content.svelte';
export { default as MapView } from './layout/map-view.svelte';

// 导航组件
export { default as Sidebar } from './navigation/sidebar.svelte';
export { default as NavMain } from './navigation/nav-main.svelte';
export { default as NavProjects } from './navigation/nav-projects.svelte';
export { default as NavSecondary } from './navigation/nav-secondary.svelte';
export { default as NavUser } from './navigation/nav-user.svelte';

// 元素组件
export { default as SearchBox } from './elements/search-box.svelte';
export { default as NotionCard } from './elements/notion-card.svelte';


// 类型导出
export * from './types';
