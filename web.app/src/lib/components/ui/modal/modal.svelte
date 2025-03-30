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
		class="fixed inset-0 z-50 bg-neutral-900/10 backdrop-blur-[2px] dark:bg-neutral-900/50"
		on:click={handleClickOutside}
		{...restProps}
	>
		<div
			bind:this={modalRef}
			class={cn(
				"fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] bg-white dark:bg-neutral-900 border border-neutral-200/50 dark:border-neutral-800/50 shadow-[0_0_0_1px_rgba(0,0,0,0.03)] dark:shadow-[0_0_0_1px_rgba(255,255,255,0.03)] duration-200 sm:rounded-lg overflow-hidden",
				className
			)}
		>
			{#if leftToolbar || rightToolbar}
				<div class="flex items-center justify-between border-b border-neutral-200/50 dark:border-neutral-800/50 p-4">
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