<script lang="ts">
	import { UserAvatar } from '$lib/components/user';
	import { Copy, RotateCcw, ThumbsUp, ThumbsDown } from '@lucide/svelte';
	import { marked } from 'marked';
	import type { Message } from '$lib/types/message';
	import type { User } from '$lib/types/user';
	import { Button } from '$lib/components/ui/button';

	let { message, onCopy, onRegenerate, onLike, onDislike, status, user, onAdopt, onOptionClick } = $props<{
		message: Message;
		onCopy?: (messageId: string) => void;
		onRegenerate?: (messageId: string) => void;
		onLike?: (messageId: string) => void;
		onDislike?: (messageId: string) => void;
		user?: User;
		status?: 'success' | 'error' | 'loading';
		onAdopt?: (type: string, data: any) => void;
		onOptionClick?: (option: any) => void;
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

<div class="flex flex-col {message.role === 'user' ? 'items-end' : 'items-start'} mb-4">
	{#if message.role === 'user'}
		<div class="flex items-start gap-2 max-w-[80%]">
			<div class="flex-shrink-0">
				<UserAvatar fallbackClass="text-xs" {user}></UserAvatar>
			</div>
			<div class="bg-primary text-primary-foreground text-sm px-4 py-2 rounded-2xl rounded-tr-none">
				{message.content}
			</div>
		</div>
	{:else}
		<div class="flex items-start gap-2 max-w-[90%]">
			<div class="flex-shrink-0">
				<div class="text-xs font-semibold rounded-full border flex items-center justify-center w-8 h-8 bg-muted">
					AI
				</div>
			</div>
			<div class="flex-1 text-sm markdown-content bg-muted/50 rounded-2xl rounded-tl-none px-4 py-2">
				<!-- 渲染消息内容 -->
				{@html renderMarkdown(message.content)}
				
				<!-- 工具调用显示 -->
				{#if message.toolCalls && message.toolCalls.length > 0}
					<div class="mt-3 space-y-2">
						{#each message.toolCalls as toolCall (toolCall.id)}
							<div class="bg-background/80 p-3 rounded-lg border">
								<div class="text-xs font-medium text-muted-foreground mb-1">
									🔧 工具调用: {toolCall.name}
								</div>
								{#if toolCall.result}
									<div class="text-xs text-muted-foreground">
										结果: {toolCall.result}
									</div>
								{:else}
									<div class="text-xs text-muted-foreground">
										执行中...
									</div>
								{/if}
							</div>
						{/each}
					</div>
				{/if}
				
				<!-- 选项显示（用于中断处理） -->
				{#if message.options && message.options.length > 0}
					<div class="mt-3 space-y-2">
						<div class="text-xs text-muted-foreground mb-2">请选择:</div>
						{#each message.options as option (option.value)}
							<Button 
								variant="outline" 
								size="sm" 
								class="mr-2 mb-2"
								onclick={() => onOptionClick?.(option)}
							>
								{option.text}
							</Button>
						{/each}
					</div>
				{/if}

				<!-- 操作按钮 -->
				<div class="flex items-center gap-1 mt-2 opacity-60 hover:opacity-100 transition-opacity">
					<Button variant="ghost" size="sm" onclick={() => onCopy?.(message.id)} title="复制">
						<Copy class="w-3 h-3" />
					</Button>
					<Button variant="ghost" size="sm" onclick={() => onRegenerate?.(message.id)} title="重新生成">
						<RotateCcw class="w-3 h-3" />
					</Button>
					<Button variant="ghost" size="sm" onclick={() => onLike?.(message.id)} title="点赞">
						<ThumbsUp class="w-3 h-3" />
					</Button>
					<Button variant="ghost" size="sm" onclick={() => onDislike?.(message.id)} title="点踩">
						<ThumbsDown class="w-3 h-3" />
					</Button>
				</div>
			</div>
		</div>
	{/if}
</div>
