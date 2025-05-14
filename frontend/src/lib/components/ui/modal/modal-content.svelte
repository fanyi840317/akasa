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

<div class={cn("relative w-full h-full flex flex-col border-t border-border/20 dark:border-white/[0.08]", className)} {...restProps}>
	{#if leftToolbar || rightToolbar}
		<div class="flex-none flex justify-between items-center border-b border-border/20 dark:border-white/[0.08] p-4">
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