<script lang="ts">
  import { fly } from "svelte/transition";
  import { UserAvatar } from "$lib/components/ui/avatar";
  import type { Event } from "$lib/types/event";
  import { goto } from "$app/navigation";

  let {
    events = [],
    maxEvents = 4,
    onEventHover = (_: Event) => {},
    onEventLeave = () => {},
    onEventClick = (_: Event) => {},
    getCoverUrl = (event: Event) => event.cover || "",
    class: className = ""
  } = $props<{
    events: Event[];
    maxEvents?: number;
    onEventHover?: (event: Event) => void;
    onEventLeave?: () => void;
    onEventClick?: (event: Event) => void;
    getCoverUrl?: (event: Event) => string;
    class?: string;
  }>();
</script>

<div class="flex flex-wrap gap-4 max-w-[800px] {className}">
    {#each events.slice(0, maxEvents) as event}
      <!-- svelte-ignore a11y_no_static_element_interactions -->
      <!-- svelte-ignore a11y_missing_attribute -->
      <!-- svelte-ignore a11y_click_events_have_key_events -->
      <div
        class="flex flex-row items-start justify-start relative p-4 
        transition-all hover:bg-base-300/90 hover:scale-105 rounded-lg 
        cursor-pointer group  h-full gap-x-4"
        transition:fly={{ y: 20, duration: 300 }}
        onmouseenter={() => onEventHover(event)}
        onmouseleave={onEventLeave}
        onclick={() => onEventClick(event)}
      >
        <div class="mb-2">
          <img
            src={getCoverUrl(event)}
            alt={event.title || "Event image"}
            class="w-[120px] h-auto aspect-[16/10] object-cover rounded-md mb-3"
          />
        </div>
        <div class="flex flex-col flex-grow justify-between w-[160px]">
          <div>
            <h3
              class="text-[13px] leading-tight break-words text-base-content/50
              line-clamp-1 text-base-content group-hover:text-primary-content mb-1"
            >
              {event.title}
            </h3>
            {#if event.summary}
              <p class="text-[12px] font-mu text-base-content line-clamp-3 mb-2">
                {event.summary}
              </p>
            {/if}
  
          </div>
          <div class="flex items-center gap-x-3 text-xs text-base-content/20">
            <span class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-1 h-4 w-4"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                {event.views || 0}
            </span>
            <span class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-1 h-4 w-4"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path></svg>
                {event.likes || 0}
            </span>
        </div>
        </div>
      </div>
    {/each}

    <!-- Add More Card Button -->
    {#if events.length >= maxEvents}
      <!-- svelte-ignore a11y_no_static_element_interactions -->
      <!-- svelte-ignore a11y_missing_attribute -->
      <!-- svelte-ignore a11y_click_events_have_key_events -->
      <div
        class="flex flex-col items-center justify-center relative p-4 m-4
        transition-all hover:bg-base-300/90 hover:scale-105 rounded-lg 
        cursor-pointer group h-full bg-base-200/50 aspect-[16/10] w-[120px] min-w-[120px]"
        transition:fly={{ y: 20, duration: 300 }}
        onclick={() => goto('/events/new')}
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="2.5em" height="2.5em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="text-base-content/30 group-hover:text-primary-content">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
      </div>
    {/if}

    
  <!-- <div
    class="pointer-events-none absolute inset-y-0 left-0 w-1/3 h-full bg-gradient-to-r from-base-100"
  ></div>
  <div
    class="pointer-events-none absolute inset-y-0 right-0 w-1/3 h-full bg-gradient-to-l from-base-100"
  ></div> -->
</div>
