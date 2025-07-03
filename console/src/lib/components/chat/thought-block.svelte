<script lang="ts">
	import { cn } from '$lib/utils';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent } from '$lib/components/ui/card';
	import {
		Collapsible,
		CollapsibleContent,
		CollapsibleTrigger
	} from '$lib/components/ui/collapsible';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import LoadingAnimation from '$lib/components/ui/loading-animation.svelte';
	import { ChevronDown, ChevronRight, Lightbulb } from '@lucide/svelte';
	import { marked } from 'marked';

	interface Props {
		class?: string;
		content: string;
		isStreaming?: boolean;
		hasMainContent?: boolean;
	}

	let { class: className, content, isStreaming = false, hasMainContent = false }: Props = $props();

	let isOpen = $state(true);
	let hasAutoCollapsed = $state(false);

	// 当有主要内容时自动折叠
	$effect(() => {
		if (hasMainContent && !hasAutoCollapsed) {
			isOpen = false;
			hasAutoCollapsed = true;
		}
	});

	// 渲染 Markdown 内容
	const renderedContent = $derived.by(() => {
		if (content) {
			return marked(content, { breaks: true });
		}
		return '';
	});

	function toggleOpen() {
		isOpen = !isOpen;
	}
</script>

{#if content && content.trim() !== ''}
	<div class={cn('mb-6 w-full', className)}>
		<Collapsible open={isOpen} onOpenChange={toggleOpen}>
			<CollapsibleTrigger>
				<Button
					variant="ghost"
					class={cn(
						'h-auto w-full justify-start rounded-xl border px-6 py-4 text-left transition-all duration-200',
						'hover:bg-accent hover:text-accent-foreground',
						isStreaming ? 'border-primary/20 bg-primary/5 shadow-sm' : 'border-border bg-card'
					)}
				>
					<div class="flex w-full items-center gap-3">
						<Lightbulb
							size={18}
							class={cn(
								'shrink-0 transition-colors duration-200',
								isStreaming ? 'text-primary' : 'text-muted-foreground'
							)}
						/>
						<span
							class={cn(
								'font-semibold leading-none transition-colors duration-200',
								isStreaming ? 'text-primary' : 'text-foreground'
							)}
						>
							Deep Thinking
						</span>
						{#if isStreaming}
							<LoadingAnimation class="ml-2 scale-75" size="sm" />
						{/if}
						<div class="flex-grow"></div>
						{#if isOpen}
							<ChevronDown
								size={16}
								class="text-muted-foreground transition-transform duration-200"
							/>
						{:else}
							<ChevronRight
								size={16}
								class="text-muted-foreground transition-transform duration-200"
							/>
						{/if}
					</div>
				</Button>
			</CollapsibleTrigger>
			<CollapsibleContent class="mt-3">
				<Card
					class={cn(
						'transition-all duration-200',
						isStreaming ? 'border-primary/20 bg-primary/5' : 'border-border'
					)}
				>
					<CardContent class="p-4">
						<ScrollArea class="h-40 w-full">
							<div class="prose prose-sm dark:prose-invert max-w-none opacity-80">
								{@html renderedContent}
							</div>
						</ScrollArea>
					</CardContent>
				</Card>
			</CollapsibleContent>
		</Collapsible>
	</div>
{/if}
