<script lang="ts">
	import type { Message } from '$lib/types/message';
	import { cn } from '$lib/utils';
	import { Button } from '$lib/components/ui/button';
	import { Badge } from '$lib/components/ui/badge';
	import { Copy, RotateCcw, ThumbsUp, ThumbsDown } from '@lucide/svelte';
	import { marked } from 'marked';
	import { fly } from 'svelte/transition';
	import MessageBubble from './message-bubble.svelte';
	import PlanCard from './plan-card.svelte';
	import ResearchCard from './research-card.svelte';
	import { chatStore } from '$lib/stores/chat.svelte';
	import { onMount } from 'svelte';

	// Props
	interface Props {
		message: Message;
		waitForFeedback?: boolean;
		interruptMessage?: Message | null;
		onCopy?: (messageId: string) => void;
		onRegenerate?: (messageId: string) => void;
		onLike?: (messageId: string) => void;
		onDislike?: (messageId: string) => void;
		onOptionClick?: (option: { text: string; value: string }) => void;
		onSendMessage?: (message: string, options?: { interruptFeedback?: string }) => void;
		onToggleResearch?: () => void;
	}

	let {
		message,
		waitForFeedback = false,
		interruptMessage,
		onCopy,
		onRegenerate,
		onLike,
		onDislike,
		onOptionClick,
		onSendMessage,
		onToggleResearch
	}: Props = $props();

	// 检查是否是研究开始
	const researchIds = $derived(() => chatStore.getResearchIds());
	const startOfResearch = $derived(() => researchIds().includes(message.id));

	// 渲染 Markdown 内容
	const renderedContent = $derived(() => {
		if (message.content) {
			console.log(message.content);
			return marked(message.content, { breaks: true });
		}
		return '';
	});

	// 处理复制
	function handleCopy() {
		if (message.content) {
			navigator.clipboard.writeText(message.content);
			onCopy?.(message.id);
		}
	}

	// 处理重新生成
	function handleRegenerate() {
		onRegenerate?.(message.id);
	}

	// 处理点赞
	function handleLike() {
		onLike?.(message.id);
	}

	// 处理点踩
	function handleDislike() {
		onDislike?.(message.id);
	}

	// 处理选项点击
	function handleOptionClick(option: { text: string; value: string }) {
		onOptionClick?.(option);
	}
	onMount(() => {});
</script>

<div class="mt-10" in:fly={{ y: 24, duration: 200, delay: 0 }}>
	{#if message.agent === 'planner'}
		<div class="w-full px-4">
			<PlanCard
				{message}
				{waitForFeedback}
				{interruptMessage}
				onFeedback={(feedback) => onOptionClick?.(feedback)}
				{onSendMessage}
			/>
		</div>
	{:else if startOfResearch()}
		<div class="w-full px-4">
			<ResearchCard researchId={message.id} {onToggleResearch} />
		</div>
	{:else if message.content}
		<div class={cn('flex w-full px-4', message.role === 'user' && 'justify-end')}>
			<MessageBubble {message}>
				<div class="flex w-full flex-col text-wrap break-words">
					<div
						class={cn(
							'prose prose-sm dark:prose-invert max-w-none',
							message.role === 'user' &&
								'prose-invert not-dark:text-primary-foreground dark:text-inherit'
						)}
					>
						{@html renderedContent()}
					</div>

					<!-- 工具调用 -->
					{#if message.toolCalls && message.toolCalls.length > 0}
						<div class="mt-3 space-y-2">
							{#each message.toolCalls as toolCall (toolCall.id)}
								<div class="bg-muted/30 rounded-md border p-3">
									<div class="mb-2 flex items-center gap-2">
										<Badge variant="outline" class="text-xs">
											{toolCall.name}
										</Badge>
									</div>

									{#if toolCall.args}
										<pre
											class="bg-background overflow-x-auto rounded border p-2 text-xs">{JSON.stringify(
												toolCall.args,
												null,
												2
											)}</pre>
									{/if}

									{#if toolCall.result}
										<div class="mt-2 text-sm">
											<strong>Result:</strong>
											<div class="bg-background mt-1 rounded border p-2">
												{toolCall.result}
											</div>
										</div>
									{/if}
								</div>
							{/each}
						</div>
					{/if}

					<!-- 选项按钮（用于中断反馈） -->
					{#if message.options && message.options.length > 0}
						<div class="mt-3 flex flex-wrap gap-2">
							{#each message.options as option (option.value)}
								<Button variant="outline" size="sm" onclick={() => handleOptionClick(option)}>
									{option.text}
								</Button>
							{/each}
						</div>
					{/if}

					<!-- 操作按钮 -->
					{#if message.role === 'assistant' && !message.isStreaming}
						<div class="border-border/50 mt-3 flex items-center gap-1 border-t pt-2">
							<Button variant="ghost" size="sm" onclick={handleCopy} title="Copy message">
								<Copy class="h-4 w-4" />
							</Button>

							<Button
								variant="ghost"
								size="sm"
								onclick={handleRegenerate}
								title="Regenerate response"
							>
								<RotateCcw class="h-4 w-4" />
							</Button>

							<Button variant="ghost" size="sm" onclick={handleLike} title="Like this response">
								<ThumbsUp class="h-4 w-4" />
							</Button>

							<Button
								variant="ghost"
								size="sm"
								onclick={handleDislike}
								title="Dislike this response"
							>
								<ThumbsDown class="h-4 w-4" />
							</Button>
						</div>
					{/if}
				</div>
			</MessageBubble>
		</div>
	{/if}
</div>

<style>
	@reference "../../../app.css";

	.message-item :global(.prose) {
		@apply text-foreground;
	}

	.message-item :global(.prose h1),
	.message-item :global(.prose h2),
	.message-item :global(.prose h3),
	.message-item :global(.prose h4),
	.message-item :global(.prose h5),
	.message-item :global(.prose h6) {
		@apply text-foreground font-semibold;
	}

	.message-item :global(.prose code) {
		@apply bg-muted rounded px-1 py-0.5 text-sm;
	}

	.message-item :global(.prose pre) {
		@apply bg-muted overflow-x-auto rounded-md p-3;
	}

	.message-item :global(.prose pre code) {
		@apply bg-transparent p-0;
	}

	.message-item :global(.prose blockquote) {
		@apply border-muted-foreground/20 border-l-4 pl-4 italic;
	}

	.message-item :global(.prose a) {
		@apply text-primary hover:underline;
	}
</style>
