<script lang="ts">
	import type { Message } from '$lib/types/message';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent } from '$lib/components/ui/card';
	import { Badge } from '$lib/components/ui/badge';
	import { Copy, RotateCcw, ThumbsUp, ThumbsDown, User, Bot } from '@lucide/svelte';
	import { marked } from 'marked';

	// Props
	interface Props {
		message: Message;
		onCopy?: (messageId: string) => void;
		onRegenerate?: (messageId: string) => void;
		onLike?: (messageId: string) => void;
		onDislike?: (messageId: string) => void;
		onOptionClick?: (option: { text: string; value: string }) => void;
	}

	let {
		message,
		onCopy,
		onRegenerate,
		onLike,
		onDislike,
		onOptionClick
	}: Props = $props();

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

<div class="message-item mb-4">
	<Card class="{message.role === 'user' ? 'ml-8 bg-primary/5' : 'mr-8'}">
		<CardContent class="p-4">
			<!-- 消息头部 -->
			<div class="flex items-center gap-2 mb-2">
				{#if message.role === 'user'}
					<User class="w-5 h-5 text-primary" />
					<span class="font-medium text-primary">You</span>
				{:else}
					<Bot class="w-5 h-5 text-muted-foreground" />
					<span class="font-medium text-muted-foreground">Assistant</span>
				{/if}
				
				{#if message.isStreaming}
					<Badge variant="secondary" class="text-xs">
						<div class="w-2 h-2 bg-green-500 rounded-full animate-pulse mr-1"></div>
						Generating...
					</Badge>
				{/if}
			</div>

			<!-- 消息内容 -->
			{#if message.content}
				<div class="prose prose-sm max-w-none dark:prose-invert">
					{@html renderedContent()}
				</div>
			{/if}

			<!-- 推理内容 -->
			{#if message.reasoningContent}
				<details class="mt-3">
					<summary class="cursor-pointer text-sm text-muted-foreground hover:text-foreground">
						Reasoning Process
					</summary>
					<div class="mt-2 p-3 bg-muted/50 rounded-md text-sm">
						<div class="prose prose-sm max-w-none dark:prose-invert">
							{@html marked(message.reasoningContent, { breaks: true })}
						</div>
					</div>
				</details>
			{/if}

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
				<div class="flex items-center gap-1 mt-3 pt-2 border-t">
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
		</CardContent>
	</Card>
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