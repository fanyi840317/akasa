<script lang="ts">
	import { onMount } from 'svelte';
	import { chatStore } from '$lib/stores/chat.svelte';
    import { type Message, type Option } from '$lib/types/message';
	import MessageItem from './message-item.svelte';
	import PlanCard from './plan-card.svelte';
	import PodcastCard from './podcast-card.svelte';
	import ResearchCard from './research-card.svelte';
	import LoadingAnimation from '$lib/components/ui/loading-animation.svelte';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import { cn } from '$lib/utils';

	// Props
	interface Props {
		class?: string;
		onFeedback?: (feedback: Option) => void;
		onSendMessage?: (message: string, options?: { interruptFeedback?: string }) => void;
	}

	let { class: className, onFeedback, onSendMessage }: Props = $props();

	// 组件引用
	let scrollContainer: HTMLElement;

	// 响应式状态
	const messageIds = $derived(chatStore.getMessageIds());
	const interruptMessage = $derived(chatStore.getLastInterruptMessage());
	const waitingForFeedbackMessageId = $derived(chatStore.getLastFeedbackMessageId());
	const responding = $derived(chatStore.getIsStreaming());
	const noOngoingResearch = $derived(chatStore.getOngoingResearchId() === null);
	const ongoingResearchIsOpen = $derived(
		chatStore.getOngoingResearchId() === chatStore.getOpenResearchId()
	);
	const researchIds = $derived(chatStore.getResearchIds());

	// 自动滚动到底部
	$effect(() => {
		if (messageIds.length > 0) {
			console.log(messageIds);
			console.log(chatStore.messages);
			setTimeout(() => {
				scrollToBottom();
			}, 100);
		}
	});

	function scrollToBottom() {
		if (scrollContainer) {
			scrollContainer.scrollTop = scrollContainer.scrollHeight;
		}
	}

	function handleToggleResearch() {
		// 修复切换研究时自动滚动到底部偶尔失败的问题
		setTimeout(() => {
			scrollToBottom();
		}, 500);
	}
</script>

<ScrollArea class={cn('flex h-full w-full flex-col overflow-hidden', className)}>
	<div bind:this={scrollContainer} class="flex h-full w-full flex-col overflow-y-auto">
		<ul class="flex flex-col">
			{#each messageIds as messageId (messageId)}
				{@const message = chatStore.getMessage(messageId)}
				{@const startOfResearch = researchIds.includes(messageId)}
				{#if message && (message.role === 'user' || message.agent === 'coordinator' || message.agent === 'planner' || message.agent === 'podcast' || startOfResearch)}
					<li class="mt-10 opacity-0 animate-in fade-in-0 slide-in-from-bottom-6 duration-200">
						{#if message.agent === 'planner'}
							<div class="w-full px-4">
								<PlanCard
									{message}
									waitForFeedback={waitingForFeedbackMessageId === messageId}
									{interruptMessage}
									{onFeedback}
									{onSendMessage}
								/>
							</div>
						{:else if message.agent === 'podcast'}
							<div class="w-full px-4">
								<PodcastCard {message} />
							</div>
						{:else if startOfResearch}
							<div class="w-full px-4">
								<ResearchCard researchId={message.id} onToggleResearch={handleToggleResearch} />
							</div>
						{:else if message.content}
							<div class={cn('flex w-full px-4', message.role === 'user' && 'justify-end')}>
								<div
									class={cn(
										'group flex w-fit max-w-[85%] flex-col rounded-2xl px-4 py-3 shadow',
										message.role === 'user' && 'bg-primary text-primary-foreground rounded-ee-none',
										message.role === 'assistant' && 'bg-card rounded-es-none'
									)}
								>
									<div class="flex w-full flex-col text-wrap break-words">
										<MessageItem
											{message}
											waitForFeedback={false}
											interruptMessage={null}
											onCopy={() => {}}
											onRegenerate={() => {}}
											onLike={() => {}}
											onDislike={() => {}}
											onOptionClick={() => {}}
											onSendMessage={() => {}}
											onToggleResearch={() => {}}
										/>
									</div>
								</div>
							</div>
						{/if}
					</li>
				{/if}
			{/each}
			<div class="flex h-8 w-full shrink-0"></div>
		</ul>
		{#if responding && (noOngoingResearch || !ongoingResearchIsOpen)}
			<LoadingAnimation class="ml-4" />
		{/if}
	</div>
</ScrollArea>