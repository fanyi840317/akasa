<script lang="ts">
  import {
    Users,
    BarChart2,
    Shield,
    MessageSquare,
    Info,
    ListFilter,
    FileText,
    ThumbsUp,
    ThumbsDown,
    MessageCircle,
    FileSearch,
    Compass,
    Plus,
    Map,
    Settings,
    Search,
    Minimize2,
    X,
    Maximize2,
    MapIcon,
  } from "lucide-svelte";
  import { page } from "$app/stores";
  import { auth } from "$lib/stores/auth";
  import { appStore } from "$lib/stores/app-state";
  import { UserAvatar } from "$lib/components/ui/avatar";
  import { BatchAddEvents } from "$lib/components/events";
  import { effects as blocksEffects } from "@blocksuite/blocks/effects";
  import { effects as presetsEffects } from "@blocksuite/presets/effects";
  import NavItem from "$lib/components/ui/nav/nav-item.svelte";
  import CategoryNavItem from "$lib/components/ui/nav/category-nav-item.svelte";
  import DraggableChatDialog from "$lib/components/ai/draggable-chat-dialog.svelte";
  import { LeftSidebar, TopBar } from "$lib/components/console-layout";
  import { goto } from "$app/navigation";

  const categories = [
    {
      name: "Discussion",
      icon: MessageSquare,
      color: "bg-blue-500/20",
      path: "/console/categories/discussion",
    },
    {
      name: "How To",
      icon: FileText,
      color: "bg-orange-500/20",
      path: "/console/categories/how-to",
    },
    {
      name: "Feature Requests",
      icon: ThumbsUp,
      color: "bg-green-500/20",
      path: "/console/categories/feature-requests",
    },
  ];

  let { children } = $props();
  let activeMenu = $state("");
  let chatDialogOpen = $state(false);
  let chatDialogX = $state(100);
  let chatDialogY = $state(100);

  // 订阅appStore状态
  let appState = $state(appStore.get());
  appStore.subscribe((state) => {
    appState = state;
  });

  // Determine activeMenu based on the current path
  $effect(() => {
    const currentPath = $page.url.pathname;

    // alert(currentPath);
    if (currentPath.startsWith("/console/users")) {
      activeMenu = "Users";
    } else if (currentPath.startsWith("/console/events")) {
      activeMenu = "Explore";
    } else if (currentPath.startsWith("/console/admin/research")) {
      activeMenu = "Research";
    } else if (currentPath.startsWith("/console/groups")) {
      activeMenu = "Groups";
    } else if (currentPath.startsWith("/console/about")) {
      activeMenu = "About";
    } else {
      // Check categories
      const activeCategory = categories.find((cat) =>
        currentPath.startsWith(cat.path)
      );
      if (activeCategory) {
        activeMenu = activeCategory.name;
      } else if (currentPath.startsWith("/console/all-categories")) {
        activeMenu = "All categories";
      } else {
        activeMenu = ""; // Default or based on other logic
      }
    }
  });

  // 处理新建按钮点击
  function handleChatClick() {
    chatDialogOpen = true;
  }

  // 处理聊天对话框关闭
  function handleChatClose() {
    chatDialogOpen = false;
  }

  // 处理窗口停靠到侧边栏
  function handleDockToSidebar() {
    // 添加聊天组件到侧边栏tabs
    appStore.addSidebarTab({
      id: "ai-chat",
      title: "AI 对话",
      component: DraggableChatDialog,
      props: {
        open: true,
        apiKey: undefined,
        modelName: "gemini-1.5-flash",
        initialMessages: [],
        hideDockButton: true,
      },
      icon: MessageSquare,
    });

    // 打开侧边栏
    appStore.setSidebarOpen(true);

    // 设置为活动标签页
    appStore.setActiveSidebarTab("ai-chat");

    // 关闭浮动对话框
    chatDialogOpen = false;
  }

  // 处理窗口最大化
  function handleMaximize() {
    // 导航到特定区域
    window.location.hash = "#L145-147";
    chatDialogOpen = false;
  }
</script>

