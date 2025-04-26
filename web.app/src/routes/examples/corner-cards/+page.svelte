<script lang="ts">
  import { ChartBar, Users, Clock, Activity, Sparkles } from "lucide-svelte";
  import BorderBeam from "$lib/components/ui/background/border-beam.svelte";
  import { fly } from "svelte/transition";
  import type { Event } from "$lib/types/event";
  
  // 模拟事件数据
  const mockEvents = [
    {
      $id: 'mock1',
      title: '神秘森林事件',
      content: '在深山密林中发现的不明现象，多人目击光怪物体。',
      cover: JSON.stringify({ url: 'https://images.unsplash.com/photo-1448375240586-882707db888b' }),
      tags: ['森林', '超自然'],
      categories: ['all'],
      date: new Date().toISOString(),
      user_id: 'user1',
      creator_name: '探索者',
      creator_avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=explorer'
    },
    {
      $id: 'mock2',
      title: '海底异常信号',
      content: '深海探测器捕捉到的不明声波信号，可能来自未知生物。',
      cover: JSON.stringify({ url: 'https://images.unsplash.com/photo-1551244072-5d12893278ab' }),
      tags: ['海洋', '信号'],
      categories: ['all'],
      date: new Date().toISOString(),
      user_id: 'user2',
      creator_name: '海洋学家',
      creator_avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=ocean'
    },
    {
      $id: 'mock3',
      title: '沙漠奇异光点',
      content: '沙漠中出现的不明光点，夜间移动并改变形状。',
      cover: JSON.stringify({ url: 'https://images.unsplash.com/photo-1509316785289-025f5b846b35' }),
      tags: ['沙漠', '光点'],
      categories: ['all'],
      date: new Date().toISOString(),
      user_id: 'user3',
      creator_name: '沙漠向导',
      creator_avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=desert'
    }
  ];
  
  // 统计数据
  const stats = [
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
  
  // 最多显示的卡片数量
  const MAX_VISIBLE = 3;
  
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
  
  // 获取随机默认封面图
  function getRandomDefaultCover(): string {
    const defaultCovers = [
      "/images/cover/c1.webp",
      "/images/cover/c2.webp",
      "/images/cover/c3.webp",
    ];
    const randomIndex = Math.floor(Math.random() * defaultCovers.length);
    return defaultCovers[randomIndex];
  }
  
  // 处理封面图片
  function getCoverUrl(event: Event): string {
    if (!event.cover) return getRandomDefaultCover();
    
    try {
      // 检查是否是有效的 URL
      if (typeof event.cover === 'string') {
        if (event.cover.startsWith("http")) {
          return event.cover;
        } else {
          // 尝试解析 JSON 格式的封面数据
          const coverData = JSON.parse(event.cover);
          return coverData.url || getRandomDefaultCover();
        }
      }
      return getRandomDefaultCover();
    } catch (e) {
      return getRandomDefaultCover();
    }
  }
  
  // 处理卡片点击
  function handleEventClick(event: Event) {
    alert(`点击了事件: ${event.title}`);
  }
</script>

<div class="min-h-screen bg-background p-8">
  <!-- 右上角事件卡片 -->
  <div class="fixed top-4 right-4 z-50 flex flex-col gap-3 max-w-[280px]">
    <div class="text-xs text-gray-400 mb-1 px-2 flex items-center gap-1">
      <Sparkles class="h-3 w-3" />
      <span>身边的神秘事件</span>
    </div>
    {#each mockEvents.slice(0, MAX_VISIBLE) as event, i}
      <button 
        type="button"
        in:fly={{ y: -20, delay: i * 100, duration: 300 }}
        class="w-full text-left bg-transparent border-none p-0 m-0 focus:outline-none focus-visible:ring-2 focus-visible:ring-purple-500/50 rounded-xl"
        on:click={() => handleEventClick(event)}
        on:keydown={(e) => e.key === 'Enter' && handleEventClick(event)}
      >
        <article class="relative rounded-2xl border border-gray-700/70 bg-black/60 backdrop-blur-sm overflow-hidden transition-all duration-300 hover:border-purple-500/50 hover:shadow-[0_0_15px_rgba(99,68,245,0.3)] hover:translate-y-[-4px] hover:scale-[1.02]">
          <BorderBeam size={80} duration={10} />
          <div class="p-4">
            <div class="relative w-full h-20 rounded-lg overflow-hidden mb-3">
              <img 
                src={getCoverUrl(event)} 
                alt={event.title}
                class="w-full h-full object-cover transition-transform duration-500 hover:scale-110"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            </div>
            
            <h3 class="text-base font-medium text-gray-200 line-clamp-1 hover:text-purple-300 transition-colors">
              {event.title}
            </h3>
            
            <div class="flex gap-2 mt-2 flex-wrap">
              {#if event.tags && event.tags.length > 0}
                {#each event.tags.slice(0, 2) as tag}
                  <span class="px-2 py-0.5 text-xs rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300">
                    {tag}
                  </span>
                {/each}
                {#if event.tags.length > 2}
                  <span class="px-2 py-0.5 text-xs rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300">
                    +{event.tags.length - 2}
                  </span>
                {/if}
              {/if}
            </div>
          </div>
        </article>
      </button>
    {/each}
  </div>
  
  <!-- 右上角统计卡片 -->
  <div class="fixed top-4 left-4 z-50 flex flex-col gap-2 max-w-[200px]">
    <div class="text-xs text-gray-400 mb-1 px-2 flex items-center gap-1">
      <ChartBar class="h-3 w-3" />
      <span>统计信息</span>
    </div>
    
    {#each stats.slice(0, MAX_VISIBLE + 1) as stat, i}
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
  
  <!-- 主要内容 -->
  <div class="container mx-auto mt-20">
    <h1 class="text-3xl font-bold mb-8 text-center">右上角卡片示例</h1>
    
    <div class="max-w-2xl mx-auto">
      <article class="flex flex-col items-start justify-between relative rounded-3xl p-7 border border-gray-700/70 bg-background">
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
              右上角卡片组件
            </a>
          </h3>
          <p class="mt-5 text-sm leading-6 text-gray-600">
            这个示例展示了如何在页面右上角显示事件卡片和统计卡片。事件卡片展示了神秘事件的信息，包括标题、标签和封面图片。
            统计卡片则展示了各种统计数据，如事件总数、活跃用户数、最近更新时间和热度指数。
          </p>
          <p class="mt-3 text-sm leading-6 text-gray-600">
            这些卡片使用了BorderBeam组件来创建神秘的边框光效，并且在悬停时有缩放和阴影效果，增强了用户交互体验。
            卡片的设计风格符合整体的神秘主题，使用了深色背景、紫色调和模糊效果。
          </p>
        </div>
        <div class="relative mt-8 flex items-center gap-x-4">
          <div class="h-10 w-10 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-300">
            <Sparkles class="h-5 w-5" />
          </div>
          <div class="text-sm leading-5">
            <p class="font-semibold text-white">
              <a href="#">
                <span class="absolute inset-0"></span>
                神秘事件团队
              </a>
            </p>
            <p class="text-gray-500">UI组件示例</p>
          </div>
        </div>
      </article>
    </div>
  </div>
</div>
