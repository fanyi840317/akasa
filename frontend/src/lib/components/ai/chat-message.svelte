<script lang="ts">
  import { Copy, RotateCcw, ThumbsUp, ThumbsDown } from "lucide-svelte";
  import { marked } from "marked";
  import type { Message } from "@ai-sdk/svelte";

  let {
    message,
    onCopy,
    onRegenerate,
    onLike,
    onDislike
  } = $props<{
    message: Message;
    onCopy?: (messageId: string) => void;
    onRegenerate?: (messageId: string) => void;
    onLike?: (messageId: string) => void;
    onDislike?: (messageId: string) => void;
  }>();

  // 渲染Markdown
  function renderMarkdown(content: string): string {
    try {
      return marked(content) as string;
    } catch (err) {
      console.error("Markdown渲染失败:", err);
      return content;
    }
  }
</script>

<div class="chat {message.role === 'user' ? 'chat-end' : 'chat-start'}">
  <div class="chat-image avatar">
    <div class="w-10 rounded-full">
      {#if message.role === 'user'}
        <div class="avatar placeholder bg-secondary text-secondary-content">
          <div class="w-10 rounded-full flex-center">
            <span class="text-xs">You</span>
          </div>
        </div>
      {:else}
        <div class="avatar placeholder bg-primary text-primary-content">
          <div class="w-10 rounded-full flex-center">
            <span class="text-xs">AI</span>
          </div>
        </div>
      {/if}
    </div>
  </div>
  <div class="chat-bubble max-w-[80%]">
    {#if message.parts && message.parts.length > 0}
      <!-- 新的流式格式 -->
      {#each message.parts as part, i (i)}
        {#if part.type === 'text'}
          {#if message.role === 'assistant'}
            {@html renderMarkdown(part.text)}
          {:else}
            {part.text}
          {/if}
        {:else if part.type === 'tool-invocation'}
          {@const toolCallId = part.toolInvocation.toolCallId}
          {@const toolName = part.toolInvocation.toolName}
          {@const state = part.toolInvocation.state}
          
          {#if state === 'partial-call'}
            <div class="text-gray-500 text-sm">正在准备调用工具: {toolName}...</div>
          {:else if state === 'call'}
            <div class="text-gray-500 text-sm">正在调用工具: {toolName}...</div>
          {:else if state === 'result'}
            <div class="text-gray-500 text-sm bg-gray-100 p-2 rounded">
              <strong>工具结果:</strong> {part.toolInvocation.result}
            </div>
          {/if}
        {/if}
      {/each}
    {:else}
      <!-- 旧的格式兼容 -->
      {#if message.role === 'assistant'}
        {@html renderMarkdown(message.content)}
      {:else}
        {message.content}
      {/if}
    {/if}
  </div>
  {#if message.role === 'assistant'}
    <div class="chat-footer opacity-50">
      <div class="flex gap-1 mt-1">
        <button
          class="btn btn-ghost btn-xs"
          onclick={() => onCopy?.(message.id)}
          title="复制"
        >
          <Copy class="w-3 h-3" />
        </button>
        <button
          class="btn btn-ghost btn-xs"
          onclick={() => onRegenerate?.(message.id)}
          title="重新生成"
        >
          <RotateCcw class="w-3 h-3" />
        </button>
        <button
          class="btn btn-ghost btn-xs"
          onclick={() => onLike?.(message.id)}
          title="点赞"
        >
          <ThumbsUp class="w-3 h-3" />
        </button>
        <button
          class="btn btn-ghost btn-xs"
          onclick={() => onDislike?.(message.id)}
          title="点踩"
        >
          <ThumbsDown class="w-3 h-3" />
        </button>
      </div>
    </div>
  {/if}
</div>