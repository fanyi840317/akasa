<script lang="ts">
	import { cn } from "$lib/utils.js";
	import type { Snippet } from "svelte";
	import { ScrollArea } from "$lib/components/ui/scroll-area";

	let {
		class: className = "",
		leftToolbar,
		rightToolbar,
		children,
		...restProps
	} = $props<{
		leftToolbar?: Snippet;
		rightToolbar?: Snippet;
		children?: Snippet;
	}>();
</script>

<div class={cn("relative w-full h-full flex flex-col", className)} {...restProps}>
	{#if leftToolbar || rightToolbar}
		<div class="flex-none flex justify-between items-center">
			<div class="flex items-center">
				{@render leftToolbar?.()}
			</div>
			<div class="flex items-center">
				{@render rightToolbar?.()}
			</div>
		</div>
	{/if}
	<ScrollArea class="flex-1">
		{@render children?.()}
	</ScrollArea>
</div>