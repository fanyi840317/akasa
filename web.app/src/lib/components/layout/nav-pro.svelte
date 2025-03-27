<script lang="ts">
  import * as Collapsible from "$lib/components/ui/collapsible/index.js";
  import * as Sidebar from "$lib/components/ui/sidebar/index.js";
  import * as Modal from "$lib/components/ui/modal/index.js";
  import ChevronRight from "@lucide/svelte/icons/chevron-right";
  import File from "@lucide/svelte/icons/file";
  import Folder from "@lucide/svelte/icons/folder";
  import PlusCircle from "@lucide/svelte/icons/plus-circle";
  import { onMount, onDestroy, type ComponentProps } from "svelte";
  import { Button } from "$lib/components/ui/button";
  import { goto } from "$app/navigation";
  import * as Card from "$lib/components/ui/card";
  import EventDetail from "../events/event-detail.svelte";
  import { Ellipsis, Forward, Plus, Save, Trash2 } from "lucide-svelte";
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";
  import { eventStore } from "$lib/stores/event";
  import { Skeleton } from "$lib/components/ui/skeleton";
  import { caseStore } from "$lib/stores/case";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
  import { useSidebar } from "$lib/components/ui/sidebar/index.js";
  import type { Event } from "$lib/types/event";
  import { page } from "$app/stores";

  // 组件属性
  let {
    ref = $bindable(null),
    ...restProps
  }: ComponentProps<typeof Sidebar.Root> = $props();

  // 状态管理
  let showDialog = $state(false);
  let userEvents = $state<Event[]>([]);
  let hasEvents = $state(false);
  let isLoading = $state(false);

  // 获取侧边栏实例
  const sidebar = useSidebar();

  // 判断事件是否激活
  function isEventActive(eventId: string): boolean {
    const pathname = $page.url.pathname;
    return pathname === `/console/events/${eventId}`;
  }

  // 事件处理函数
  const handleEventSelect = (eventId: string) => {
    // 如果点击的是当前选中的事件，不做任何操作
    if (isEventActive(eventId)) {
      return;
    }
    // 导航到事件详情页面
    goto(`/console/events/${eventId}`);
  };

  const handleEventDelete = async (eventId: string) => {
    try {
      await eventStore.deleteEvent(eventId);
    } catch (error) {
      console.error('删除事件失败:', error);
    }
  };

  const handleEventCreate = (result: { detail?: Event }) => {
    showDialog = false;
    if (result?.detail?.$id) {
      const newEventId = result.detail.$id;
      // 导航到新创建的事件
      goto(`/console/events/${newEventId}`);
    }
  };

  // Store 订阅
  const unsubscribeEventStore = eventStore.subscribe((state) => {
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
    unsubscribeEventStore();
  });
</script>

<Sidebar.Group>
  <Sidebar.GroupLabel>私人</Sidebar.GroupLabel>

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
    <Card.Root class="shadow-none my-2 mx-2">
      <form>
        <Card.Header class="p-4 pb-0">
          <Card.Title class="text-sm">分享身边的神秘事件</Card.Title>
          <Card.Description class="text-xs">
            记录和分享你遇到的神秘事件，让更多人了解这个世界的未知面
          </Card.Description>
        </Card.Header>
        <Card.Content class="grid gap-2.5 p-4">
          <Button
            class="bg-sidebar-primary text-sidebar-primary-foreground w-full shadow-none"
            size="sm"
            onclick={() => (showDialog = true)}
          >
            分享事件
          </Button>
        </Card.Content>
      </form>
    </Card.Root>
  {:else}
    <Sidebar.GroupAction
      title="Add Project"
      onclick={() => (showDialog = true)}
    >
      <Plus /> <span class="sr-only">Add Project</span>
    </Sidebar.GroupAction>

    <Sidebar.GroupContent>
      <Sidebar.Menu>
        {#each userEvents as event}
          {@render events({ id: event.$id ?? '', title: event.title ?? '' })}
        {/each}
      </Sidebar.Menu>
    </Sidebar.GroupContent>
  {/if}
</Sidebar.Group>

<Modal.Root bind:open={showDialog} class="sm:max-w-[900px] h-[80vh]">
  <Modal.Content>
    <EventDetail
      x_event={undefined}
      on:close={handleEventCreate}
    />
  </Modal.Content>
</Modal.Root>

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
