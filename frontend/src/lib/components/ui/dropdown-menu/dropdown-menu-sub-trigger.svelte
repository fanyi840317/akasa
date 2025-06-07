<script lang="ts">
	import { DropdownMenu as DropdownMenuPrimitive } from "bits-ui";
	import { ChevronRightIcon } from "lucide-svelte";
	import { cn } from "$lib/utils.js";

	let {
		ref = $bindable(null),
		class: className,
		inset,
		children,
		...restProps
	}: DropdownMenuPrimitive.SubTriggerProps & {
		inset?: boolean;
	} = $props();
</script>

<DropdownMenuPrimitive.SubTrigger
	bind:ref
	data-slot="dropdown-menu-sub-trigger"
	data-inset={inset}
	class={cn(
			"data-highlighted:bg-base-200 data-highlighted:text-base-content data-[state=open]:bg-base-200 data-[state=open]:text-base-content outline-hidden [&_svg:not([class*='text-'])]:text-base-content/70 flex cursor-default select-none items-center gap-2 rounded-btn px-2 py-1.5 text-sm data-[disabled]:pointer-events-none data-[inset]:pl-8 data-[disabled]:opacity-50 [&_svg:not([class*='size-'])]:size-4 [&_svg]:pointer-events-none [&_svg]:shrink-0",
			className,
		)}
	{...restProps}
>
	{@render children?.()}
	<ChevronRightIcon class="ml-auto size-4" />
</DropdownMenuPrimitive.SubTrigger>
