<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Separator } from '$lib/components/ui/separator';
	import { ArrowLeft, MoreHorizontal, Clock, MapPin, Image, Loader2Icon } from '@lucide/svelte';
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

	// 格式化日期显示
	function formatDate(date: string | Date): string {
		if (!date) return '';
		if (typeof date === 'string') {
			return date;
		}
		try {
			return date.toLocaleDateString('zh-CN', {
				month: 'short',
				day: 'numeric',
				hour: '2-digit',
				minute: '2-digit'
			});
		} catch {
			return 'Invalid Date';
		}
	}

	let {
		class: className,
		eventData,
		isSaving = false,
		showEditor = $bindable(false),
		showTimePicker = $bindable(false),
		showMapPicker = $bindable(false),
		showCoverPicker = $bindable(false),
		onBack,
		onNameSave,
		onTimeSave,
		onSave,
		onMapSave,
		onCoverSelect,
		onCoverLinkSubmit,
		onSettings
	} = $props<{
		class ?: string;
		eventData: Event;
		isSaving?: boolean;
		showEditor?: boolean;
		showTimePicker?: boolean;
		showMapPicker?: boolean;
		showCoverPicker?: boolean;
		onBack?: () => void;
		onNameSave?: (name: string, summary: string) => void;
		onTimeSave?: (date: string | Date) => void;
		onSave?: () => void;
		onMapSave?: (location: string) => void;
		onCoverSelect?: (url: string) => void;
		onCoverLinkSubmit?: (url: string) => void;
		onSettings?: () => void;
	}>();
</script>

<header class="w-full px-4 h-[56px] flex-between {className}">
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
			<Button variant="link" class=" max-w-64 truncate">
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
			{#if eventData.date}
				{@render propBtn(Clock,'时间', formatDate(eventData.date))}
			{:else}
				{@render iconBtn( '时间')}
			{/if}
		</TimePicker>
		<MapPicker
			value={eventData.location_data}
			onSave={onMapSave}
			bind:isSaving
			bind:isOpen={showMapPicker}
		>
			{#if eventData.location_data}
				{@render propBtn(MapPin, 
					'地点',
					JSON.parse(eventData.location_data).name || JSON.parse(eventData.location_data).address || '未知地点'
				)}
			{:else}
				{@render iconBtn('地点')}
			{/if}
		</MapPicker>
		<CoverPicker
			onSelect={onCoverSelect}
			onLinkSubmit={onCoverLinkSubmit}
			userId="user-123"
			bind:isOpen={showCoverPicker}
		>
			{#if eventData.cover}
				{@render propBtn(Image, '封面', '已设置')}
			{:else}
				{@render iconBtn('封面')}
			{/if}
		</CoverPicker>

		<MoreMenu {onSettings}>
			<Button variant="ghost">
				<MoreHorizontal class="size-4" />
			</Button>
		</MoreMenu>
	</div>

	<div class="flex-center gap-2">
		<!-- 保存状态指示器 -->
		<Button variant="outline" onclick={onSave} disabled={isSaving}>
			{#if isSaving}
				<Loader2Icon class="animate-spin"></Loader2Icon>
			{/if}
			保存 (Ctrl+S)</Button
		>

		<Button variant="ghost" class="px-2 pr-3 rounded-full">
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

{#snippet propBtn(IconComponent: any, label: string, value: string)}
	<Button variant="ghost" class="text-foreground/50 text-xs border-0 max-w-32">
		<IconComponent class="size-4 text-foreground/50" />
		<div class="text-left text-xs min-w-0 flex-1">
			<!-- <div class="text-foreground/70 font-medium">{label}</div> -->
			
			<div class="text-foreground/50 truncate" title={value}>{value}</div>
		</div>
	</Button>
{/snippet}

{#snippet iconBtn(label: string)}
	<Button variant="outline" class="text-foreground/50 text-xs border-0">
		<!--  -->
		
		<Badge class="size-4 rounded-full bg-accent text-foreground/50">?</Badge>
		<div class="text-center text-xs">{label}</div>
	</Button>
{/snippet}
