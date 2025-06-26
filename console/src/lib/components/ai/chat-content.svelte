<script lang="ts">
	import { ScrollArea } from '../ui/scroll-area';
	import ChatMessage from './chat-message.svelte';
	import AiInput from './ai-input.svelte';
	import type { Message } from '@ai-sdk/svelte';
	import { Button } from '../ui/button';

	// Props - 移除业务相关的props，只保留UI相关的
	let {
		class: className = '',
		height = 'h-[calc(100%-120px)]',
		messages = $bindable([]),
		status = $bindable('ready'),
		error = $bindable(undefined),
		input = $bindable(''),
		suggestions = [],
		user,
		onSubmit,
		onCopyMessage,
		onRegenerateMessage,
		onLikeMessage,
		onDislikeMessage,
		onAdopt
	} = $props<{
		class?: string;
		height?: string;
		messages?: Message[];
		status?: string;
		error?: any;
		suggestions?: string[];
		input?: string;
		user?: any;
		onSubmit?: (text: string) => void;
		onCopyMessage?: (messageId: string) => void;
		onRegenerateMessage?: (messageId: string) => void;
		onLikeMessage?: (messageId: string) => void;
		onDislikeMessage?: (messageId: string) => void;
		onAdopt?: (type: string, data: any) => void;
	}>();

	// State
	let scrollAreaRef = $state<any>(null);

	// 滚动到底部函数
	function scrollToBottom() {
		if (scrollAreaRef) {
			// 使用ScrollArea的viewport来滚动
			const viewport = scrollAreaRef.querySelector('[data-slot="scroll-area-viewport"]');
			if (viewport) {
				viewport.scrollTop = viewport.scrollHeight;
			}
		}
	}

	// 处理消息发送 - 简化为纯UI逻辑
	function handleSubmit(text: string) {
		// 调用父组件提供的回调
		onSubmit?.(text);

		// 清空输入框
		input = '';

		// 滚动到底部
		setTimeout(() => {
			scrollToBottom();
		}, 100);
	}





	// 监听消息变化，自动滚动到底部
	$effect(() => {
		if (messages.length > 0) {
			setTimeout(() => {
				scrollToBottom();
			}, 100);
		}
	});
</script>

<div class="flex flex-col h-full {className} relative">
	<!-- Chat Messages -->
	<ScrollArea
		class="p-4 {height}"
		orientation="vertical"
		bind:ref={scrollAreaRef}
	>
		<div class="min-h-full">
			{#if messages.length === 0}
				<div class="flex-center flex-col">
					<div class="text-center opacity-60 py-8">
						
						<p>开始与 AI 对话</p>
						<p class="text-sm opacity-50">输入你的问题，我会尽力帮助你</p>
					</div>

					<div class="flex flex-col gap-4">
						{#each suggestions as suggestion}
							<Button variant="secondary"
								class="w-56 py-2 text-xs rounded-full"
								onclick={() => {
									handleSubmit(suggestion);
								}}>{suggestion}</Button
							>
						{/each}
					</div>
				</div>
			{/if}
			<div class="flex flex-col gap-4 pb-4">
				{#each messages as message}
					<ChatMessage
					{message}
					{status}
					{user}
					onCopy={onCopyMessage}
					onRegenerate={onRegenerateMessage}
					onLike={onLikeMessage}
					onDislike={onDislikeMessage}
					onAdopt={onAdopt}
				/>
				{/each}
			</div>
		</div>
	</ScrollArea>

	<!-- 输入区域 -->
	<AiInput 
		class="mx-4 absolute bottom-0 left-0 right-0 z-10" 
		placeholder="输入消息..." 
		bind:inputValue={input} 
		onSubmit={handleSubmit}
		onSuggestionClick={handleSubmit}
		{suggestions}
		showRemind={true}
	/>
</div>
