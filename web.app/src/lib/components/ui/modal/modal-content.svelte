<script lang="ts">
	import { cn } from "$lib/utils.js";
	import type { Snippet } from "svelte";

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

<div class={cn("relative w-full overflow-y-auto", className)} {...restProps}>
	<div class="flex justify-between items-center mb-4">
		<div class="flex items-center">
			{@render leftToolbar?.()}
		</div>
		<div class="flex items-center">
			{@render rightToolbar?.()}
		</div>
	</div>
	{@render children?.()}
</div>