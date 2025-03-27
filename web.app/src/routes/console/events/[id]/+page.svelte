<script lang="ts">
  import { onDestroy } from "svelte";
  import { page } from "$app/stores";
  import { eventStore } from "$lib/stores/event";
  import { toast } from "svelte-sonner";
  import type { Event } from "$lib/types/event";
  import Header from "$lib/components/layout/header.svelte";
  import EventDetail from "$lib/components/events/event-detail.svelte";
  import { Save } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";

  // 事件数据
  let event: Event | null = null;
  let isLoading = $state(false);

  // 面包屑数据
  let titles = [
    { name: "事件", path: "/console/events" },
    { name: "无标题", path: `/console/events/${$page.params.id}` },
  ];

  // 加载事件数据
  async function loadEventData(eventId: string) {
    if (!eventId) return;
    await eventStore.fetchEvent(eventId);
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
    isLoading = state.eventLoading;
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
    // 处理关闭事件
  }
</script>

<div class="flex flex-col h-full">
  <Header {titles}>
    <div>
      <Button variant="ghost" size="icon" class="gap-2">
        <Save class="h-4 w-4" />
      </Button>
    </div>
  </Header>

  <div class="flex-1">
    {#if isLoading}
      <div class="flex items-center justify-center h-full">
        <div class="text-center">加载中...</div>
      </div>
    {:else}
      <EventDetail x_event={event} on:close={handleClose} />
    {/if}
  </div>
</div>

<style>
  :global(.affine-editor) {
    padding: 0 !important;
  }
</style>
