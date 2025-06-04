<script lang="ts">
  import { onMount } from "svelte";
  import { auth } from "$lib/stores/auth";
  import { eventStore } from "$lib/stores/event";
  import { appStore } from "$lib/stores/app-state";
  import EventCard from "$lib/components/events/event-card.svelte";
  import type { Event } from "$lib/types/event";
  import {
    Calendar,
    Plus,
    FileText,
    PlusCircle,
    Heart,
    FolderHeart,
  } from "lucide-svelte";
  import { LeftSidebar } from "$lib/components/console-layout";
  import EventList from "$lib/components/events/event-list.svelte";
  import CategoryNavItem from "$lib/components/ui/nav/category-nav-item.svelte";
  import {SearchButton,CollapseButton} from "$lib/components/ui/buttons";
  import NavItem from "$lib/components/ui/nav/nav-item.svelte";
  import { page } from "$app/state";

  let { children } = $props();
  let events: Event[] = $state([]);
  let loading = $state(false);
  let error = $state<string | null>(null);

  let categories: any[] = [
    {
      name: "All categories",
      path: "/console/my/events",
      icon: Calendar,
      color: "primary",
    },
  ];
  let activeMenu = $state("");
  const currentPath = $derived(page.url.pathname);
  $effect(() => {
    // alert(currentPath);
    if (currentPath.startsWith("/console/my/favorites")) {
      activeMenu = "favorites";
    } else if (currentPath.startsWith("/console/my/collections")) {
      activeMenu = "collections";
    } else if (currentPath.startsWith("/console/my/research")) {
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

  // 获取当前用户的events
  async function loadUserEvents() {
    const authState = $auth;
    if (!authState.user) {
      error = "请先登录";
      return;
    }

    loading = true;
    error = null;

    try {
      const userEvents = await eventStore.fetchEvents(authState.user.$id);
      events = userEvents || [];
    } catch (err) {
      error = err instanceof Error ? err.message : "加载事件失败";
      console.error("Failed to load user events:", err);
    } finally {
      loading = false;
    }
  }

  // 处理事件卡片点击
  function handleEventClick(event: Event) {
    // 可以导航到事件详情页面
    console.log("Event clicked:", event);
  }

  // 组件挂载时加载数据
  onMount(() => {
    loadUserEvents();
  });
</script>

<div class="flex h-full">
  <!-- 左侧导航栏 -->
  <div class="{$appStore.sidebarCollapsed ? 'w-0 overflow-hidden' : 'w-fit'} bg-base-100 transition-all duration-300">
    <!-- 左侧导航栏内容 -->
    <!-- <LeftSidebar /> -->

    <div class="flex-1 flex flex-col w-54 p-4 py-6">
      <!-- Sidebar content here -->
      <!-- 搜索按钮 -->
      <SearchButton
        class="mb-2"
        variant="outline"
        onClick={() => console.log("Search clicked")}
      />
      <!-- 新建按钮 -->
      <span class="menu-title text-xs mt-2">Navigation</span>
      <NavItem
        href="/console/my/favorites"
        icon={FolderHeart}
        label="Favorites"
        isActive={activeMenu === "favorites"}
      />
      <NavItem
        href="/console/my/collections"
        icon={PlusCircle}
        label="collections"
        isActive={activeMenu === "collections"}
      />
      <span class="menu-title text-xs mt-2">Categories</span>
      {#each categories as category}
        <CategoryNavItem
          href={category.path}
          icon={category.icon}
          label={category.name}
          color={category.color}
          isActive={activeMenu === category.name}
        />
      {/each}
    </div>
  </div>

  <!-- 右侧内容区域 -->
  {@render children()}
</div>
