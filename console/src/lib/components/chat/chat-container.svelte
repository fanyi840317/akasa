<script lang="ts">
	import { onMount } from 'svelte';
	import { chatStore } from '$lib/stores/chat.svelte';
	import MessageItem from './message-item.svelte';
	import ChatInput from './chat-input.svelte';
	import ChatConfig from './chat-config.svelte';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent } from '$lib/components/ui/card';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from '$lib/components/ui/sheet';
	import { Alert, AlertDescription } from '$lib/components/ui/alert';
	import { Settings, Trash2, AlertCircle } from '@lucide/svelte';

	// Props
	interface Props {
		threadId?: string;
		autoFocus?: boolean;
	}

	let {
		threadId,
		autoFocus = true
	}: Props = $props();

	// 组件引用
	let chatInputRef: any;
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

	// 处理配置变化
	function handleConfigChange(newConfig: any) {
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

<div class="chat-container flex flex-col h-full">
	<!-- 头部工具栏 -->
	<div class="flex items-center justify-between p-4 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
		<div class="flex items-center gap-2">
			<h2 class="text-lg font-semibold">Chat</h2>
			{#if threadId}
				<span class="text-sm text-muted-foreground">#{threadId.slice(0, 8)}</span>
			{/if}
		</div>
		
		<div class="flex items-center gap-2">
			<!-- 配置按钮 -->
			<Sheet bind:open={configSheetOpen}>
				<SheetTrigger asChild>
					<Button variant="ghost" size="sm" title="Chat settings">
						<Settings class="w-4 h-4" />
					</Button>
				</SheetTrigger>
				<SheetContent side="right" class="w-80">
					<SheetHeader>
						<SheetTitle>Chat Settings</SheetTitle>
					</SheetHeader>
					<div class="mt-6">
						<ChatConfig
							config={config}
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
				<Trash2 class="w-4 h-4" />
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
					<Button 
						variant="ghost" 
						size="sm" 
						onclick={dismissError}
						class="h-auto p-1 ml-2"
					>
						×
					</Button>
				</AlertDescription>
			</Alert>
		</div>
	{/if}

	<!-- 消息列表 -->
	<div class="flex-1 overflow-hidden">
		<ScrollArea class="h-full">
			<div 
				bind:this={messagesContainer}
				class="p-4 space-y-4 min-h-full"
			>
				{#if messages.length === 0}
					<!-- 空状态 -->
					<div class="flex items-center justify-center h-full">
						<Card class="w-full max-w-md">
							<CardContent class="p-6 text-center">
								<div class="w-12 h-12 mx-auto mb-4 rounded-full bg-muted flex items-center justify-center">
									<Settings class="w-6 h-6 text-muted-foreground" />
								</div>
								<h3 class="text-lg font-semibold mb-2">Start a conversation</h3>
								<p class="text-muted-foreground text-sm mb-4">
									Type a message below to begin chatting with the AI assistant.
								</p>
								<Button 
									variant="outline" 
									size="sm"
									onclick={() => configSheetOpen = true}
								>
									<Settings class="w-4 h-4 mr-2" />
									Configure Chat
								</Button>
							</CardContent>
						</Card>
					</div>
				{:else}
					<!-- 消息列表 -->
					{#each messages as message (message.id)}
						<MessageItem
							message={message}
							onCopy={handleCopy}
							onRegenerate={handleRegenerate}
							onLike={handleLike}
							onDislike={handleDislike}
							onOptionClick={handleOptionClick}
						/>
					{/each}
				{/if}
			</div>
		</ScrollArea>
	</div>

	<!-- 输入区域 -->
	<div class="border-t bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
		<div class="p-4">
			<ChatInput
				bind:this={chatInputRef}
				value={input}
				isStreaming={isStreaming}
				onSubmit={handleSubmit}
				onStop={handleStop}
				onInput={handleInput}
				placeholder="Type your message..."
			/>
		</div>
	</div>
</div>

<style>
	.chat-container {
		@apply bg-background;
	}
	
	/* 自定义滚动条样式 */
	.chat-container :global(.scroll-area-viewport) {
		@apply scrollbar-thin scrollbar-track-transparent scrollbar-thumb-muted-foreground/20;
	}
	
	.chat-container :global(.scroll-area-viewport:hover) {
		@apply scrollbar-thumb-muted-foreground/40;
	}
</style>