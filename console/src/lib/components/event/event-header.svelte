<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Separator } from '$lib/components/ui/separator';
	import { ArrowLeft, MoreHorizontal } from '@lucide/svelte';
	import { Badge } from '$lib/components/ui/badge';
	import UserAvatar from '$lib/components/user';
	import TimePicker from './time-picker.svelte';
	import MapPicker from './map-picker.svelte';
	import CoverPicker from './cover-picker.svelte';
	import MoreMenu from './more-menu.svelte';
	import NameEditor from './name-editor.svelte';
	import type { Event } from '$lib/types/event';
	import type { Snippet } from 'svelte';
	import { parseDate, getLocalTimeZone } from '@internationalized/date';

	let {
		eventData,
		isSaving = false,
		showEditor = $bindable(false),
		showTimePicker = $bindable(false),
		showMapPicker = $bindable(false),
		onBack,
		onNameSave,
		onTimeSave,
		onSave,
		onMapSave,
		onCoverSelect,
		onCoverLinkSubmit,
		onCoverFileUpload,
		onSettings
	} = $props<{
		eventData: Event;
		isSaving?: boolean;
		showEditor?: boolean;
		showTimePicker?: boolean;
		showMapPicker?: boolean;
		onBack?: () => void;
		onNameSave?: (name: string, summary: string) => void;
		onTimeSave?: (date: string | Date) => void;
		onSave?: () => void;
		onMapSave?: (location: string) => void;
		onCoverSelect?: (url: string) => void;
		onCoverLinkSubmit?: (url: string) => void;
		onCoverFileUpload?: (file: File) => void;
		onSettings?: () => void;
	}>();
</script>

<header class="px-4 h-14 flex-between">
	<div class="flex-center gap-2">
		<Button
			variant="ghost"
			onclick={() => {
				onBack?.();
			}}
		>
			<ArrowLeft class="size-4" />
			<div class="text-left">
				Back
				<p class="text-foreground/50 text-[10px]">to Events</p>
			</div>
		</Button>

		<Separator orientation="vertical" class="mx-2 !h-4" />
		<NameEditor
			eventName={eventData.name || 'New Event'}
			eventSummary={eventData.summary || ''}
			onSave={onNameSave}
			{isSaving}
			bind:showEditor
		>
			<Button variant="link">
				{eventData.name || 'New Event'}
			</Button>
		</NameEditor>
		<Separator orientation="vertical" class="mx-2 !h-4" />
		<TimePicker
			value={eventData.date}
			bind:showPicker={showTimePicker}
			bind:isSaving
			onSave={onTimeSave}
		>
			{@render propBtn('时间')}
		</TimePicker>
		<MapPicker
			value={eventData.location}
			onSave={onMapSave}
			bind:isSaving
			bind:isOpen={showMapPicker}
		>{@render propBtn('地点')}</MapPicker>
		<CoverPicker
			onSelect={onCoverSelect}
			onLinkSubmit={onCoverLinkSubmit}
			onFileUpload={onCoverFileUpload}
			userId="user-123">{@render propBtn('封面')}</CoverPicker
		>

		<MoreMenu onSettings={onSettings}>
			<Button variant="secondary">
				<MoreHorizontal class="size-4" />
			</Button>
		</MoreMenu>
	</div>

	<div class="flex-center gap-2">
		<!-- 保存状态指示器 -->
		{#if isSaving}
			<div class="flex-center gap-2 text-sm text-muted-foreground">
				<div class="animate-spin rounded-full h-4 w-4 border-b-2 border-primary"></div>
				保存中...
			</div>
		{:else}
			<Button variant="outline" onclick={onSave} disabled={isSaving}>保存 (Ctrl+S)</Button>
		{/if}

		<Button variant="secondary" class="px-2 pr-3 rounded-full">
			<div
				class="*:data-[slot=avatar]:ring-background/20 *:data-[slot=avatar]:ring-2 flex -space-x-2 *:data-[slot=avatar]:grayscale"
			>
				<UserAvatar class="size-6" user={{ name: 'Akasa' }}></UserAvatar>
				<UserAvatar class="size-6" user={{ name: '?' }}></UserAvatar>
				<UserAvatar class="size-6" user={{ name: '?' }}></UserAvatar>
			</div>
			<div class="text-left text-xs">
				<p class="text-foreground/50 text-[8px]">评论</p>
				0条
			</div>
		</Button>
	</div>
</header>

{#snippet propBtn(label: string)}
	<Button variant="outline" class="text-foreground/50 text-xs border-0">
		<Badge class="size-4 rounded-full bg-accent text-foreground/50">?</Badge>
		<div class="text-center text-xs">{label}</div>
	</Button>
{/snippet}