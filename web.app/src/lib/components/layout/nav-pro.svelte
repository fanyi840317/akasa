<script lang="ts">
  import * as Sidebar from "$lib/components/ui/sidebar/index.js";
  import File from "@lucide/svelte/icons/file";
  import Folder from "@lucide/svelte/icons/folder";
  import { onMount, onDestroy, type ComponentProps } from "svelte";
  import { Button } from "$lib/components/ui/button";
  import * as Card from "$lib/components/ui/card";
  import { Ellipsis, Forward, Plus, Trash2, Sparkles, BookOpen, Link, FilePlus } from "lucide-svelte"; // Import new icons
  import AiEventCreatorModal from "$lib/components/events/ai-event-creator-modal.svelte"; // Import the new modal
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";
  import { eventStore } from "$lib/stores/event";
  import { Skeleton } from "$lib/components/ui/skeleton";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
  // Popover import removed as it's no longer used here
  import { useSidebar } from "$lib/components/ui/sidebar/index.js";
  import { page } from "$app/stores";
  import { appStore } from "$lib/stores/appState";
  import type { Event } from "$lib/types/event";
  import { goto } from '$app/navigation';


  // 组件属性
  let {
    ref = $bindable(null),
    ...restProps
  }: ComponentProps<typeof Sidebar.Root> = $props();

  // 获取侧边栏实例
  const sidebar = useSidebar();

  // 状态
  let showEventTypeSelector = $state(false);
  let showAiCreatorModal = $state(false); // State for the new AI creator modal

  // 从 eventStore 获取状态
  let userEvents: Event[] = $state([]);
  let hasEvents = $state(false);
  let isLoading = $state(false);

  // 事件处理函数
  function openAiEventCreator() {
    showAiCreatorModal = true;
  }

  function handleOrganizeEvents() {
    console.log("整理已知事件 clicked");
    // TODO: Implement logic for organizing events
  }

  function handleImportFromUrl() {
    console.log("从url导入 clicked");
    // TODO: Implement logic for importing from URL
  }

  function handleAiEventSave(event: CustomEvent<{ title: string; content: string; entities?: any }>) {
    // 保存由 AI 生成或用户修改后的事件
    const { title, content, entities } = event.detail;
    console.log('保存 AI 生成的事件:', { title, content, entities });

    // 构建完整的 Event 对象
    const eventData = {
      title: title,
      // 使用 Markdown 格式的内容
      content: content,
      category_id: '', // TODO: Allow category selection or use a default
      tags: [],
      location: entities?.locations?.[0]?.name || '',
      location_data: entities?.locations ? JSON.stringify(entities.locations) : undefined,
      cover_image_url: '',
      date: entities?.timeline?.[0]?.time || new Date().toISOString(), // 添加 date 字段
      start_date: entities?.timeline?.[0]?.time ? new Date(entities.timeline[0].time).toISOString() : new Date().toISOString(),
      end_date: entities?.timeline?.[entities.timeline.length - 1]?.time ? new Date(entities.timeline[entities.timeline.length - 1].time).toISOString() : undefined,
      status: 'draft',
      privacy: 'private',
      significance_level: 1,
      confidence_level: 1,
      uncertainty_level: 1,
      hypothesis_id: undefined,
      timeline_id: undefined,
      // 存储实体信息
      entities_data: entities ? JSON.stringify(entities) : undefined,
      user_id: get(auth).user?.$id ?? ''
    };

    eventStore.createEvent(eventData)
      .then((newEvent) => {
        eventStore.fetchEvents(); // 刷新列表
        if (newEvent && newEvent.$id) {
           goto(`/console/events/${newEvent.$id}`); // Navigate to the newly created event
        }
        // Modal closing is handled by bind:open
      })
      .catch(error => {
        console.error('创建事件失败:', error);
        // TODO: Add user feedback (e.g., toast message)
      });
  }

  type EventType = "experience" | "documentation" | "witness" | "evidence";
  function handleEventTypeSelect(event: CustomEvent<{ type: EventType }>) {
    showEventTypeSelector = false;
    appStore.openEventCreator(event.detail.type);
  }

  function handleEventSelect(eventId: string) {
    goto(`/console/events/${eventId}`);
  }

  function handleEventDelete(eventId: string) {
    eventStore.deleteEvent(eventId);
  }

  // 判断事件是否激活
  function isEventActive(eventId: string): boolean {
    const pathname = $page.url.pathname;
    return pathname === `/console/events/${eventId}`;
  }

  // Store 订阅
  const unsubscribe = eventStore.subscribe((state) => {
    userEvents = state.events;
    hasEvents = state.events.length > 0;
    isLoading = state.listLoading;
  });

  // 生命周期钩子
  onMount(async () => {
    const userId = get(auth).user?.$id;
    if (userId) {
      try {
        await eventStore.fetchEvents(userId);
      } catch (error) {
        console.error('获取用户事件失败:', error);
      }
    }
  });

  onDestroy(() => {
    unsubscribe();
  });
