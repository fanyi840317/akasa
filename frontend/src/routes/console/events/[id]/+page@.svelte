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
  import { Minimize, Maximize, Eye, EyeOff } from "lucide-svelte"; // 导入收缩和预览图标
  import ChatContent from "$lib/components/ai/chat-content.svelte";
  import { Chat } from "@ai-sdk/svelte";
  import type { Message } from "@ai-sdk/svelte";

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

  let comments = [
    {
      id: "1",
      author: { name: "wafsn2218", avatar: "/images/avatars/user_w.png" }, // Example avatar
      content:
        "我始终相信兼听则明，二爷的故事始终是我了解历史真相的一块拼图，不偏不倚。希望二爷可以坚持，不要像某些youtuber为了黑而黑，而是有事实有依据的真实讲述历史故事。",
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24 * 30 * 4), // 4 months ago
      likes: 850,
      isEdited: true,
      paidAmount: "US$200.00",
      replies: [
        {
          id: "1-1",
          author: { name: "范翼", avatar: "/images/avatars/user_fan.png" },
          content: "说得好！",
          timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24 * 30 * 3), // 3 months ago
          likes: 10,
        },
      ],
    },
    {
      id: "2",
      author: {
        name: "riverhe2853",
        avatar: "/images/avatars/user_dog.png",
      },
      content: "谢谢精彩视频，祝二爷一家新年快乐🎉🎊",
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24 * 30 * 4), // 4 months ago
      likes: 23,
      paidAmount: "CA$5.00",
      replies: [],
    },
  ];

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
  let chatContentHeight = $state(pageHeight - 100); // 初始值，将在onMount中更新
  let resizeObserver: ResizeObserver | null = null;

  // 真实聊天功能
  const chat = new Chat({
    api: '/api/chat',
    maxSteps: 5,
    onError: (error) => {
      console.error('AI 对话错误:', error);
    },
  });

  // 聊天消息操作函数
  function copyMessage(messageId: string) {
    const message = chat.messages.find(m => m.id === messageId);
    if (message) {
      navigator.clipboard.writeText(message.content);
      console.log('消息已复制:', messageId);
    }
  }

  function regenerateMessage(messageId: string) {
    const messageIndex = chat.messages.findIndex((m) => m.id === messageId);
    if (messageIndex > 0) {
      chat.reload();
      console.log('重新生成消息:', messageId);
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
    if (!text.trim() || chat.status !== 'ready') return;
    
    // 使用 Chat 类发送消息
    await chat.append({
      role: 'user',
      content: text.trim(),
    });
    
    console.log('消息已发送:', text);
  }

  onMount(() => {
    appStore.setShowHeader(false);
    console.log("Event page mounted");
    
    // 计算ChatContent的高度
    updateChatContentHeight();
    
    // 使用ResizeObserver监听窗口大小变化
    resizeObserver = new ResizeObserver(() => {
      pageHeight = window.innerHeight;
      updateChatContentHeight();
    });
    
    // 观察document.body的大小变化
    resizeObserver.observe(document.body);
  });
  
  // 更新ChatContent高度的函数
  function updateChatContentHeight() {
    // 计算高度：页面高度减去ActionBar高度(约60px)和其他边距
    chatContentHeight = pageHeight - 100; // 100是ActionBar和padding的估计高度
  }

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
</script>

<!-- This outer div will be the drop target and relative positioning context -->
<div class="h-screen flex flex-col bg-muted">
  <EventActionbar
    bind:title={currentEventTitle}
    editable={!eventLoading}
    showSaveButton={!eventLoading}
    onClose={handleClose}
    onSaveDocument={handleSaveDocument}
    onTitleChange={handleTitleChange}
    bind:isPropertiesPanelOpen
    bind:isCommentsPanelOpen
  />
  <div class="w-full flex-1 flex flex-row overflow-hidden">
    
    {#if !isInputAreaCollapsed}
    <div class="w-128 flex flex-col p-4 justify-between relative">
      <ChatContent 
        bind:messages={chat.messages}
        bind:status={chat.status}
        bind:error={chat.error}
        bind:input={chat.input}
        windowHeight={chatContentHeight}
        onCopyMessage={copyMessage}
        onRegenerateMessage={regenerateMessage}
        onLikeMessage={likeMessage}
        onDislikeMessage={dislikeMessage}
        onMessageSent={(text) => {
          console.log('Message submitted:', text);
          chat.handleSubmit();
          console.log('Chat messages after submit:', chat.messages.length);
        }}
      />
    </div>
    {/if}
    <div class="relative w-full h-full pt-1">
      <div
        class="w-full h-full flex flex-col rounded-tl-2xl
      outline-1 outline-base-300 shadow-xl"
      >
        {#if eventLoading}
          <!-- Use eventLoading from store -->
          <div class="flex justify-center items-center h-full">
            <span class="loading loading-spinner loading-lg"></span>
          </div>
        {:else}
          <div
            class="flex flex-row gap-2 p-2 w-full h-14 border-b border-border outline-b outline-sidebar-border relative"
          >
          <button
              class="btn btn-sm btn-ghost btn-square"
              on:click={() => (isInputAreaCollapsed = !isInputAreaCollapsed)}
              title={isInputAreaCollapsed ? "展开输入区域" : "收缩输入区域"}
            >
              {#if isInputAreaCollapsed}
                <Maximize class="w-4 h-4" />
                
              {:else}
                <Minimize class="w-4 h-4" />
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
          </div>
          <BlockSuiteEditor
            class="rounded-xl"
            bind:this={editorComponent}
            initialJsonContent={currentEvent?.content}
            readonly={isEditorReadonly}
          />
        {/if}
      </div>
      {#if isPropertiesPanelOpen}
        <div
          class="absolute top-18 left-22 z-10 transition-transform duration-300 ease-in-out"
          in:fade={{ duration: 300 }}
          out:fade={{ duration: 300 }}
        >
          <!-- <EventPropertyCard
            eventDate={currentEvent?.date}
            locationData={currentEvent?.location_data}
            selectedCategories={currentEvent?.categories || []}
            categories={[]}
          /> -->
        </div>
      {/if}
    </div>
    {#if isCommentsPanelOpen && eventId && eventId !== 'new'}
      <div
        class=""
        in:fly={{ x: 100, duration: 300 }}
        out:fly={{ x: 100, duration: 300 }}
      >
        <EventCommentsPanel eventId={eventId} />
      </div>
    {/if}
  </div>
</div>
