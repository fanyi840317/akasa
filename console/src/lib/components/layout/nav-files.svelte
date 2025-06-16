<script lang="ts">
	import {
		ChevronRightIcon,
		FolderIcon,
		FileIcon,
		MoreHorizontalIcon,
		EyeIcon,
		TrashIcon,
		EllipsisIcon
	} from '@lucide/svelte';
	import * as Collapsible from '$lib/components/ui/collapsible/index.js';
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu/index.js';
	import type { Component, ComponentProps } from 'svelte';
	import Button from '../ui/button/button.svelte';

	let {
		files,
		onFileClick,
		onEventView,
		onEventDelete
	}: {
		files: [];
		onFileClick?: (fileName: string) => void;
		onEventView?: (eventId: string) => void;
		onEventDelete?: (eventId: string) => void;
	} = $props();

	const handleFileClick = (fileName: string) => {
		onFileClick?.(fileName);
	};

	const handleEventView = (eventId: string) => {
		onEventView?.(eventId);
	};

	const handleEventDelete = (eventId: string) => {
		onEventDelete?.(eventId);
	};
</script>

<Sidebar.Menu>
	{#each files as item, index (index)}
		{@render Tree({ item })}
	{/each}
</Sidebar.Menu>

{#snippet Tree({ item }: { item: string | any[] | { name: string; id: string; type: string } })}
	{@const isObject = typeof item === 'object' && !Array.isArray(item)}
	{@const [name, ...items] = isObject ? [item.name] : Array.isArray(item) ? item : [item]}
	{@const isEvent = isObject && item.type === 'event'}
	{#if !items.length}
		<Sidebar.MenuItem>
			<Sidebar.MenuButton onclick={() => handleFileClick(name)} class="text-xs truncate line-clamp-1 ">
				{name}
				{#if isEvent}
					<DropdownMenu.Root>
						<DropdownMenu.Trigger>
							{#snippet child({ props })}
								<Sidebar.MenuAction showOnHover {...props}>
									<EllipsisIcon />
									<span class="sr-only">More</span>
								</Sidebar.MenuAction>
							{/snippet}
							<!-- <Button
								class="opacity-0 group-hover:opacity-100 p-1 hover:bg-accent rounded transition-opacity"
								onclick={(e) => {
									e.stopPropagation();
								}}
							>
								<MoreHorizontalIcon class="h-4 w-4" /> -->

							<!-- </Button> -->
						</DropdownMenu.Trigger>
						<DropdownMenu.Content class="w-48 rounded-[16px]" align="start">
							<DropdownMenu.Item
								onclick={() => handleEventView(item.id)}
								class="flex items-center gap-2"
							>
								<EyeIcon class="h-4 w-4" />
								查看事件
							</DropdownMenu.Item>
							<DropdownMenu.Item
								onclick={() => handleEventDelete(item.id)}
								class="flex items-center gap-2 text-destructive"
							>
								<TrashIcon class="h-4 w-4" />
								删除事件
							</DropdownMenu.Item>
						</DropdownMenu.Content>
					</DropdownMenu.Root>
				{/if}
			</Sidebar.MenuButton>
		</Sidebar.MenuItem>
	{:else}
		<Sidebar.MenuItem>
			<Collapsible.Root
				class="group/collapsible [&[data-state=open]>button>svg:first-child]:rotate-90"
				open={name === 'lib' || name === 'components'}
			>
				<Collapsible.Trigger>
					{#snippet child({ props })}
						<Sidebar.MenuButton {...props}>
							<ChevronRightIcon className="transition-transform" />
							<FolderIcon />
							{name}
						</Sidebar.MenuButton>
					{/snippet}
				</Collapsible.Trigger>
				<Collapsible.Content>
					<Sidebar.MenuSub>
						{#each items as subItem, index (index)}
							{@render Tree({ item: subItem })}
						{/each}
					</Sidebar.MenuSub>
				</Collapsible.Content>
			</Collapsible.Root>
		</Sidebar.MenuItem>
	{/if}
{/snippet}
