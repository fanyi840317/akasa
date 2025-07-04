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

<div
	class={cn(
		'flex h-full w-full justify-center px-4 pt-12 pb-4',
		doubleColumnMode && 'gap-8'
	)}
>
	<MessagesBlock
		class={cn(
			'shrink-0 transition-all duration-300 ease-out',
			!doubleColumnMode && 'w-[768px]',
			doubleColumnMode && 'w-[538px]'
		)}
		{threadId}
		autoFocus={false}
	/>
	<ResearchBlock
		class={cn(
			'w-[min(max(calc((100vw-538px)*0.75),575px),960px)] pb-4 transition-all duration-300 ease-out',
			!doubleColumnMode && 'scale-0',
			doubleColumnMode && ''
		)}
		researchId={openResearchId}
	/>
</div>
