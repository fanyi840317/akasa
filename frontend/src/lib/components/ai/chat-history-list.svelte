<script lang="ts">
	import ChatHistoryCard from './chat-history-card.svelte';

	interface ChatHistory {
		id: string;
		title: string;
		summary: string;
		messageCount: number;
		timestamp: string;
	}

	export let histories: ChatHistory[] = [];
	export let onCardClick: ((history: ChatHistory) => void) | undefined = undefined;
	export let title: string = '历史对话';
</script>

<div class=" ">
	<!-- <h3 class="text-lg font-semibold mb-4">{title}</h3> -->
	<div class="stack space-y-3">
		{#each histories.slice(1)  as history (history.id)}
			<ChatHistoryCard
				title={history.title}
				summary={history.summary}
				messageCount={history.messageCount}
				timestamp={history.timestamp}
				onClick={() => onCardClick?.(history)}
			/>
		{/each}
		
		{#if histories.length === 0}
			<div class="text-center text-base-content/50 py-8">
				暂无历史对话
			</div>
		{/if}
	</div>
</div>