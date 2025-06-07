<script lang="ts">
  import { onMount, createEventDispatcher } from "svelte";
  import {
    Loader2,
    Send,
    Image,
    Mic,
  } from "lucide-svelte";
  import { Chat } from "@ai-sdk/svelte";
  import DraggableWindow from "../ui/draggable-window/draggable-window.svelte";
  import InputArea from "./input-area.svelte";
  import { ScrollArea } from "../ui/scroll-area";
  import type { ChatMessage } from "$lib/types/ai";
  import ChatDialogContent from "./chat-content.svelte";

  // Props
  let {
    open = $bindable(false),
    initialMessages = [],
    x = $bindable(0),
    y = $bindable(0),
    onclose,
    onDock,
    onMaximize,
    hideDockButton = false,
  } = $props<{
    open?: boolean;
    placeholder?: string;
    initialMessages?: Array<ChatMessage>;
    x?: number;
    y?: number;
    onclose?: () => void;
    onDock?: () => void;
    onMaximize?: () => void;
    hideDockButton?: boolean;
  }>();

  // Window management
  let windowId = `chat-${Date.now()}`;
  let windowHeight = $state(600); // 绑定窗口高度

  // State
  let scrollAreaRef = $state<HTMLDivElement | null>(null);
  let portalContainer: HTMLElement | null = null;
  let componentElement: HTMLElement | null = null;
  let showCollapsedCard = $state(false);
  let collapsedCardX = $state(0); // 绑定收缩卡片的X坐标
  let collapsedCardY = $state(0); // 绑定收缩卡片的Y坐标

  // 本地存储键名
  const STORAGE_KEY = `chat-messages-${windowId}`;

  // Convert initial messages to AI SDK format
  // const convertedInitialMessages = initialMessages.map((msg: ChatMessage) => ({
  //   id: msg.id,
  //   role: msg.role === 'model' ? 'assistant' : msg.role,
  //   content: msg.content,
  //   createdAt: msg.timestamp,
  // }));
  // AI Chat instance
  const chat = new Chat({
    api: '/api/chat',
    maxSteps: 5,
    onError: (error) => {
      console.error('AI 对话错误:', error);
      // 可以在这里添加用户友好的错误提示
    },
  });

  // Scroll to bottom function
  function scrollToBottom() {
    if (scrollAreaRef) {
      scrollAreaRef.scrollTop = scrollAreaRef.scrollHeight;
    }
  }

  onMount(() => {
    // Component mounted
  });

  // 消息操作函数
  function copyMessage(messageId: string) {
    const message = chat.messages.find(m => m.id === messageId);
    if (message) {
      navigator.clipboard.writeText(message.content);
    }
  }

  function regenerateMessage(messageId: string) {
    // Find the message and regenerate from that point
    const messageIndex = chat.messages.findIndex((m) => m.id === messageId);
    if (messageIndex > 0) {
      // Use reload to regenerate the last assistant message
      chat.reload();
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



  // 外部调用的发送消息函数
  export async function sendMessage(messageText: string) {
    if (!messageText.trim() || chat.status !== 'ready') return;
    
    // Use the Chat class to append and submit the message
    await chat.append({
      role: 'user',
      content: messageText.trim(),
    });
    
    // Scroll to bottom after a short delay
    setTimeout(() => {
      if (scrollAreaRef) {
        scrollAreaRef.scrollTop = scrollAreaRef.scrollHeight;
      }
    }, 100);
  }

  function closeDialog() {
    // 保存关闭位置

    // 如果有消息，显示收缩卡片
    if (chat.messages.length > 0) {
      showCollapsedCard = true;
    }

    open = false;
    onclose?.();
  }

  function openFromCard() {
    showCollapsedCard = false;
    open = true;
    x = collapsedCardX;
    y = collapsedCardY;
  }

  function closeCard() {
    // alert("关闭");
    showCollapsedCard = false;
  }

  function handleDock() {
    // 调用父组件传递的onDock事件处理器
    onDock?.();
    // 隐藏当前浮动窗口
    open = false;
  }

  function handleMinimize() {
    // 保存当前位置到收缩卡片位置
    collapsedCardX = x;
    collapsedCardY = y;

    // 调用父组件传递的onMaximize事件处理器
    onMaximize?.();
    // 隐藏当前浮动窗口
    open = false;

    // 如果有消息，显示收缩卡片
    if (chat.messages.length > 0) {
      showCollapsedCard = true;
    }
  }

  // Auto-scroll effect when new messages arrive
  $effect(() => {
    if (chat.messages.length > 0) {
      scrollToBottom();
    }
  });



  // 计算最后一条消息
  let lastMessage = $derived(
    chat.messages.length > 0 ? chat.messages[chat.messages.length - 1] : null,
  );

  // Auto-scroll when new messages arrive
  $effect(() => {
    if (chat.messages.length > 0) {
      setTimeout(() => {
        if (scrollAreaRef) {
          scrollAreaRef.scrollTop = scrollAreaRef.scrollHeight;
        }
      }, 100);
    }
  });
</script>

<div bind:this={componentElement}>
  {#if open}
    <DraggableWindow
      bind:open
      title="AI 对话"
      width={550}
      bind:height={windowHeight}
      minWidth={350}
      minHeight={400}
      bind:windowX={x}
      bind:windowY={y}
      {hideDockButton}
      onClose={closeDialog}
      onDock={handleDock}
      onMinimize={handleMinimize}
    >
      <ChatDialogContent
        messages={chat.messages}
        status={chat.status}
        error={chat.error}
        bind:input={chat.input}
        {windowHeight}
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
    </DraggableWindow>
  {/if}

  <!-- 收缩卡片 -->
  {#if !open && showCollapsedCard}
    <div
      class="absolute bottom-2 right-2 bg-base-100 border border-base-300 rounded-lg shadow-lg p-3 max-w-xs w-[260px] h-[140px]
  cursor-pointer hover:shadow-xl transition-shadow z-50"
    >
      <!-- 关闭按钮 -->
      <button
        class="absolute top-1 right-1 w-5 h-5 rounded-full bg-base-200 hover:bg-base-300 flex items-center justify-center text-xs opacity-60 hover:opacity-100"
        onclick={closeCard}
        aria-label="关闭卡片"
      >
        ×
      </button>

      <!-- 头部 -->
      <div class="flex items-center gap-2 mb-2">
        <div
          class="bg-primary text-primary-content rounded-full w-6 h-6 flex items-center justify-center"
        >
          <span class="text-xs">AI</span>
        </div>
        <span class="text-sm font-medium">AI 对话</span>
      </div>
      <div
        class=""
        onclick={openFromCard}
        onkeydown={(e) => e.key === "Enter" && openFromCard()}
      >
        <!-- 最后一条消息 -->
        {#if lastMessage}
          <div class="text-sm opacity-80">
            <div class="flex items-start gap-2">
              <div
                class="w-4 h-4 rounded-full {lastMessage.role === 'user'
                  ? 'bg-primary'
                  : 'bg-secondary'} flex-shrink-0 mt-0.5"
              >
                <span
                  class="text-xs text-white flex items-center justify-center w-full h-full"
                >
                  {lastMessage.role === "user" ? "你" : "AI"}
                </span>
              </div>
              <p class="line-clamp-2 text-xs leading-relaxed">
                {lastMessage.content.length > 60
                  ? lastMessage.content.substring(0, 60) + "..."
                  : lastMessage.content}
              </p>
            </div>
          </div>

          <!-- 时间戳 -->
          <div class="text-xs opacity-50 mt-2 text-right">
            {lastMessage.createdAt ? new Date(lastMessage.createdAt).toLocaleTimeString() : ''}
          </div>
        {:else}
          <!-- 暂无对话提示 -->
          <div class="text-sm opacity-60 text-center py-2">
            <p class="text-xs">暂无对话</p>
          </div>
        {/if}
      </div>
    </div>
  {/if}
</div>
