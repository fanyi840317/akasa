<script lang="ts">
	import { page } from '$app/stores';
	import { chatStore } from '$lib/stores/chat.svelte';
	import { cn } from '$lib/utils';
	import MessagesBlock from '$lib/components/chat/messages-block.svelte';
	import ResearchBlock from '$lib/components/chat/research-block.svelte';
	import { onMount, untrack } from 'svelte';
	import { appStore } from '$lib/stores/app-state';

	const threadId = $derived($page.params.id);
	const openResearchId = $derived(chatStore.openResearchId);
	const doubleColumnMode = $derived(openResearchId !== null);

	// 初始化侧边栏状态
	onMount(() => {
		appStore.setSidebarCollapsed(true);
	});

	// 监听 threadId 变化，重新加载聊天
	// 使用 untrack 避免不必要的响应式依赖
	let lastThreadId = $state<string | undefined>(undefined);
	
	$effect(() => {
		// 只有当 threadId 真正变化时才重新初始化
		if (threadId && threadId !== lastThreadId) {
			lastThreadId = threadId;
			// 使用 untrack 避免 initializeChat 内部的状态变化触发新的 effect
			untrack(() => {
				chatStore.initializeChat(threadId);
			});
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
