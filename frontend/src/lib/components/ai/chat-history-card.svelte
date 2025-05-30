<script lang="ts">
	import InfoCard from '$lib/components/ui/card/info-card.svelte';

	export let title: string;
	export let summary: string;
	export let messageCount: number;
	export let timestamp: string;
	export let onClick: (() => void) | undefined = undefined;
</script>

<InfoCard
	class="shadow-sm rounded-lg bg-base-300 w-[100px] min-w-[120px] max-w-[200px] hover:shadow-md transition-shadow cursor-pointer m-2"
	title={title}
	description={timestamp}
	info={messageCount.toString()}
	size="xs"
	onclick={onClick}
	role="button"
>
	<div class="text-[10px] leading-tight text-base-content/70 line-clamp-3 px-1">
		{summary}
	</div>
</InfoCard>