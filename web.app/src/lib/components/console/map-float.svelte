<script lang="ts">
  import { onMount, afterUpdate } from 'svelte';
  import mapboxgl from 'mapbox-gl';
  import 'mapbox-gl/dist/mapbox-gl.css';
  import { mode } from 'mode-watcher';
  import { get } from 'svelte/store';
  import { MapPin } from 'lucide-svelte';
  import * as Popover from "$lib/components/ui/popover";
  import { Button } from "$lib/components/ui/button";
  import { cn } from "$lib/utils";

  export let locationName = "";
  export let locationData = {
    longitude: 104.06,
    latitude: 30.67
  };
  export let showUserLocation = true;
  export let size = "small"; // small, medium, large

  let container: HTMLDivElement;
  let map: mapboxgl.Map;
  let resizeObserver: ResizeObserver;
  let isExpanded = false;

  mapboxgl.accessToken = 'pk.eyJ1IjoiZmFueWk4NDAzMTciLCJhIjoiY202cDE4OW9wMHZxMzJscTBtbW82NDNxdCJ9.90mwfIpA62nmCY0_C7IkUw';

  function toggleExpand() {
    isExpanded = !isExpanded;
    
    if (isExpanded) {
      // 当展开时，如果地图尚未初始化，则初始化地图
      setTimeout(() => {
        if (!map && container) {
          initMap();
        } else if (map) {
          map.resize();
        }
      }, 100);
    } else {
      // 收起时只需调整大小
      setTimeout(() => map?.resize(), 100);
    }
  }

  let modeUnsubscribe: () => void;

  function initMap() {
    if (!container) return;
    
    map = new mapboxgl.Map({
      container,
      style: get(mode) === 'light' ? 'mapbox://styles/mapbox/light-v10' : 'mapbox://styles/mapbox/dark-v11',
      zoom: 13,
      center: [locationData.longitude, locationData.latitude],
      pitch: 0,
      antialias: true
    });

    if (showUserLocation) {
      const userMarkerElement = document.createElement('div');
      userMarkerElement.className = 'user-location-marker';
      new mapboxgl.Marker({
        element: userMarkerElement,
        anchor: 'center'
      })
        .setLngLat([locationData.longitude, locationData.latitude])
        .addTo(map);
    }

    // 确保在重新初始化地图前取消之前的订阅
    if (modeUnsubscribe) {
      modeUnsubscribe();
    }

    modeUnsubscribe = mode.subscribe(currentMode => {
      map?.setStyle(currentMode === 'light' ? 'mapbox://styles/mapbox/light-v10' : 'mapbox://styles/mapbox/dark-v11');
    });

    // 监听容器大小变化并调整地图
    if (resizeObserver) {
      resizeObserver.disconnect();
    }
    
    resizeObserver = new ResizeObserver(() => {
      if (map) map.resize();
    });
    
    if (container) {
      resizeObserver.observe(container);
    }
  }

  onMount(() => {
    // 只在组件初始化时设置清理函数，不立即初始化地图
    // 地图将在用户点击展开按钮时初始化
    return () => {
      if (map) map.remove();
      if (resizeObserver) resizeObserver.disconnect();
      if (modeUnsubscribe) modeUnsubscribe();
    };
  });

  afterUpdate(() => {
    if (map) {
      // 确保地图大小正确刷新
      setTimeout(() => map.resize(), 0);
    }
  });
</script>

<div class="map-float-container {isExpanded ? 'expanded' : ''} card">
  {#if !isExpanded}
    <Button 
      variant="outline" 
      size="sm" 
      class="map-toggle-button"
      onclick={toggleExpand}
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
        onclick={toggleExpand}
      >
        收起
      </Button>
    </div>
    <div bind:this={container} class="mapContainer"></div>
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

  .mapContainer {
    width: 100%;
    height: calc(100% - 2.5rem);
    position: relative;
    overflow: hidden;
    display: block;
  }

  :global(.mapboxgl-ctrl-bottom-right) {
    display: none;
  }

  :global(.user-location-marker) {
    width: 15px;
    height: 15px;
    background-color: rgb(37, 99, 235);
    border: 3px solid rgba(255, 255, 255, 0.8);
    border-radius: 50%;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.3);
    cursor: pointer;
    position: relative;
  }
  
  :global(.user-location-marker::after) {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100%;
    height: 100%;
    background-color: rgba(37, 99, 235, 0.6);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    animation: pulse-scale 2s infinite;
  }
  
  @keyframes pulse-scale {
    0% {
      transform: translate(-50%, -50%) scale(1);
      opacity: 1;
    }
    70% {
      transform: translate(-50%, -50%) scale(18);
      opacity: 0;
    }
    100% {
      transform: translate(-50%, -50%) scale(1);
      opacity: 0;
    }
  }
</style>