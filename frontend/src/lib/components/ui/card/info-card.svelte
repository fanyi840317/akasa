<script lang="ts">
  import { cn } from "$lib/utils";
  import type { Snippet } from "svelte";

  let {
    class: className = "",
    children,
    title,
    description,
    info,
    ...restProps
  } = $props<{
    class?: string;
    children?: Snippet;
    title: string;
    description?: string;
    info?: string;
  }>();
</script>

<div
  class={cn(
    "card bg-base-100 card-border border-base-300 card-sm overflow-hidden",
    className
  )}
  {...restProps}
>
  <div class="card-body gap-4">{@render children?.()}</div>
  <div class="bg-base-300">
    <div class="flex items-center gap-2 p-4">
      <div class="grow">
        <div class="text-sm font-medium">
          {title}
        </div>
        {#if description}
          <div class="text-xs opacity-60">
            {description}
          </div>
        {/if}
      </div>
      {#if info}
        <div class="shrink-0">
          <span class="badge badge-sm badge-neutral">{info}</span>
        </div>
      {/if}
    </div>
  </div>
</div>
