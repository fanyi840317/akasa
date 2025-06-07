<script lang="ts">
  import EventTimeEditor from "./event-time-editor.svelte";
  import EventLocationEditor from "./event-location-editor.svelte";
  import type { Location } from "$lib/types/map";

  let {
    eventTime = $bindable<Date | null>(null),
    location = $bindable<Location | null>(null),
    onTimeChange = (newTime: Date | null) => {},
    onLocationChange = (newLocation: Location | null) => {},
    class: className = ""
  } = $props<{
    eventTime?: Date | null;
    location?: Location | null;
    onTimeChange?: (newTime: Date | null) => void;
    onLocationChange?: (newLocation: Location | null) => void;
    class?: string;
  }>();
</script>

<div class="flex items-center gap-2 {className}">
  <span aria-hidden="true" class="text-base-content/40 w-4 min-w-4 select-none text-center text-lg">/</span>
  
  <!-- 时间编辑器组件 -->
  <EventTimeEditor 
    bind:eventTime
    {onTimeChange}
  />
  
  <span aria-hidden="true" class="text-base-content/40 w-4 min-w-4 select-none text-center text-lg">/</span>
  
  <!-- 地点编辑器组件 -->
  <EventLocationEditor 
    bind:location
    {onLocationChange}
  />
</div>