<script lang="ts">
  import { Loader2 } from "lucide-svelte";
  import ChatMessage from "./chat-message.svelte";
  import type { Message } from "@ai-sdk/svelte";

  let {
    messages,
    status,
    error,
    onCopyMessage,
    onRegenerateMessage,
    onLikeMessage,
    onDislikeMessage
  } = $props<{
    messages: Message[];
    status: string;
    error?: any;
    onCopyMessage?: (messageId: string) => void;
    onRegenerateMessage?: (messageId: string) => void;
    onLikeMessage?: (messageId: string) => void;
    onDislikeMessage?: (messageId: string) => void;
  }>();

  $effect(() => {
  if (status === "error") {
    console.error("AI 对话错误:", error);
  }
});
</script>


<div class="flex flex-col gap-4">
  {#if messages.length === 0}
    <div class="text-center opacity-60 py-8">
      <div class="avatar placeholder mb-2">
        <div class="bg-primary text-primary-content rounded-full w-12">
          <span class="text-lg">AI</span>
        </div>
      </div>
      <p>开始与 AI 对话</p>
      <p class="text-sm opacity-50">输入你的问题，我会尽力帮助你</p>
    </div>
  {/if}

  {#each messages as message}
    <ChatMessage
      {message}
      onCopy={onCopyMessage}
      onRegenerate={onRegenerateMessage}
      onLike={onLikeMessage}
      onDislike={onDislikeMessage}
    />
  {/each}

  {#if status === 'submitted' || status === 'streaming'}
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
        <p>{error.message || error}</p>
      </div>
    </div>
  {/if}
</div>