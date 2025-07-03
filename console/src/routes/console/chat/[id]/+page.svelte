<script lang="ts">
	import { page } from '$app/stores';
	import { chatStore } from '$lib/stores/chat.svelte';
	import { cn } from '$lib/utils';
	import MessagesBlock from '$lib/components/chat/messages-block.svelte';
	import ResearchBlock from '$lib/components/chat/research-block.svelte';
	import { onMount } from 'svelte';

	const threadId = $derived($page.params.id);
	const openResearchId = $derived(chatStore.openResearchId);
	const doubleColumnMode = $derived(openResearchId !== null);

	// 初始化聊天
	onMount(() => {
		if (threadId) {
			chatStore.initializeChat(threadId);
		}
	});
</script>

<div class="flex-1 w-full h-content overflow-hidden">
	<div
		class={cn(
			'flex h-full w-full transition-all duration-300 ease-out',
			!doubleColumnMode && 'justify-center',
			doubleColumnMode && 'justify-center gap-2'
		)}
	>
		<MessagesBlock
			class={cn(
				'shrink-0 transition-all duration-300 ease-out',
				!doubleColumnMode && 'h-full w-full',
				doubleColumnMode && 'h-full w-[538px]'
			)}
			{threadId}
			autoFocus={false}
		/>
		{#if doubleColumnMode}
			<ResearchBlock
				class="h-full w-full transition-all duration-300 ease-out"
				researchId={openResearchId}
			/>
		{/if}
	</div>
</div>
