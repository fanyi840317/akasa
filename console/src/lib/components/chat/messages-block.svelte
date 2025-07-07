<script lang="ts">
	import { onMount } from 'svelte';
	import { chatStore, type ChatConfig } from '$lib/stores/chat.svelte';
	import { type Option, type Resource } from '$lib/types/message';
	import MessageListView from './message-list-view.svelte';
	import ChatInput from './chat-input.svelte';
	import ChatConfigComponent from './chat-config.svelte';
	import ConversationStarter from './conversation-starter.svelte';
	import { Button } from '$lib/components/ui/button';
	import {
		Sheet,
		SheetContent,
		SheetHeader,
		SheetTitle,
		SheetTrigger
	} from '$lib/components/ui/sheet';
	import { Alert, AlertDescription } from '$lib/components/ui/alert';
	import { Settings, Trash2, AlertCircle } from '@lucide/svelte';
	import { cn } from '$lib/utils';

	// Props
	interface Props {
		class?: string;
		threadId?: string;
		autoFocus?: boolean;
	}

	let { class: className, threadId, autoFocus = true }: Props = $props();

	// 组件引用
	let chatInputRef: { focus: () => void } | undefined;
	let abortControllerRef: AbortController | null = null;
	let configSheetOpen = $state(false);

	// 响应式状态
	const messageIds = $derived(chatStore.getMessageIds());
	const messageCount = $derived(messageIds.length);
	const responding = $derived(chatStore.getIsStreaming());
	const error = $derived(chatStore.getError());
	const input = $derived(chatStore.getInput());
	const config = $derived(chatStore.getConfig());

	// 反馈状态
	let feedback = $state<Option | undefined>(undefined);

	// 自动聚焦
	onMount(() => {
		if (autoFocus) {
			// 延迟聚焦，确保组件已渲染
			setTimeout(() => {
				chatInputRef?.focus();
			}, 100);
		}
	});

	// 处理消息发送
	async function handleSend(
		message: string,
		options?: {
			interruptFeedback?: string;
			resources?: Array<Resource>;
		}
	) {
		const abortController = new AbortController();
		abortControllerRef = abortController;
		try {
			await chatStore.sendMessage(message, {
				interruptFeedback: options?.interruptFeedback ?? feedback?.value,
				resources: options?.resources
			});
		} catch (error) {
			// 处理发送错误
			console.error('Send message error:', error);
		}
	}

	// 处理取消
	function handleCancel() {
		abortControllerRef?.abort();
		abortControllerRef = null;
		chatStore.stopStreaming();
	}

	// 处理反馈
	function handleFeedback(feedbackData: Option) {
		feedback = feedbackData;
	}

	// 移除反馈
	function handleRemoveFeedback() {
		feedback = undefined;
	}

	// 处理输入变化
	function handleInput(text: string) {
		chatStore.setInput(text);
	}

</script>

<div class={cn('bg-base-200 flex-between h-full flex-col rounded-2xl border', className)}>
	<!-- 头部工具栏 -->
	<div class="flex-between w-full border-b p-1">
		<div class="flex items-center gap-2 px-4">
			<h2 class="text-lg font-semibold">Chat</h2>
			{#if threadId}
				<span class="text-muted-foreground text-sm">#{threadId.slice(0, 8)}</span>
			{/if}
		</div>
	</div>
	<!-- MessageListView -->
	<MessageListView class="flex flex-grow" onFeedback={handleFeedback} onSendMessage={handleSend} />

	<!-- 输入区域 -->
	<div class="min-h-32 relative flex shrink-0 pb-4 w-full max-w-3xl">
		{#if !responding && messageCount === 0}
			<ConversationStarter class="absolute left-0 top-[-218px]" onSend={handleSend} />
		{/if}
		<ChatInput
			bind:this={chatInputRef}
			class="h-full w-full"
			value={input}
			{responding}
			{feedback}
			onSend={handleSend}
			onCancel={handleCancel}
			onInput={handleInput}
			onRemoveFeedback={handleRemoveFeedback}
			placeholder="Type your message..."
		/>
	</div>
</div>
