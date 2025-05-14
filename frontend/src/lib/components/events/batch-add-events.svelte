<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchEventsByRange } from '../../services/eventService';

  let recentEvents: string | any[] = [];
  let selectedEvent: any = null;
  let startDate = '';
  let endDate = '';
  let loading = false;
  let error = '';

  async function queryEvents() {
    loading = true;
    error = '';
    try {
      recentEvents = await fetchEventsByRange(startDate, endDate);
      if (recentEvents.length > 0) {
        selectEvent(recentEvents[0]);
      } else {
        selectedEvent = null;
      }
    } catch (e) {
      error = '查询失败，请稍后重试。';
    } finally {
      loading = false;
    }
  }

  function selectEvent(event: any) {
    selectedEvent = event;
    // 假设事件详情已包含来源信息
    if (!selectedEvent.details) {
      selectedEvent.details = {
        location: event.location || '未知地点',
        eventDescription: event.eventDescription || '事件正在调查中...',
        relatedPeople: event.relatedPeople || ['调查员A', '目击者B'],
        timeline: event.timeline || [
          { time: event.date + ' 10:00', description: '首次报告' },
          { time: event.date + ' 14:00', description: '初步调查' },
        ],
        summary: event.summary || '这是一个神秘的事件，充满了未知。',
        source: event.source || '未知来源',
        sourceUrl: event.sourceUrl || ''
      };
    }
  }

  onMount(() => {
    const today = new Date();
    const lastWeek = new Date();
    lastWeek.setDate(today.getDate() - 7);
    startDate = lastWeek.toISOString().slice(0, 10);
    endDate = today.toISOString().slice(0, 10);
    queryEvents();
  });
</script>

<div class="flex flex-col md:flex-row gap-4 p-4 h-[60vh] max-h-[700px]">
  <!-- 左侧：时间范围选择与事件列表 -->
  <div class="w-full md:w-1/3 bg-base-100 p-4 rounded-lg shadow overflow-y-auto">
    <h4 class="text-lg font-semibold mb-3">最近一周的神秘事件</h4>
    <div class="flex gap-2 mb-3 items-center">
      <label>起始日期：</label>
      <input type="date" bind:value={startDate} class="input input-bordered input-sm" />
      <label>结束日期：</label>
      <input type="date" bind:value={endDate} class="input input-bordered input-sm" />
      <button class="btn btn-primary btn-sm" on:click={queryEvents} disabled={loading}>查询</button>
    </div>
    {#if error}
      <div class="text-error mb-2">{error}</div>
    {/if}
    {#if loading}
      <div class="text-base-content/60">正在加载...</div>
    {:else if recentEvents.length > 0}
      <ul class="menu p-0">
        {#each recentEvents as event (event.id)}
          <li>
            <a 
              class="block p-2 rounded-md {selectedEvent && selectedEvent.id === event.id ? 'bg-primary text-primary-content' : 'hover:bg-base-200'}"
              on:click={() => selectEvent(event)}
            >
              <div class="font-medium">{event.title}</div>
              <div class="text-xs text-base-content/70">{event.date}</div>
              <div class="text-xs text-base-content/50">来源：{event.source}</div>
            </a>
          </li>
        {/each}
      </ul>
    {:else}
      <p class="text-base-content/60">暂无最近事件。</p>
    {/if}
  </div>

  <!-- 右侧：事件详情 -->
  <div class="w-full md:w-2/3 bg-base-100 p-6 rounded-lg shadow overflow-y-auto">
    {#if selectedEvent && selectedEvent.details}
      <h3 class="text-xl font-bold mb-4">{selectedEvent.title} - 详情</h3>
      <div class="mb-4">
        <h5 class="font-semibold text-base-content/80">地点:</h5>
        <p>{selectedEvent.details.location}</p>
      </div>
      <div class="mb-4">
        <h5 class="font-semibold text-base-content/80">事件描述:</h5>
        <p>{selectedEvent.details.eventDescription}</p>
      </div>
      <div class="mb-4">
        <h5 class="font-semibold text-base-content/80">相关人物:</h5>
        <ul class="list-disc list-inside ml-4">
          {#each selectedEvent.details.relatedPeople as person}
            <li>{person}</li>
          {/each}
        </ul>
      </div>
      <div class="mb-4">
        <h5 class="font-semibold text-base-content/80">时间线:</h5>
        <ul class="steps steps-vertical lg:steps-horizontal">
          {#each selectedEvent.details.timeline as item}
            <li class="step step-primary">
              <div class="text-left">
                <div class="font-semibold">{item.time}</div>
                <div>{item.description}</div>
              </div>
            </li>
          {/each}
        </ul>
      </div>
      <div class="mb-4">
        <h5 class="font-semibold text-base-content/80">简介:</h5>
        <p>{selectedEvent.details.summary}</p>
      </div>
      <div>
        <h5 class="font-semibold text-base-content/80">来源:</h5>
        {#if selectedEvent.details.sourceUrl}
          <a class="link link-primary" href={selectedEvent.details.sourceUrl} target="_blank">{selectedEvent.details.source}</a>
        {:else}
          <span>{selectedEvent.details.source}</span>
        {/if}
      </div>
    {:else if selectedEvent}
      <p class="text-base-content/60">正在加载事件详情...</p>
    {:else}
      <p class="text-base-content/60">请在左侧选择一个事件查看详情。</p>
    {/if}
  </div>
</div>