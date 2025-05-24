<script lang="ts">
  import { MapBase } from "$lib/components/map";
  import ActionbarCard from "./actionbar-card.svelte";
  import type { Location } from "$lib/types/map";
  import { cn } from "$lib/utils";
  import InfoCard from '$lib/components/ui/card/info-card.svelte'; // Import InfoCard
  // 这里可以引入地图相关依赖
  // import MapBase from "$lib/components/map/map-base.svelte";
  let {
    class: className = "",
    locationData = $bindable(null),
    ...restProps
  } = $props<{ mapData?: any; class?: string; locationData?: Location }>();

  let showMapTooltip = $state(false); // State for controlling map tooltip visibility

  function handleMouseEnterTrigger() { // Add mouse enter handler
    showMapTooltip = true;
  }

  function handleMouseLeaveTrigger() { // Add mouse leave handler
    showMapTooltip = false;
  }
</script>

<div class="relative">
  <ActionbarCard 
    class={cn("border-neutral min-w-18", className)}
    {...restProps}
    onmouseenter={handleMouseEnterTrigger} 
    onmouseleave={handleMouseLeaveTrigger} 
  >
    <div class="relative w-full h-full">
      <MapBase bind:locationData showUserLocation={false} clickable={false}
      ></MapBase>
      <div class="absolute top-0 right-0 w-full h-full z-1000"></div>
    </div>

  </ActionbarCard>

  {#if showMapTooltip}
    <div
      class="absolute z-50 top-full left-1/2 -translate-x-1/2 mt-2 pointer-events-none"
    >
      <InfoCard
        class="shadow-xl min-w-20 rounded-lg" 
        size="xs"
        contentClass="p-0"
        title={locationData?.name || "未设置地点"}
        description={locationData?.coordinates
          ? `${locationData.coordinates.lng.toFixed(2)}, ${locationData.coordinates.lat.toFixed(2)}`
          : "点击设置地点"}
      >
        <!-- Optional: Add more content to the tooltip body if needed -->
      </InfoCard>
    </div>
  {/if}
</div>
