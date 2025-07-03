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
</script>

{#if message.role === 'user' || message.agent === 'coordinator' || message.agent === 'planner' || message.agent === 'podcast' || startOfResearch}
	<div
		class="mt-10"
		in:fly={{ y: 24, duration: 200, delay: 0 }}
	>
		{#if message.agent === 'planner'}
			<div class="w-full px-4">
				<PlanCard
				{message}
				{waitForFeedback}
				{interruptMessage}
				onFeedback={(feedback) => onOptionClick?.(feedback.option)}
				{onSendMessage}
			/>
			</div>
		{:else if startOfResearch()}
			<div class="w-full px-4">
				<ResearchCard researchId={message.id} {onToggleResearch} />
			</div>
		{:else if message.content}
			<div
				class={cn(
					'flex w-full px-4',
					message.role === 'user' && 'justify-end'
				)}
			>
				<MessageBubble {message}>
					{#snippet children()}
						<div class="flex w-full flex-col text-wrap break-words">
							<div
								class={cn(
									'prose prose-sm max-w-none dark:prose-invert',
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
										<div class="border rounded-md p-3 bg-muted/30">
											<div class="flex items-center gap-2 mb-2">
												<Badge variant="outline" class="text-xs">
													{toolCall.name}
												</Badge>
											</div>
											
											{#if toolCall.args}
												<pre class="text-xs bg-background p-2 rounded border overflow-x-auto">{JSON.stringify(toolCall.args, null, 2)}</pre>
											{/if}
											
											{#if toolCall.result}
												<div class="mt-2 text-sm">
													<strong>Result:</strong>
													<div class="mt-1 p-2 bg-background rounded border">
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
										<Button 
											variant="outline" 
											size="sm"
											onclick={() => handleOptionClick(option)}
										>
											{option.text}
										</Button>
									{/each}
								</div>
							{/if}

							<!-- 操作按钮 -->
							{#if message.role === 'assistant' && !message.isStreaming}
								<div class="flex items-center gap-1 mt-3 pt-2 border-t border-border/50">
									<Button 
										variant="ghost" 
										size="sm"
										onclick={handleCopy}
										title="Copy message"
									>
										<Copy class="w-4 h-4" />
									</Button>
									
									<Button 
										variant="ghost" 
										size="sm"
										onclick={handleRegenerate}
										title="Regenerate response"
									>
										<RotateCcw class="w-4 h-4" />
									</Button>
									
									<Button 
										variant="ghost" 
										size="sm"
										onclick={handleLike}
										title="Like this response"
									>
										<ThumbsUp class="w-4 h-4" />
									</Button>
									
									<Button 
										variant="ghost" 
										size="sm"
										onclick={handleDislike}
										title="Dislike this response"
									>
										<ThumbsDown class="w-4 h-4" />
									</Button>
								</div>
							{/if}
						</div>
					{/snippet}
				</MessageBubble>
			</div>
		{/if}
	</div>
{/if}

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
		@apply bg-muted px-1 py-0.5 rounded text-sm;
	}
	
	.message-item :global(.prose pre) {
		@apply bg-muted p-3 rounded-md overflow-x-auto;
	}
	
	.message-item :global(.prose pre code) {
		@apply bg-transparent p-0;
	}
	
	.message-item :global(.prose blockquote) {
		@apply border-l-4 border-muted-foreground/20 pl-4 italic;
	}
	
	.message-item :global(.prose a) {
		@apply text-primary hover:underline;
	}
</style>