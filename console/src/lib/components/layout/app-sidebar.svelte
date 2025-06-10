<script lang="ts">
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import NavActions from './nav-actions.svelte';
	import type { ComponentProps } from 'svelte';
	import NavFiles from './nav-files.svelte';

	let {
		actions,
		files,
		isOpen = $bindable(true),
		...restProps
	}: ComponentProps<typeof Sidebar.Root> & {
		actions?: any;
		isOpen?: boolean;
		files?: any;
	} = $props();
</script>

<Sidebar.Root variant="inset" collapsible="icon">
	<Sidebar.Header>
		{#if isOpen}
			<h1 class="text-xl font-extrabold px-4">Aksas</h1>
		{:else}
			<span class="flex-center p-1 szie-8 rounded-full bg-accent transition-all duration-500">
				<h1 class="text-md font-extrabold">A</h1>
			</span>
		{/if}
	</Sidebar.Header>
	<Sidebar.Content class="py-6 px-2">
		<Sidebar.Group>
			<NavActions items={actions} />
		</Sidebar.Group>
		<Sidebar.Group>
			<Sidebar.GroupLabel>Files</Sidebar.GroupLabel>
			<NavFiles {files} />
		</Sidebar.Group>
	</Sidebar.Content>
	<Sidebar.Footer />
</Sidebar.Root>
