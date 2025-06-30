<script lang="ts">
	import { getContext } from 'svelte';
	import type { Snippet } from 'svelte';

	interface Props {
		placeholder?: string;
		children?: Snippet;
	}

	let { placeholder = 'Select an option...', children }: Props = $props();

	// 从 Select.Root 上下文获取当前选中的值
	const selectContext = getContext<{
		value: string | string[] | undefined;
		items?: Array<{ value: string; label: string; disabled?: boolean }>;
	}>('select');

	// 计算显示的标签
	const displayValue = $derived(() => {
		if (!selectContext?.value) return placeholder;
		
		// 如果是数组（多选）
		if (Array.isArray(selectContext.value)) {
			if (selectContext.value.length === 0) return placeholder;
			if (selectContext.value.length === 1) {
				// 尝试从 items 中找到对应的 label
				const item = selectContext.items?.find(item => item.value === selectContext.value?.[0]);
				return item?.label || selectContext.value[0];
			}
			return `${selectContext.value.length} items selected`;
		}
		
		// 单选情况
		const item = selectContext.items?.find(item => item.value === selectContext.value);
		return item?.label || selectContext.value;
	});
</script>

{#if children}
	{@render children()}
{:else}
	<span class="select-value">
		{displayValue}
	</span>
{/if}

<style>
	.select-value {
		pointer-events: none;
		user-select: none;
	}
</style>