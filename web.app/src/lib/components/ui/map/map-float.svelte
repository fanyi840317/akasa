<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { MapPin } from "lucide-svelte";
  import MapBase from "./map-base.svelte";
  import type { LocationData } from '.';

  export let locationName = "";
  export let locationData: LocationData = {
    longitude: 104.06,
    latitude: 30.67
  };
  export let showUserLocation = true;

  let isExpanded = false;
  let mapComponent: MapBase;

  function toggleExpand() {
    isExpanded = !isExpanded;
  }
</script>

<div class="map-float-container {isExpanded ? 'expanded' : ''} card">
  {#if !isExpanded}
    <Button 
      variant="outline" 
      size="sm" 
      class="map-toggle-button"
      on:click={() => toggleExpand()}
    >
      <MapPin class="h-4 w-4 mr-2" />
      {locationName || "查看位置"}
    </Button>
  {:else}
    <div class="map-header">
      <span class="map-title">{locationName || "位置信息"}</span>
      <Button 
        variant="ghost" 
        size="sm" 
        class="map-close-button"
        on:click={() => toggleExpand()}
      >
        收起
      </Button>
    </div>
    <div class="map-wrapper">
      <MapBase
        bind:this={mapComponent}
        {locationData}
        {showUserLocation}
      />
    </div>
  {/if}
</div>

<style>
  .map-float-container {
    position: fixed;
    right: 1rem;
    bottom: 1rem;
    z-index: 50;
    border-radius: 0.75rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15), 0 2px 8px rgba(0, 0, 0, 0.1);
    background-color: var(--card);
    border: 1px solid var(--border);
    overflow: hidden;
    transition: all 0.3s ease;
  }

  .map-float-container.expanded {
    width: 320px;
    height: 240px;
  }

  .map-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem;
    border-bottom: 1px solid var(--border);
  }

  .map-title {
    font-size: 0.875rem;
    font-weight: 500;
  }

  .map-wrapper {
    width: 100%;
    height: calc(100% - 2.5rem);
    position: relative;
  }
</style> 