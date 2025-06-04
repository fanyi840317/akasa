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

  import { onMount } from "svelte";

  const categories = [
    {
      name: "My Events",
      icon: MessageSquare,
      color: "bg-blue-500/20",
      path: "/console/my/events",
    },
    {
      name: "Favorites",
      icon: FileText,
      color: "bg-orange-500/20",
      path: "/console/my/favorites",
    },
    {
      name: "Collections",
      icon: ThumbsUp,
      color: "bg-green-500/20",
      path: "/console/my/collections",
    },
  ];

  let { children } = $props();
  let activeMenu = $state("");
  let chatDialogOpen = $state(false);
  let chatDialogX = $state(100);
  let chatDialogY = $state(100);
  let showTooltip = $state(false);
  let isFirstTimeUser = $state(true);
  let chatDialogRef;

  // 订阅appStore状态
  let appState = $state(appStore.get());
  appStore.subscribe((state) => {
    appState = state;
  });

  // 组件挂载时检查是否为首次使用
  onMount(() => {
    const hasUsedBefore = localStorage.getItem("chatDialogFirstTime");
    if (hasUsedBefore === "false") {
      isFirstTimeUser = false;
    }
  });

  // Determine activeMenu based on the current path
 
  // 处理新建按钮点击
  function handleChatClick() {
    // 计算AI按钮的位置，将对话框显示在按钮下方

    const windowWidth = window.innerWidth;
    // 设置对话框位置在AI按钮下方
    chatDialogX = windowWidth - 600; // 向左偏移一些，让对话框居中对齐按钮
    chatDialogY = 100; // 按钮下方10px
    chatDialogOpen = true;

    // 如果是首次使用，显示tooltip
    if (isFirstTimeUser) {
      showTooltip = true;
      // 3秒后自动隐藏tooltip
      setTimeout(() => {
        showTooltip = false;
        isFirstTimeUser = false;
        // 可以将首次使用状态保存到localStorage
        localStorage.setItem("chatDialogFirstTime", "false");
      }, 3000);
    }
  }

  // 处理聊天对话框关闭
  function handleChatClose() {
    chatDialogOpen = false;
    showTooltip = false;
  }

  // 处理窗口最大化
  function handleMaximize() {
    // 导航到特定区域
    window.location.hash = "#L145-147";
    chatDialogOpen = false;
  }
</script>

<div class="flex flex-col overflow-hidden h-screen">
  <TopBar
    class="py-1 px-6"
    handleCreate={() => {
      goto("/console/events/new");
    }}
    title={$page.data.pageTitle}
    subtitle={$page.data.pageSubtitle}
    handleUseAI={handleChatClick}
  ></TopBar>
  <div class="flex-1 overflow-hidden animate-[fadeIn_0.5s_ease-in-out]  ">
    {@render children?.()}
  </div>
</div>



<!-- 全局 DraggableChatDialog 组件 -->
<DraggableChatDialog
  bind:this={chatDialogRef}
  bind:open={chatDialogOpen}
  bind:x={chatDialogX}
  bind:y={chatDialogY}
  onclose={handleChatClose}
  onMaximize={handleMaximize}
/>

<!-- 首次使用提示tooltip -->
{#if showTooltip && chatDialogOpen}
  <div
    class="fixed z-[10000] bg-primary text-primary-content px-3 py-2 rounded-lg shadow-lg text-sm pointer-events-none"
    style="left: {chatDialogX + 50}px; top: {chatDialogY - 40}px;"
  >
    <div class="flex items-center gap-2">
      <span>提示：可以拖动窗口到任意位置</span>
    </div>
    <!-- 小箭头指向窗口 -->
    <div
      class="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-primary"
    ></div>
  </div>
{/if}

<style>
  .box-s {
    box-shadow: -16px -6px 30px var(--color-base-200);
  }
</style>
