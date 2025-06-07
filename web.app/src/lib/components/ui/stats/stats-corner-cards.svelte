<script lang="ts">
  import { fly } from "svelte/transition";
  import { ChartBar, Users, Clock, Activity } from "lucide-svelte";
  import BorderBeam from "$lib/components/ui/background/border-beam.svelte";
  
  export let stats = [
    { 
      title: "事件总数", 
      value: "42", 
      icon: ChartBar,
      color: "purple" 
    },
    { 
      title: "活跃用户", 
      value: "128", 
      icon: Users,
      color: "blue" 
    },
    { 
      title: "最近更新", 
      value: "2小时前", 
      icon: Clock,
      color: "green" 
    },
    { 
      title: "热度指数", 
      value: "高", 
      icon: Activity,
      color: "orange" 
    }
  ];
  
  // 最多显示的统计卡片数量
  const MAX_VISIBLE = 4;
  
  // 颜色映射
  const colorMap = {
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
</script>

<div class="fixed top-4 right-4 z-50 flex flex-col gap-2 max-w-[200px]">
  <div class="text-xs text-gray-400 mb-1 px-2 flex items-center justify-end gap-1">
    <ChartBar class="h-3 w-3" />
    <span>统计信息</span>
  </div>
  
  {#each stats.slice(0, MAX_VISIBLE) as stat, i}
    <button 
      type="button"
      in:fly={{ y: -20, delay: i * 100, duration: 300 }}
      class="w-full text-left bg-transparent border-none p-0 m-0 focus:outline-none focus-visible:ring-2 focus-visible:ring-purple-500/50 rounded-xl"
    >
      <article class="relative rounded-xl border bg-black/60 backdrop-blur-sm overflow-hidden transition-all duration-300 hover:shadow-[0_0_15px_rgba(99,68,245,0.3)] hover:translate-y-[-2px] hover:scale-[1.02]"
        class:border-purple-500/30={stat.color === 'purple'}
        class:border-blue-500/30={stat.color === 'blue'}
        class:border-green-500/30={stat.color === 'green'}
        class:border-orange-500/30={stat.color === 'orange'}
        class:border-red-500/30={stat.color === 'red'}
      >
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
    </button>
  {/each}
</div>
