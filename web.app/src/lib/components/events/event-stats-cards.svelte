<script lang="ts">
  import { fly } from "svelte/transition";
  import { ChartBar, Clock, Activity } from "lucide-svelte";
  import BorderBeam from "$lib/components/ui/background/border-beam.svelte";
  import type { Event } from "$lib/types/event";

  export let events: Event[] = [];

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
      color: "purple"
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

  // 最多显示的统计卡片数量
  const MAX_VISIBLE = 4;

  // 颜色映射
  const colorMap: Record<string, string> = {
    purple: "from-purple-500/20 to-purple-500/5 border-purple-500/30 text-purple-300",
    blue: "from-blue-500/20 to-blue-500/5 border-blue-500/30 text-blue-300",
    green: "from-green-500/20 to-green-500/5 border-green-500/30 text-green-300",
    orange: "from-orange-500/20 to-orange-500/5 border-orange-500/30 text-orange-300",
    red: "from-red-500/20 to-red-500/5 border-red-500/30 text-red-300"
  };

  // 获取颜色类
  function getColorClass(color: string): string {
    return colorMap[color] || colorMap.purple;
  }

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

<div class="fixed top-4 right-4 z-50 flex flex-col gap-2 max-w-[200px]">
  <div class="text-xs text-gray-400 mb-1 px-2 flex items-center justify-end gap-1">
    <ChartBar class="h-3 w-3" />
    <span>统计信息</span>
  </div>

  {#each stats.slice(0, MAX_VISIBLE) as stat, i}
    <div
      in:fly={{ y: -20, delay: i * 100, duration: 300 }}
      class="w-full"
    >
      <article class="relative rounded-xl border bg-black/60 backdrop-blur-sm overflow-hidden transition-all duration-300 hover:shadow-[0_0_15px_rgba(99,68,245,0.3)] {stat.color === 'purple' ? 'border-purple-500/30' : ''} {stat.color === 'blue' ? 'border-blue-500/30' : ''} {stat.color === 'green' ? 'border-green-500/30' : ''} {stat.color === 'orange' ? 'border-orange-500/30' : ''} {stat.color === 'red' ? 'border-red-500/30' : ''}">
        <BorderBeam size={60} duration={8} />
        <div class="p-3 bg-gradient-to-br {getColorClass(stat.color)}">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-xs opacity-80">{stat.title}</p>
              <p class="text-lg font-semibold">{stat.value}</p>
            </div>
            <div class="rounded-full bg-black/20 p-2">
              <svelte:component this={stat.icon} class="h-4 w-4" />
            </div>
          </div>
        </div>
      </article>
    </div>
  {/each}
</div>
