<script lang="ts">
  import { onMount, createEventDispatcher } from "svelte";
  import {
    Loader2,
    Send,
    Image,
    Mic,
    Copy,
    RotateCcw,
    ThumbsUp,
    ThumbsDown,
  } from "lucide-svelte";
  import { Chat } from "@ai-sdk/svelte";
  import DraggableWindow from "../ui/draggable-window/draggable-window.svelte";
  import InputArea from "./input-area.svelte";
  import { ScrollArea } from "../ui/scroll-area";
  import { marked } from "marked";
  import type { ChatMessage } from "$lib/types/ai";

  const dispatch = createEventDispatcher();

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
  const convertedInitialMessages = initialMessages.map((msg: ChatMessage) => ({
    id: msg.id,
    role: msg.role === 'model' ? 'assistant' : msg.role,
    content: msg.content,
    createdAt: msg.timestamp,
  }));

  // AI Chat instance
  const chat = new Chat({
    api: '/api/chat',
    maxSteps: 5,
    initialMessages: convertedInitialMessages,
    get id() {
      return windowId;
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
  function copyMessage(content: string) {
    navigator.clipboard.writeText(content);
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

  // 渲染Markdown
  function renderMarkdown(content: string): string {
    try {
      return marked(content) as string;
    } catch (err) {
      console.error("Markdown渲染失败:", err);
      return content;
    }
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
      <div class="flex flex-col h-full">
        <!-- Chat Messages -->
        <ScrollArea
          class="p-4"
          style="height: {windowHeight - 210}px; overflow: hidden;"
          bind:ref={scrollAreaRef}
        >
          <div class="flex flex-col gap-4">
            {#if chat.messages.length === 0}
              <div class="text-center opacity-60 py-8">
                <div class="avatar placeholder mb-2">
                  <div
                    class="bg-primary text-primary-content rounded-full w-12"
                  >
                    <span class="text-lg">AI</span>
                  </div>
                </div>
                <p>开始与 AI 对话</p>
                <p class="text-sm opacity-50">输入你的问题，我会尽力帮助你</p>
              </div>
            {/if}

            {#each chat.messages as message}
              <div
                class="chat {message.role === 'user'
                  ? 'chat-end'
                  : 'chat-start'}"
              >
                <div class="chat-image avatar">
                  <div class="w-10 rounded-full">
                    {#if message.role === 'user'}
                      <div
                        class="avatar placeholder bg-secondary text-secondary-content"
                      >
                        <div class="w-10 rounded-full">
                          <span class="text-xs">You</span>
                        </div>
                      </div>
                    {:else}
                      <div
                        class="avatar placeholder bg-primary text-primary-content"
                      >
                        <div class="w-10 rounded-full">
                          <span class="text-xs">AI</span>
                        </div>
                      </div>
                    {/if}
                  </div>
                </div>
                <div class="chat-bubble max-w-[80%]">
                  {#if message.role === 'assistant'}
                    {@html renderMarkdown(message.content)}
                  {:else}
                    {message.content}
                  {/if}
                </div>
                {#if message.role === 'assistant'}
                  <div class="chat-footer opacity-50">
                    <div class="flex gap-1 mt-1">
                      <button
                        class="btn btn-ghost btn-xs"
                        onclick={() => copyMessage(message.id)}
                        title="复制"
                      >
                        <Copy class="w-3 h-3" />
                      </button>
                      <button
                        class="btn btn-ghost btn-xs"
                        onclick={() => regenerateMessage(message.id)}
                        title="重新生成"
                      >
                        <RotateCcw class="w-3 h-3" />
                      </button>
                      <button
                        class="btn btn-ghost btn-xs"
                        onclick={() => likeMessage(message.id)}
                        title="点赞"
                      >
                        <ThumbsUp class="w-3 h-3" />
                      </button>
                      <button
                        class="btn btn-ghost btn-xs"
                        onclick={() => dislikeMessage(message.id)}
                        title="点踩"
                      >
                        <ThumbsDown class="w-3 h-3" />
                      </button>
                    </div>
                  </div>
                {/if}
              </div>
            {/each}

            {#if chat.status === 'submitted' || chat.status === 'streaming'}
              <div class="chat chat-start">
                <div class="chat-image avatar">
                  <div class="w-8 rounded-full">
                    <div
                      class="bg-secondary text-secondary-content rounded-full w-8 h-8 flex items-center justify-center"
                    >
                      <span class="text-xs">AI</span>
                    </div>
                  </div>
                </div>
                <div
                  class="chat-bubble chat-bubble-secondary flex items-center justify-center"
                >
                  <Loader2 class="h-4 w-4 animate-spin opacity-70" />
                  <span class="ml-2 text-sm">思考中...</span>
                </div>
              </div>
            {/if}

            {#if chat.error}
              <div class="flex justify-center">
                <div class="alert alert-error text-sm max-w-xs">
                  <p>{chat.error.message || chat.error}</p>
                </div>
              </div>
            {/if}
          </div>
        </ScrollArea>

        <!-- 输入区域 -->
        <div class=" p-5">
          <InputArea
            disabled={chat.status !== 'ready'}
            placeholder="输入消息..."
            bind:inputValue={chat.input}
            onSubmit={(text) => {
              chat.input = text;
              chat.handleSubmit();
            }}
          />
        </div>
      </div>
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
