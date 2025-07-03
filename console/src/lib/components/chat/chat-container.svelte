<script lang="ts">
	import { onMount } from 'svelte';
	import { chatStore, type ChatConfig } from '$lib/stores/chat.svelte';
	import MessageItem from './message-item.svelte';
	import ChatInput from './chat-input.svelte';
	import ChatConfigComponent from './chat-config.svelte';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent } from '$lib/components/ui/card';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import {
		Sheet,
		SheetContent,
		SheetHeader,
		SheetTitle,
		SheetTrigger
	} from '$lib/components/ui/sheet';
	import { Alert, AlertDescription } from '$lib/components/ui/alert';
	import { Settings, Trash2, AlertCircle } from '@lucide/svelte';

	// Props
	interface Props {
		threadId?: string;
		autoFocus?: boolean;
	}

	let { threadId, autoFocus = true }: Props = $props();

	// 组件引用
	let chatInputRef: { focus: () => void } | undefined;
	let messagesContainer: HTMLElement;
	let configSheetOpen = $state(false);

	// 响应式状态
	const messages = $derived(chatStore.getMessages());
	const isStreaming = $derived(chatStore.getIsStreaming());
	const error = $derived(chatStore.getError());
	const input = $derived(chatStore.getInput());
	const config = $derived(chatStore.getConfig());

	// 初始化聊天
	onMount(() => {
		alert(0);
		if (threadId) {
			chatStore.initializeChat(threadId);
		}

		if (autoFocus) {
			// 延迟聚焦，确保组件已渲染
			setTimeout(() => {
				chatInputRef?.focus();
			}, 100);
		}
	});

	// 监听消息变化，自动滚动到底部
	$effect(() => {
		if (messages.length > 0) {
			console.log('Chat initialized with threadId:',messages);
			setTimeout(() => {
				scrollToBottom();
			}, 100);
		}
	});

	// 滚动到底部
	function scrollToBottom() {
		if (messagesContainer) {
			messagesContainer.scrollTop = messagesContainer.scrollHeight;
		}
	}

	// 处理消息发送
	function handleSubmit(text: string) {
		chatStore.sendMessage(text);
	}

	// 处理停止生成
	function handleStop() {
		chatStore.stopStreaming();
	}

	// 处理输入变化
	function handleInput(text: string) {
		chatStore.setInput(text);
	}

	// 处理消息复制
	function handleCopy(messageId: string) {
		// 可以添加复制成功的提示
		console.log('Message copied:', messageId);
	}

	// 处理消息重新生成
	function handleRegenerate(messageId: string) {
		chatStore.regenerateMessage(messageId);
	}

	// 处理消息点赞
	function handleLike(messageId: string) {
		// 可以添加点赞逻辑
		console.log('Message liked:', messageId);
	}

	// 处理消息点踩
	function handleDislike(messageId: string) {
		// 可以添加点踩逻辑
		console.log('Message disliked:', messageId);
	}

	// 处理选项点击
	function handleOptionClick(option: { text: string; value: string }) {
		chatStore.handleOptionClick(option);
	}

	// 处理发送消息（用于计划反馈）
	function handleSendMessage(message: string, options?: { interruptFeedback?: string }) {
		chatStore.sendMessage(message);
	}

	// 处理切换研究报告
	function handleToggleResearch() {
		// 可以添加研究报告切换逻辑
		console.log('Toggle research report');
	}

	// 处理配置变化
	function handleConfigChange(newConfig: Partial<ChatConfig>) {
		chatStore.updateConfig(newConfig);
	}

	// 重置配置
	function handleConfigReset() {
		chatStore.updateConfig({
			deepThinking: true,
			backgroundInvestigation: false,
			planIterations: 3,
			temperature: 0.7,
			maxTokens: 2000,
			model: 'gpt-4-turbo',
			streamResponse: true
		});
	}

	// 清空聊天
	function handleClearChat() {
		if (confirm('Are you sure you want to clear this chat? This action cannot be undone.')) {
			chatStore.clearChat();
		}
	}

	// 关闭错误提示
	function dismissError() {
		chatStore.clearError();
	}
</script>

