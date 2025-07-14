<script lang="ts">
	import { ChevronRightIcon, FolderIcon, FileIcon } from '@lucide/svelte';
	import AiInput from '$lib/components/ai/ai-input.svelte';
	import * as Card from '$lib/components/ui/card';
	import { goto } from '$app/navigation';
	import EventCard from '$lib/components/events/event-card.svelte';
	import { eventStore } from '$lib/stores/event.svelte';
	import { onMount } from 'svelte';
	import { appStore } from '$lib/stores/app-state';
	import { ScrollArea } from '$lib/components/ui/scroll-area';

	appStore.setSidebarCollapsed(false);
	// let events: Event[] = $state([]);
	let events: any[] = [];
	onMount(async () => {
		events = await eventStore.getEvents();
	});
</script>

<ScrollArea
	class="h-content bg-base-200 flex rounded-2xl border p-8"
>
	<div class="flex-center flex-col gap-10 p-10">
		<h1 class="text-3xl font-extrabold">What do you want to create today?</h1>
		<AiInput class="w-4xl max-w-2xl" />
		<!-- <div class="">
			<p class="text-muted-foreground text-sm">Create a new event</p>
		</div> -->
		<div class="min-w-4xl flex flex-col items-start gap-4 pt-10">
			<header class="flex-center gap-2">
				<FolderIcon class="text-foreground/50 h-6 w-6" />
				<h1 class="text-foreground/50 text-sm font-extrabold">Create by you</h1>
			</header>
			<div class="grid w-full auto-rows-min gap-4 sm:grid-cols-3 md:grid-cols-3">
				{#each events as event}
					<!-- <div class="bg-card border aspect-square rounded-xl"></div> -->
					<EventCard {event} />
				{/each}
			</div>
		</div>
	</div>
</ScrollArea>
