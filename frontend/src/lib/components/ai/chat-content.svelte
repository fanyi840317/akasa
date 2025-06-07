<script lang="ts">
  import { OutlineButton } from "../ui";
  import { ScrollArea } from "../ui/scroll-area";
  import ChatMessage from "./chat-message.svelte";
  import InputArea from "./input-area.svelte";
  import type { Message } from "@ai-sdk/svelte";

  // Props
  let {
    messages = $bindable([]),
    status = $bindable("ready"),
    error = $bindable(undefined),
    input = $bindable(""),
    windowHeight = 600,
    onCopyMessage,
    suggestions,
    onSuggestionClick,
    onRegenerateMessage,
    onLikeMessage,
    onDislikeMessage,
    onMessageSent, // 消息发送后的回调
  } = $props<{
    messages?: Message[];
    status?: string;
    error?: any;
    suggestions?: string[];
    input?: string;
    windowHeight?: number;
    onCopyMessage?: (messageId: string) => void;
    onRegenerateMessage?: (messageId: string) => void;
    onLikeMessage?: (messageId: string) => void;
    onDislikeMessage?: (messageId: string) => void;
    onMessageSent?: (text: string) => void; // 消息发送后的回调
  }>();

  // State
  let scrollAreaRef = $state<HTMLDivElement | null>(null);

  // 滚动到底部函数
  function scrollToBottom() {
    if (scrollAreaRef) {
      scrollAreaRef.scrollTop = scrollAreaRef.scrollHeight;
    }
  }

  // 处理消息发送
  function handleSubmit(text: string) {
    console.log("Message submitted:", text);

    // 不直接修改 status，而是通过回调通知父组件
    // status = "submitted";

    // 调用父组件提供的回调
    onMessageSent?.(text);

    // 发送后清空输入框
    // input = "";

    // 滚动到底部
    setTimeout(() => {
      scrollToBottom();
    }, 100);
  }

  // 处理复制消息
  function handleCopyMessage(messageId: string) {
    const message = messages.find((m: { id: string }) => m.id === messageId);
    if (message) {
      navigator.clipboard.writeText(message.content);
      console.log("Message copied:", messageId);
    }

    // 如果需要，可以调用父组件提供的回调
    onCopyMessage?.(messageId);
  }

  // 处理重新生成消息
  function handleRegenerateMessage(messageId: string) {
    console.log("Regenerate message:", messageId);

    // 如果需要，可以调用父组件提供的回调
    onRegenerateMessage?.(messageId);
  }

  // 处理点赞消息
  function handleLikeMessage(messageId: string) {
    console.log("Like message:", messageId);

    // 如果需要，可以调用父组件提供的回调
    onLikeMessage?.(messageId);
  }

  // 处理点踩消息
  function handleDislikeMessage(messageId: string) {
    console.log("Dislike message:", messageId);

    // 如果需要，可以调用父组件提供的回调
    onDislikeMessage?.(messageId);
  }

  // 监听消息变化，自动滚动到底部
  $effect(() => {
    if (messages.length > 0) {
      setTimeout(() => {
        scrollToBottom();
      }, 100);
    }
  });
</script>

<div class="flex flex-col h-full">
  <!-- Chat Messages -->
  <ScrollArea
    class="px-4"
    style="height: {windowHeight - 190}px; overflow: hidden;"
    bind:ref={scrollAreaRef}
  >
    {#if messages.length === 0}
      <div class="flex-center flex-col">
        <div class="text-center opacity-60 py-8">
          <div class="avatar placeholder mb-2">
            <div class="bg-primary text-primary-content rounded-full w-12">
              <span class="text-md">AI</span>
            </div>
          </div>
          <p>开始与 AI 对话</p>
          <p class="text-sm opacity-50">输入你的问题，我会尽力帮助你</p>
        </div>

        <div class="flex flex-col gap-4">
          {#each suggestions as suggestion}
            <OutlineButton class="w-56 py-5 text-xs rounded-full" onclick={()=>{
              handleSubmit(suggestion)
            }}>{suggestion}</OutlineButton>
          {/each}
        </div>
      </div>
    {/if}
    <div class="flex flex-col gap-4">
      {#each messages as message}
        <ChatMessage
          {message}
          {status}
          onCopy={onCopyMessage}
          onRegenerate={onRegenerateMessage}
          onLike={onLikeMessage}
          onDislike={onDislikeMessage}
        />
      {/each}
    </div>
  </ScrollArea>

  <!-- 输入区域 -->
  <InputArea
    class="px-4"
    placeholder="输入消息..."
    bind:inputValue={input}
    onSubmit={handleSubmit}
  />
</div>