<div class="bg-base-200 flex-between h-content flex-col rounded-2xl border">
	<!-- 头部工具栏 -->
	<div class="flex-between w-full border-b p-1">
		<div class="flex items-center gap-2 px-4">
			<h2 class="text-lg font-semibold">Chat</h2>
			{#if threadId}
				<span class="text-muted-foreground text-sm">#{threadId.slice(0, 8)}</span>
			{/if}
		</div>

		<div class="flex items-center gap-2">
			<!-- 配置按钮 -->
			<Sheet bind:open={configSheetOpen}>
				<SheetTrigger>
					<Button variant="ghost" size="sm" title="Chat settings">
						<Settings class="h-4 w-4" />
					</Button>
				</SheetTrigger>
				<SheetContent side="right" class="w-80">
					<SheetHeader>
						<SheetTitle>Chat Settings</SheetTitle>
					</SheetHeader>
					<div class="mt-6">
						<ChatConfigComponent
							{config}
							onConfigChange={handleConfigChange}
							onReset={handleConfigReset}
						/>
					</div>
				</SheetContent>
			</Sheet>

			<!-- 清空聊天按钮 -->
			<Button
				variant="ghost"
				size="sm"
				onclick={handleClearChat}
				title="Clear chat"
				disabled={messages.length === 0}
			>
				<Trash2 class="h-4 w-4" />
			</Button>
		</div>
	</div>

	<!-- 错误提示 -->
	{#if error}
		<div class="p-4">
			<Alert variant="destructive">
				<AlertCircle class="h-4 w-4" />
				<AlertDescription class="flex items-center justify-between">
					<span>{error}</span>
					<Button variant="ghost" size="sm" onclick={dismissError} class="ml-2 h-auto p-1">
						×
					</Button>
				</AlertDescription>
			</Alert>
		</div>
	{/if}

	<!-- 消息列表 -->
	<div class="w-full flex-1 overflow-hidden">
		<ScrollArea class=" h-full w-full ">
			<div class="h-full w-full flex flex-center">
			<div bind:this={messagesContainer} class="min-h-full min-w-3xl max-w-4xl space-y-4 p-4">
				<!-- 消息列表 -->
				{#each messages as message (message.id)}
					<MessageItem
						{message}
						waitForFeedback={false}
						interruptMessage={null}
						onCopy={handleCopy}
						onRegenerate={handleRegenerate}
						onLike={handleLike}
						onDislike={handleDislike}
						onOptionClick={handleOptionClick}
						onSendMessage={handleSendMessage}
						onToggleResearch={handleToggleResearch}
					/>
				{/each}
			</div>

			</div>
		</ScrollArea>
	</div>

	<!-- 输入区域 -->
	<div class="flex-center w-full">
		<div class="p-4">
			<ChatInput
				class="w-3xl"
				bind:this={chatInputRef}
				value={input}
				{isStreaming}
				onSubmit={handleSubmit}
				onStop={handleStop}
				onInput={handleInput}
				placeholder="Type your message..."
			/>
		</div>
	</div>
</div>

<style>
	@reference "../../../app.css";

	.chat-container {
		@apply bg-background rounded-2xl border;
	}

	/* 自定义滚动条样式 */
	.chat-container :global(.scroll-area-viewport) {
		scrollbar-width: thin;
		scrollbar-color: hsl(var(--muted-foreground) / 0.2) transparent;
	}

	.chat-container :global(.scroll-area-viewport:hover) {
		scrollbar-color: hsl(var(--muted-foreground) / 0.4) transparent;
	}

	/* WebKit 浏览器滚动条样式 */
	.chat-container :global(.scroll-area-viewport::-webkit-scrollbar) {
		width: 6px;
	}

	.chat-container :global(.scroll-area-viewport::-webkit-scrollbar-track) {
		background: transparent;
	}

	.chat-container :global(.scroll-area-viewport::-webkit-scrollbar-thumb) {
		background-color: hsl(var(--muted-foreground) / 0.2);
		border-radius: 3px;
	}

	.chat-container :global(.scroll-area-viewport:hover::-webkit-scrollbar-thumb) {
		background-color: hsl(var(--muted-foreground) / 0.4);
	}
</style>
