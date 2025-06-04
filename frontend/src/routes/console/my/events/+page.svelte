<script lang="ts">
  import { onMount } from "svelte";
  import { auth } from "$lib/stores/auth";
  import { eventStore } from "$lib/stores/event";
  import { appStore } from "$lib/stores/app-state";
  import EventCard from "$lib/components/events/event-card.svelte";
  import type { Event } from "$lib/types/event";
  import {
    Plus,
    FileText,
    PlusCircle,
    Heart,
    FolderHeart,
    Settings,
    MoreHorizontal,
    SparklesIcon,
  } from "lucide-svelte";
  import { LeftSidebar } from "$lib/components/console-layout";
  import EventList from "$lib/components/events/event-list.svelte";
  import CategoryNavItem from "$lib/components/ui/nav/category-nav-item.svelte";
  import { SearchButton, CollapseButton } from "$lib/components/ui/buttons";
  import NavItem from "$lib/components/ui/nav/nav-item.svelte";
  import { goto } from "$app/navigation";
  import EventCardList from "$lib/components/events/event-card-list.svelte";
  import { EventCardGrid } from "$lib/components/events";
  import EmptyCard from "$lib/components/my/empty-card.svelte";
  import { InputArea } from "$lib/components/ai";
  import IconButton from "$lib/components/ui/buttons/icon-button.svelte";
  import TextCarousel from "$lib/components/ui/carousel/text-carousel.svelte";

  let events: Event[] = $state([]);
  let loading = $state(false);
  let error = $state<string | null>(null);
  let sidebarCollapsed = $derived($appStore.sidebarCollapsed);

  let categories: any[] = [
    {
      name: "All categories",
      path: "/console/all-categories",
      icon: FolderHeart,
      color: "primary",
    },
  ];
  let activeMenu = $state("");

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
    goto(`/console/events/${event.$id}`);
  }

  // 组件挂载时加载数据
  onMount(() => {
    loadUserEvents();
  });
</script>

<!-- 右侧内容区域 -->
<div class="flex flex-col w-full flex-1 bg-base-200 rounded-tl-xl h-full">
  <!-- 页面标题 -->
  <div
    class="flex items-center justify-between border-b border-border p-4 py-3"
  >
    <div class="flex items-center gap-3">
      <CollapseButton
        collapsed={sidebarCollapsed}
        onClick={() => appStore.setSidebarCollapsed(!sidebarCollapsed)}
        class="mr-1"
      />
      <h1 class="text-sm font-semibold text-base-content/70">我的事件</h1>
      <h1 class="text-xs font-semibold text-base-content/50">/</h1>

      <h1 class="text-sm text-base-content">All</h1>
    </div>
    <div class="flex gap-2 flex-row">
      <IconButton>
        <Settings class="size-4" />
      </IconButton>
      <IconButton>
        <MoreHorizontal class="size-4" />
      </IconButton>
      <IconButton>
        <SparklesIcon class="size-4" />
      </IconButton>
    </div>
  </div>

  <!-- 多语言文本轮播 -->

  <!-- 加载状态 -->
  {#if loading}
    <div class="flex items-center justify-center h-64">
      <div class="loading loading-spinner loading-lg text-primary"></div>
    </div>
  {:else if error}
    <!-- 错误状态 -->
    <div class="flex flex-col items-center justify-center h-64 text-center">
      <div class="text-error mb-2">⚠️</div>
      <p class="text-base-content/70">{error}</p>
      <button class="btn btn-outline btn-sm mt-4" onclick={loadUserEvents}>
        重试
      </button>
    </div>
  {:else if events.length === 0}
    <!-- 空状态 - 使用EmptyCard组件 -->
    <div class="flex flex-col items-center justify-start h-full">
      
      <div class="flex-center flex-col min-w-lg max-w-lg gap-4  py-10 rounded-2xl">
        <EmptyCard
          title="暂无事件"
          
          description="也许你的一个线索，就是解开谜题的钥匙。
              创建事件，留下见证，让真相浮出水面。"
          buttonText="创建第一个事件"
          onButtonClick={() => goto("/console/events/new")}
          aiPlaceholder="告诉AI你想创建什么样的事件..."
        />
        <!-- <a href="/console/events/new"
          ><div class="w-[200px]">
            <div class="font-medium text-base mb-2 flex items-center">
              快速开始
              <div class="pointer">
               
              </div>
            </div>
            <div class="text-xs text-text-default">
              也许你的一个线索，就是解开谜题的钥匙。
              创建事件，留下见证，让真相浮出水面。
            </div>
            <button class="btn btn-xs mt-2 btn-outline p-1 px-4">
              <PlusCircle class="w-4 h-4" />
              <div class="text-xs">创建</div>
            </button>
          </div></a
        > -->
        <div class="divider text-sm  h-20">Or use ai to help you create</div>
        <!-- AI输入框 - 使用第二张图片样式 -->
        <div>

          <InputArea
          class="flex flex-col min-w-lg "
          placeholder="告诉AI你想创建什么样的事件..."
          onSubmit={(input) => console.log(input)}
        />
        </div>
      </div>
    </div>
  {:else}
    <!-- 事件列表 -->
    <div class="p-4">
      <EventCardGrid cardSize="xs" {events} onEventClick={handleEventClick} />
    </div>
    <!-- <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {#each events as event (event.$id)}
            <EventCard 
              {event} 
              onClick={handleEventClick}
              size="sm"
              class="cursor-pointer hover:shadow-lg transition-shadow"
            />
          {/each}
        </div> -->
  {/if}
</div>
