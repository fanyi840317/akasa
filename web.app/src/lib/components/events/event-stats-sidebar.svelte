<script lang="ts">
  import { fly } from "svelte/transition";
  import { ChartBar, Users, Clock, Activity, Globe } from "lucide-svelte";
  import type { Event } from "$lib/types/event";
  
  export let events: Event[] = [];
  export let title: string = "统计信息";
  
  // 计算统计数据
  $: totalEvents = events.length;
  $: recentEvents = events.filter(e => {
    const date = new Date(e.date);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays <= 7; // 最近7天的事件
  }).length;
  
  // 获取最近更新时间
  $: lastUpdated = events.length > 0 
    ? getLastUpdatedText(events.sort((a, b) => 
        new Date(b.$updatedAt || b.date).getTime() - 
        new Date(a.$updatedAt || a.date).getTime()
      )[0].$updatedAt || events[0].date) 
    : "无数据";
  
  // 计算热度指数
  $: heatIndex = calculateHeatIndex(events);
  
  // 统计数据
  $: stats = [
    { 
      title: "事件总数", 
      value: totalEvents.toString(), 
      icon: ChartBar,
      color: "primary" 
    },
    { 
      title: "最近新增", 
      value: recentEvents.toString(), 
      icon: Activity,
      color: "green" 
    },
    { 
      title: "最近更新", 
      value: lastUpdated, 
      icon: Clock,
      color: "blue" 
    },
    { 
      title: "热度指数", 
      value: heatIndex.text, 
      icon: Activity,
      color: heatIndex.color 
    }
  ];
  
  // 计算最近更新时间文本
  function getLastUpdatedText(dateStr: string): string {
    const date = new Date(dateStr);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffMinutes = Math.floor(diffTime / (1000 * 60));
    const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffMinutes < 60) {
      return `${diffMinutes}分钟前`;
    } else if (diffHours < 24) {
      return `${diffHours}小时前`;
    } else {
      return `${diffDays}天前`;
    }
  }
  
  // 计算热度指数
  function calculateHeatIndex(_events: Event[]): { text: string; color: string } {
    // 这里可以根据实际需求实现更复杂的热度计算逻辑
    const recentCount = recentEvents;
    
    if (recentCount >= 10) {
      return { text: "极高", color: "red" };
    } else if (recentCount >= 5) {
      return { text: "高", color: "orange" };
    } else if (recentCount >= 2) {
      return { text: "中", color: "blue" };
    } else {
      return { text: "低", color: "green" };
    }
  }
</script>

<div class="fixed bottom-4 right-4 z-50 w-[280px]">
  <div class="text-base font-medium text-gray-800 dark:text-gray-200 mb-2 px-2">
    <span>{title}</span>
  </div>
  
  <div class="overflow-hidden rounded-xl bg-white/10 dark:bg-black/10 backdrop-blur-md border border-gray-200/20 dark:border-gray-800/20">
    <div class="grid grid-cols-2 gap-px bg-gray-200/20 dark:bg-gray-800/20">
      {#each stats as stat, i}
        <div 
          in:fly={{ y: 10, delay: i * 100, duration: 300 }}
          class="bg-white/30 dark:bg-black/30 p-3"
        >
          <div class="flex flex-col">
            <div class="flex items-center gap-2 mb-1">
              <svelte:component this={stat.icon} class="h-3.5 w-3.5 text-gray-500 dark:text-gray-400" />
              <p class="text-xs text-gray-500 dark:text-gray-400">{stat.title}</p>
            </div>
            <p class="text-lg font-semibold text-gray-800 dark:text-gray-200">{stat.value}</p>
          </div>
        </div>
      {/each}
    </div>
  </div>
</div>
