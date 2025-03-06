<script lang="ts">
	import type { WithElementRef } from "bits-ui";
	import type { HTMLInputAttributes } from "svelte/elements";
	import { cn } from "$lib/utils.js";

	type $$Props = WithElementRef<HTMLInputAttributes> & {
		value?: string | number | undefined;
	};

	let {
		type = "text",
		class: className = undefined,
		ref = $bindable(null),
		value = $bindable(undefined),
		...restProps
	} = $props();
</script>

<input
	bind:this={ref}
	{type}
	class={cn(
		"border-input placeholder:text-muted-foreground focus-visible:ring-ring flex h-10 w-full rounded-md border bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
		className
	)}
	bind:value
	{...restProps}
	on:keypress
	on:input
	on:change
	on:focus
	on:blur
/>