</script>


<AiEventCreatorModal bind:open={showAiCreatorModal} on:save={handleAiEventSave} />

<Sidebar.Group>
  {#if isLoading}
    <div class="flex items-center space-x-4 p-4">
      <div class="space-y-2 flex-1">
        <Skeleton class="h-4 w-[80%]" />
        <Skeleton class="h-3 w-[60%]" />
        <Skeleton class="h-4 w-[80%]" />
        <Skeleton class="h-3 w-[60%]" />
      </div>
    </div>
  {:else if !hasEvents}
  <Card.Root class="shadow-none bg-muted/10 border-primary/10">
    <form>
      <Card.Header class="p-4 pb-0">
        <Card.Title class="text-sm  text-primary/70">探索未知的世界</Card.Title>
        <Card.Description class="text-xs">
          每一个神秘事件背后都有一个等待被讲述的故事，分享你的发现
        </Card.Description>
      </Card.Header>
      <Card.Content class="grid px-2 py-4">
        <Button
          variant="outline"
          class="w-full "
          size="sm"
          onclick={openAiEventCreator}
        >
          <Sparkles class="mr-2 h-4 w-4" />
          我要爆料
        </Button>
      </Card.Content>
    </form>
  </Card.Root>
  {:else}
  <Sidebar.GroupLabel>私人</Sidebar.GroupLabel>
    <!-- Use DropdownMenu for adding events -->
    <DropdownMenu.Root>
      <DropdownMenu.Trigger>
        <Sidebar.GroupAction
          title="添加事件"
        >
          <Plus /> <span class="sr-only">添加事件</span>
        </Sidebar.GroupAction>
      </DropdownMenu.Trigger>
      <DropdownMenu.Content class="w-48 p-1" side="right" align="start">
        <DropdownMenu.Item onclick={openAiEventCreator}>
          <Sparkles class="mr-2 h-4 w-4 text-muted-foreground" />
          用AI创建
        </DropdownMenu.Item>
        <DropdownMenu.Item onclick={() => appStore.openEventCreator('documentation')}>
          <FilePlus class="mr-2 h-4 w-4 text-muted-foreground" />
          全新创建
        </DropdownMenu.Item>
      </DropdownMenu.Content>
    </DropdownMenu.Root>

    <Sidebar.GroupContent>
      <Sidebar.Menu>
        {#each userEvents as event}
          {@render events({ id: event.$id ?? '', title: event.title ?? '' })}
        {/each}
      </Sidebar.Menu>
    </Sidebar.GroupContent>
  {/if}
</Sidebar.Group>

{#snippet events({ id, title }: { id: string; title: string })}
  <Sidebar.MenuItem>
    <Sidebar.MenuButton
      isActive={isEventActive(id)}
      onclick={() => handleEventSelect(id)}
      class={isEventActive(id) ? 'bg-sidebar-accent text-sidebar-accent-foreground' : ''}
    >
      {#snippet child({ props })}
        <a href="javascript:void(0)" {...props}>
          <File />
          <span>{title}</span>
        </a>
      {/snippet}
    </Sidebar.MenuButton>
    <DropdownMenu.Root>
      <DropdownMenu.Trigger>
        {#snippet child({ props })}
          <Sidebar.MenuAction showOnHover {...props}>
            <Ellipsis />
            <span class="sr-only">More</span>
          </Sidebar.MenuAction>
        {/snippet}
      </DropdownMenu.Trigger>
      <DropdownMenu.Content
        class="w-48 rounded-lg"
        side={sidebar.isMobile ? "bottom" : "right"}
        align={sidebar.isMobile ? "end" : "start"}
      >
        <DropdownMenu.Item onclick={() => handleEventSelect(id)}>
          <Folder class="text-muted-foreground" />
          <span>查看事件</span>
        </DropdownMenu.Item>
        <DropdownMenu.Item>
          <Forward class="text-muted-foreground" />
          <span>分享事件</span>
        </DropdownMenu.Item>
        <DropdownMenu.Separator />
        <DropdownMenu.Item onclick={() => handleEventDelete(id)}>
          <Trash2 class="text-muted-foreground" />
          <span>删除事件</span>
        </DropdownMenu.Item>
      </DropdownMenu.Content>
    </DropdownMenu.Root>
  </Sidebar.MenuItem>
{/snippet}
