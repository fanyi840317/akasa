<script lang="ts">
  import type { Marker } from '$lib/markers';
  import { createEventDispatcher } from 'svelte';

  export let marker: Marker;
  const dispatch = createEventDispatcher();

  function handleClick() {
    dispatch('markerClick', marker);
  }
</script>

<div 
  class="marker" 
  on:click={handleClick}
  on:keydown={(e) => e.key === 'Enter' && handleClick()}
  role="button"
  tabindex="0"
>
  <div class="marker-pin"></div>
  <div class="marker-popup">
    <h3>{marker.name}</h3>
    <p>{marker.description}</p>
  </div>
</div>

<style>
  .marker {
    cursor: pointer;
    position: relative;
    width: 30px;
    height: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .marker-pin {
    width: 0;
    height: 0;
    border-left: 15px solid transparent;
    border-right: 15px solid transparent;
    border-top: 25px solid #ff4444;
    position: relative;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
  }

  .marker-pin::after {
    content: '';
    position: absolute;
    top: -25px;
    left: -15px;
    width: 30px;
    height: 25px;
    background: linear-gradient(45deg, #ff4444 50%, #dd3333 50%);
    clip-path: polygon(50% 0, 100% 100%, 0 100%);
  }

  .marker-popup {
    display: none;
    position: absolute;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    background: white;
    padding: 10px;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    white-space: nowrap;
    z-index: 1;
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