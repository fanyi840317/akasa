<script lang="ts">
  import { onDestroy } from "svelte";
  import { page } from "$app/stores";
  import { eventStore } from "$lib/stores/event";
  import { toast } from "svelte-sonner";
  import type { Event } from "$lib/types/event";
  import Header from "$lib/components/layout/header.svelte";
  import EventCreatorWindow from "$lib/components/events/event-creator-window.svelte";

  import { Loader2 } from "lucide-svelte";
  import EventHeaderActions from "$lib/components/events/event-header-actions.svelte";

  // 事件数据
  let event = $state<Event | null>(null);
  let isLoading = $state(false);
  let isEditing = $state(false);
  let isSidebarOpen = $state(true);
  let isShareOpen = $state(false);

  // 面包屑数据
  let titles = $state([
    { name: "事件", path: "/console/events" },
    { name: "无标题", path: `/console/events/${$page.params.id}` },
  ]);

  // 加载事件数据
  async function loadEventData(eventId: string) {
    if (!eventId) return;
    isLoading = true;
    try {
      await eventStore.fetchEvent(eventId);
    } catch (error) {
      console.error("加载事件失败:", error);
      toast.error("加载事件失败");
    } finally {
      isLoading = false;
    }
  }

  // 加载事件数据
  const eventId = $page.params.id;
  if (eventId) {
    loadEventData(eventId);
  }

  // 订阅事件数据变化
  const unsubscribe = eventStore.subscribe((state) => {
    event = state.currentEvent;
  });

  // 监听事件标题变化更新面包屑
  $effect(() => {
    if (event?.title) {
      titles = [
        { name: "事件", path: "/console/events" },
        { name: event.title, path: `/console/events/${$page.params.id}` },
      ];
    }
  });

  onDestroy(() => {
    unsubscribe();
    eventStore.setCurrentEvent(null);
  });

  function handleClose() {
    isEditing = false;
  }

  function handleEdit() {
    isEditing = true;
  }

  function handleSave() {
    // 保存逻辑
    toast.success("保存成功");
    isEditing = false;
  }
</script>
{#snippet actions()}
  <EventHeaderActions
    bind:isSidebarOpen
    bind:isShareOpen
    onEdit={handleEdit}
    onShare={() => toast.info('分享功能开发中')}
    onCopy={() => toast.info('复制链接开发中')}
    onTwitter={() => toast.info('Twitter分享开发中')}
    onFacebook={() => toast.info('Facebook分享开发中')}
    onQrCode={() => toast.info('二维码分享开发中')}
    onCoverUpload={() => toast.info('更换封面开发中')}
    onExport={() => toast.info('导出功能开发中')}
    onDelete={() => toast.info('删除功能开发中')}
    onToggleSidebar={() => {
      // 侧边栏状态已经通过 bind:isSidebarOpen 自动同步
      // 不需要额外的操作
    }}
    creator={{
      name: event?.creator_name || "未知用户",
      avatar: event?.creator_avatar || null
    }}
    lastModified={event?.$updatedAt || new Date().toISOString()}
    createdAt={event?.$createdAt || new Date().toISOString()}
  />
{/snippet}
<div class="flex flex-col h-full overflow-hidden">
  <Header {titles} actions={actions}>
  </Header>

  <div class="flex-1">
    {#if isLoading}
      <div class="flex items-center justify-center h-full">
        <div class="flex flex-col items-center gap-2">
          <Loader2 class="h-8 w-8 animate-spin text-muted-foreground" />
          <div class="text-center text-muted-foreground">加载中...</div>
        </div>
      </div>
    {:else if event}
      <EventCreatorWindow
        mode="embedded"
        open={true}
        {event}
        {isSidebarOpen}
        on:close={handleClose}
      />
    {:else}
      <div class="flex items-center justify-center h-full">
        <div class="text-center text-muted-foreground">未找到事件</div>
      </div>
    {/if}
  </div>
</div>

<style>
  :global(.affine-editor) {
    padding: 0 !important;
  }
</style>
