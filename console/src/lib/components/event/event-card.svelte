<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import { goto } from '$app/navigation';
	import type { Event } from '$lib/types/event';
	import UserAvatar from '../user/user-avatar.svelte';

	let { event }: { event: Event } = $props();

	function handleClick() {
		goto(`/console/events/${event.$id}`);
	}

	function formatDate(date?: Date | string) {
		if (!date) return '';
		const dateObj = date instanceof Date ? date : new Date(date);
		return dateObj.toLocaleDateString('zh-CN', {
			year: 'numeric',
			month: 'short',
			day: 'numeric'
		});
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

<Card.Root class="h-72 cursor-pointer hover:shadow-lg transition-shadow" onclick={handleClick}>
	<Card.Header>
		<div class="flex justify-between items-start">
			<div class="flex-1">
				<Card.Title class="line-clamp-1">{event.name}</Card.Title>
				<Card.Description class="line-clamp-3 mt-2">{event.summary || '暂无描述'}</Card.Description>
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

	<Card.Footer class="flex justify-between items-center">
		<span class="text-sm text-foreground/50">{formatDate(event.createdAt)}</span>
		<!-- <UserAvatar class="size-6" user={{ name: event.creator_name || '?', avatar: event.creator_avatar || '' }} /> -->
	</Card.Footer>
</Card.Root>