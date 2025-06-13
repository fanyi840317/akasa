<script lang="ts">
	import * as Popover from '$lib/components/ui/popover';
	import * as Card from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import Textarea from '$lib/components/ui/textarea/textarea.svelte';
	import type { Snippet } from 'svelte';
	import { Loader2Icon } from '@lucide/svelte';

	let {
		children,
		eventName = $bindable('New Event'),
		eventSummary = $bindable(''),
		showEditor = $bindable(false),
		isSaving = $bindable(false),
		onSave
	} = $props<{
		children?: Snippet;
		eventName?: string;
		eventSummary?: string;
		showEditor?: boolean;
		isSaving?: boolean;
		onSave?: (name: string, summary: string) => void;
	}>();

	// 编辑状态
	let tempName = $state(eventName);
	let tempSummary = $state(eventSummary);

	// 保存名称和摘要
	function saveNameAndSummary() {
		eventName = tempName;
		eventSummary = tempSummary;
		if (onSave) {
			onSave(eventName, eventSummary);
		}
	}

	// 取消编辑
	function cancelEdit() {
		showEditor = false;
	}
</script>

<Popover.Root bind:open={showEditor}>
	<!-- 背景蒙层 -->
	{#if showEditor}
		<!-- svelte-ignore a11y_click_events_have_key_events -->
		<!-- svelte-ignore a11y_no_static_element_interactions -->
		<div class="fixed inset-0 bg-black/50 z-40" onclick={cancelEdit}></div>
	{/if}

	<Popover.Trigger class={showEditor ? 'relative z-50' : ''}>
		{@render children?.()}
	</Popover.Trigger>
	<Popover.Content class="w-auto p-0 z-50" align="start">
		<Card.Root class="border-0 w-[400px]">
			<Card.Header>
				<Card.Title>Event Information</Card.Title>
				<Card.Description>修改活动的名称和摘要</Card.Description>
				<Card.Action><Button variant="ghost"></Button></Card.Action>
			</Card.Header>
			<Card.Content class="space-y-4">
				<div class="space-y-2">
					<!-- <label for="event-name" class="">活动名称</label> -->
					<Input disabled={isSaving} id="event-name" bind:value={tempName} placeholder="输入活动名称" class="w-full" />
				</div>
				<div class="grid gap-2">
					<label for="event-summary" class="text-sm">Event Summary</label>
					<Textarea
						id="event-summary"
						disabled={isSaving}
						bind:value={tempSummary}
						placeholder="输入活动摘要或描述"
						class="h-[100px] w-full  placeholder:text-xs"
					/>
				</div>
			</Card.Content>
			<Card.Footer class="flex-row flex-end gap-2">
				<Button variant="ghost" disabled={isSaving} onclick={cancelEdit} class="text-foreground/50">cancel</Button>
				<Button variant="outline" disabled={isSaving} onclick={saveNameAndSummary}>
					{#if isSaving}
						<Loader2Icon class="animate-spin" />
					{/if}

					Save</Button
				>
			</Card.Footer>
		</Card.Root>
	</Popover.Content>
</Popover.Root>
