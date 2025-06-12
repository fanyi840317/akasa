<script lang="ts">
	import { Calendar } from '$lib/components/ui/calendar';
	import * as Popover from '$lib/components/ui/popover';
	import type { DateValue } from '@internationalized/date';
	import { DateFormatter, getLocalTimeZone, parseDate } from '@internationalized/date';

	import type { Snippet } from 'svelte';
	import Textarea from '../ui/textarea/textarea.svelte';
	import * as Card from '$lib/components/ui/card';
	import Button from '../ui/button/button.svelte';
	
	let { value, onDateChange, children } = $props<{
		value?: string;
		onDateChange?: (e: { date: DateValue }) => void;
		children?: Snippet;
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

	let inputValue = '';

	// 当 value 变化时，更新输入框的值
	$effect(() => {
		if (value) {
			inputValue = dateStrFormatter.format(value.toDate(getLocalTimeZone()));
		}
	});

	let showError = false;

	// 当日期通过日历选择时
	function handleCalendarSelect(newValue: DateValue | undefined) {
		if (newValue) {
			value = newValue;
			inputValue = dateStrFormatter.format(newValue.toDate(getLocalTimeZone()));
			showError = false;
			if (onDateChange) {
				onDateChange({ date: newValue });
			}
			// dispatch('dateChange', { date: newValue });
		}
	}

	// 当输入框值改变时
	function handleInputChange() {
		try {
			// 尝试解析输入的日期字符串
			const parts = inputValue.split(/[-/.]/);
			if (parts.length === 3) {
				const [year, month, day] = parts.map((p) => parseInt(p));
				if (!isNaN(year) && !isNaN(month) && !isNaN(day)) {
					const date = parseDate(
						`${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`
					);
					value = date;
					showError = false;
					if (onDateChange) onDateChange({ date });
					return;
				}
			}
			showError = true;
		} catch (e) {
			showError = true;
		}
	}
</script>

<Popover.Root>
	<Popover.Trigger>
		{@render children()}
	</Popover.Trigger>
	<Popover.Content class="w-auto px-2 flex-center flex-row gap-2" align="start">
		
		<Card.Root class="border-0 mb-12 p-0">
			<Card.Header>
				<Card.Title>Event time</Card.Title>
				<Card.Description>Event happens on this time</Card.Description>
				<Card.Action>
					<Button variant="ghost"></Button>
				</Card.Action>
			</Card.Header>
			<Card.Content class="">
				<Textarea
					id="name-2"
					placeholder="如果你不清楚具体时间你可以输入 like:'公元300年前','1980年前后'"
					bind:value={inputValue}
					class="h-[100px] w-[260px] rounded-2xl placeholder:text-xs"
				/>
			</Card.Content>
			<Card.Footer class="gap-2 flex-end">
				<Button variant="ghost">cancel</Button>
				<Button variant="secondary">Save</Button>
			</Card.Footer>
		</Card.Root>

		<span class="text-foreground/50 text-xs">or</span>
		<Calendar type="single" bind:value 
		onValueChange={handleCalendarSelect} captionLayout="dropdown"
		/>
	</Popover.Content>
</Popover.Root>
