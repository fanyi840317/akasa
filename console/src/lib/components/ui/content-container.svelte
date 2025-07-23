<script lang="ts">
	import type { Snippet } from 'svelte';
	import { ScrollArea } from '$lib/components/ui/scroll-area';

	interface Props {
		children: Snippet;
		maxWidth?: string;
		padding?: string;
		centered?: boolean;
	}

	let {
		children,
		maxWidth = 'max-w-[776px]',
		padding = 'p-6',
		centered = true
	}: Props = $props();
</script>

<ScrollArea class="h-full">
	<div class="{centered ? 'flex-center' : 'flex flex-col'} space-y-6">
		<div class="{centered ? 'mx-auto' : ''} w-full {maxWidth} space-y-6 {padding}">
			<!-- 内容区域 -->
			{@render children()}
		</div>
	</div>
</ScrollArea>