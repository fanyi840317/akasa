<script lang="ts">
	import { goto } from '$app/navigation';
	import AiInput from '$lib/components/ai/ai-input.svelte';
	// import BlocksuiteWrapper from '$lib/components/editor/blocksuite-wrapper.svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Resizable from '$lib/components/ui/resizable/index.js';
	import { Separator } from '$lib/components/ui/separator';
	import {
		ChevronRightIcon,
		ChevronsUpDown,
		FileIcon,
		ArrowLeft,
		MoreHorizontal
	} from '@lucide/svelte';
	import * as Tabs from '$lib/components/ui/tabs';
	import { Badge } from '$lib/components/ui/badge';
	import UserAvatar from '$lib/components/user';
	import { BlocksuiteEditor } from '$lib/components/editor/index.js';
	import TimePicker from '$lib/components/event/time-picker.svelte';
	import MapPicker from '$lib/components/event/map-picker.svelte';
	// let number = 0;
	let actionTab = $state('info');
</script>

<div class="w-full h-full flex flex-col">
	
	<Resizable.PaneGroup direction="horizontal" class="w-full flex-1 ">
		<Resizable.Pane defaultSize={25} class="p-2 pr-0 flex flex-col h-[calc(100vh)]">
			<header class="h-14 w-full flex-between flex-row">
				<div class="flex-center gap-2">
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
			</header>
			<div class="flex-end flex-col h-full  rounded-2xl p-0">
				<AiInput class="w-full rounded-xl h-[180px]" />
			</div>
		</Resizable.Pane>
		<!-- <Resizable.Handle class="" /> -->
		<Resizable.Handle class="bg-transparent" />
		<Resizable.Pane defaultSize={75} class="flex flex-col p-2">
			<header class="h-14 flex-between flex-row">
				<div class="flex-center gap-2">
					<TimePicker>
						{@render propBtn('时间')}
					</TimePicker>
					<MapPicker>{@render propBtn('地点')}</MapPicker>

					{@render propBtn('封面')}

					<Button variant="secondary">
						<MoreHorizontal class="size-4" />
					</Button>
				</div>
				<div class="flex-center gap-2">
					<Button variant="secondary" class="px-2 pr-3 border rounded-full">
						<div
							class="*:data-[slot=avatar]:ring-background flex -space-x-2 *:data-[slot=avatar]:grayscale"
						>
							<UserAvatar class="size-6" user={{ name: 'Akasa' }}></UserAvatar>
							<UserAvatar class="size-6" user={{ name: '?' }}></UserAvatar>
							<UserAvatar class="size-6" user={{ name: '?' }}></UserAvatar>
						</div>
						<div class="text-center text-xs">
							0
							<p class="text-foreground/50 text-[10px]">条评论</p>
						</div>
					</Button>
				</div>
			</header>
			<div class="flex-1 overflow-y-auto rounded-2xl border">
				{#if actionTab === 'info'}
					<BlocksuiteEditor />
				{:else if actionTab === 'properties'}{:else if actionTab === 'password1'}
					<div></div>
				{/if}
			</div>
		</Resizable.Pane>
	</Resizable.PaneGroup>
</div>

{#snippet propBtn(label: string)}
	<Button variant="outline" class="text-foreground/50 text-xs border-0">
		<Badge class="size-4 rounded-full bg-accent text-foreground/50">?</Badge>
		<div class="text-center text-xs">{label}</div>
		<!-- <ChevronsUpDown class="size-4"></ChevronsUpDown> -->
	</Button>
{/snippet}
