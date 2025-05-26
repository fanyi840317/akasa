<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { eventStore } from "$lib/stores/event";
  import {
    ChevronDown,
    Grid,
    List,
    Subtitles,
    Plus,
    PenTool,
    FileText as FileTextIcon,
    Presentation,
    Zap,
    Globe,
    UploadCloud,
    Trash2
  } from "lucide-svelte";
  import { BatchAddEvents, EventConsoleCard } from "$lib/components/events";
  import * as Modal from "$lib/components/ui/modal";
  import { Root } from "$lib/components/ui/scroll-area";
  import * as Dropdown from "$lib/components/ui/dropdown-menu";

  let viewMode: "table" | "card" = $state("card");
  let searchTerm = "";
  let showBatchAddModal = $state(false);
  let showDeleteConfirmModal = $state(false);
  let selectedEventIds: string[] = $state([]);

  // 订阅事件数据
  let events: any[] = $state([]);
  let listLoading = $state(false);
  let error: string | null = $state(null);
  // let filteredEvents: any[] = $state([]);
  const unsubscribe = eventStore.subscribe((state) => {
    events = state.events;
    listLoading = state.listLoading;
    error = state.error;
  });

  onMount(() => {
    eventStore.fetchEvents();
    return () => unsubscribe();
  });

  // 搜索过滤
  // $effect() filteredEvents = events.filter((e) =>
  //   e.title?.toLowerCase().includes(searchTerm.toLowerCase())
  // );

  // $effect(() => {
  //   filteredEvents = events.filter((e) =>
  //     e.title?.toLowerCase().includes(searchTerm.toLowerCase())
  //   );
  // });

  function toggleSelectEvent(eventId: string) {
    if (selectedEventIds.includes(eventId)) {
      selectedEventIds = selectedEventIds.filter((id) => id !== eventId);
    } else {
      selectedEventIds = [...selectedEventIds, eventId];
    }
  }

  function confirmDelete() {
    showDeleteConfirmModal = true;
  }

  async function deleteSelectedEvents() {
    if (selectedEventIds.length === 0) return;
    // Assuming eventStore has a deleteEvents method
    await eventStore.deleteEvents(selectedEventIds);
    selectedEventIds = []; // Clear selection after deletion
    showDeleteConfirmModal = false;
  }

  function cancelDelete() {
    showDeleteConfirmModal = false;
  }
</script>

<div class="p-6 py-4">
  <div class="flex justify-between items-center mb-2">
    <div class="flex items-center gap-2">
      <h1 class="text-2xl font-semibold">Week MAY 7 - MAY 13</h1>
      <button class="btn btn-ghost btn-sm p-1">
        <ChevronDown class="w-5 h-5" />
      </button>
    </div>
    <div class="flex items-center gap-4">
      {#if selectedEventIds.length > 0}
        <button class="btn btn-error btn-sm" onclick={confirmDelete}>
          <Trash2 class="w-4 h-4" />
          删除 ({selectedEventIds.length})
        </button>
      {/if}
      <div class="tabs tabs-box tabs-xs">
        <label class="tab">
          <input
            type="radio"
            name="my_tabs_4"
            checked={viewMode === "table"}
            onchange={() => (viewMode = "table")}
          />
          <List class="w-4" />
        </label>
        <label class="tab">
          <input
            type="radio"
            name="my_tabs_4"
            checked={viewMode === "card"}
            onchange={() => (viewMode = "card")}
          />
          <Grid class="w-4 " />
        </label>
      </div>
      <Dropdown.Root>
        <Dropdown.Trigger>
          <button class="btn btn-neutral btn-sm">
            <Plus class="w-4 h-4" />
            Create
            <ChevronDown class="w-4 h-4" />
          </button>
        </Dropdown.Trigger>
        <Dropdown.Content class="w-56">
          <Dropdown.Group>
            <Dropdown.Item onclick={() => goto("/console/events/new")}>
              <PenTool class="w-4 h-4 mr-2" />
              <span>新建事件</span>
            </Dropdown.Item>
            <Dropdown.Item>
              <UploadCloud class="w-4 h-4 mr-2" />
              <span>Import</span>
            </Dropdown.Item>
          </Dropdown.Group>
        </Dropdown.Content>
      </Dropdown.Root>
    </div>
  </div>
  <p class="text-xs text-base-content/60 mb-6">
    Last Updated: May 12, 2025 12:06 pm
  </p>

  {#if listLoading}
    <div class="flex justify-center items-center h-32">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
  {:else if error}
    <div class="alert alert-error">{error}</div>
  {:else if events.length === 0}
    <div class="text-center text-base-content/60">暂无事件</div>
  {:else if viewMode === "table"}
    <!-- <div class="overflow-x-auto">
      <table class="table table-zebra w-full">
        <thead>
          <tr class="text-base-content/80">
            <th>标题</th>
            <th>时间</th>
            <th>地点</th>
            <th>创建人</th>
          </tr>
        </thead>
        <tbody>
          {#each events as event (event.$id)}
            <tr
              class="hover cursor-pointer"
              onclick={() => goto(`/console/events/${event.$id}`)}
            >
              <td>{event.title}</td>
              <td>{event.date || "-"}</td>
              <td>{event.location || "-"}</td>
              <td>{event.user_id || "-"}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div> -->
  {:else}
    <div
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
    >
      {#each events as event (event.$id)}
        <EventConsoleCard
          title={event.title}
          description={event.description || "-"}
          duration={event.duration || "-"}
          onDblClick={() => goto(`/console/events/${event.$id}`)}
          onClick={() => toggleSelectEvent(event.$id)}
          isSelected={selectedEventIds.includes(event.$id)}
        />
      {/each}
    </div>
  {/if}
</div>
<!-- <Modal.Root bind:open={showBatchAddModal}>
  <Modal.Content>
    <BatchAddEvents />
  </Modal.Content>
</Modal.Root> -->

<Modal.Root bind:open={showDeleteConfirmModal} class="w-[400px]">
    <div class="p-4">
      <h3 class="font-bold text-lg">确认删除事件?</h3>
      <p class="py-4">您确定要删除选中的 {selectedEventIds.length} 个事件吗？此操作不可撤销。</p>
      <div class="modal-action">
        <button class="btn btn-outline" onclick={cancelDelete}>取消</button>
        <button class="btn btn-error" onclick={deleteSelectedEvents}>确认删除</button>
      </div>
    </div>
</Modal.Root>
