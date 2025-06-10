<script lang="ts">
	import { goto } from '$app/navigation';
	import AiInput from '$lib/components/ai/ai-input.svelte';
	import BlocksuiteWrapper from '$lib/components/editor/blocksuite-wrapper.svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Resizable from '$lib/components/ui/resizable/index.js';
	import { Separator } from '$lib/components/ui/separator';
	import { ChevronRightIcon, FileIcon, ArrowLeft, MoreHorizontal } from '@lucide/svelte';
	import * as Tabs from '$lib/components/ui/tabs';
	import { Badge } from '$lib/components/ui/badge';
	import UserAvatar from '$lib/components/user';
	import Pro from "./pro.svelte";
	// import BlocksuiteEditor from '$lib/components/editor/blocksuite-editor.svelte';
	// let number = 0;
	let actionTab = $state('info');
</script>

<Resizable.PaneGroup direction="horizontal" class="w-full ">
	<Resizable.Pane defaultSize={30} class="h-[calc(100vh)] p-2 pr-0 flex flex-col">
		<header class="h-14 w-full flex-between flex-row">
			<div class="flex-center">
				<Button
					variant="ghost"
					onclick={() => {
						goto('/console/events');
					}}
				>
					<ArrowLeft class="size-4" />
					<div class="text-left">
						Back
						<p class="text-foreground/50 text-[10px]">to Events</p>
					</div>
				</Button>

				<Separator orientation="vertical" class="mx-2 !h-4" />
				<Button variant="link">New Event</Button>
			</div>
			<Button variant="ghost">
				<MoreHorizontal class="size-4" />
			</Button>
		</header>
		<div class="flex-end flex-col h-full border rounded-2xl p-4">
			<AiInput class="w-full" />
		</div>
	</Resizable.Pane>
	<!-- <Resizable.Handle class="" /> -->
	<Resizable.Handle class="bg-transparent" />
	<Resizable.Pane defaultSize={70} class="flex flex-col p-2">
		<header class="h-14 flex-between">
			<Tabs.Root bind:value={actionTab}>
				<Tabs.List class="bg-transparent">
					<Tabs.Trigger value="info">
						{@render numberBadge(1)}
						events</Tabs.Trigger
					>
					<Tabs.Trigger value="properties">
						{@render numberBadge(2)}
						属性</Tabs.Trigger
					>
					<Tabs.Trigger value="password1">
						{@render numberBadge(3)}
						位置</Tabs.Trigger
					>
				</Tabs.List>
			</Tabs.Root>
			<Button variant="outline" class="px-2">
				<div
					class="*:data-[slot=avatar]:ring-background flex -space-x-2 *:data-[slot=avatar]:grayscale"
				>
					<UserAvatar class="size-6" user={{ name: 'Akasa' }}></UserAvatar>
					<UserAvatar class="size-6" user={{ name: '?' }}></UserAvatar>
					<UserAvatar class="size-6" user={{ name: '?' }}></UserAvatar>
				</div>
				0 评论
			</Button>
		</header>
		{#if actionTab === 'info'}
			<BlocksuiteWrapper class="rounded-2xl border h-full" />
		{:else if actionTab === 'properties'}
			<div class="rounded-2xl border h-full bg-muted">
				<Pro />
			</div>
		{:else if actionTab === 'password1'}
			<div class="rounded-2xl border h-full"></div>
		{/if}
	</Resizable.Pane>
</Resizable.PaneGroup>

{#snippet numberBadge(number: number = 0)}
	<Badge class="size-4 rounded-full font-mono tabular-nums text-foreground/50" variant="secondary"
		>{number}</Badge
	>
{/snippet}
