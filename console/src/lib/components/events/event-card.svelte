<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import { goto } from '$app/navigation';
	import type { Event } from '$lib/types/event';
	import UserAvatar from '../user/user-avatar.svelte';
	import { formatDate } from '$lib/utils.js';

	let { event }: { event: Event } = $props();

	function handleClick() {
		goto(`/console/events/${event.$id}`);
	}

	function getStatusColor(status?: string) {
		switch (status) {
			case 'published':
				return 'bg-green-100 text-green-800';
			case 'draft':
				return 'bg-yellow-100 text-yellow-800';
			case 'archived':
				return 'bg-gray-100 text-gray-800';
			default:
				return 'bg-gray-100 text-gray-800';
		}
	}
</script>

<Card.Root class="h-72 cursor-pointer transition-shadow hover:shadow-lg" onclick={handleClick}>
	<Card.Header>
		<div class="flex items-start justify-between">
			<div class="flex-1">
				<Card.Title class="line-clamp-1">{event.name}</Card.Title>
				<Card.Description class="mt-2 line-clamp-3">{event.summary || '暂无描述'}</Card.Description>
			</div>
			<!-- {#if event.status}
				<span class="px-2 py-1 text-xs rounded-full {getStatusColor(event.status)}">
					{event.status}
				</span>
			{/if} -->
		</div>
	</Card.Header>

	<Card.Content class="h-full flex-1">
		<!-- {#if event.cover}
			<div class="w-full h-32 bg-gray-100 rounded-md overflow-hidden">
				<img src={event.cover} alt={event.name} class="w-full h-full object-cover" />
			</div>
		{:else}
			<div class="w-full h-32 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-md flex items-center justify-center">
				<span class="text-gray-400 text-sm">无预览图</span>
			</div>
		{/if}
		{#if event.tags && event.tags.length > 0}
			<div class="mt-2 flex flex-wrap gap-1">
				{#each event.tags.slice(0, 3) as tag}
					<span class="px-2 py-1 text-xs bg-blue-50 text-blue-700 rounded">{tag}</span>
				{/each}
			</div>
		{/if} -->
	</Card.Content>

	<Card.Footer class="flex items-center justify-between">
		<span class="text-foreground/50 text-sm"
			>{formatDate(event.createdAt, { includeYear: true })}</span
		>
		<!-- <UserAvatar class="size-6" user={{ name: event.creator_name || '?', avatar: event.creator_avatar || '' }} /> -->
	</Card.Footer>
</Card.Root>
