<script lang="ts">
  import { onMount } from "svelte";
  import type { Snippet } from "svelte";
  import * as Sidebar from "$lib/components/ui/sidebar";
  import NavSidebar from "$lib/components/console/navigation/sidebar.svelte";
  import Header from "$lib/components/console/layout/header.svelte";

  /**
   * 控制台主外壳组件 - 提供整体布局骨架
   * @param {Snippet} child - 主内容区域
   * @param {Snippet} leftView - 左侧内容区域
   * @param {Snippet} rightView - 右侧内容区域
   * @param {Snippet} actions - 右上角操作区域
   * @param {Snippet} footer - 底部区域
   * @param {{ name: string; path: string; }[]} titles - 页面标题数组
   * @param {boolean} showLeftSidebar - 是否显示左侧导航栏
   * @param {boolean} showLeftContent - 是否显示左侧内容区域 
   * @param {boolean} showRightSidebar - 是否显示右侧边栏
   * @param {'none' | 'icon' | 'offcanvas'} leftSidebarMode - 左侧导航栏模式
   * @param {'none' | 'icon' | 'offcanvas'} rightSidebarMode - 右侧边栏模式
   * @param {'none' | 'icon' | 'offcanvas'} leftContentMode - 左侧内容区域的模式
   * @param {string} contentClass - 主内容区域额外的样式类
   * @param {boolean} showHeader - 是否显示头部区域
   * @param {boolean} showFooter - 是否显示底部区域
   */
  let { 
    child, 
    titles = [] as { name: string; path: string; }[],
    actions = undefined,
    leftView = undefined,
    rightView = undefined,
    footer = undefined,
    showLeftSidebar = true,
    showLeftContent = true,
    showRightSidebar = false,
    leftSidebarMode = "icon",
    rightSidebarMode = "icon",
    leftContentMode = "icon",
    contentClass = "",
    showHeader = true,
    showFooter = false,
  } = $props<{
    child: Snippet;
    titles?: { name: string; path: string; }[];
    actions?: Snippet;
    leftView?: Snippet;
    rightView?: Snippet;
    footer?: Snippet;
    showLeftSidebar?: boolean;
    showLeftContent?: boolean;
    showRightSidebar?: boolean;
    leftSidebarMode?: 'none' | 'icon' | 'offcanvas';
    rightSidebarMode?: 'none' | 'icon' | 'offcanvas';
    leftContentMode?: 'none' | 'icon' | 'offcanvas';
    contentClass?: string;
    showHeader?: boolean;
    showFooter?: boolean;
  }>();

  onMount(() => {
    // 组件挂载完成后的初始化逻辑
  });
</script>

<Sidebar.Provider open={showLeftContent}>
  <!-- 导航栏 - NavSidebar 不需要我们管理 -->
  <NavSidebar collapsible="icon" />
  
  <!-- 左侧内容区域 -->
  {#if leftView}
    <Sidebar.Root collapsible={leftContentMode}>
      {@render leftView()}
    </Sidebar.Root>
  {/if}
  
  <!-- 主内容区域 -->
  <Sidebar.Inset>
    {#if showHeader}
      <Header {titles} {actions} />
    {/if}
    
    {@render child()}
    
    {#if showFooter && footer}
      <footer class="border-t mt-auto">
        {@render footer()}
      </footer>
    {/if}
  </Sidebar.Inset>
  
  <!-- 右侧内容区域 -->
  {#if rightView}
    <Sidebar.Root 
      collapsible={showRightSidebar ? rightSidebarMode : "none"} 
      side="right"
    >
      {@render rightView()}
    </Sidebar.Root>
  {/if}
</Sidebar.Provider>

<style>

</style>
