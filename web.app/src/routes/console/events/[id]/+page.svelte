<script lang="ts">
  import { onDestroy } from "svelte";
  import { page } from "$app/stores";
  import { eventStore } from "$lib/stores/event";
  import { toast } from "svelte-sonner";
  import type { Event } from "$lib/types/event";
  import Header from "$lib/components/layout/header.svelte";
  import EventCreatorWindow from "$lib/components/events/event-creator-window.svelte";
  import { Save } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";
  import { Loader2 } from "lucide-svelte";

  // 事件数据
  let event: Event | null = null;
  let isLoading = $state(false);
  let isEditing = $state(false);

  // 面包屑数据
  let titles = [
    { name: "事件", path: "/console/events" },
    { name: "无标题", path: `/console/events/${$page.params.id}` },
  ];

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

  // 监听 URL 变化
  $effect(() => {
    const eventId = $page.params.id;
    if (eventId) {
      loadEventData(eventId);
    }
  });

  // 订阅事件数据变化
  const unsubscribe = eventStore.subscribe((state) => {
    event = state.currentEvent;
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

<div class="flex flex-col h-full">
  <Header {titles}>
    <div class="flex gap-2">
      <button
        class="inline-flex items-center justify-center gap-2 rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 disabled:pointer-events-none disabled:opacity-50 h-9 w-9 hover:bg-accent hover:text-accent-foreground"
        on:click={() => (isEditing = true)}
      >
        <Save class="h-4 w-4" />
      </button>
    </div>
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
      <EventCreatorWindow open={true} {event} on:close={handleClose} />
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
