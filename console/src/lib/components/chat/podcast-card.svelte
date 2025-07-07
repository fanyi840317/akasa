<script lang="ts">
	import { type Message } from '$lib/types/message';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Download, Headphones } from '@lucide/svelte';
	import LoadingAnimation from '$lib/components/ui/loading-animation.svelte';
	import RainbowText from '$lib/components/ui/rainbow-text.svelte';
	import { cn } from '$lib/utils';

	// Props
	interface Props {
		class?: string;
		message: Message;
	}

	let { class: className, message }: Props = $props();

	// 解析播客数据
	const data = $derived(() => {
		try {
			return JSON.parse(message.content || '{}');
		} catch {
			return {};
		}
	});

	const title = $derived(data.title);
	const audioUrl = $derived(data.audioUrl);
	const isGenerating = $derived(message.isStreaming);
	const hasError = $derived(data.error !== undefined);

	// 播放状态
	let isPlaying = $state(false);

	function handlePlay() {
		isPlaying = true;
	}

	function handlePause() {
		isPlaying = false;
	}
</script>

<Card class={cn('w-[508px]', className)}>
	<CardHeader>
		<div class="text-muted-foreground flex items-center justify-between text-sm">
			<div class="flex items-center gap-2">
				{#if isGenerating}
					<LoadingAnimation class="h-4 w-4" />
				{:else}
					<Headphones size={16} />
				{/if}
				{#if !hasError}
					<RainbowText animated={isGenerating}>
						{#if isGenerating}
							Generating podcast...
						{:else if isPlaying}
							Now playing podcast...
						{:else}
							Podcast
						{/if}
					</RainbowText>
				{:else}
					<div class="text-red-500">
						Error when generating podcast. Please try again.
					</div>
				{/if}
			</div>
			{#if !hasError && !isGenerating && audioUrl}
				<div class="flex">
					<Button variant="ghost" size="icon" title="Download podcast">
						<a
							href={audioUrl}
							download={`${(title ?? 'podcast').replaceAll(' ', '-')}.mp3`}
							class="flex items-center justify-center"
						>
							<Download size={16} />
						</a>
					</Button>
				</div>
			{/if}
		</div>
		<CardTitle>
			<div class="text-lg font-medium">
				<RainbowText animated={isGenerating}>{title}</RainbowText>
			</div>
		</CardTitle>
	</CardHeader>
	<CardContent>
		{#if audioUrl}
			<audio
				class="w-full"
				src={audioUrl}
				controls
				onplay={handlePlay}
				onpause={handlePause}
			/>
		{:else}
			<div class="w-full"></div>
		{/if}
	</CardContent>
</Card>