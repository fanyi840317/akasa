<script lang="ts">
  import { fly } from "svelte/transition";
  import { UserAvatar } from "$lib/components/ui/avatar";
  import type { Event } from "$lib/types/event";

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

<div class="flex-row relative items-center justify-center {className}">
  <div class="flex flex-row">
    {#each events.slice(0, maxEvents) as event}
      <!-- svelte-ignore a11y_no_static_element_interactions -->
      <!-- svelte-ignore a11y_missing_attribute -->
      <!-- svelte-ignore a11y_click_events_have_key_events -->
      <div
        class="flex flex-row items-start justify-center relative gap-x-4 p-4 transition-all
         hover:bg-base-300/90 hover:scale-105 rounded-lg cursor-pointer group"
        transition:fly={{ y: 20, duration: 300 }}
        onmouseenter={() => onEventHover(event)}
        onmouseleave={onEventLeave}
        onclick={() => onEventClick(event)}
      >
        <div class="flex flex-col items-center justify-center gap-y-1">
          <img
            src={getCoverUrl(event)}
            placeholder="blur"
            alt={event.title || "Event image"}
            class="w-[120px] h-[80px] object-cover rounded-sm"
          />
        </div>
        <div
          class="flex flex-col flex-1 h-full items-start justify-center gap-y-1"
        >
          <h3
            class="text-md font-semibold leading-6 break-words line-clamp-1 text-base-content group-hover:text-gray-50"
          >
          {event.title.substring(0, 10)}
          </h3>
          <div class="text-base-content/50 text-[10px]">
            {event.date.split("T")[0]}
          </div>
          <div class="relative flex items-center gap-x-2">
            <UserAvatar
              class="h-4 w-4"
              src={event.creator_avatar || "https://avatars.githubusercontent.com/u/93428946?v=4"}
              alt="avatar"
              fallback={event.creator_name?.[0] || "?"}
            />
            <div class="text-[8px]">
              <p class="text-base-content">
                {event.creator_name}
              </p>
            </div>
          </div>
        </div>
      </div>
    {/each}
  </div>
  <div
    class="pointer-events-none absolute inset-y-0 left-0 w-1/3 h-full bg-gradient-to-r from-base-100"
  ></div>
  <div
    class="pointer-events-none absolute inset-y-0 right-0 w-1/3 h-full bg-gradient-to-l from-base-100"
  ></div>
</div>
