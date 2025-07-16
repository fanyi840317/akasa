<script lang="ts">
	import { ChevronRightIcon, FolderIcon, FileIcon, Search } from '@lucide/svelte';
	import { Input } from '$lib/components/ui/input';
	import * as Card from '$lib/components/ui/card';
	import { goto } from '$app/navigation';
	import EventCard from '$lib/components/events/event-card.svelte';
	import { eventStore } from '$lib/stores/event.svelte';
	import { onMount } from 'svelte';
	import { appStore } from '$lib/stores/app-state';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import PageHeader from '$lib/components/ui/page-header.svelte';

	appStore.setSidebarCollapsed(false);

	let allEvents: any[] = $state([]);
	let searchQuery = $state('');

	// 过滤后的事件
	const filteredEvents = $derived.by(() => {
		if (!searchQuery.trim()) return allEvents;
		return allEvents.filter(
			(event) =>
				event.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
				event.summary?.toLowerCase().includes(searchQuery.toLowerCase()) ||
				event.content?.toLowerCase().includes(searchQuery.toLowerCase())
		);
	});

	onMount(async () => {
		allEvents = await eventStore.getEvents();
	});
</script>

<div class="h-content bg-base-200 flex flex-col rounded-2xl border overflow-hidden">
	<PageHeader title="Events"  />
	<ScrollArea class="flex-center flex-col gap-10 p-10 h-full">
		<div class="flex-center flex-col gap-10 p-10">
			<h1 class="text-3xl font-extrabold">Search your events</h1>
			<div class="relative w-full max-w-2xl">
				<Search class="text-muted-foreground absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2" />
				<Input
					class="pl-10"
					placeholder="Search events by name, summary, or content..."
					bind:value={searchQuery}
				/>
			</div>
			<!-- <div class="">
				<p class="text-muted-foreground text-sm">Create a new event</p>
			</div> -->
			<div class="min-w-4xl flex flex-col items-start gap-4 pt-10">
				<header class="flex-center gap-2">
					<FolderIcon class="text-foreground/50 h-6 w-6" />
					<h1 class="text-foreground/50 text-sm font-extrabold">Create by you</h1>
				</header>
				<div class="grid w-full auto-rows-min gap-4 sm:grid-cols-3 md:grid-cols-3">
					{#each filteredEvents as event}
						<EventCard {event} />
					{/each}
					{#if filteredEvents.length === 0 && searchQuery.trim()}
						<div class="col-span-full py-8 text-center">
							<p class="text-muted-foreground">No events found matching "{searchQuery}"</p>
						</div>
					{/if}
				</div>
			</div>
		</div>
	</ScrollArea>
</div>
