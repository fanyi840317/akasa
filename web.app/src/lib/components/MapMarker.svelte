<script lang="ts">
  import type { Marker } from '$lib/markers';

  export let marker: Marker;
  export let onMarkerClick: (marker: Marker) => void;
</script>

<div 
  class="marker" 
  on:click|stopPropagation={() => {
    console.log('Marker clicked:', marker);
    onMarkerClick(marker);
  }}
  on:keydown|stopPropagation={(e) => e.key === 'Enter' && onMarkerClick(marker)}
  role="button"
  tabindex="0"
>
<!-- Start of Selection -->
<svg class="w-4 h-4 mr-2 glow" fill="currentColor" viewBox="0 0 20 20">
  <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
</svg>
<style>
  .glow {
    filter: drop-shadow(0 0 5px rgba(0, 255, 204, 0.7));
  }
</style>
<!-- End of Selection -->
  <div class="marker-popup">
    <h3>{marker.name}</h3>
    <p>{marker.description}</p>
  </div>
</div>

<style>
  .marker {
    cursor: pointer;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .marker-icon {
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
  }
  .marker-popup {
    display: none;
    position: absolute;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(255, 255, 255, 0.9);
    padding: 10px;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    white-space: nowrap;
    z-index: 1;
    pointer-events: none;
  }
  .marker:hover .marker-popup {
    display: block;
  }

  h3 {
    margin: 0 0 5px 0;
    font-size: 14px;
  }

  p {
    margin: 0;
    font-size: 12px;
  }
</style>