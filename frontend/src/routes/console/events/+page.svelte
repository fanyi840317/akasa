<script lang="ts">
  import { onMount } from "svelte";
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
  } from "lucide-svelte";
  import { BatchAddEvents } from "$lib/components/events";
  import * as Modal from "$lib/components/ui/modal";
  import { Root } from "$lib/components/ui/scroll-area";
  // import { eventStore } from "$lib/stores/event";

  let viewMode: "table" | "card" = $state("card");
  let searchTerm = "";
  let showBatchAddModal = $state(false);

  // 订阅事件数据
  let events: any[] = [];
  let listLoading = false;
  let error: string | null = null;
  let filteredEvents: any[] = $state([]);
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

  $effect(() => {
    filteredEvents = events.filter((e) =>
      e.title?.toLowerCase().includes(searchTerm.toLowerCase())
    );
  });
</script>

<div class="p-6">
  <div class="flex justify-between items-center mb-2">
    <div class="flex items-center gap-2">
      <h1 class="text-2xl font-semibold">Week MAY 7 - MAY 13</h1>
      <button class="btn btn-ghost btn-sm p-1">
        <ChevronDown class="w-5 h-5" />
      </button>
    </div>
    <div class="flex items-center gap-4">
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
      <div class="dropdown dropdown-end">
        <button tabindex="0" class="btn btn-neutral btn-sm">
          <Plus class="w-4 h-4" />
          Create
          <ChevronDown class="w-4 h-4" />
        </button>
        <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
        {#if !showBatchAddModal}
        <ul
          tabindex="0"
          class="dropdown-content z-[1] menu p-2 shadow-2xl bg-base-300 rounded-xl w-56"
        >
          <li>
            <button
              class="hover:bg-base-300 active:bg-primary active:text-primary-content"
            >
              <PenTool class="w-4 h-4" /> 新建事件
            </button>
          </li>
          <li>
            <button
              class="hover:bg-base-300"
              onclick={() => {
                showBatchAddModal = true;
              }}
            >
              <FileTextIcon class="w-4 h-4" /> 批量添加
            </button>
          </li>
          <li>
            <a class="hover:bg-base-300">
              <Presentation class="w-4 h-4 text-orange-500" /> Slides
            </a>
          </li>
          <li>
            <a class="hover:bg-base-300 flex justify-between">
              <div>
                <Zap class="w-4 h-4 text-pink-500 inline-block mr-2" /> Buzz
              </div>
              <span class="badge badge-sm badge-info">Beta</span>
            </a>
          </li>
          <li>
            <a class="hover:bg-base-300 flex justify-between">
              <div>
                <Globe class="w-4 h-4 text-green-500 inline-block mr-2" /> Site
              </div>
              <span class="badge badge-sm badge-info">Beta</span>
            </a>
          </li>
          <div class="divider my-1"></div>
          <li>
            <a class="hover:bg-base-300">
              <UploadCloud class="w-4 h-4" /> Import
            </a>
          </li>
        </ul>
        {/if}
      </div>
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
  {:else if filteredEvents.length === 0}
    <div class="text-center text-base-content/60">暂无事件</div>
  {:else if viewMode === "table"}
    <div class="overflow-x-auto">
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
          {#each filteredEvents as event (event.$id)}
            <tr>
              <td>{event.title}</td>
              <td>{event.date || "-"}</td>
              <td>{event.location || "-"}</td>
              <td>{event.user_id || "-"}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {:else}
    <div
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
    >
      {#each filteredEvents as event (event.$id)}
        <div
          class="card bg-base-200 shadow-md rounded-xl hover:shadow-xl coursor-pointer
           hover:ring-primary hover:ring-offset-2
           hover:bg-base-300 transition-all duration-200 ease-in-out"
        >
          <figure
            class="overflow-hidden h-32 bg-base-300 flex items-center justify-center"
          >
            <!-- <img src={event.image || '/static/favicon.png'} alt="event cover" class="object-cover w-full h-full" /> -->
          </figure>
          <div class="card-body">
            <span class="text-sm">{event.title}</span>
            <!-- <p class="text-sm text-base-content/70">
              {event.date || "-"} | {event.location || "-"}
            </p> -->
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
<Modal.Root bind:open={showBatchAddModal}>
  <Modal.Content>
    <BatchAddEvents />
  </Modal.Content>
</Modal.Root>
