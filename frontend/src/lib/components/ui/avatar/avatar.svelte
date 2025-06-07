<script lang="ts">
    import { cn } from "$lib/utils";
	import { Avatar, type WithoutChildrenOrChild } from "bits-ui";
 
	let {
		src,
		alt,
		class: className,
		fallback,
		fallbackClass,
		ref = $bindable(null),
		imageRef = $bindable(null),
		fallbackRef = $bindable(null),
		...restProps
	}: WithoutChildrenOrChild<Avatar.RootProps> & {
		src?: string |null;
		alt?: string;
		fallback?: string;
		imageRef?: HTMLImageElement | null;
		fallbackRef?: HTMLElement | null;
		fallbackClass?: string;
	} = $props();
</script>
 
<Avatar.Root class={cn("avatar size-full size-10 bg-neutral rounded-full", className)} {...restProps} bind:ref>
	<Avatar.Image class="aspect-square size-full rounded-full" {src} {alt} bind:ref={imageRef} />
	<Avatar.Fallback class="flex size-full items-center justify-center" bind:ref={fallbackRef}>
		<span class={cn("text-base-content font-semibold text-sm",fallbackClass)}>{fallback}</span>
	</Avatar.Fallback>
</Avatar.Root>