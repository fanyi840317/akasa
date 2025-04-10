<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { fade, fly } from "svelte/transition";
  import { MapPin } from "lucide-svelte";
  import MapBase from "$lib/components/map/map-base.svelte";
  import type { LocationData } from "$lib/components/map/types";

  const dispatch = createEventDispatcher();

  let {
    locationData = $bindable(null),
  } = $props<{
    locationData?: LocationData | null;
  }>();

  // 处理点击事件
  function handleClick(action: string) {
    dispatch("action", { type: action });
  }

  // 处理位置变化
  function handleLocationChange(event: CustomEvent<LocationData>) {
    dispatch("locationChange", { location: event.detail });
  }
</script>


<!-- 地图组件 -->
<div class="w-[160px] bg-card/40 rounded-sm overflow-hidden">
  <div class="h-[100px] p-1">
    <div class="w-full h-full rounded-t-sm overflow-hidden map-container">
      <MapBase
        {locationData}
        on:locationChange={handleLocationChange}
        showUserLocation={false}
      />
    </div>
  </div>
  <div class="p-2 mt-2 text-xs text-muted-foreground/50 border-border/50 flex items-center gap-1">
    <MapPin class="h-3 w-3" />
    {#if locationData?.address}
      {locationData.address}
    {:else}
      未设置位置
    {/if}
  </div>
</div>
 <!-- 地图组件 -->
 <div class="w-[160px] bg-card/40 rounded-sm overflow-hidden">
  <div class="h-[100px] p-1">
    <div class="w-full h-full bg-muted rounded-t-sm overflow-hidden map-container">
      
    </div>
  </div>
  <div class="p-2 mt-2 text-xs text-muted-foreground/50 border-border/50 flex items-center gap-1">
    <MapPin class="h-3 w-3" />
    {#if locationData?.address}
      {locationData.address}
    {:else}
      未设置位置
    {/if}
  </div>
</div>
<style>
  :global(.mapboxgl-map) {
    border-radius: 2px !important;
  }
  
  :global(.map-container .mapboxgl-canvas) {
    border-radius: 2px !important;
  }
  
  :global(.map-container .mapboxgl-canvas-container) {
    border-radius: 2px !important;
  }
</style> 