<div class="drawer lg:drawer-open bg-base-100 min-h-screen relative">
  <input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
  <div class="drawer-content flex flex-col px-4 py-3 z-0">
    <!-- Page content will be rendered here by SvelteKit -->
    <div
      class="animate-[fadeIn_0.5s_ease-in-out] p-4 overflow-hidden"
      id="L145-147"
    >
      <TopBar handleCreate={()=>{goto("/console/events/new");}} 
        title={$page.data.pageTitle} subtitle={$page.data.pageSubtitle}
        handleUseAI={handleChatClick}
      ></TopBar>
      {@render children()}
    </div>
    <label
      for="my-drawer-2"
      class="btn btn-sm btn-circle btn-soft lg:hidden fixed 
      bottom-4 right-4 shadow-depth-2 hover:shadow-depth-3 transition-smooth"
      >Open drawer</label>
  </div>

  <!-- 右侧边栏tabs区域 -->
  {#if appState.sidebarOpen && appState.sidebarTabs.length > 0}
    <div
      class="fixed right-0 top-0 h-full w-80 bg-base-200/50 backdrop-blur-sm border-l border-base-300 z-40 flex flex-col"
    >
      <!-- Tabs 头部 -->
      <div class="flex border-b border-base-300 bg-base-100/80">
        {#each appState.sidebarTabs as tab (tab.id)}
          <button
            class="flex-1 px-3 py-2 text-sm font-medium transition-colors
                   {appState.activeSidebarTab === tab.id
              ? 'bg-primary text-primary-content border-b-2 border-primary'
              : 'text-base-content/70 hover:text-base-content hover:bg-base-200/50'}"
            on:click={() => appStore.setActiveSidebarTab(tab.id)}
          >
            {#if tab.icon}
              <svelte:component this={tab.icon} class="w-4 h-4 mr-2 inline" />
            {/if}
            {tab.title}
          </button>
        {/each}
        <button
          class="px-2 py-2 text-base-content/50 hover:text-base-content hover:bg-base-200/50"
          on:click={() => appStore.setSidebarOpen(false)}
        >
          <X class="w-4 h-4" />
        </button>
      </div>

      <!-- Tab 内容区域 -->
      <div class="flex-1 overflow-hidden">
        {#each appState.sidebarTabs as tab (tab.id)}
          {#if appState.activeSidebarTab === tab.id}
            <div class="h-full overflow-y-auto">
              {#if tab.component === "DraggableChatDialog"}
                <!-- 侧边栏中的AI对话组件 -->
                <div class="flex flex-col h-full">
                  <div class="p-4 border-b border-base-300">
                    <h3 class="font-medium text-base-content">AI 对话助手</h3>
                  </div>
                  <div class="flex-1 p-4">
                    <div class="text-center opacity-60 py-8">
                      <div class="avatar placeholder mb-2">
                        <div
                          class="bg-primary text-primary-content rounded-full w-12"
                        >
                          <span class="text-lg">AI</span>
                        </div>
                      </div>
                      <p>开始与 AI 对话</p>
                      <p class="text-sm opacity-50">
                        输入你的问题，我会尽力帮助你
                      </p>
                    </div>
                  </div>
                  <div class="p-4 border-t border-base-300">
                    <div class="flex gap-2">
                      <input
                        type="text"
                        placeholder="输入消息..."
                        class="input input-bordered flex-1 input-sm"
                      />
                      <button class="btn btn-primary btn-sm"> 发送 </button>
                    </div>
                  </div>
                </div>
              {:else}
                <div>未知组件: {tab.component}</div>
              {/if}
            </div>
          {/if}
        {/each}
      </div>
    </div>
  {/if}

  <div class="drawer-side">
    <label for="my-drawer-2" aria-label="close sidebar" class="drawer-overlay"></label>
    <LeftSidebar class="" {categories} {activeMenu} />
  </div>
</div>

<!-- 全局 DraggableChatDialog 组件 -->
<DraggableChatDialog
  bind:open={chatDialogOpen}
  bind:x={chatDialogX}
  bind:y={chatDialogY}
  onclose={handleChatClose}
  onDock={handleDockToSidebar}
  onMaximize={handleMaximize}
/>

<style>
  .box-s {
    box-shadow: -16px -6px 30px var(--color-base-200);
  }
</style>
