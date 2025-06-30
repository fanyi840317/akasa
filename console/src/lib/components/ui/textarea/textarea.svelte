<script lang="ts">
	import { tv, type VariantProps } from 'tailwind-variants';
	import type { HTMLTextareaAttributes } from 'svelte/elements';

	const textareaVariants = tv({
		base: 'flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50'
	});

	type $$Props = HTMLTextareaAttributes & {
		class?: string;
	};

	let { class: className, value = $bindable(), ...restProps }: $$Props = $props();

	// 导出 DOM 元素引用
	let textareaElement: HTMLTextAreaElement;
	export { textareaElement as element };
</script>

<textarea
	bind:this={textareaElement}
	bind:value
	class={textareaVariants({ class: className })}
	{...restProps}
></textarea>