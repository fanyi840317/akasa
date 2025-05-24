<script lang="ts">
  import { cn } from "$lib/utils";
  import type { Snippet } from "svelte";
    import { fade } from "svelte/transition";

  let {
    class: className = "",
    children,
    title,
    description,
    info,
    size = 'sm', // Default to 'sm'
    contentClass = '', // Added contentClass prop
    ...restProps
  } = $props<{
    class?: string;
    children?: Snippet;
    title?: string;
    description?: string;
    info?: string;
    size?: 'xs' | 'sm'; // Added size prop
    contentClass?: string; // Added contentClass prop
  }>();
</script>

<div
  class={cn(
    "card bg-base-100 card-border border-base-200 overflow-hidden",
    size === 'sm' && "card-sm", // Apply card-sm only if size is 'sm'
    size === 'xs' && "p-0", // Custom padding for xs, or adjust as needed
    className,
  )}
  in:fade={{ duration: 200 }}
  out:fade={{ duration: 200 }}
  {...restProps}
>
  <div 
    class={cn(
      "card-body relative",
      size === 'sm' && "gap-4", // Default gap for sm
      size === 'xs' && "p-2 gap-1",  // Smaller padding and gap for xs
      contentClass // Apply contentClass here
    )}
  >
    {@render children?.()}
  </div>
  <div 
      class={cn(
        "bg-base-200 flex items-center gap-2",
        size === 'sm' && "py-4", // Default padding for sm footer content
        size === 'xs' && "py-2"   // Smaller padding for xs footer content
      )}
    >
      <div class="grow min-w-0 gap-1 ">
        {#if title}
          <div 
            class={cn(
              "font-medium ",
              size === 'sm' && "text-xs px-4 ",
              size === 'xs' && "text-[11px] leading-tight px-2"
            )}
          >
            {title}
          </div>
        {/if}
        {#if description}
          <div 
            class={cn(
              "opacity-60  overflow-hidden text-ellipsis",
              size === 'sm' && "text-[10px] px-4",
              size === 'xs' && "text-[10px] leading-tight px-2"
            )}
          >
            {description}
          </div>
        {/if}
      </div>
      {#if info}
        <div class="shrink-0">
          <span 
            class={cn(
              "badge badge-neutral",
              size === 'sm' && "badge-sm",
              size === 'xs' && "badge-xs" // Smaller badge for xs
            )}
          >
            {info}
          </span>
        </div>
      {/if}
    </div>
</div>
