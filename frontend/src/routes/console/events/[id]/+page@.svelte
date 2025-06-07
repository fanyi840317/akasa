<script lang="ts">
  import BlockSuiteEditor from "$lib/components/editor/blocksuite-editor.svelte";
  import { EventActionbar, EventPropertyCard } from "$lib/components/events";
  import { page } from "$app/stores";
  import { appStore } from "$lib/stores/app-state";
  import { onDestroy, onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { eventStore } from "$lib/stores/event"; // Added import for eventStore
  import type { Event as EventType } from "$lib/types/event"; // Added import for Event type
  import { get } from "svelte/store"; // Added import for get
  import EventCommentsPanel from "$lib/components/events/event/event-comments-panel.svelte"; // Import the comments panel
  import { fade, fly } from "svelte/transition";
  import { UserAvatar } from "$lib/components/ui/avatar";
  import { auth } from "$lib/stores/auth";
  import CoverCard from "$lib/components/events/event/actionbar-cards/cover-card.svelte";
  import { InputArea } from "$lib/components/ai";
  import { ChevronLeft, ChevronRight, ChevronLeftSquare, ChevronRightSquare, Eye, EyeOff, Save } from "lucide-svelte"; // 导入收缩和预览图标
  import ChatContent from "$lib/components/ai/chat-content.svelte";
  import { Chat } from "@ai-sdk/svelte";
  import type { Message } from "@ai-sdk/svelte";
  import LocationCard from "$lib/components/events/event/property-cards/location-card.svelte";
  import EventTimeLocationEditor from "$lib/components/events/event/event-time-location-editor.svelte";

  // let eventData: any = null; // Replaced by store
  // let loading = true; // Replaced by store
  let eventId: string | undefined; // To store the current event ID
  let lastLoadedEventId: string | undefined | null = $state(null); // To track the last loaded event ID
  let currentEventTitle: string | undefined = $state("New Event");
  // let editorContent: string | undefined = $state(undefined); // To store editor's current content
  // svelte-ignore non_reactive_update
  let editorComponent: BlockSuiteEditor; // Reference to the editor component

  // Subscribe to store's currentEvent and eventLoading
  let currentEvent: EventType | null = $state(null);
  let eventLoading = $state(true);
  let isPropertiesPanelOpen = $state(true); // State for the properties panel
  let isCommentsPanelOpen = $state(false); // State for the comments panel
  let isInputAreaCollapsed = $state(false); // 控制输入区域是否收缩
  let isEditorReadonly = $state(false); // 控制编辑器是否为只读模式
  
  // 为绑定创建响应式变量
  let eventTime = $state<Date | null>(null);
  let eventLocation = $state<any>(null);
  
  // 同步currentEvent的变化到绑定变量
  $effect(() => {
    if (currentEvent) {
      eventTime = currentEvent.date || null;
      eventLocation = currentEvent.location || null;
    } else {
      eventTime = null;
      eventLocation = null;
    }
  });

  const unsubscribeEvent = eventStore.subscribe((store) => {
    currentEvent = store.currentEvent;
    console.log("EventStore currentEvent:", currentEvent);
    eventLoading = store.eventLoading;
    if (currentEvent) {
      currentEventTitle = currentEvent.title;
    }
  });

  // Get event ID from route params
  $effect(() => {
    if ($page.params.id) {
      const newEventId = $page.params.id;
      eventId = newEventId;
      if (newEventId !== "new" && newEventId !== lastLoadedEventId) {
        loadEventData(newEventId);
        lastLoadedEventId = newEventId;
        currentEventTitle = "Loading Event...";
      }
    }
  });
  // $: eventId = $page.params.id;

  async function loadEventData(id: string) {
    // loading = true; // Handled by store
    console.log(`Loading event data for ID: ${id}`);
    await eventStore.fetchEvent(id);
    // eventData and loading will be updated by the store subscription
  }
  let coverRfe: HTMLDivElement;
  let pageHeight = $state(window.innerHeight);
  let chatContentHeight = $derived(pageHeight); // 初始值，将在onMount中更新
  let resizeObserver: ResizeObserver | null = null;

  // 真实聊天功能
  const chat = new Chat({
    api: "/api/chat",
    maxSteps: 5,
    onError: (error) => {
      console.error("AI 对话错误:", error);
    },
  });

  // 聊天消息操作函数
  function copyMessage(messageId: string) {
    const message = chat.messages.find((m) => m.id === messageId);
    if (message) {
      navigator.clipboard.writeText(message.content);
      console.log("消息已复制:", messageId);
    }
  }

  function regenerateMessage(messageId: string) {
    const messageIndex = chat.messages.findIndex((m) => m.id === messageId);
    if (messageIndex > 0) {
      chat.reload();
      console.log("重新生成消息:", messageId);
    }
  }

  function likeMessage(messageId: string) {
    console.log("点赞消息:", messageId);
    // 这里可以添加点赞逻辑
  }

  function dislikeMessage(messageId: string) {
    console.log("点踩消息:", messageId);
    // 这里可以添加点踩逻辑
  }

  // 处理消息发送
  async function handleMessageSent(text: string) {
    if (!text.trim() || chat.status !== "ready") return;

    // 使用 Chat 类发送消息
    await chat.append({
      role: "user",
      content: text.trim(),
    });

    console.log("消息已发送:", text);
  }

  onMount(() => {
    appStore.setShowHeader(false);
    console.log("Event page mounted");

    // 计算ChatContent的高度

    // 使用ResizeObserver监听窗口大小变化
    resizeObserver = new ResizeObserver(() => {
      pageHeight = window.innerHeight;
    });

    // 观察document.body的大小变化
    resizeObserver.observe(document.body);
  });

  onDestroy(() => {
    appStore.setShowHeader(true);
    unsubscribeEvent(); // Unsubscribe from the store
    eventStore.setCurrentEvent(null); // Clear current event when leaving the page

    // 清理ResizeObserver
    if (resizeObserver) {
      resizeObserver.disconnect();
      resizeObserver = null;
    }
  });

  async function handleSaveDocument() {
    if (!editorComponent) return; // Should not happen if UI is correct

    const editorContent = await editorComponent.getContent();

    const eventToSave: Partial<EventType> = {};

    // If editing an existing event, copy its properties (that are part of EventType)
    if (currentEvent) {
      // $id is crucial for updates if not passed as a separate param to updateEvent
      // However, eventId is passed to updateEvent, so $id in payload might be redundant or for confirmation.
      // Let's include it if present in currentEvent.
      if (currentEvent.$id !== undefined) eventToSave.$id = currentEvent.$id;

      // Copy other EventType fields from currentEvent
      // Required fields in EventType: title, content, date, user_id. Others are optional.
      if (currentEvent.summary !== undefined)
        eventToSave.summary = currentEvent.summary;
      if (currentEvent.categories !== undefined)
        eventToSave.categories = currentEvent.categories;
      if (currentEvent.tags !== undefined) eventToSave.tags = currentEvent.tags;
      if (currentEvent.date !== undefined) eventToSave.date = currentEvent.date;
      if (currentEvent.privacy !== undefined)
        eventToSave.privacy = currentEvent.privacy;
      if (currentEvent.user_id !== undefined)
        eventToSave.user_id = currentEvent.user_id;
      if (currentEvent.cover !== undefined)
        eventToSave.cover = currentEvent.cover;
      if (currentEvent.location_data !== undefined)
        eventToSave.location_data = currentEvent.location_data;
      if (currentEvent.status !== undefined)
        eventToSave.status = currentEvent.status;
      if (currentEvent.entities_data !== undefined)
        eventToSave.entities_data = currentEvent.entities_data;
      if (currentEvent.creator_name !== undefined)
        eventToSave.creator_name = currentEvent.creator_name;
      if (currentEvent.creator_avatar !== undefined)
        eventToSave.creator_avatar = currentEvent.creator_avatar;
      if (currentEvent.folder_id !== undefined)
        eventToSave.folder_id = currentEvent.folder_id;
      // $createdAt and $updatedAt are generally managed by backend.
    }

    // Set title and content from the UI state. These are required fields in EventType.
    // currentEventTitle is initialized to "New Event" or event's title, so it should be a string.
    eventToSave.title = currentEventTitle!;
    eventToSave.content = editorContent;

    // Note: For new events (eventId === 'new'), currentEvent is null.
    // eventToSave will primarily contain { title, content }.
    // If eventStore.createEvent(eventToSave as EventType) is called,
    // it implies that 'date' and 'user_id' must be either:
    //  a) added to eventToSave here for new events (e.g., new Date().toISOString(), currentUserId)
    //  b) or, eventStore.createEvent is robust enough to add them if missing (preferred).
    // This change focuses on ensuring eventToSave *only* contains EventType fields,
    // assuming the store handles completion of new event objects.

    console.log(
      "Save action triggered for event:",
      currentEventTitle,
      "ID:",
      eventId,
      "Content to save:",
      editorContent
    );

    if (eventId === "new") {
      await eventStore.createEvent(eventToSave as EventType);
    } else if (eventId) {
      await eventStore.updateEvent(eventId, eventToSave);
    }
  }

  function handleTitleChange(title: string) {
    currentEventTitle = title;
  }

  function handleClose() {
    goto("/console/events");
  }

  // Drag and drop state and handlers for EventPropertyCard
  // Initial position (approximating original top-20, and some right offset relative to right edge)
  let cardPosition = $state({ x: 10, y: 40 });
  // It's better to calculate initial position based on viewport or a saved state.

  function handleDragOver(event: DragEvent) {
    event.preventDefault(); // Necessary to allow dropping
    if (event.dataTransfer) {
      event.dataTransfer.dropEffect = "move";
    }
  }

  function handleDrop(event: DragEvent) {
    event.preventDefault();
    const target = event.currentTarget as HTMLElement;
    const rect = target.getBoundingClientRect();

    // This is a simplified version. The child's dragStart should ideally pass dragOffsetX/Y
    // For instance, via a shared store or custom event, or even dataTransfer if possible across components.
    // We'll retrieve the offset from dataTransfer if the child component sets it.
    // Assuming child sets: event.dataTransfer.setData("application/json", JSON.stringify({dragOffsetX, dragOffsetY}));
    let dragOffsetX = 0;
    let dragOffsetY = 0;
    try {
      const data = event.dataTransfer?.getData("application/json");
      if (data) {
        const parsed = JSON.parse(data);
        dragOffsetX = parsed.dragOffsetX || 0;
        dragOffsetY = parsed.dragOffsetY || 0;
      }
    } catch (e) {
      console.warn("Could not parse drag offset data from child component", e);
    }

    // Calculate position relative to the right edge
    console.log(
      "Dropped at:",
      event.clientX,
      event.clientY,
      "Offset:",
      dragOffsetX,
      dragOffsetY,
      "Right edge:",
      rect,
      "Top edge:",
      rect.top
    );
    cardPosition = {
      x: rect.right - event.clientX - dragOffsetX,
      y: event.clientY - rect.top - dragOffsetY,
    };
  }

  // Function to be called by BlockSuiteEditor on content change
  // function handleContentChange(content: JSON) {
  //   const newContentString = JSON.stringify(content);
  //   if (newContentString !== editorContent) {
  //     editorContent = newContentString;
  //     console.log("Content changed (JSON):", editorContent);
  //     // Optionally, mark as dirty or auto-save
  // }
  
  // 处理地图按钮点击事件
  function handleMapButtonClick() {
    console.log("Map button clicked in parent component");
    // 这里可以添加打开地图设置的逻辑
    // 例如打开一个地图设置对话框
    
    // 模拟打开地图设置对话框
    setTimeout(() => {
      // 模拟用户设置了地图位置
      const mapLocation = {
        lat: 39.9042,
        lng: 116.4074,
        zoom: 12,
        name: "北京市"
      };
      
      // 更新编辑器中的地图
      if (editorComponent) {
        // editorComponent.setMapLocation(mapLocation);
      }
    }, 1000); // 模拟1秒后用户完成设置
  }
  
  // 处理封面按钮点击事件
  function handleCoverButtonClick() {
    console.log("Cover button clicked in parent component");
    // 这里可以添加自定义封面设置的逻辑
    
    // 在这里，我们可以选择让编辑器内部的封面选择器显示
    // 或者实现自己的封面选择逻辑
    
    // 示例：设置一个新的封面URL
    setTimeout(() => {
      // 模拟用户选择了新封面
      const newCoverUrl = "https://images.unsplash.com/photo-1506744038136-46273834b3fb";
      
      // 更新编辑器中的封面
      if (editorComponent) {
        // editorComponent.setCoverUrl(newCoverUrl);
      }
    }, 1000); // 模拟1秒后用户完成选择
  }
  
  // 处理分享按钮点击事件
  function handleShare() {
    console.log("Share button clicked in parent component");
    // 这里可以添加分享功能的逻辑
    
    // 例如：生成分享链接，打开分享对话框等
    const shareUrl = window.location.href;
    
    // 模拟分享功能
    alert(`分享链接已生成：${shareUrl}\n\n您可以将此链接发送给他人以分享此事件。`);
    
    // 在实际应用中，这里可以实现更复杂的分享功能
    // 例如：复制链接到剪贴板，打开社交媒体分享对话框等
  }
</script>

<!-- This outer div will be the drop target and relative positioning context -->
<div class="h-screen flex flex-col bg-background">
  <EventActionbar
    bind:title={currentEventTitle}
    editable={!eventLoading}
    showSaveButton={!eventLoading}
    onClose={handleClose}
    onSaveDocument={handleSaveDocument}
    onTitleChange={handleTitleChange}
    bind:isPropertiesPanelOpen
    bind:isCommentsPanelOpen
    onShare={handleShare}
  />
  <div class="w-full flex-1 flex flex-row overflow-hidden p-2 pt-0 gap-2">
    {#if !isInputAreaCollapsed}
      <div
        class="w-[420px] flex flex-col rounded-2xl border border-border shadow-xl justify-between relative pt-2"
      >
        <ChatContent
          bind:messages={chat.messages}
          bind:status={chat.status}
          bind:error={chat.error}
          suggestions={[
            "查询最近一周的神秘事件",
            "从这篇文章中提取人物和地点",
            "为这篇文章生成摘要",
            "为这篇文章生成标题",
          ]}
          windowHeight={chatContentHeight}
          onCopyMessage={copyMessage}
          onRegenerateMessage={regenerateMessage}
          onLikeMessage={likeMessage}
          onDislikeMessage={dislikeMessage}
          bind:input={chat.input}
          onMessageSent={(text) => {
            console.log("Message submitted:", text);
            chat.input = text;
            chat.handleSubmit();
            console.log("Chat messages after submit:", chat.messages.length);
          }}
        />
      </div>
    {/if}
    <div class="relative flex-1 h-full">
      <div
        class="w-full h-full flex flex-col rounded-2xl border border-border shadow-xl"
      >
        {#if eventLoading}
          <!-- Use eventLoading from store -->
          <div class="flex justify-center items-center h-full">
            <span class="loading loading-spinner loading-lg"></span>
          </div>
        {:else}
          <div
            class="flex flex-row gap-2 p-2 w-full h-14 relative justify-between"
          >
            <div class="flex flex-row gap-2">
              <button
                class="btn btn-sm btn-ghost"
                on:click={() => (isInputAreaCollapsed = !isInputAreaCollapsed)}
                title={isInputAreaCollapsed ? "展开输入区域" : "收缩输入区域"}
              >
                {#if isInputAreaCollapsed}
                  <ChevronRight class="w-4 h-4" />
                  
                {:else}
                  <ChevronLeft class="w-4 h-4" />
                  
                {/if}
              </button>
              <button
                class="btn btn-sm btn-ghost btn-square"
                on:click={() => (isEditorReadonly = !isEditorReadonly)}
                title={isEditorReadonly ? "退出预览模式" : "进入预览模式"}
              >
                {#if isEditorReadonly}
                  <EyeOff class="w-4 h-4" />
                {:else}
                  <Eye class="w-4 h-4" />
                {/if}
              </button>
              
              <!-- 时间和地点编辑器 -->
              <EventTimeLocationEditor
                bind:eventTime
                bind:location={eventLocation}
                onTimeChange={(newTime) => {
                  eventTime = newTime;
                  if (currentEvent) {
                    eventStore.updateEvent(currentEvent.id, { eventTime: newTime });
                  }
                }}
                onLocationChange={(newLocation) => {
                  eventLocation = newLocation;
                  if (currentEvent) {
                    eventStore.updateEvent(currentEvent.id, { location: newLocation });
                  }
                }}
              />
            </div>
            <div class="flex flex-row gap-2">
              <button
                class="btn btn-sm btn-ghost btn-square"
                on:click={handleSaveDocument}
                title="保存"
              >
                <Save class="w-4 h-4" />
              </button>
            </div>
          </div>

          <BlockSuiteEditor
            class="border-t-1 border-border"
            bind:this={editorComponent}
            initialJsonContent={currentEvent?.content}
            readonly={isEditorReadonly}
          />
        {/if}
      </div>
     
    </div>
    {#if isCommentsPanelOpen && eventId && eventId !== "new"}
      <div
        class=""
        in:fly={{ x: 100, duration: 300 }}
        out:fly={{ x: 100, duration: 300 }}
      >
        <EventCommentsPanel class=" w-[400px] " {eventId} />
      </div>
    {/if}
  </div>
</div>
