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
  import { GoogleGenerativeAI } from "@google/generative-ai";
  import { PUBLIC_GEMINI_API_KEY } from "$env/static/public";
  import DraggableWindow from "../ui/draggable-window/draggable-window.svelte";
  import InputArea from "./input-area.svelte";
  import { ScrollArea } from "../ui/scroll-area";
  import { marked } from "marked";
  import type { ChatMessage } from "$lib/types/ai";

  const dispatch = createEventDispatcher();

  // Props
  let {
    open = $bindable(false),
    apiKey = PUBLIC_GEMINI_API_KEY,
    modelName = "gemini-1.5-flash",
    initialMessages = [],
    x = $bindable(0),
    y = $bindable(0),
    collapsedCardX = $bindable(0),
    collapsedCardY = $bindable(0),
    onclose,
    onDock,
    onMaximize,
    hideDockButton = false,
  } = $props<{
    open?: boolean;
    apiKey?: string;
    modelName?: string;
    placeholder?: string;
    initialMessages?: Array<ChatMessage>;
    x?: number;
    y?: number;
    collapsedCardX?: number;
    collapsedCardY?: number;
    onclose?: () => void;
    onDock?: () => void;
    onMaximize?: () => void;
    hideDockButton?: boolean;
  }>();

  // Window management
  let windowId = `chat-${Date.now()}`;
  let windowHeight = $state(600); // 绑定窗口高度

  // State
  let messages = $state<ChatMessage[]>(initialMessages);
  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let scrollAreaRef = $state<HTMLDivElement | null>(null);
  let portalContainer: HTMLElement | null = null;
  let componentElement: HTMLElement | null = null;
  let showCollapsedCard = $state(false);

  // 本地存储键名
  const STORAGE_KEY = `chat-messages-${windowId}`;

  // AI Client
  let genAI: GoogleGenerativeAI;
  let model: any;

  onMount(() => {
    initializeAI();
    loadMessagesFromStorage();

    // 创建portal容器并添加到document.body
    portalContainer = document.createElement("div");
    portalContainer.id = `chat-portal-${windowId}`;
    portalContainer.style.position = "fixed";
    portalContainer.style.top = "0";
    portalContainer.style.left = "0";
    portalContainer.style.width = "100%";
    portalContainer.style.height = "100%";
    portalContainer.style.pointerEvents = "none";
    portalContainer.style.zIndex = "10000";
    document.body.appendChild(portalContainer);

    return () => {
      // 清理portal容器
      if (portalContainer && portalContainer.parentNode) {
        portalContainer.parentNode.removeChild(portalContainer);
      }
    };
  });

  function initializeAI() {
    try {
      genAI = new GoogleGenerativeAI(apiKey);
      model = genAI.getGenerativeModel({
        model: modelName,
      });
    } catch (err) {
      console.error("初始化 AI 失败:", err);
      error = "无法初始化 AI 服务，请检查 API 密钥。";
    }
  }

  // 本地存储相关函数
  function saveMessagesToStorage() {
    if (typeof localStorage !== "undefined") {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
    }
  }

  function loadMessagesFromStorage() {
    if (typeof localStorage !== "undefined") {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        try {
          const parsedMessages = JSON.parse(stored);
          // 恢复Date对象
          messages = parsedMessages.map((msg: any) => ({
            ...msg,
            timestamp: new Date(msg.timestamp),
          }));
        } catch (err) {
          console.error("加载消息失败:", err);
        }
      }
    }
  }

  function clearMessagesFromStorage() {
    if (typeof localStorage !== "undefined") {
      localStorage.removeItem(STORAGE_KEY);
    }
  }

  // 消息操作函数
  function copyMessage(message: ChatMessage) {
    navigator.clipboard.writeText(message.content);
  }

  function regenerateMessage(message: ChatMessage) {
    if (message.role === "model") {
      // 找到这条消息的前一条用户消息
      const messageIndex = messages.findIndex((m) => m.id === message.id);
      if (messageIndex > 0) {
        const previousUserMessage = messages[messageIndex - 1];
        if (previousUserMessage.role === "user") {
          // 删除当前AI消息并重新生成
          messages = messages.slice(0, messageIndex);
          sendMessage(previousUserMessage.content);
        }
      }
    }
  }

  function likeMessage(message: ChatMessage) {
    console.log("点赞消息:", message.id);
    // 这里可以添加点赞逻辑
  }

  function dislikeMessage(message: ChatMessage) {
    console.log("点踩消息:", message.id);
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
    if (!messageText.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      role: "user",
      content: messageText.trim(),
      timestamp: new Date(),
    };

    messages = [...messages, userMessage];
    saveMessagesToStorage();
    isLoading = true;
    error = null;

    try {
      // Prepare chat history for the AI
      const chatHistory = messages.map((msg) => ({
        role: msg.role === "user" ? "user" : "model",
        parts: [{ text: msg.content }],
      }));

      const chat = model.startChat({
        history: chatHistory.slice(0, -1), // Exclude the current message
        generationConfig: {
          temperature: 0.9,
          topK: 1,
          topP: 0.95,
          maxOutputTokens: 1024,
        },
      });

      const result = await chat.sendMessage(userMessage.content);
      const response = result.response;
      const responseText = response.text();

      // Add AI response to messages
      const aiMessage: ChatMessage = {
        id: `ai-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        role: "model",
        content: responseText,
        timestamp: new Date(),
        isMarkdown: true,
        actions: [
          { id: "copy", label: "复制", icon: Copy, handler: copyMessage },
          {
            id: "regenerate",
            label: "重新生成",
            icon: RotateCcw,
            handler: regenerateMessage,
          },
          { id: "like", label: "点赞", icon: ThumbsUp, handler: likeMessage },
          {
            id: "dislike",
            label: "点踩",
            icon: ThumbsDown,
            handler: dislikeMessage,
          },
        ],
      };

      messages = [...messages, aiMessage];
      saveMessagesToStorage();
    } catch (err) {
      console.error("AI 响应失败:", err);
      error = err instanceof Error ? err.message : "AI 响应失败，请稍后再试。";
    } finally {
      isLoading = false;

      // Scroll to bottom after a short delay to ensure content is rendered
      setTimeout(() => {
        if (scrollAreaRef) {
          scrollAreaRef.scrollTop = scrollAreaRef.scrollHeight;
        }
      }, 100);
    }
  }

  function closeDialog() {
    // 保存关闭位置
    // collapsedCardX = x;
    // collapsedCardY = y;

    // 如果有消息，显示收缩卡片
    if (messages.length > 0) {
      showCollapsedCard = true;
    }

    open = false;
    onclose?.();
  }

  function openFromCard() {
    showCollapsedCard = false;
    open = true;
  }

  function closeCard() {
    showCollapsedCard = false;
  }

  function handleDock() {
    // 调用父组件传递的onDock事件处理器
    onDock?.();
    // 隐藏当前浮动窗口
    open = false;
  }

  function handleMinimize() {
    // 调用父组件传递的onMaximize事件处理器
    onMaximize?.();
    // 隐藏当前浮动窗口
    open = false;
  }

  // Watch for initialMessages changes
  $effect(() => {
    if (initialMessages.length > 0) {
      messages = [...initialMessages];
    }
  });

  // Watch for open state changes to move component to portal
  $effect(() => {
    if ((open || showCollapsedCard) && portalContainer && componentElement) {
      console.log(x, y);
      // 将组件移动到portal容器中
      portalContainer.appendChild(componentElement);
      // portalContainer.style.pointerEvents =
      //   open || showCollapsedCard ? "auto" : "none";
    } else if (!open && !showCollapsedCard && portalContainer) {
      // 隐藏时重置pointer-events
      portalContainer.style.pointerEvents = "none";
    }
  });



  // 处理input-area的generate事件
  function handleGenerate(event: CustomEvent<{ text: string }>) {
    sendMessage(event.detail.text);
  }

  // 计算最后一条消息
  let lastMessage = $derived(
    messages.length > 0 ? messages[messages.length - 1] : null
  );
</script>

<div bind:this={componentElement}>
  {#if open}
    <DraggableWindow
      bind:open
      title="AI 对话"
      width={450}
      bind:height={windowHeight}
      minWidth={350}
      minHeight={400}
      {x}
      {y}
      {hideDockButton}
      onClose={closeDialog}
      onDock={handleDock}
      onMinimize={handleMinimize}
    >
      <div class="flex flex-col h-full">
        <!-- Chat Messages -->
        <ScrollArea
          class="p-4"
          style="height: {windowHeight - 80}px; overflow: hidden;"
          bind:ref={scrollAreaRef}
        >
          <div class="flex flex-col gap-4">
            {#if messages.length === 0}
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

            {#each messages as message}
              <div
                class="chat {message.role === 'user'
                  ? 'chat-end'
                  : 'chat-start'}"
              >
                <div class="chat-image avatar">
                  <div class="w-8 rounded-full">
                    {#if message.role === "user"}
                      <div
                        class="bg-primary text-primary-content rounded-full w-8 h-8 flex items-center justify-center"
                      >
                        <span class="text-xs">你</span>
                      </div>
                    {:else}
                      <div
                        class="bg-secondary text-secondary-content rounded-full w-8 h-8 flex items-center justify-center"
                      >
                        <span class="text-xs">AI</span>
                      </div>
                    {/if}
                  </div>
                </div>
                <div
                  class="chat-bubble {message.role === 'user'
                    ? 'chat-bubble-primary'
                    : 'chat-bubble-secondary'} max-w-xs group relative"
                >
                  {#if message.isMarkdown && message.role === "model"}
                    <div class="prose prose-sm max-w-none text-sm">
                      {@html renderMarkdown(message.content)}
                    </div>
                  {:else}
                    <p class="whitespace-pre-wrap break-words text-sm">
                      {message.content}
                    </p>
                  {/if}

                  <!-- 消息操作按钮 -->
                  {#if message.actions && message.actions.length > 0}
                    <div
                      class="absolute -bottom-8 right-0 opacity-0 group-hover:opacity-100 transition-opacity bg-base-100 border border-base-300 rounded-lg p-1 flex gap-1 shadow-lg"
                    >
                      {#each message.actions as action}
                        <button
                          class="btn btn-xs btn-ghost hover:btn-primary"
                          on:click={() => action.handler(message)}
                          title={action.label}
                        >
                          {#if action.icon}
                            <svelte:component
                              this={action.icon}
                              class="w-3 h-3"
                            />
                          {/if}
                        </button>
                      {/each}
                    </div>
                  {/if}
                </div>
                <div class="chat-footer opacity-50 text-xs">
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            {/each}

            {#if isLoading}
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

            {#if error}
              <div class="flex justify-center">
                <div class="alert alert-error text-sm max-w-xs">
                  <p>{error}</p>
                </div>
              </div>
            {/if}
          </div>
        </ScrollArea>

        <!-- 输入区域 -->
        <div class="border-t border-base-300">
          <InputArea
            on:generate={handleGenerate}
            disabled={isLoading}
            placeholder="输入消息..."
          />
        </div>
      </div>
    </DraggableWindow>
  {/if}

  <!-- 收缩卡片 -->
  {#if showCollapsedCard && lastMessage}
    <div
      class="absolute bg-base-100 border border-base-300 rounded-lg shadow-lg p-3 max-w-xs cursor-pointer hover:shadow-xl transition-shadow z-50"
      style="left: {collapsedCardX ||
        window.innerWidth - 320}px; top: {collapsedCardY ||
        window.innerHeight - 120}px;"
      on:click={openFromCard}
      on:keydown={(e) => e.key === "Enter" && openFromCard()}
      role="button"
      tabindex="0"
    >
      <!-- 关闭按钮 -->
      <button
        class="absolute top-1 right-1 w-5 h-5 rounded-full bg-base-200 hover:bg-base-300 flex items-center justify-center text-xs opacity-60 hover:opacity-100"
        on:click|stopPropagation={closeCard}
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

      <!-- 最后一条消息 -->
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
        {lastMessage.timestamp.toLocaleTimeString()}
      </div>
    </div>
  {/if}
</div>
