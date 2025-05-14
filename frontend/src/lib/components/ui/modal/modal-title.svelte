<script lang="ts">
	import { cn } from "$lib/utils.js";
	import { X } from "lucide-svelte";
	import type { Snippet } from "svelte";

	let {
		class: className = "",
		onClose = () => {},
		title,
		...restProps
	} = $props<{
		title?: Snippet;
	}>();
</script>

<div class={cn("flex items-center justify-between", className)} {...restProps}>
	<h2 class="text-lg font-semibold leading-none tracking-tight">
		{@render title?.()}
	</h2>
	<button
		class="rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground"
		on:click={onClose}
	>
		<X class="h-4 w-4" />
		<span class="sr-only">Close</span>
	</button>
</div>