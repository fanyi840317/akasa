<script lang="ts">
  import { ChevronDown } from "lucide-svelte";
  import EventList from "$lib/components/events/event-list.svelte";
  import type { Event } from "$lib/types/event";
  import { onMount } from "svelte";
  import { eventStore } from "$lib/stores/event";
  import { auth } from "$lib/stores/auth";
  import { goto } from "$app/navigation";
  import ScrollArea from "$lib/components/ui/scroll-area/scroll-area.svelte";
  import {InputArea, ChatHistoryList} from "$lib/components/ai";

  // 示例历史对话数据
  const chatHistories = [
    {
      id: '1',
      title: '关于项目架构的讨论',
      summary: '讨论了前端组件架构设计，包括状态管理和组件通信方式的优化建议...',
      messageCount: 12,
      timestamp: '2小时前'
    },
    {
      id: '2',
      title: 'API接口设计问题',
      summary: '关于RESTful API设计规范和错误处理机制的讨论，涉及状态码和响应格式...',
      messageCount: 8,
      timestamp: '1天前'
    },
    {
      id: '3',
      title: '数据库优化策略',
      summary: '探讨了数据库查询优化、索引设计和缓存策略，提升系统整体性能...',
      messageCount: 15,
      timestamp: '3天前'
    },
    {
      id: '4',
      title: '用户体验改进建议',
      summary: '分析了当前界面的用户体验问题，提出了交互优化和视觉设计改进方案...',
      messageCount: 6,
      timestamp: '1周前'
    }
  ];

  function handleChatHistoryClick(history: any) {
    console.log('点击了历史对话:', history);
    // 这里可以添加打开历史对话的逻辑
  }

  let events: Event[] = $derived($eventStore.events);
  onMount(async () => {
    events = await eventStore.fetchEvents($auth.user?.$id);
  });
  function handEventClick(event: Event) {
    goto(`/console/events/${event.$id}`);
  }
</script>

<div
  class="mx-auto px-6 pt-6 xs:px-8 sm:px-12 lg:px-6  flex flex-col
   justify-start  w-full"
  style="max-width: 1608px;"
>
  <!-- <div class="flex flex-col text-center gap-4 mb-14">
    <h1 class="text-3xl font-extrabold sm:text-4xl lg:text-5xl" role="heading">
      Events
    </h1>
    <p class="text-base-content/50">A space to manage and organize your events</p>
    
  </div> -->

  <div class="flex flex-col justify-center items-center -ml-30">
    <div class="flex items-center gap-2">
      <h1 class="text-2xl font-semibold">Week MAY 7 - MAY 13</h1>
      <button class="btn btn-ghost btn-sm p-1">
        <ChevronDown class="w-5 h-5" />
      </button>
    </div>
    <p class="text-xs text-base-content/60 mb-10">
      Last Updated: May 12, 2025 12:06 pm
    </p>
    <!-- <div class="flex items-center gap-4">
      <span class="text-sm text-base-content/50">42182 users</span>
      <div class="form-control">
        <input
          type="text"
          placeholder="filter by username"
          class="input input-sm w-full max-w-xs"
        />
      </div>
    </div> -->
  </div>
  <!-- <p class="text-xs text-base-content/60 mb-10">
    Last Updated: May 12, 2025 12:06 pm
  </p> -->
  <ScrollArea class="h-[calc(100vh-298px)]">
    <EventList {events} onclick={handEventClick} />
  </ScrollArea>
  <div class="flex-center">
    <div class="flex gap-4 items-start">
      <!-- InputArea -->
      <div class="w-[560px] py-4">
        <InputArea></InputArea>
      </div>
      
      <!-- 历史聊天卡片 -->
      <ChatHistoryList 
        histories={chatHistories} 
        onCardClick={handleChatHistoryClick}
      />
    </div>
  </div>

</div>
