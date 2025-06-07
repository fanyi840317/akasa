<script lang="ts">
  import { ChartBar, Users, Clock, Activity, Zap } from "lucide-svelte";
  import StatsCornerCards from "$lib/components/ui/stats/stats-corner-cards.svelte";
  import BorderBeam from "$lib/components/ui/background/border-beam.svelte";
  
  // 自定义统计数据
  const customStats = [
    { 
      title: "事件总数", 
      value: "128", 
      icon: ChartBar,
      color: "purple" 
    },
    { 
      title: "活跃用户", 
      value: "256", 
      icon: Users,
      color: "blue" 
    },
    { 
      title: "最近更新", 
      value: "5分钟前", 
      icon: Clock,
      color: "green" 
    },
    { 
      title: "热度指数", 
      value: "极高", 
      icon: Activity,
      color: "orange" 
    },
    { 
      title: "新增事件", 
      value: "+12", 
      icon: Zap,
      color: "red" 
    }
  ];
</script>

<div class="min-h-screen bg-background p-8">
  <!-- 右上角统计卡片 -->
  <StatsCornerCards stats={customStats} />
  
  <!-- 主要内容 -->
  <div class="container mx-auto mt-20">
    <h1 class="text-3xl font-bold mb-8 text-center">统计卡片示例</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- 示例卡片 1 -->
      <article class="flex max-w-xl flex-col items-start justify-between relative rounded-3xl p-7 border border-gray-700/70 bg-background">
        <BorderBeam size={150} duration={12} />
        <div class="flex items-center gap-x-4 text-xs">
          <time datetime="2024-06-07" class="text-gray-300">June 7, 2024</time>
          <a href="#" class="relative z-10 rounded-full bg-transparent px-3 py-1.5 font-medium text-gray-200 border border-gray-100">
            Svelte-Components
          </a>
        </div>
        <div class="group relative">
          <h3 class="mt-3 text-lg font-semibold leading-6 text-gray-200 group-hover:text-gray-50">
            <a href="#">
              <span class="absolute inset-0"></span>
              Animation Svelte
            </a>
          </h3>
          <p class="mt-5 line-clamp-3 text-sm leading-6 text-gray-600">
            Welcome to Svelte Animation website. This website includes Quality
            Tailwind CSS and Framer Motion Components. Inspired from 
            <span class="text-gray-300 underline underline-offset-2">Magic UI</span>
            and <span class="text-gray-300 underline underline-offset-2">Luxe</span>
            Components.
          </p>
        </div>
        <div class="relative mt-8 flex items-center gap-x-4">
          <img src="https://avatars.githubusercontent.com/u/93428946?v=4" alt="bhide" class="h-10 w-10 rounded-full bg-gray-50" />
          <div class="text-sm leading-5">
            <p class="font-semibold text-white">
              <a href="#">
                <span class="absolute inset-0"></span>
                Sikandar Bhide
              </a>
            </p>
            <p class="text-gray-500">Svelte Developer</p>
          </div>
        </div>
      </article>
      
      <!-- 示例卡片 2 -->
      <article class="flex max-w-xl flex-col items-start justify-between relative rounded-3xl p-7 border border-gray-700/70 bg-background">
        <BorderBeam size={150} duration={12} />
        <div class="flex items-center gap-x-4 text-xs">
          <time datetime="2024-06-10" class="text-gray-300">June 10, 2024</time>
          <a href="#" class="relative z-10 rounded-full bg-transparent px-3 py-1.5 font-medium text-gray-200 border border-gray-100">
            神秘事件
          </a>
        </div>
        <div class="group relative">
          <h3 class="mt-3 text-lg font-semibold leading-6 text-gray-200 group-hover:text-gray-50">
            <a href="#">
              <span class="absolute inset-0"></span>
              深山密林奇遇
            </a>
          </h3>
          <p class="mt-5 line-clamp-3 text-sm leading-6 text-gray-600">
            在深山密林中发现的不明现象，多人目击光怪物体。据当地居民描述，这种现象已经持续了数月，但一直未被官方记录。
          </p>
        </div>
        <div class="relative mt-8 flex items-center gap-x-4">
          <div class="h-10 w-10 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-300">
            <Users class="h-5 w-5" />
          </div>
          <div class="text-sm leading-5">
            <p class="font-semibold text-white">
              <a href="#">
                <span class="absolute inset-0"></span>
                探索小组
              </a>
            </p>
            <p class="text-gray-500">5名成员</p>
          </div>
        </div>
      </article>
      
      <!-- 示例卡片 3 -->
      <article class="flex max-w-xl flex-col items-start justify-between relative rounded-3xl p-7 border border-gray-700/70 bg-background">
        <BorderBeam size={150} duration={12} />
        <div class="flex items-center gap-x-4 text-xs">
          <time datetime="2024-06-12" class="text-gray-300">June 12, 2024</time>
          <a href="#" class="relative z-10 rounded-full bg-transparent px-3 py-1.5 font-medium text-gray-200 border border-gray-100">
            数据分析
          </a>
        </div>
        <div class="group relative">
          <h3 class="mt-3 text-lg font-semibold leading-6 text-gray-200 group-hover:text-gray-50">
            <a href="#">
              <span class="absolute inset-0"></span>
              事件热度分析报告
            </a>
          </h3>
          <p class="mt-5 line-clamp-3 text-sm leading-6 text-gray-600">
            根据最近一个月的数据分析，神秘事件的报告数量增长了32%，用户参与度提升了45%，这表明公众对超自然现象的关注度正在显著提高。
          </p>
        </div>
        <div class="relative mt-8 flex items-center gap-x-4">
          <div class="h-10 w-10 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-300">
            <ChartBar class="h-5 w-5" />
          </div>
          <div class="text-sm leading-5">
            <p class="font-semibold text-white">
              <a href="#">
                <span class="absolute inset-0"></span>
                数据团队
              </a>
            </p>
            <p class="text-gray-500">月度报告</p>
          </div>
        </div>
      </article>
    </div>
  </div>
</div>
