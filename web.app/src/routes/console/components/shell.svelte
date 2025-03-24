<script lang="ts">
  import { onMount } from "svelte";
  import type { Snippet } from "svelte";
  import * as Sidebar from "$lib/components/ui/sidebar";
  import NavSidebar from "./sidebar.svelte";
  import Header from "./header.svelte";
  import { fly, slide, fade } from "svelte/transition";
  import { Collapsible } from "bits-ui";
  import * as Resizable from "$lib/components/ui/resizable";
  import { page } from "$app/stores";
  import type { NavItem, User } from "./types";
  import * as Dialog from "$lib/components/ui/dialog";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import { Separator } from "$lib/components/ui/separator";
  import { appStore,sidebarStore } from "$lib/stores/appState";
  

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
   * @param {Snippet} dialogView - 对话框内容区域
   * @param {User} user - 用户信息
   */
  let {
    child,
    titles = [] as { name: string; path: string }[],
    actions = undefined,
    leftView = undefined,
    rightView = undefined,
    footer = undefined,
    dialogView = undefined,
    showLeftView = false,
    showRightView = false,
    showHeader = true,
    showFooter = false,
    onLeftViewChange = (item: NavItem | null) => {},
    user = undefined,
  } = $props<{
    child: Snippet;
    titles?: { name: string; path: string }[];
    actions?: Snippet;
    leftView?: Snippet;
    rightView?: Snippet;
    footer?: Snippet;
    dialogView?: Snippet;
    showLeftView?: boolean;
    showRightView?: boolean;
    showHeader?: boolean;
    showFooter?: boolean;
    onLeftViewChange?: (item: NavItem | null) => void;
    user?: User;
  }>();

  // 使用appStore中的状态
  let sidebarCollapsed = $state(appStore.get().sidebarCollapsed);
  let sidebarWidthIcon = appStore.get().sidebarWidthIcon;
  let sidebarWidth = appStore.get().sidebarWidth;
  let selectedItem = $state<string | null>(appStore.get().selectedItem);
  let showDialog = $state(appStore.get().showDialog);
  let dialogItem = $state<NavItem | null>(appStore.get().dialogItem);
  
  // 订阅appStore以获取最新状态
  appStore.subscribe(state => {
    sidebarCollapsed = state.sidebarCollapsed;
    selectedItem = state.selectedItem;
    showDialog = state.showDialog;
    dialogItem = state.dialogItem;
  });

  $effect(() => {
    const currentPath = $page.url.pathname;
    if (currentPath) {
      appStore.setSelectedItem(currentPath);
    }
  });

  function handleNavAction(item: NavItem | null, action?: string) {
    console.log('Nav action:', item, action);
    
    // 处理左侧视图变更
    if (!action || action === 'leftView') {
      appStore.toggleLeftView();
      onLeftViewChange(item);
    }
    
    // 处理模态框显示
    if (item && item.onClickAction === 'modal') {
      appStore.setShowDialog(true, item);
    }
  }

  onMount(() => {
  });
</script>

<!-- 左侧内容区域 -->
{#if leftView && showLeftView}
  <div class="absolute z-10 h-full w-full">
    <div class="fixed inset-0 bg-card/20 backdrop-blur-sm"  
    transition:fade={{ duration: 200 }}
    onclick={() => appStore.setShowLeftView(false)}
    onkeydown={(e) => e.key === 'Escape' && appStore.setShowLeftView(false)}
    role="button"
    tabindex="0"></div>
    <div
      class="bg-muted backdrop-blur-sm h-full absolute transition-[width,transform] duration-300 ease-in-out border-r shadow-lg overflow-hidden"
      style="left: {sidebarCollapsed ? sidebarWidth : sidebarWidth}px; width: 400px;"
      in:fly|local={{ x: -sidebarWidth, duration: 200 }}
      out:fly|local={{ x: -sidebarWidth, duration: 200 }}
    >
      {@render leftView()}
    </div>
  </div>
 
{/if}

<!-- Dialog组件 -->
{#if showDialog && dialogView}
  <Dialog.Root bind:open={showDialog} on:openChange={(e) => appStore.setShowDialog(e.detail)}>
    {@render dialogView()}
  </Dialog.Root>
{/if}

<Sidebar.Provider open={showRightView} style="--sidebar-width: {400}px">
  <Sidebar.Provider open={sidebarCollapsed} style="--sidebar-width: {sidebarWidth}px">
    <NavSidebar 
      collapsible="icon" 
      selectedItem={$page.url.pathname}
      onNavItemClick={(item) => handleNavAction(item)}
      user={user}
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

  <Sidebar.Root side="right" class="z-9">
    {#if rightView && showRightView}
    {@render rightView()}
    {/if}
  </Sidebar.Root>
</Sidebar.Provider>
<!-- -->