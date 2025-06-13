<script lang="ts">
	import { Calendar } from '$lib/components/ui/calendar';
	import * as Popover from '$lib/components/ui/popover';
	import type { DateValue } from '@internationalized/date';
	import { DateFormatter, getLocalTimeZone, parseDate } from '@internationalized/date';
	import { Loader2Icon } from '@lucide/svelte';

	import type { Snippet } from 'svelte';
	import Textarea from '../ui/textarea/textarea.svelte';
	import * as Card from '$lib/components/ui/card';
	import Button from '../ui/button/button.svelte';
	import Mask from './mask.svelte';

	let {
		children,
		value,
		showPicker = $bindable(false),
		isSaving = $bindable(false),
		onDateChange,
		onSave
	} = $props<{
		children?: Snippet;
		value?: DateValue | string;
		showPicker?: boolean;
		isSaving?: boolean;
		onDateChange?: (e: { date: DateValue }) => void;
		onSave?: (date: DateValue) => void;
	}>();

	// 日期格式化
	const df = new DateFormatter('zh-CN', {
		dateStyle: 'long'
	});

	// 日期字符串格式化
	const dateStrFormatter = new DateFormatter('zh-CN', {
		year: 'numeric',
		month: '2-digit',
		day: '2-digit'
	});

	// 编辑状态
	let tempValue = $state<DateValue | undefined>(typeof value === 'string' ? undefined : value);
	let inputValue = $state('');
	let showError = $state(false);

	// 当 value 变化时，更新临时值和输入框的值
	$effect(() => {
		if (value) {
			if (typeof value === 'string') {
				// 如果是字符串，尝试解析为DateValue
				try {
					const parsedDate = parseDate(value.split('T')[0]);
					tempValue = parsedDate;
					inputValue = dateStrFormatter.format(parsedDate.toDate(getLocalTimeZone()));
				} catch (e) {
					// 如果解析失败，直接使用字符串作为输入值
					inputValue = value;
					tempValue = undefined;
				}
			} else {
				// 如果是DateValue，直接使用
				tempValue = value;
				inputValue = dateStrFormatter.format(value.toDate(getLocalTimeZone()));
			}
		}
	});

	// 当日期通过日历选择时
	function handleCalendarSelect(newValue: DateValue | undefined) {
		if (newValue) {
			tempValue = newValue;
			inputValue = dateStrFormatter.format(newValue.toDate(getLocalTimeZone()));
			showError = false;
			// 直接保存
			saveDateAndDescription();
		}
	}

	// 保存日期
	function saveDateAndDescription() {
		console.log('saveDateAndDescription', tempValue);

		value = inputValue;
		if (onSave) {
			// 确保传递正确的格式给onSave回调
			if (tempValue) {
				// 如果原始value是字符串，返回本地日期字符串（避免时区转换）
				if (typeof value === 'string') {
					const localDate = tempValue.toDate(getLocalTimeZone());
					// 使用本地日期格式，避免UTC转换导致的日期偏移
					const year = localDate.getFullYear();
					const month = String(localDate.getMonth() + 1).padStart(2, '0');
					const day = String(localDate.getDate()).padStart(2, '0');
					onSave(`${year}-${month}-${day}`);
				} else {
					// 否则返回DateValue对象
					onSave(tempValue);
				}
			} else {
				// 如果没有tempValue，使用inputValue
				onSave(inputValue);
			}
		}
	}

	// 取消编辑
	function cancelEdit() {
		showPicker = false;
		// 重置临时值
		if (value) {
			if (typeof value === 'string') {
				try {
					const parsedDate = parseDate(value.split('T')[0]);
					tempValue = parsedDate;
					inputValue = dateStrFormatter.format(parsedDate.toDate(getLocalTimeZone()));
				} catch (e) {
					inputValue = value;
					tempValue = undefined;
				}
			} else {
				tempValue = value;
				inputValue = dateStrFormatter.format(value.toDate(getLocalTimeZone()));
			}
		} else {
			tempValue = undefined;
			inputValue = '';
		}
		showError = false;
	}

	// 当输入框值改变时
</script>

<Popover.Root bind:open={showPicker}>
	<Mask bind:show={showPicker} onCancel={cancelEdit} />

	<Popover.Trigger class={showPicker ? 'relative z-50' : ''}>
		{@render children?.()}
	</Popover.Trigger>
	<Popover.Content class="w-auto px-2 flex-center flex-row gap-2 z-50" align="start">
		<Card.Root class="border-0 mb-10 p-0 w-[320px]">
			<Card.Header>
				<Card.Title>Event Time</Card.Title>
				<Card.Description>设置活动的时间</Card.Description>
				<Card.Action><Button variant="ghost"></Button></Card.Action>
			</Card.Header>
			<Card.Content class="space-y-4">
				<div class="grid gap-1">
					<label for="time-description" class="text-xs text-foreground/50 ml-2">手动输入</label>
					<Textarea
						id="time-description"
						disabled={isSaving}
						bind:value={inputValue}
						placeholder="如果你不清楚具体时间你可以输入 like:'公元300年前','1980年前后'"
						class="h-[100px] w-full placeholder:text-xs"
					/>
				</div>
				{#if showError}
					<p class="text-sm text-red-500">日期格式不正确，请重新输入</p>
				{/if}
			</Card.Content>
			<Card.Footer class="flex-row flex-end gap-2">
				<Button variant="ghost" disabled={isSaving} onclick={cancelEdit} class="text-foreground/50"
					>cancel</Button
				>
				<Button variant="outline" disabled={isSaving} onclick={saveDateAndDescription}>
					{#if isSaving}
						<Loader2Icon class="animate-spin" />
					{/if}
					Save
				</Button>
			</Card.Footer>
		</Card.Root>

		<span class="text-foreground/50 text-xs">or</span>
		<Calendar
			type="single"
			bind:value={tempValue}
			onValueChange={handleCalendarSelect}
			captionLayout="dropdown"
			disabled={isSaving}
		/>
	</Popover.Content>
</Popover.Root>
