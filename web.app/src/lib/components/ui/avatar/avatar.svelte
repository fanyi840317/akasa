<script lang="ts">
	import { Avatar as AvatarPrimitive } from "bits-ui";
	import { cn } from "$lib/utils.js";

	let {
		class: className,
		ref = $bindable(null),
		loadingStatus = $bindable("loading"),
		shape = $bindable("circle"), // 新增shape属性，默认为circle，可选值为circle, squircle
		...restProps
	}: AvatarPrimitive.RootProps & { shape?: "circle" | "squircle" } = $props();

	// 根据shape属性决定使用哪种圆角样式
	$effect(() => {
		if (shape !== "circle" && shape !== "squircle") {
			shape = "circle"; // 默认回退到circle
		}
	});
</script>

<AvatarPrimitive.Root
	bind:loadingStatus
	bind:ref
	class={cn(
		"relative flex size-10 shrink-0 overflow-hidden",
		shape === "squircle" ? "rounded-2xl" : "rounded-full",
		className
	)}
	{...restProps}
/>
