<script lang="ts">
  import {
    Users,
    BarChart2,
    Shield,
    MessageSquare,
    Info,
    Settings,
    Search,
    ListFilter,
    FileText,
    ThumbsUp,
    ThumbsDown,
    MessageCircle,
    FileSearch,
    Minimize2,
    X,
    Maximize2
  } from "lucide-svelte";
  import { page } from "$app/stores";
  import { auth } from "$lib/stores/auth"; // 假设 auth store 的路径
  import { UserAvatar } from "$lib/components/ui/avatar";
  import { BatchAddEvents } from "$lib/components/events";
  import { effects as blocksEffects } from "@blocksuite/blocks/effects";
  import { effects as presetsEffects } from "@blocksuite/presets/effects";

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
    }, // Assuming FileText is for 'How To'
    {
      name: "Feature Requests",
      icon: ThumbsUp,
      color: "bg-green-500/20",
      path: "/console/categories/feature-requests",
    }, // Assuming ThumbsUp is for 'Feature Requests'
    {
      name: "Bug Reports",
      icon: ThumbsDown,
      color: "bg-purple-500/20",
      path: "/console/categories/bug-reports",
    }, // Assuming ThumbsDown is for 'Bug Reports'
    {
      name: "Feedback",
      icon: MessageCircle,
      color: "bg-blue-500/20",
      path: "/console/categories/feedback",
    }, // Assuming MessageCircle is for 'Feedback'
  ];

  let { children } = $props();
  let activeMenu = $state("");
  let dockedWindows = $state([]);
  let minimizedWindows = $state([]);

  // Determine activeMenu based on the current path
  $effect(() => {
    const currentPath = $page.url.pathname;

    // alert(currentPath);
    if (currentPath.startsWith("/console/users")) {
      activeMenu = "Users";
    } else if (currentPath.startsWith("/console/events")) {
      activeMenu = "Events";
    } else if (currentPath.startsWith("/console/admin/research")) {
      activeMenu = "Research";
    } else if (currentPath.startsWith("/console/groups")) {
      activeMenu = "Groups";
    } else if (currentPath.startsWith("/console/about")) {
      activeMenu = "About";
    } else {
      // Check categories
      const activeCategory = categories.find((cat) =>
        currentPath.startsWith(cat.path),
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

  // 窗口管理函数
  function addDockedWindow(window) {
    dockedWindows = [...dockedWindows, window];
  }
  
  function removeDockedWindow(windowId) {
    dockedWindows = dockedWindows.filter(w => w.id !== windowId);
  }
  
  function addMinimizedWindow(window) {
    minimizedWindows = [...minimizedWindows, window];
  }
  
  function removeMinimizedWindow(windowId) {
    minimizedWindows = minimizedWindows.filter(w => w.id !== windowId);
  }
  
  function restoreWindow(windowId) {
    const window = minimizedWindows.find(w => w.id === windowId);
    if (window && window.onRestore) {
      window.onRestore();
      removeMinimizedWindow(windowId);
    }
  }
  
  // 全局窗口管理器
  if (typeof window !== 'undefined') {
    window.windowManager = {
      addDockedWindow,
      removeDockedWindow,
      addMinimizedWindow,
      removeMinimizedWindow
    };
  }
  
  // Helper function to create navigation links, assuming you might want to navigate
  // For buttons that just set activeMenu, on:click is fine as is.
  // If actual navigation is needed, use <a> tags or programmatic navigation.
</script>
<style>
  .box-s {
    box-shadow: -16px -6px 30px var(--color-base-200);
  }
  
  .dock-area {
    background: rgba(0, 0, 0, 0.05);
    border: 2px dashed rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
  }
  
  .dock-area.active {
    background: rgba(59, 130, 246, 0.1);
    border-color: rgba(59, 130, 246, 0.3);
  }
  
  .docked-window {
    transition: all 0.3s ease;
    animation: slideInRight 0.3s ease;
  }
  
  .minimized-card {
    transition: all 0.3s ease;
    animation: slideInUp 0.3s ease;
  }
  
  .minimized-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
  
  @keyframes slideInRight {
    from {
      transform: translateX(100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
  
  @keyframes slideInUp {
    from {
      transform: translateY(20px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
</style>
<div class="drawer lg:drawer-open bg-base-100 min-h-screen relative">
  <input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
  <div class="drawer-content flex flex-col px-4 py-2 box-s z-0">
    <!-- Page content will be rendered here by SvelteKit -->
    {@render children()}
    <label
      for="my-drawer-2"
      class="btn btn-primary drawer-button lg:hidden fixed bottom-4 right-4"
      >Open drawer</label
    >
  </div>
  
  <!-- 右边栏停靠区域 -->
   {#if false}
  <div class="fixed right-0 top-0 h-full w-80 bg-base-200/50 backdrop-blur-sm border-l border-base-300 z-40 flex flex-col">
    <!-- 停靠窗口区域 -->
    <div class="flex-1 p-4">
      <h3 class="text-sm font-medium text-base-content/70 mb-3">停靠窗口</h3>
      <div class="dock-area rounded-lg p-2 min-h-32 mb-4" class:active={dockedWindows.length > 0}>
        {#if dockedWindows.length === 0}
          <div class="text-center text-base-content/50 text-xs py-8">
            拖拽窗口到此处停靠
          </div>
        {:else}
          {#each dockedWindows as window (window.id)}
            <div class="docked-window bg-base-100 rounded-lg p-3 mb-2 shadow-sm">
              <div class="flex items-center justify-between mb-2">
                <h4 class="text-sm font-medium truncate">{window.title}</h4>
                <div class="flex gap-1">
                  <button 
                    class="btn btn-ghost btn-xs"
                    onclick={() => window.onUndock?.()}
                  >
                    <Maximize2 class="w-3 h-3" />
                  </button>
                  <button 
                    class="btn btn-ghost btn-xs"
                    onclick={() => {
                      window.onClose?.();
                      removeDockedWindow(window.id);
                    }}
                  >
                    <X class="w-3 h-3" />
                  </button>
                </div>
              </div>
              <div class="text-xs text-base-content/60">
                {window.content || '窗口内容'}
              </div>
            </div>
          {/each}
        {/if}
      </div>
    </div>
    
    <!-- 最小化窗口区域 -->
    <div class="p-4 border-t border-base-300">
      <h3 class="text-sm font-medium text-base-content/70 mb-3">最小化窗口</h3>
      <div class="grid grid-cols-2 gap-2">
        {#each minimizedWindows as window (window.id)}
          <div 
            class="minimized-card bg-base-100 rounded-lg p-3 cursor-pointer shadow-sm hover:shadow-md"
            onclick={() => restoreWindow(window.id)}
          >
            <div class="flex items-center justify-between mb-1">
              <h4 class="text-xs font-medium truncate">{window.title}</h4>
              <button 
                class="btn btn-ghost btn-xs"
                onclick={(e) => {
                  e.stopPropagation();
                  window.onClose?.();
                  removeMinimizedWindow(window.id);
                }}
              >
                <X class="w-2 h-2" />
              </button>
            </div>
            <div class="text-xs text-base-content/50 truncate">
              {window.content || '点击恢复'}
            </div>
          </div>
        {/each}
      </div>
    </div>
  </div>
  {/if}
  <div class="drawer-side">
    <label for="my-drawer-2" aria-label="close sidebar" class="drawer-overlay"
    ></label>
    <ul class="menu pl-10 py-10 w-68 min-h-full text-base-content/50 -mr-4">
        <h1 class="text-2xl font-bold mb-4 text-center">Akas</h1>
      <div class=" w-full rounded-xl bg-base-200 p-4 ">
        <button
          class="btn btn-ghost w-full items-center justify-between my-4 text-base-content/50"
        >
          <div class="flex gap-2 items-center">
            <Search class="w-4 h-4" />Search
          </div>
          <div class="">
            <kbd class="kbd kbd-xs">Ctrl</kbd>
            <kbd class="kbd kbd-xs">k</kbd>
          </div>
        </button>
        <!-- Sidebar content here -->
        <li class="menu-title text-xs">Navigation</li>
        <li>
          <a
            href="/console/admin/research"
            class:btn-active={activeMenu === "Research"}
            class:text-base-content={activeMenu === "Research"}
            class="btn btn-secondary hover:bg-base-100/80 text-base-content/50 btn-ghost justify-start"
            ><FileSearch class="w-4 h-4" /> Research</a
          >
        </li>
        <li>
          <a
            href="/console/events"
            class:text-base-content={activeMenu === "Events"}
            class="btn btn-neutral hover:btn-netural {activeMenu === "Events"? 'bg-base-100/80':'' } btn-ghost justify-start"
            ><BarChart2 class="w-4 h-4" /> Events</a
          >
        </li>
        <li>
          <a
            href="/console/users"
            class:btn-active={activeMenu === "Users"}
            class="btn btn-secondary text-base-content/50 btn-ghost justify-start"
            ><Users class="w-4 h-4" /> Users</a
          >
        </li>
        <li>
          <a
            href="/console/groups"
            class:btn-active={activeMenu === "Groups"}
            class="btn btn-secondary text-base-content/50 btn-ghost justify-start"
            ><Users class="w-4 h-4" /> Groups</a
          >
        </li>
        <li>
          <a
            href="/console/about"
            class:btn-active={activeMenu === "About"}
            class="btn btn-secondary text-base-content/50 btn-ghost justify-start"
            ><Info class="w-4 h-4" /> About</a
          >
        </li>

        <li class="menu-title text-xs mt-4">Categories</li>
        {#each categories as category}
          <li>
            <a
              href={category.path}
              class:btn-active={activeMenu === category.name}
              class="btn btn-secondary text-base-content/50 btn-ghost justify-start"
            >
              <!-- svelte-ignore svelte_component_deprecated -->
              <svelte:component
                this={category.icon}
                class={`w-3 h-3 mr-1 p-0.5 rounded-sm ${category.color} text-base-content/50`}
              />
              {category.name}
            </a>
          </li>
        {/each}
        <li>
          <a
            href="/console/all-categories"
            class:btn-active={activeMenu === "All categories"}
            class="btn btn-ghost btn-secondary text-base-content/50 justify-start"
            ><ListFilter class="w-4 h-4" /> All categories</a
          >
        </li>
      </div>

      <div class="mt-auto flex justify-center items-center p-2">
        {#if $auth.user}
          <div class="pb-4">
            <div class="flex items-center space-x-2">
              <UserAvatar
                tabindex={0}
                fallbackClass="text-base-content/50"
                class="cursor-pointer size-8 "
                src={$auth.user.prefs["avatarUrl"] || ""}
                alt={$auth.user.name}
                fallback={$auth.user.name.substring(0, 1).toUpperCase() ||
                  $auth.user.email?.substring(0, 2).toUpperCase()}
              ></UserAvatar>

              <!-- <div>
                <div class="font-semibold text-sm">
                  {$auth.user.name || "N/A"}
                </div>
                <div class="text-xs text-base-content/50">
                  {$auth.user.email || "N/A"}
                </div>
              </div> -->
            </div>
          </div>
        {/if}
        <!-- <button class="btn btn-ghost btn-secondary text-base-content/50   p-1"><Settings class="w-5 h-5" /></button>
        <button class="btn btn-ghost btn-secondary text-base-content/50   p-1"><Search class="w-5 h-5" /></button> -->
      </div>
    </ul>
  </div>
</div>
