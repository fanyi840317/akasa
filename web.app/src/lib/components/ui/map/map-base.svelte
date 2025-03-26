<script lang="ts">
  import { onMount, afterUpdate } from 'svelte';
  import mapboxgl from 'mapbox-gl';
  import 'mapbox-gl/dist/mapbox-gl.css';
  import { mode } from 'mode-watcher';
  import { get } from 'svelte/store';
  import type { LocationData } from '.';

  export let locationData: LocationData = {
    longitude: 104.06,
    latitude: 30.67
  };
  export let zoom = 13;
  export let showUserLocation = true;
  export let onClick: ((e: { lngLat: { lng: number; lat: number } }) => void) | undefined = undefined;

  let container: HTMLDivElement;
  let map: mapboxgl.Map;
  let resizeObserver: ResizeObserver;
  let marker: mapboxgl.Marker | undefined;

  mapboxgl.accessToken = 'pk.eyJ1IjoiZmFueWk4NDAzMTciLCJhIjoiY202cDE4OW9wMHZxMzJscTBtbW82NDNxdCJ9.90mwfIpA62nmCY0_C7IkUw';

  function initMap() {
    if (!container) return;
    
    map = new mapboxgl.Map({
      container,
      style: get(mode) === 'light' ? 'mapbox://styles/mapbox/light-v10' : 'mapbox://styles/mapbox/dark-v11',
      zoom,
      center: [locationData.longitude, locationData.latitude],
      pitch: 0,
      antialias: true
    });

    if (showUserLocation) {
      const userMarkerElement = document.createElement('div');
      userMarkerElement.className = 'user-location-marker';
      marker = new mapboxgl.Marker({
        element: userMarkerElement,
        anchor: 'center'
      })
        .setLngLat([locationData.longitude, locationData.latitude])
        .addTo(map);
    }

    // 监听主题变化
    const unsubscribe = mode.subscribe(currentMode => {
      map?.setStyle(currentMode === 'light' ? 'mapbox://styles/mapbox/light-v10' : 'mapbox://styles/mapbox/dark-v11');
    });

    // 监听容器大小变化
    resizeObserver = new ResizeObserver(() => {
      if (map) map.resize();
    });
    
    if (container) {
      resizeObserver.observe(container);
    }

    // 点击事件处理
    if (onClick) {
      map.on('click', (e) => {
        onClick(e);
        if (marker) {
          marker.setLngLat(e.lngLat);
        } else {
          const userMarkerElement = document.createElement('div');
          userMarkerElement.className = 'user-location-marker';
          marker = new mapboxgl.Marker({
            element: userMarkerElement,
            anchor: 'center'
          })
            .setLngLat(e.lngLat)
            .addTo(map);
        }
      });
    }

    return () => {
      if (map) map.remove();
      if (resizeObserver) resizeObserver.disconnect();
      unsubscribe();
    };
  }

  onMount(() => {
    const cleanup = initMap();
    return () => {
      if (cleanup) cleanup();
    };
  });

  afterUpdate(() => {
    if (map) {
      map.resize();
      if (marker) {
        marker.setLngLat([locationData.longitude, locationData.latitude]);
      }
    }
  });

  export function setLocation(lng: number, lat: number) {
    if (map) {
      map.setCenter([lng, lat]);
      if (marker) {
        marker.setLngLat([lng, lat]);
      }
    }
  }

  export function getMap() {
    return map;
  }
</script>

<div bind:this={container} class="map-container">
  <slot />
</div>

<style>
  .map-container {
    width: 100%;
    height: 100%;
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