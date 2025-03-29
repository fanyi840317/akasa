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
  import type { NavItem } from "$lib/types/types";
  import * as Dialog from "$lib/components/ui/dialog";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import { Separator } from "$lib/components/ui/separator";
  import { appStore } from "$lib/stores/appState";
  import type { User } from "$lib/types/user";
  import { setContext } from "svelte";
  import { NotionPanel } from "$lib/components/layout";
  import PanelContent from "./panel-content.svelte";

  interface NavSidebarEvents {
    navItemClick: CustomEvent<NavItem>;
  }

  interface HeaderProps {
    titles?: { name: string; path: string }[];
    actions?: Snippet;
  }

  /**
   * 控制台主外壳组件 - 提供整体布局骨架
   * @param {Snippet} child - 主内容区域
   * @param {Snippet} leftView - 左侧内容区域
   @param {Snippet} rightView - 右侧内容区域
   * @param {Snippet} actions - 右上角操作区域
   * @param {Snippet} footer - 底部区域
   * @param {{ name: string; path: string; }[]} titles - 页面标题数组
   * @param {boolean} showLeftView - 是否显示左侧内容区域
   * @param {boolean} showRightView - 是否显示右侧内容区域
   * @param {boolean} showHeader - 是否显示头部区域
   * @param {boolean} showFooter - 是否显示底部区域
   * @param {(item: NavItem | null) => void} onLeftViewChange - 左侧视图变更回调
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
    showLeftView?: boolean;
    showRightView?: boolean;
    showHeader?: boolean;
    showFooter?: boolean;
    onLeftViewChange?: (item: NavItem | null) => void;
    user?: User;
  }>();

  /**
   * 使用appStore统一管理状态
   * 避免状态管理混乱和重复定义
   */
  let sidebarCollapsed = $state(false);
  let sidebarWidthIcon = $state(56); // 默认值
  let sidebarWidth = $state(256); // 默认值
  let selectedItem = $state<string | null>(null);
  let showDialog = $state(false);
  let dialogItem = $state<NavItem | null>(null);
  
  // 订阅appStore以获取最新状态，统一状态来源
  appStore.subscribe(state => {
    sidebarCollapsed = state.sidebarCollapsed;
    sidebarWidthIcon = state.sidebarWidthIcon;
    sidebarWidth = state.sidebarWidth;
    showDialog = state.showDialog;
    dialogItem = state.dialogItem;
    showLeftView = state.showLeftView;
    showRightView = state.showRightView;
  });

  // 事件面板状态
  let showEventPanel = false;
  let selectedEvent: any = null;

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

  // 处理事件点击
  function handleEventClick(event: any) {
    selectedEvent = event;
    showEventPanel = true;
  }

  // 处理面板关闭
  function handlePanelClose() {
    showEventPanel = false;
    selectedEvent = null;
  }

  // 设置上下文，让子组件可以访问这些函数
  setContext('shell', {
    openEvent: handleEventClick,
    closeEvent: handlePanelClose
  });

  onMount(() => {
  });
</script>

<!-- 左侧内容区域 -->
{#if leftView && showLeftView}
  <div class="absolute z-10 h-full w-full">
    <div class="fixed inset-0 bg-card/20 backdrop-blur-sm"  
    transition:fade={{ duration: 200 }}
    on:click={() => appStore.setShowLeftView(false)}
    on:keydown={(e) => e.key === 'Escape' && appStore.setShowLeftView(false)}
    role="button"
    tabindex="0"></div>
    <div
      class="bg-muted backdrop-blur-sm h-full absolute transition-[width,transform] duration-300 ease-in-out border-r shadow-lg overflow-hidden"
      style="left: {sidebarCollapsed ? sidebarWidthIcon : sidebarWidth}px; width: 400px;"
      in:fly|local={{ x: -sidebarWidth, duration: 200 }}
      out:fly|local={{ x: -sidebarWidth, duration: 200 }}
    >
      {@render leftView()}
    </div>
  </div>
 
{/if}

<!-- Dialog组件 -->


<Sidebar.Provider open={showRightView} style="--sidebar-width: {400}px">
  <Sidebar.Provider open={sidebarCollapsed} style="--sidebar-width: {sidebarWidth}px">
    <NavSidebar 
      collapsible="icon" 
      selectedItem={$page.url.pathname}
      on:navItemClick={e => handleNavAction(e.detail)}
      user={user}
    />

    <!-- 主内容区域 -->
    <Sidebar.Inset>
      {#if showHeader}
        <Header titles={titles} actions={actions} />
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

  <Sidebar.Root side="right" class="z-10">
    {#if rightView && showRightView}
    {@render rightView()}
    {/if}
  </Sidebar.Root>
</Sidebar.Provider>

<!-- 事件详情面板 -->
<NotionPanel 
    open={showEventPanel}
    title={selectedEvent?.title || '事件详情'}
    width={40}
    maxWidth={60}
    showHeader={true}
    showFooter={false}
    component={PanelContent}
    componentProps={{
        title: selectedEvent?.title || '',
        time: selectedEvent?.time || '',
        status: selectedEvent?.status || '',
        content: selectedEvent?.content || ''
    }}
    properties={[
        { label: "标题", value: selectedEvent?.title || '' },
        { label: "时间", value: selectedEvent?.time || '' },
        { label: "状态", value: selectedEvent?.status || '' }
    ]}
    on:close={handlePanelClose}
/>