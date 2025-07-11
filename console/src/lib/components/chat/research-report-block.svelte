<script lang="ts">
	import { chatStore } from '$lib/stores/chat.svelte';
	import { cn } from '$lib/utils';
	import { FileText, Edit3, Save, X } from '@lucide/svelte';
	import { Button } from '$lib/components/ui/button';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Card } from '$lib/components/ui/card';
	import LoadingAnimation from '$lib/components/ui/loading-animation.svelte';
	import AutoScrollContainer from '$lib/components/ui/auto-scroll-container.svelte';
	import { marked } from 'marked';

	interface Props {
		class?: string;
		researchId: string;
		messageId: string;
		editing?: boolean;
	}

	let { class: className, researchId, messageId, editing = false }: Props = $props();

	// 获取报告消息
	const message = $derived(chatStore.getMessage(messageId));
	const isCompleted = $derived(message?.isStreaming === false && message?.content !== '');

	// 处理 Markdown 内容变化（如果需要编辑功能）
	function handleMarkdownChange(markdown: string) {
		if (message) {
			// 更新消息内容
			chatStore.updateMessage(messageId, { content: markdown });
		}
	}
</script>

<AutoScrollContainer 
	class={cn('w-full pt-4 pb-8', className)}
	scrollTriggers={[message?.content]}
	continuousScroll={false}
>
	{#snippet children()}
		{#if editing && isCompleted}
			<!-- 编辑模式 - 可以在这里添加富文本编辑器 -->
			<div class="border rounded-md p-4">
				<textarea 
					class="w-full h-96 p-4 border rounded resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
					value={message?.content || ''}
					placeholder="编辑报告内容..."
				></textarea>
				<div class="mt-2 text-sm text-gray-500">
					支持 Markdown 格式
				</div>
			</div>
		{:else}
			<!-- 显示模式 -->
			<div class="prose prose-lg max-w-none">
				{#if message?.content}
					{@html marked(message.content)}
				{:else}
					<div class="text-gray-500 italic">报告内容为空</div>
				{/if}
			</div>
			
			{#if message?.isStreaming}
				<LoadingAnimation class="my-12" />
			{/if}
		{/if}
	{/snippet}
</AutoScrollContainer>

<style>
	/* 自定义 prose 样式以适应主题 */
	.prose {
		color: inherit;
		max-width: none;
	}
	
	.prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6 {
		color: inherit;
		margin-top: 2em;
		margin-bottom: 1em;
		font-weight: 600;
	}
	
	.prose h1 {
		font-size: 2.25em;
		line-height: 1.2;
	}
	
	.prose h2 {
		font-size: 1.875em;
		line-height: 1.3;
	}
	
	.prose h3 {
		font-size: 1.5em;
		line-height: 1.4;
	}
	
	.prose p {
		margin-top: 1.25em;
		margin-bottom: 1.25em;
		line-height: 1.7;
	}
	
	.prose ul, .prose ol {
		margin-top: 1.25em;
		margin-bottom: 1.25em;
		padding-left: 1.5em;
	}
	
	.prose li {
		margin-top: 0.5em;
		margin-bottom: 0.5em;
	}
	
	.prose blockquote {
		border-left: 4px solid hsl(var(--border));
		padding-left: 1em;
		margin: 1.5em 0;
		font-style: italic;
		color: hsl(var(--muted-foreground));
	}
	
	.prose code {
		background-color: hsl(var(--muted));
		padding: 0.2em 0.4em;
		border-radius: 0.25rem;
		font-size: 0.875em;
	}
	
	.prose pre {
		background-color: hsl(var(--muted));
		padding: 1em;
		border-radius: 0.5rem;
		overflow-x: auto;
		margin: 1.5em 0;
	}
	
	.prose pre code {
		background-color: transparent;
		padding: 0;
	}
	
	.prose table {
		width: 100%;
		border-collapse: collapse;
		margin: 1.5em 0;
	}
	
	.prose th, .prose td {
		border: 1px solid hsl(var(--border));
		padding: 0.75em;
		text-align: left;
	}
	
	.prose th {
		background-color: hsl(var(--muted));
		font-weight: 600;
	}
	
	.prose a {
		color: hsl(var(--primary));
		text-decoration: underline;
	}
	
	.prose a:hover {
		color: hsl(var(--primary) / 0.8);
	}
	
	.prose img {
		max-width: 100%;
		height: auto;
		border-radius: 0.5rem;
		margin: 1.5em 0;
	}
	
	.prose hr {
		border: none;
		border-top: 1px solid hsl(var(--border));
		margin: 2em 0;
	}
</style>