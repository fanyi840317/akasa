<script lang="ts">
  import { cn } from "$lib/utils.js";
  import type { Snippet } from "svelte";
  import { ScrollArea } from "../scroll-area";
  import { fade } from "svelte/transition";

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

  // svelte-ignore non_reactive_update
  let modalRef: HTMLDivElement;

  function handleClickOutside(event: MouseEvent) {
    if (modalRef && !modalRef.contains(event.target as Node)) {
      open = false;
    }
  }
</script>

{#if open}
  <div
    class="fixed inset-0 z-50 base-200 backdrop-blur-[2px]
		duration-200 data-[state=open]:animate-in
		 data-[state=closed]:animate-out data-[state=closed]:fade-out-0
		 data-[state=open]:fade-in-0"
    data-state={open ? "open" : "closed"}
    onclick={handleClickOutside}
    {...restProps}
  >
    <div
      bind:this={modalRef}
      class={cn(
        "fixed left-[50%] top-[50%] z-50 card bg-base-100 border border-base-300  w-full shadow-3xl translate-x-[-50%] translate-y-[-50%] rounded-3xl overflow-hidden ",
        className
      )}
      in:fade={{ duration: 200 }}
      out:fade={{ duration: 200 }}
      data-state={open ? "open" : "closed"}
    >
      <div class="flex flex-col h-full">
        {#if leftToolbar || rightToolbar}
          <div class="flex items-center justify-between p-2">
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
  </div>
{/if}
