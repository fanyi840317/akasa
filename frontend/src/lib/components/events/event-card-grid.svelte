<script lang="ts">
  import { fade } from "svelte/transition";
  import type { Event } from "$lib/types/event";
  import EventCard from "./event-card.svelte";
  import { cn } from "$lib/utils";

  let {
    events = [],
    onEventClick = (_: Event) => {},
    class: className = "",
    cardSize = "sm",
  } = $props<{
    events: Event[];
    onEventClick?: (event: Event) => void;
    class?: string;
    cardSize?: "xs" | "sm";
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
        <EventCard
          {event}
          onClick={onEventClick}
          size={cardSize}
          class="h-full"
        />
      {/each}
    {:else}
      <div class="col-span-full flex justify-center items-center py-8 text-base-content/50">
        暂无事件数据
      </div>
    {/if}
  </div>
</div>