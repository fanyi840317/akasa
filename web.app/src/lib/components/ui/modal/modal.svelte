<script lang="ts">
	import { cn } from "$lib/utils.js";
	import type { Snippet } from "svelte";

	let {
		open = $bindable(false),
		class: className,
		leftToolbar,
		rightToolbar,
		children,
		...restProps
	} = $props<{
		leftToolbar?: Snippet;
		rightToolbar?: Snippet;
		children?: Snippet;
	}>();

	let modalRef: HTMLDivElement;

	function handleClickOutside(event: MouseEvent) {
		if (modalRef && !modalRef.contains(event.target as Node)) {
			open = false;
		}
	}
</script>

{#if open}
	<div
		class="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm"
		on:click={handleClickOutside}
		{...restProps}
	>
		<div
			bind:this={modalRef}
			class={cn(
				"fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] bg-background shadow-xl duration-200 sm:rounded-lg overflow-hidden",
				className
			)}
		>
			{#if leftToolbar || rightToolbar}
				<div class="flex items-center justify-between">
					<div class="flex items-center gap-2">
						{@render leftToolbar?.()}
					</div>
					<div class="flex items-center gap-2">
						{@render rightToolbar?.()}
					</div>
				</div>
			{/if}
			{@render children?.()}
		</div>
	</div>
{/if}