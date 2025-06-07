<script lang="ts">
  import { fade } from "svelte/transition";
  import type { Event } from "$lib/types/event";
  import { cn } from "$lib/utils";
  import { MyEventCard } from ".";

  let {
    events = [],
    onEventClick = (_: Event) => {},
    onEventShare = (_: Event) => {},
    onEventRename = (_: Event) => {},
    onEventDelete = (_: Event) => {},
    class: className = "",
    cardSize = "sm",
    showActions = true,
  } = $props<{
    events: Event[];
    onEventClick?: (event: Event) => void;
    onEventShare?: (event: Event) => void;
    onEventRename?: (event: Event) => void;
    onEventDelete?: (event: Event) => void;
    class?: string;
    cardSize?: "xs" | "sm";
    showActions?: boolean;
  }>();
</script>

<div
  class={cn(
    "w-full max-w-7xl mx-auto",
    className
  )}
  in:fade={{ duration: 300 }}
>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
    {#if events && events.length > 0}
      {#each events as event (event.$id)}
        <MyEventCard
          {event}
          onClick={onEventClick}
          onShare={onEventShare}
          onRename={onEventRename}
          onDelete={onEventDelete}
          size={cardSize}
          class="h-full"
          {showActions}
        />
      {/each}
    {:else}
      <div class="col-span-full flex justify-center items-center py-8 text-base-content/50">
        暂无事件数据
      </div>
    {/if}
  </div>
</div>