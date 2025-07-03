<script lang="ts">
	import { cn } from '$lib/utils';
	import type { Message } from '$lib/types/message';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '$lib/components/ui/card';
	import RainbowText from '$lib/components/ui/rainbow-text.svelte';
	import ThoughtBlock from './thought-block.svelte';
	import { marked } from 'marked';
	import { fly } from 'svelte/transition';

	interface Props {
		class?: string;
		message?: Message;
		interruptMessage?: Message | null;
		onFeedback?: (feedback: { option: { text: string; value: string } }) => void;
		waitForFeedback?: boolean;
		onSendMessage?: (message: string, options?: { interruptFeedback?: string }) => void;
	}

	let {
		class: className,
		message = $bindable(undefined),
		interruptMessage,
		onFeedback,
		waitForFeedback = false,
		onSendMessage
	}: Props = $props();

	const GREETINGS = ['Cool', 'Sounds great', 'Looks good', 'Great', 'Awesome'];

	// 解析计划内容
	const plan = $derived.by(() => {
		try {
			return JSON.parse(message?.content ?? '{}');
		} catch {
			return {};
		}
	});

	const reasoningContent = $derived(message?.reasoningContent);
	const hasMainContent = $derived(Boolean(message?.content && message?.content.trim() !== ''));

	// 判断是否正在思考：有推理内容但还没有主要内容
	const isThinking = $derived(Boolean(reasoningContent) && !hasMainContent);

	// 判断是否应该显示计划：有主要内容就显示（无论是否还在流式传输）
	const shouldShowPlan = $derived(hasMainContent);

	function handleAccept() {
		if (onSendMessage) {
			const greeting = GREETINGS[Math.floor(Math.random() * GREETINGS.length)];
			const action = Math.random() > 0.5 ? "Let's get started." : "Let's start.";
			onSendMessage(`${greeting}! ${action}`, {
				interruptFeedback: 'accepted'
			});
		}
	}

	function handleOptionClick(option: { text: string; value: string }) {
		if (option.value === 'accepted') {
			handleAccept();
		} else {
			onFeedback?.({ option });
		}
	}
</script>

<div class={cn('w-full', className)}>
	{#if reasoningContent}
		<ThoughtBlock content={reasoningContent||""} isStreaming={Boolean(isThinking)} {hasMainContent} />
	{/if}

	{#if shouldShowPlan}
		<div in:fly={{ y: 20, duration: 300 }}>
			<Card class="w-full">
				<CardHeader>
					<CardTitle>
						<div class="prose prose-sm dark:prose-invert max-w-none">
							{@html marked(
								`### ${
									plan.title !== undefined && plan.title !== '' ? plan.title : 'Deep Research'
								}`
							)}
						</div>
					</CardTitle>
				</CardHeader>
				<CardContent>
					{#if plan.thought}
						<div class="prose prose-sm dark:prose-invert mb-4 max-w-none opacity-80">
							{@html marked(plan.thought)}
						</div>
					{/if}

					{#if plan.steps && Array.isArray(plan.steps)}
						<ul class="border-border my-2 flex list-decimal flex-col gap-4 border-l-2 pl-8">
							{#each plan.steps as step, i (i)}
								<li>
									{#if step.title}
										<h3 class="mb-1 text-lg font-medium">
											<div class="prose prose-sm dark:prose-invert max-w-none">
												{@html marked(step.title)}
											</div>
										</h3>
									{/if}
									{#if step.description}
										<div class="text-muted-foreground text-sm">
											<div class="prose prose-sm dark:prose-invert max-w-none">
												{@html marked(step.description)}
											</div>
										</div>
									{/if}
								</li>
							{/each}
						</ul>
					{/if}
				</CardContent>
				<CardFooter class="flex justify-end">
					{#if !message?.isStreaming && interruptMessage?.options?.length}
						<div class="flex gap-2" in:fly={{ y: 12, duration: 300, delay: 300 }}>
							{#each interruptMessage.options as option (option.value)}
								<Button
									variant={option.value === 'accepted' ? 'default' : 'outline'}
									disabled={!waitForFeedback}
									onclick={() => handleOptionClick(option)}
								>
									{option.text}
								</Button>
							{/each}
						</div>
					{/if}
				</CardFooter>
			</Card>
		</div>
	{/if}
</div>
