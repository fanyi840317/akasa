<script lang="ts">
  import { UserAvatar } from "../ui";
  import { Copy, RotateCcw, ThumbsUp, ThumbsDown } from "lucide-svelte";
  import { marked } from "marked";
  import type { Message } from "@ai-sdk/svelte";
  import type { User } from "$lib/types/user";

  let { message, onCopy, onRegenerate, onLike, onDislike, user } = $props<{
    message: Message;
    onCopy?: (messageId: string) => void;
    onRegenerate?: (messageId: string) => void;
    onLike?: (messageId: string) => void;
    onDislike?: (messageId: string) => void;
    user?: User;
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

<div
  class="flex flex-col gap-2 {message.role === 'user'
    ? 'items-end'
    : 'items-start'} mb-4"
>
  {#if message.role === "user"}
    <UserAvatar class="size-6" src={user?.avatar} fallback={user?.name || "You"}
    ></UserAvatar>
    <div class="bg-base-300 text-base-content py-2 px-4 rounded-2xl">
      {message.content}
    </div>
  {:else}
    <UserAvatar class="size-6" fallback="AI"></UserAvatar>
    <div class="py-3 rounded-lg">
      {#if message.parts && message.parts.length > 0}
        <!-- 新的流式格式 -->
        {#each message.parts as part, i (i)}
          {#if part.type === "text"}
            {@html renderMarkdown(part.text)}
          {:else if part.type === "tool-invocation"}
            {@const toolCallId = part.toolInvocation.toolCallId}
            {@const toolName = part.toolInvocation.toolName}
            {@const state = part.toolInvocation.state}

            {#if state === "partial-call"}
              <div class="text-gray-500 text-sm">
                正在准备调用工具: {toolName}...
              </div>
            {:else if state === "call"}
              <div class="text-gray-500 text-sm">
                正在调用工具: {toolName}...
              </div>
            {:else if state === "result"}
              <div class="text-gray-500 text-sm bg-gray-100 p-2 rounded">
                <strong>工具结果:</strong>
                {part.toolInvocation.result}
              </div>
            {/if}
          {/if}
        {/each}
      {:else}
        <!-- 旧的格式兼容 -->
        {@html renderMarkdown(message.content)}
      {/if}

      <div class="opacity-50 mt-2">
        <div class="flex gap-1">
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
    </div>
  {/if}
</div>
