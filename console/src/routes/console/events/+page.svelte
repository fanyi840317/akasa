<script lang="ts">
	import { ChevronRightIcon, FolderIcon, FileIcon } from '@lucide/svelte';
	import AiInput from '$lib/components/ai/ai-input.svelte';
	import * as Card from '$lib/components/ui/card';
	import { goto } from '$app/navigation';
	import EventCard from '$lib/components/event/event-card.svelte';
	import { eventStore } from '$lib/stores/event.svelte';
	import { onMount } from 'svelte';

	// let events: Event[] = $state([]);
	let events: any[]  = [];
	onMount(async () => {
		events = await eventStore.getEvents();
	});
</script>

<div class="flex-center flex-col p-10 gap-10">
	<h1 class="text-2xl font-extrabold">what do you want to create today?</h1>
	<AiInput class="w-4xl max-w-2xl" />
	<div class="flex flex-col items-start gap-4 min-w-4xl pt-10">
		<header class="flex-center gap-2">
			<FolderIcon class="w-6 h-6 text-foreground/50" />
			<h1 class="text-sm font-extrabold text-foreground/50">Create by you</h1>
		</header>
		<div class="w-full grid auto-rows-min gap-4 md:grid-cols-3 sm:grid-cols-3">
			{#each events as event}
				<!-- <div class="bg-card border aspect-square rounded-xl"></div> -->
				<EventCard {event} />
			{/each}
		</div>
	</div>
</div>

