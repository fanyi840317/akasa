<script lang="ts">
  import { Globe } from "lucide-svelte";
  import EventSidebarCards from "$lib/components/events/event-sidebar-cards.svelte";
  import EventStatsSidebar from "$lib/components/events/event-stats-sidebar.svelte";
  import type { Event } from "$lib/types/event";
  
  // 模拟事件数据
  const mockEvents: Event[] = [
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
    },
    {
      $id: 'mock4',
      title: '古城府密室发现',
      content: '考古队在古城府遗址发现的密室，内有不明文字和图案。',
      cover: JSON.stringify({ url: 'https://images.unsplash.com/photo-1461988320302-91bde64fc8e4' }),
      tags: ['古迹', '密室'],
      categories: ['all'],
      date: new Date().toISOString(),
      user_id: 'user4',
      creator_name: '考古学家',
      creator_avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=ancient'
    },
    {
      $id: 'mock5',
      title: '天空不明飞行物',
      content: '多人目击的天空不明飞行物，移动速度超过已知飞行器。',
      cover: JSON.stringify({ url: 'https://images.unsplash.com/photo-1419242902214-272b3f66ee7a' }),
      tags: ['天空', 'UFO'],
      categories: ['all'],
      date: new Date().toISOString(),
      user_id: 'user5',
      creator_name: '天文爱好者',
      creator_avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=sky'
    }
  ];
  
  // 处理卡片点击
  function handleEventClick(event: Event) {
    alert(`点击了事件: ${event.title}`);
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 p-8">
  <!-- 侧边栏事件卡片 -->
  <EventSidebarCards events={mockEvents} onEventClick={handleEventClick} />
  
  <!-- 侧边栏统计卡片 -->
  <EventStatsSidebar events={mockEvents} title="环境数据" />
  
  <!-- 主要内容 -->
  <div class="container mx-auto mt-20 flex flex-col items-center justify-center">
    <h1 class="text-5xl font-bold mb-4 text-gray-800 dark:text-white">保护地球</h1>
    <p class="text-gray-600 dark:text-gray-300 max-w-xl text-center mb-8">
      每秒钟都有超过一英亩的雨林被砍伐。从全球变暖到物种灭绝，森林砍伐的后果正在逐渐显现。
    </p>
    
    <div class="relative w-[500px] h-[500px] flex items-center justify-center">
      <div class="absolute inset-0 rounded-full bg-gradient-to-br from-blue-100 to-blue-300 dark:from-blue-900 dark:to-blue-700 opacity-20 blur-xl"></div>
      <div class="relative w-[400px] h-[400px]">
        <Globe class="w-full h-full text-blue-500 dark:text-blue-400" />
      </div>
    </div>
    
    <button class="mt-8 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex items-center gap-2 transition-colors">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
      观看视频
    </button>
  </div>
</div>
