<script lang="ts">
  import { ChevronDown } from "lucide-svelte";
  import EventList from "$lib/components/events/event-list.svelte";
  import type { Event } from "$lib/types/event";
  import { onMount } from "svelte";
  import { eventStore } from "$lib/stores/event";
  import { auth } from "$lib/stores/auth";
  import { goto } from "$app/navigation";
  import ScrollArea from "$lib/components/ui/scroll-area/scroll-area.svelte";
  import InputArea from "$lib/components/ai/InputArea.svelte";

  let events: Event[] = $derived($eventStore.events);
  onMount(async () => {
    events = await eventStore.fetchEvents($auth.user?.$id);
  });
  function handEventClick(event: Event) {
    goto(`/console/events/${event.$id}`);
  }
</script>

<div
  class="mx-auto px-6 pt-10 xs:px-8 sm:px-12 lg:px-6 pt-6 flex flex-col
   justify-start  w-full"
  style="max-width: 1608px;"
>
  <!-- <div class="flex flex-col text-center gap-4 mb-14">
    <h1 class="text-3xl font-extrabold sm:text-4xl lg:text-5xl" role="heading">
      Events
    </h1>
    <p class="text-base-content/50">A space to manage and organize your events</p>
    
  </div> -->

  <div class="flex flex-col justify-center items-center -ml-30">
    <div class="flex items-center gap-2">
      <h1 class="text-2xl font-semibold">Week MAY 7 - MAY 13</h1>
      <button class="btn btn-ghost btn-sm p-1">
        <ChevronDown class="w-5 h-5" />
      </button>
    </div>
    <p class="text-xs text-base-content/60 mb-10">
      Last Updated: May 12, 2025 12:06 pm
    </p>
    <!-- <div class="flex items-center gap-4">
      <span class="text-sm text-base-content/50">42182 users</span>
      <div class="form-control">
        <input
          type="text"
          placeholder="filter by username"
          class="input input-sm w-full max-w-xs"
        />
      </div>
    </div> -->
  </div>
  <!-- <p class="text-xs text-base-content/60 mb-10">
    Last Updated: May 12, 2025 12:06 pm
  </p> -->
  <ScrollArea class="h-[calc(100vh-300px)]">
    <EventList {events} onclick={handEventClick} />
  </ScrollArea>
  <div class="flex-center">

    <div class="w-[600px] p-4 -ml-30">

  <InputArea></InputArea>
    </div>
  </div>

</div>
