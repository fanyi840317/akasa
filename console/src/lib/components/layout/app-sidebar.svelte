<script lang="ts">
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import NavActions from './nav-actions.svelte';
	import type { ComponentProps } from 'svelte';
	import NavFiles from './nav-files.svelte';
	import { PlusIcon } from '@lucide/svelte';

	let {
		actions,
		files,
		chats,
		isOpen = $bindable(true),
		onCreateEvent,
		onFileClick,
		onEventView,
		onEventDelete,
		...restProps
	}: ComponentProps<typeof Sidebar.Root> & {
		actions?: any;
		isOpen?: boolean;
		chats?:string[];
		files?: any;
		onCreateEvent?: () => void;
		onFileClick?: (fileName: string) => void;
		onEventView?: (eventId: string) => void;
		onEventDelete?: (eventId: string) => void;
	} = $props();

	const handleCreateEvent = () => {
		onCreateEvent?.();
	};
</script>

<Sidebar.Root variant="inset" collapsible="icon">
	<!-- <Sidebar.Header class="py-1">
		{#if isOpen}
			<h1 class="text-xl font-extrabold px-4">Aksas</h1>
		{:else}
			<span class="flex-center p-1 szie-8 rounded-full bg-accent transition-all duration-500">
				<h1 class="text-md font-extrabold">A</h1>
			</span>
		{/if}
	</Sidebar.Header> -->
	<Sidebar.Content class="py-6">
		<Sidebar.Group class="px-1">
			<NavActions items={actions} />
		</Sidebar.Group>
		<Sidebar.Group class="px-2">
			<div class="flex items-center justify-between py-1">
				<Sidebar.GroupLabel>My Files</Sidebar.GroupLabel>
				<button 
					class="p-1 rounded-md hover:bg-accent transition-colors" 
					onclick={handleCreateEvent}
					title="创建事件"
				>
					<PlusIcon class="w-4 h-4" />
				</button>
			</div>
			<!-- <NavFiles {files} {onFileClick} {onEventView} {onEventDelete} /> -->
		</Sidebar.Group>
	</Sidebar.Content>
	<Sidebar.Footer />
</Sidebar.Root>
