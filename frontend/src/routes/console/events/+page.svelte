<script lang="ts">
  import { onMount } from "svelte";
  import { eventStore } from "$lib/stores/event";
  import { derived } from "svelte/store";
  import { ChevronDown, Grid, List } from "lucide-svelte";

  let viewMode: "table" | "card" = "table";
  let searchTerm = "";

  // 订阅事件数据
  let events: any[] = [];
  let listLoading = false;
  let error: string | null = null;
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
  $: filteredEvents = events.filter((e) =>
    e.title?.toLowerCase().includes(searchTerm.toLowerCase())
  );
</script>

<div class="p-6">
  <!-- <div class="flex justify-between items-center mb-4">
    <div class="flex items-center gap-2">
      <h1 class="text-2xl font-semibold">Events</h1>
    </div>
    <div class="flex items-center gap-4 mb-6">
        <input type="text" placeholder="搜索事件标题" class="input input-sm w-full max-w-xs" bind:value={searchTerm} />
        <div class="flex items-center gap-2">
          <div class="flex items-center gap-2">
            <a role="tab" class="tab tabs-box {viewMode==='table' ? 'tab-active' : ''}" on:click={() => viewMode='table'}>
                <span class="tooltip tooltip-bottom" data-tip="表格视图"><List class="w-5 h-5" /></span>
            </a>
            <a role="tab" class="tab tabs-box {viewMode==='card' ? 'tab-active' : ''}" on:click={() => viewMode='card'}>
                <span class="tooltip tooltip-bottom" data-tip="卡片视图"><Grid class="w-5 h-5" /></span>
         
            </a>
          </div>
        </div>
      </div>
  </div> -->
  <div class="flex justify-between items-center mb-4">
    <div class="flex items-center gap-2">
      <h1 class="text-2xl font-semibold">Week MAY 7 - MAY 13</h1>
      <button class="btn btn-ghost btn-sm p-1">
        <ChevronDown class="w-5 h-5" />
      </button>
    </div>
    <div class="flex items-center gap-4">
      <div class="tabs tabs-lift">
        <label class="tab">
          <input type="radio" name="my_tabs_4" checked={viewMode === 'table'} on:change={() => viewMode = 'table'} />
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4 me-2"><path stroke-linecap="round" stroke-linejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347a1.125 1.125 0 0 1-1.667-.986V5.653Z" /></svg>
          表格视图
        </label>
        <label class="tab">
          <input type="radio" name="my_tabs_4" checked={viewMode === 'card'} on:change={() => viewMode = 'card'} />
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4 me-2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.182 15.182a4.5 4.5 0 0 1-6.364 0M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0ZM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75Zm-.375 0h.008v.015h-.008V9.75Zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75Zm-.375 0h.008v.015h-.008V9.75Z" /></svg>
          卡片视图
        </label>
      </div>
      <!-- <div class="form-control">
        <input
          type="text"
          placeholder="filter by username"
          class="input input-sm w-full max-w-xs"
          bind:value={searchTerm}
        />
      </div> -->
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
        <div class="card bg-base-200 shadow-md">
          <figure class="rounded-t-xl overflow-hidden h-32 bg-base-300 flex items-center justify-center">
            <img src={event.image || '/static/favicon.png'} alt="event cover" class="object-cover w-full h-full" />
          </figure>
          <div class="card-body h-[60px]">
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
