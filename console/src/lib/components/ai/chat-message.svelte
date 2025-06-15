<script lang="ts">
	import { UserAvatar } from '$lib/components/user';
	import { Copy, RotateCcw, ThumbsUp, ThumbsDown } from '@lucide/svelte';
	import { marked } from 'marked';
	import type { Message } from '@ai-sdk/svelte';
	import type { User } from '$lib/types/user';
	import { Button } from '$lib/components/ui/button';

	let { message, onCopy, onRegenerate, onLike, onDislike, status, user, onAdoptTitle } = $props<{
		message: Message;
		onCopy?: (messageId: string) => void;
		onRegenerate?: (messageId: string) => void;
		onLike?: (messageId: string) => void;
		onDislike?: (messageId: string) => void;
		user?: User;
		status?: 'success' | 'error' | 'loading';
		onAdoptTitle?: (title: string) => void;
	}>();

	// 渲染Markdown
	function renderMarkdown(content: string): string {
		try {
			// 配置marked选项
			marked.setOptions({
				breaks: true,
				gfm: true,
			});
			return marked.parse(content) as string;
		} catch (err) {
			console.error('Markdown渲染失败:', err);
			return content;
		}
	}
</script>

<style>
	.markdown-content :global(h1) {
		font-size: 1.5rem;
		font-weight: bold;
		margin: 1rem 0 0.5rem 0;
		line-height: 1.2;
	}

	.markdown-content :global(h2) {
		font-size: 1.25rem;
		font-weight: bold;
		margin: 0.875rem 0 0.5rem 0;
		line-height: 1.3;
	}

	.markdown-content :global(h3) {
		font-size: 1.125rem;
		font-weight: bold;
		margin: 0.75rem 0 0.5rem 0;
		line-height: 1.4;
	}

	.markdown-content :global(p) {
		margin: 0.5rem 0;
		line-height: 1.6;
	}

	.markdown-content :global(ul), .markdown-content :global(ol) {
		margin: 0.5rem 0;
		padding-left: 1.5rem;
	}

	.markdown-content :global(li) {
		margin: 0.25rem 0;
		line-height: 1.5;
	}

	.markdown-content :global(code) {
		background-color: rgba(0, 0, 0, 0.1);
		padding: 0.125rem 0.25rem;
		border-radius: 0.25rem;
		font-family: 'Geist Mono', monospace;
		font-size: 0.875rem;
	}

	.markdown-content :global(pre) {
		background-color: rgba(0, 0, 0, 0.05);
		padding: 1rem;
		border-radius: 0.5rem;
		margin: 0.75rem 0;
		overflow-x: auto;
	}

	.markdown-content :global(pre code) {
		background-color: transparent;
		padding: 0;
	}

	.markdown-content :global(blockquote) {
		border-left: 4px solid rgba(0, 0, 0, 0.2);
		padding-left: 1rem;
		margin: 0.75rem 0;
		font-style: italic;
		color: rgba(0, 0, 0, 0.7);
	}

	.markdown-content :global(strong) {
		font-weight: bold;
	}

	.markdown-content :global(em) {
		font-style: italic;
	}

	.markdown-content :global(a) {
		color: #0066cc;
		text-decoration: underline;
	}

	.markdown-content :global(a:hover) {
		color: #0052a3;
	}

	/* 暗色主题适配 */
	:global(.dark) .markdown-content :global(code) {
		background-color: rgba(255, 255, 255, 0.1);
	}

	:global(.dark) .markdown-content :global(pre) {
		background-color: rgba(255, 255, 255, 0.05);
	}

	:global(.dark) .markdown-content :global(blockquote) {
		border-left-color: rgba(255, 255, 255, 0.3);
		color: rgba(255, 255, 255, 0.7);
	}
</style>

<div class="flex flex-row gap-3 {message.role === 'user' ? 'items-start' : 'items-start'} mb-4">
	{#if message.role === 'user'}
		<div class="flex-shrink-0">
			<UserAvatar fallbackClass="text-xs" {user}></UserAvatar>
		</div>
		<div
			class="bg-card text-foreground text-sm px-4 py-2 rounded-2xl rounded-tl-none max-w-[80%]"
		>
			{message.content}
		</div>
	{:else}
		<div class="flex-shrink-0">
			<div
				class=" text-xs font-semibold rounded-full flex-center"
			>
				Aksas
			</div>
		</div>
		<div class="px-1 rounded-lg flex-1 max-w-[90%] text-sm markdown-content">
			{#if message.parts && message.parts.length > 0}
				<!-- 新的流式格式 -->
				{#each message.parts as part, i (i)}
					{#if part.type === 'text'}
						{@html renderMarkdown(part.text)}
					{:else if part.type === 'tool-invocation'}
						{@const toolCallId = part.toolInvocation.toolCallId}
						{@const toolName = part.toolInvocation.toolName}
						{@const state = part.toolInvocation.state}

						{#if state === 'partial-call'}
							<div class="text-gray-500 text-sm">
								正在准备调用工具: {toolName}...
							</div>
						{:else if state === 'call'}
							<div class="text-gray-500 text-sm">
								正在调用工具: {toolName}...
							</div>
						{:else if state === 'result'}
							<div class="text-gray-500 text-sm bg-base-300 p-2 mb-2 rounded">
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

			<!-- 标题建议的特殊处理 -->
			{#if message.data?.type === 'title-suggestion'}
				<div class="mt-3 flex gap-2">
					<Button 
						variant="outline"
						size="sm"
						onclick={() => onAdoptTitle?.(message.data.title)}
					>
						采用这个标题
					</Button>
					<Button variant="ghost" size="sm">
						重新生成
					</Button>
				</div>
			{/if}

			<div class="opacity-50 mt-2">
				<div class="flex gap-1">
					<button class="btn btn-ghost btn-xs" onclick={() => onCopy?.(message.id)} title="复制">
						<Copy class="w-3 h-3" />
					</button>
					<button
						class="btn btn-ghost btn-xs"
						onclick={() => onRegenerate?.(message.id)}
						title="重新生成"
					>
						<RotateCcw class="w-3 h-3" />
					</button>
					<button class="btn btn-ghost btn-xs" onclick={() => onLike?.(message.id)} title="点赞">
						<ThumbsUp class="w-3 h-3" />
					</button>
					<button class="btn btn-ghost btn-xs" onclick={() => onDislike?.(message.id)} title="点踩">
						<ThumbsDown class="w-3 h-3" />
					</button>
				</div>
			</div>
		</div>
	{/if}
</div>
