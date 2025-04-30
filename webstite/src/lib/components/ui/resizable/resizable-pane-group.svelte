<script lang="ts">
	import * as ResizablePrimitive from "paneforge";
	import { cn } from "$lib/utils";

	let {
		ref = $bindable(null),
		class: className,
		direction,
		this: paneGroup = $bindable(),
		...restProps
	} = $props();
</script>

<ResizablePrimitive.PaneGroup
	bind:this={ref}
	bind:this={paneGroup}
	{direction}
	class={cn("flex h-full w-full data-[direction=vertical]:flex-col", className)}
	{...restProps}
/>
