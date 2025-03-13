<script lang="ts">
  import { onMount, afterUpdate } from 'svelte';
  import mapboxgl from 'mapbox-gl';
  import 'mapbox-gl/dist/mapbox-gl.css';
  import { mode } from 'mode-watcher';
  import { get } from 'svelte/store';
  import { goto } from '$app/navigation';

  export let locationData = {
    longitude: 104.06,
    latitude: 30.67
  };
  export let showUserLocation = true;

  let container: HTMLDivElement;
  let map: mapboxgl.Map;
  let resizeObserver: ResizeObserver;

  mapboxgl.accessToken = 'pk.eyJ1IjoiZmFueWk4NDAzMTciLCJhIjoiY202cDE4OW9wMHZxMzJscTBtbW82NDNxdCJ9.90mwfIpA62nmCY0_C7IkUw';

  onMount(() => {
    // 创建地图前先确保容器可见
    setTimeout(() => {
      if (!container) return;
      
      map = new mapboxgl.Map({
        container,
        style: get(mode) === 'light' ? 'mapbox://styles/mapbox/light-v10' : 'mapbox://styles/mapbox/dark-v11',
        zoom: 8,
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

      const unsubscribe = mode.subscribe(currentMode => {
        map?.setStyle(currentMode === 'light' ? 'mapbox://styles/mapbox/light-v10' : 'mapbox://styles/mapbox/dark-v11');
      });

      // 监听容器大小变化并调整地图
      resizeObserver = new ResizeObserver(() => {
        if (map) map.resize();
      });
      
      if (container) {
        resizeObserver.observe(container);
      }

      return () => {
        if (map) map.remove();
        if (resizeObserver) resizeObserver.disconnect();
        unsubscribe();
      };
    }, 100);
  });

  afterUpdate(() => {
    if (map) {
      // 确保地图大小正确刷新
      setTimeout(() => map.resize(), 0);
    }
  });
</script>

<div bind:this={container} class="mapContainer">
</div>

<style>
  .mapContainer {
    width: 100%;
    height: 100%;
    position: relative;
    overflow: hidden;
    display: block;
  }

  :global(.mapboxgl-ctrl-bottom-right) {
    display: none;
  }

  :global(.mapboxgl-map) {
    /* border-radius: 0.75rem; */
  }
  
  :global(.mapboxgl-canvas-container),
  :global(.mapboxgl-canvas) {
    /* border-radius: 0.75rem; */
  }
  
  :global(.mapboxgl-ctrl-attrib) {
    /* border-top-left-radius: 0.5rem; */
    background-color: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(4px);
    font-family: 'Inter', sans-serif;
    font-size: 11px;
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
  @keyframes pulse {
    0% {
      box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.6);
    }
    70% {
      box-shadow: 0 0 0 100px rgba(37, 99, 235, 0);
    }
    100% {
      box-shadow: 0 0 0 0 rgba(37, 99, 235, 0);
    }
  }
</style>