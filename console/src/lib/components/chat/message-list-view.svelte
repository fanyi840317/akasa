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
		if (chatStore.messages) {
			console.log('正在自动滚动到底部');
		}
		if (messageIds.length > 0) {
			// 使用 requestAnimationFrame 确保 DOM 更新完成后再滚动
			requestAnimationFrame(() => {
				scrollToBottom();
			});
		}
	});

	// 监听流式响应状态变化，确保新内容出现时滚动到底部
	$effect(() => {
		if (responding) {
			console.log('正在流式响应');
			const scrollInterval = setInterval(() => {
				scrollToBottom();
			}, 100);

			return () => clearInterval(scrollInterval);
		}
	});

	function scrollToBottom() {
		if (scrollContainer) {
			// 使用更可靠的滚动方法
			const scrollHeight = scrollContainer.scrollHeight;
			const clientHeight = scrollContainer.clientHeight;
			scrollContainer.scrollTop = scrollHeight - clientHeight;

			// 备用方法：使用 scrollIntoView
			const lastChild = scrollContainer.lastElementChild;
			if (lastChild) {
				lastChild.scrollIntoView({ behavior: 'smooth', block: 'end' });
			}
		}
	}

	function handleToggleResearch() {
		// 修复切换研究时自动滚动到底部偶尔失败的问题
		requestAnimationFrame(() => {
			setTimeout(() => {
				scrollToBottom();
			}, 300);
		});
	}
</script>

<ScrollArea class={cn('flex  h-full w-full flex-col overflow-hidden  p-4', className)}>
	<div bind:this={scrollContainer} class="flex-start h-full w-full flex-col overflow-y-auto">
		<ul class="flex max-w-3xl flex-col gap-2">
			{#each messageIds as messageId (messageId)}
				{@const message = chatStore.getMessage(messageId)}
				{@const startOfResearch = researchIds.includes(messageId)}
				{#if message && (message.role === 'user' || message.agent === 'coordinator' || message.agent === 'planner' || message.agent === 'podcast' || startOfResearch)}
					<li class="animate-in fade-in-0 slide-in-from-bottom-6 duration-200
					{message.role === 'user' && 'flex items-center justify-end'}">
						{#if message.agent === 'planner'}
							<div class="w-full">
								<PlanCard {message} {interruptMessage} {onSendMessage} />
							</div>
						{:else if startOfResearch}
							<div class="w-full">
								<ResearchCard researchId={message.id} onToggleResearch={handleToggleResearch} />
							</div>
						{:else if message.content}
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
