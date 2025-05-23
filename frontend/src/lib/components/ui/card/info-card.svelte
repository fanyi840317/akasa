<script lang="ts">
  import { cn } from "$lib/utils";
  import type { Snippet } from "svelte";

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
    "card bg-base-100 card-border border-base-300 overflow-hidden",
    size === 'sm' && "card-sm", // Apply card-sm only if size is 'sm'
    size === 'xs' && "p-0", // Custom padding for xs, or adjust as needed
    className,
  )}
  {...restProps}
>
  <div 
    class={cn(
      "card-body",
      size === 'sm' && "gap-4", // Default gap for sm
      size === 'xs' && "p-2 gap-1",  // Smaller padding and gap for xs
      contentClass // Apply contentClass here
    )}
  >
    {@render children?.()}
  </div>
  <div class={cn("bg-base-300", size === 'xs' && "py-1.5 px-2")}> 
    <div 
      class={cn(
        "flex items-center gap-2",
        size === 'sm' && "p-4", // Default padding for sm footer content
        size === 'xs' && "p-1.5"   // Smaller padding for xs footer content
      )}
    >
      <div class="grow">
        {#if title}
          <div 
            class={cn(
              "font-medium",
              size === 'sm' && "text-xs",
              size === 'xs' && "text-[10px] leading-tight" // Smaller font for xs title
            )}
          >
            {title}
          </div>
        {/if}
        {#if description}
          <div 
            class={cn(
              "opacity-60",
              size === 'sm' && "text-[10px]",
              size === 'xs' && "text-[9px] leading-tight" // Smaller font for xs description
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
</div>
