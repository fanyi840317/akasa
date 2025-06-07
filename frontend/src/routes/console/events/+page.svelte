<script lang="ts">
  import { ChevronDown, PlusIcon, SparklesIcon } from "lucide-svelte";
  import { EventCardGrid } from "$lib/components/events";
  import type { Event } from "$lib/types/event";
  import { onMount } from "svelte";
  import { eventStore } from "$lib/stores/event";
  import { auth } from "$lib/stores/auth";
  import { goto } from "$app/navigation";
  import ScrollArea from "$lib/components/ui/scroll-area/scroll-area.svelte";
  import { InputArea, ChatHistoryList } from "$lib/components/ai";
  import DraggableChatDialog from "$lib/components/ai/draggable-chat-dialog.svelte";
  import EventList from "$lib/components/events/event-list.svelte";

  // 示例历史对话数据
  const chatHistories = [
    {
      id: "1",
      title: "关于项目架构的讨论",
      summary:
        "讨论了前端组件架构设计，包括状态管理和组件通信方式的优化建议...",
      messageCount: 12,
      timestamp: "2小时前",
    },
    {
      id: "2",
      title: "API接口设计问题",
      summary:
        "关于RESTful API设计规范和错误处理机制的讨论，涉及状态码和响应格式...",
      messageCount: 8,
      timestamp: "1天前",
    },
    {
      id: "3",
      title: "数据库优化策略",
      summary: "探讨了数据库查询优化、索引设计和缓存策略，提升系统整体性能...",
      messageCount: 15,
      timestamp: "3天前",
    },
    {
      id: "4",
      title: "用户体验改进建议",
      summary:
        "分析了当前界面的用户体验问题，提出了交互优化和视觉设计改进方案...",
      messageCount: 6,
      timestamp: "1周前",
    },
  ];

  function handleChatHistoryClick(history: any) {
    console.log("点击了历史对话:", history);
    // 这里可以添加打开历史对话的逻辑
  }

  let events: Event[] = $derived($eventStore.events);
  onMount(async () => {
    events = await eventStore.fetchEvents($auth.user?.$id);
  });
  function handEventClick(event: Event) {
    goto(`/console/events/${event.$id}`);
  }

  // AI对话窗口相关
  let showChatDialog = $state(false);
  let dialogX = $state(window.innerWidth / 2 - 225); // 居中显示
  let dialogY = $state(100);

  function handleUseAI() {
    showChatDialog = true;
  }

  function handleCreate(
    event: MouseEvent & { currentTarget: EventTarget & HTMLButtonElement }
  ) {
    event.currentTarget.blur();
    goto("/console/events/new");
  }
</script>

<div
  class="mx-auto flex flex-col justify-start w-full overflow-hidden p-14 h-content"
>
<ScrollArea class="h-full">
  <EventCardGrid {events} onEventClick={handEventClick} />
   <!-- <EventList events={events} onEventClick={handEventClick} /> -->
</ScrollArea>
</div>

