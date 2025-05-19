<script lang="ts">
	import { cn } from "$lib/utils.js";
	import { X } from "lucide-svelte";
	import type { Snippet } from "svelte";

	let {
		class: className = "",
		onClose = () => {},
		children,
		...restProps
	} = $props<{
		title?: Snippet;
		children: Snippet;
		class?: string;
		onClose?: () => void;
	}>();
</script>

<div class={cn("flex items-center justify-between p-4 ", className)} {...restProps}>
	<h2 class="text-lg font-semibold leading-none tracking-tight">
		{@render children?.()}
	</h2>
	<button
		class="btn btn-sm btn-circle btn-ghost"
		onclick={onClose}
	>
		<X class="h-4 w-4" />
		<span class="sr-only">Close</span>
	</button>
</div>