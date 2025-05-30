<script lang="ts">
	import { cn } from "$lib/utils.js";
	import { DropdownMenu as DropdownMenuPrimitive } from "bits-ui";

	let {
		ref = $bindable(null),
		class: className,
		inset,
		variant = "default",
		...restProps
	}: DropdownMenuPrimitive.ItemProps & {
		inset?: boolean;
		variant?: "default" | "destructive";
	} = $props();
</script>

<DropdownMenuPrimitive.Item
	bind:ref
	data-slot="dropdown-menu-item"
	data-inset={inset}
	data-variant={variant}
	class={cn(
			"data-highlighted:bg-base-200 data-highlighted:text-base-content data-[variant=destructive]:text-error data-[variant=destructive]:data-highlighted:bg-error/10 data-[variant=destructive]:data-highlighted:text-error data-[variant=destructive]:*:[svg]:!text-error [&_svg:not([class*='text-'])]:text-base-content/70 outline-hidden relative flex cursor-default select-none items-center gap-2 rounded-md px-2 py-1.5 text-sm data-[disabled]:pointer-events-none data-[inset]:pl-8 data-[disabled]:opacity-50 [&_svg:not([class*='size-'])]:size-4 [&_svg]:pointer-events-none [&_svg]:shrink-0",
			className
		)}
	{...restProps}
/>
