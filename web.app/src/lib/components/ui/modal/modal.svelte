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
		open?: boolean;
		class?: string;
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
		class="fixed inset-0 z-50 bg-muted/10 backdrop-blur-[2px]
		 dark:bg-neutral-900/50 duration-200 data-[state=open]:animate-in
		 data-[state=closed]:animate-out data-[state=closed]:fade-out-0
		 data-[state=open]:fade-in-0"
		data-state={open ? "open" : "closed"}
		onclick={handleClickOutside}
		{...restProps}
	>
		<div
			bind:this={modalRef}
			class={cn(
				"fixed left-[50%] top-[50%] z-50 grid w-full translate-x-[-50%] translate-y-[-50%] bg-white dark:bg-neutral-900 border border-neutral-200/50 dark:border-neutral-800/50 shadow-[0_8px_30px_rgba(0,0,0,0.12)] dark:shadow-[0_8px_30px_rgba(0,0,0,0.3)] duration-200 sm:rounded-lg overflow-hidden data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%]",
				className,
			)}
			data-state={open ? "open" : "closed"}
		>
			<div class="flex flex-col h-full">
				{#if leftToolbar || rightToolbar}
					<div
						class="flex items-center justify-between p-2 bg-white dark:bg-neutral-900 z-10"
					>
						<div class="flex items-center gap-2">
							{@render leftToolbar?.()}
						</div>
						<div class="flex items-center gap-2">
							{@render rightToolbar?.()}
						</div>
					</div>
				{/if}
				<div class="flex-1 overflow-auto">
					{@render children?.()}
				</div>
			</div>
		</div>
	</div>
{/if}
