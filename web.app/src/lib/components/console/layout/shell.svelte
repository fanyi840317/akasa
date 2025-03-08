<script lang="ts">
  import { onMount } from "svelte";
  import type { Snippet } from "svelte";
  import * as Sidebar from "$lib/components/ui/sidebar";
  import NavSidebar from "$lib/components/console/navigation/sidebar.svelte";
  import Header from "$lib/components/console/layout/header.svelte";
  import { fly, slide, fade } from "svelte/transition";
    import { Collapsible } from "bits-ui";

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
   * @param {'floating' | 'inset'} leftViewMode - 左侧内容区域的显示模式：浮动或嵌入
   * @param {string} contentClass - 主内容区域额外的样式类
   * @param {boolean} showHeader - 是否显示头部区域
   * @param {boolean} showFooter - 是否显示底部区域
   */
  let {
    child,
    titles = [] as { name: string; path: string }[],
    actions = undefined,
    leftView = undefined,
    rightView = undefined,
    footer = undefined,
    showLeftView = true,
    showRightView = false,
    showHeader = true,
    showFooter = false,
  } = $props<{
    child: Snippet;
    titles?: { name: string; path: string }[];
    actions?: Snippet;
    leftView?: Snippet;
    rightView?: Snippet;
    footer?: Snippet;
    showLeftView?: boolean;
    showRightView?: boolean;
    showHeader?: boolean;
    showFooter?: boolean;
  }>();

  let sidebarCollapsed = $state(true);
  let sidebarWidthIcon = 56;
  let sidebarWidth = 256;

  
  // 监听sidebarCollapsed变化
  $effect(() => {
    if (sidebarCollapsed !== undefined) {
      // alert(`侧边栏状态已变更为: ${sidebarCollapsed ? '折叠' : '展开'}`);
    }
  });
  
	import { useSidebar } from "$lib/components/ui/sidebar/index.js";

	onMount(()=>{
		alert(useSidebar().state);
	})
</script>
  <!-- 左侧内容区域 -->
  {#if leftView && showLeftView}
  <div
    class="bg-muted backdrop-blur-sm h-full absolute z-10 transition-[width,transform] duration-300 ease-in-out border-r shadow-lg overflow-hidden"
    style="left: {sidebarCollapsed ? sidebarWidth : sidebarWidthIcon}px; width: 400px;"
    in:fly|local={{ x: -sidebarWidth, duration: 200 }}
    out:fly|local={{ x: -sidebarWidth, duration: 200 }}
  >
    {@render leftView()}
  </div>
{/if}

<Sidebar.Provider open={showRightView} style="--sidebar-width: {400}px">
  <Sidebar.Provider open={sidebarCollapsed}>
  
    <NavSidebar 
      collapsible="icon" 
      class=""
    />

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
  </Sidebar.Provider>

  <!-- 右侧内容区域 -->
  <Sidebar.Root side="right">
    {#if rightView && showRightView}
      {@render rightView()}
    {/if}
  </Sidebar.Root>
</Sidebar.Provider>
