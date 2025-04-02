<script lang="ts">
  import { onMount, afterUpdate, onDestroy } from 'svelte';
  import mapboxgl from 'mapbox-gl';
  import 'mapbox-gl/dist/mapbox-gl.css';
  import { mode } from 'mode-watcher';
  import { get } from 'svelte/store';
  import type { LocationData } from '.';
  import { createEventDispatcher } from 'svelte';
  import { mapStore } from '$lib/stores/map';
  import type { MapMarker } from '$lib/types/map';
  import { EVENT_CATEGORIES } from '$lib/data/event-categories';
  import { PUBLIC_MAPBOX_TOKEN } from '$env/static/public';

  export let locationData: LocationData | undefined = undefined;
  export let zoom = 13;
  export let showUserLocation = true;
  export let onClick: ((e: { lngLat: { lng: number; lat: number } }) => void) | undefined = undefined;

  let container: HTMLDivElement;
  let map: mapboxgl.Map | undefined;
  let resizeObserver: ResizeObserver | undefined;
  let marker: mapboxgl.Marker | undefined;
  let customMarkers: mapboxgl.Marker[] = [];
  let cleanup: (() => void) | undefined;

  const dispatch = createEventDispatcher();

  // 设置 Mapbox token
  mapboxgl.accessToken = PUBLIC_MAPBOX_TOKEN;

  const categories = Object.keys(EVENT_CATEGORIES);

  // 获取随机分类
  function getRandomCategory() {
    const randomIndex = Math.floor(Math.random() * categories.length);
    return EVENT_CATEGORIES[categories[randomIndex]];
  }

  function cleanupMap() {
    if (map) {
      map.remove();
      map = undefined;
    }
    if (resizeObserver) {
      resizeObserver.disconnect();
      resizeObserver = undefined;
    }
    if (marker) {
      marker.remove();
      marker = undefined;
    }
    customMarkers.forEach(m => m.remove());
    customMarkers = [];
  }

  function initMap() {
    if (!container) return;
    
    // 清理现有实例
    cleanupMap();
    
    // 如果没有位置数据，使用默认值
    const defaultLocation = { longitude: 104.06, latitude: 30.67 };
    const currentLocation = locationData || defaultLocation;
    
    console.log('Initializing map with location:', currentLocation);
    
    const newMap = new mapboxgl.Map({
      container,
      style: get(mode) === 'light' ? 'mapbox://styles/mapbox/light-v10' : 'mapbox://styles/mapbox/dark-v11',
      zoom,
      center: [currentLocation.longitude, currentLocation.latitude],
      pitch: 0,
      antialias: true
    });

    map = newMap; // 赋值给外部变量

    // 等待地图加载完成
    newMap.on('load', () => {
      console.log('Map loaded successfully');
      console.log('Current center:', newMap.getCenter());
      console.log('Current zoom:', newMap.getZoom());
      dispatch('mapLoad', { map: newMap });
    });

    // 添加错误处理
    newMap.on('error', (e) => {
      console.error('Map error:', e);
    });

    if (showUserLocation) {
      const userMarkerElement = document.createElement('div');
      userMarkerElement.className = 'user-location-marker';
      marker = new mapboxgl.Marker({
        element: userMarkerElement,
        anchor: 'center'
      })
        .setLngLat([currentLocation.longitude, currentLocation.latitude])
        .addTo(newMap);
      
      console.log('Added user location marker at:', [currentLocation.longitude, currentLocation.latitude]);
    }

    // 监听主题变化
    const unsubscribe = mode.subscribe(currentMode => {
      if (newMap) {
        newMap.setStyle(currentMode === 'light' ? 'mapbox://styles/mapbox/light-v10' : 'mapbox://styles/mapbox/dark-v11');
      }
    });

    // 监听容器大小变化
    resizeObserver = new ResizeObserver(() => {
      if (newMap) newMap.resize();
    });
    
    if (container) {
      resizeObserver.observe(container);
    }

    // 点击事件处理
    newMap.on('click', (e) => {
      console.log('Map clicked at:', e.lngLat);
      if (onClick) {
        onClick(e);
      }
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
          .addTo(newMap);
      }
      // 更新位置数据
      locationData = {
        longitude: e.lngLat.lng,
        latitude: e.lngLat.lat
      };
      dispatch('locationDataChange', locationData);
    });

    // 添加鼠标样式
    newMap.on('mouseenter', () => {
      newMap.getCanvas().style.cursor = 'crosshair';
    });

    newMap.on('mouseleave', () => {
      newMap.getCanvas().style.cursor = '';
    });

    // 监听标记变化
    const unsubscribeMarkers = mapStore.subscribe(markers => {
      if (!newMap) {
        console.log('Map not initialized yet');
        return;
      }
      
      console.log('Received markers:', markers);
      
      // 清除现有标记
      customMarkers.forEach(marker => marker.remove());
      customMarkers = [];

      // 添加新标记
      markers.forEach(markerData => {
        console.log('Processing marker:', markerData);

        const markerElement = document.createElement('div');
        markerElement.className = markerData.className || 'custom-marker';
        markerElement.style.display = 'flex';
        markerElement.style.flexDirection = 'column';
        markerElement.style.alignItems = 'center';
        markerElement.style.position = 'relative';

        // 如果没有分类，随机分配一个
        const randomCategory = getRandomCategory();
        const markerColor = markerData.color || randomCategory.color;

        // 创建标记容器
        const markerContainer = document.createElement('div');
        markerContainer.className = 'marker-container';
        
        // 创建标记点容器
        const dotContainer = document.createElement('div');
        dotContainer.className = 'marker-dot';
        
        // 创建主要标记点
        const mainDot = document.createElement('div');
        mainDot.className = 'main-dot';
        mainDot.style.setProperty('color', markerColor);
        
        // 创建外环
        const outerRing = document.createElement('div');
        outerRing.className = 'outer-ring';
        outerRing.style.setProperty('color', markerColor);
        
        // 创建信息容器
        const infoContainer = document.createElement('div');
        infoContainer.className = 'marker-info';
        infoContainer.style.setProperty('color', markerColor);
        infoContainer.innerHTML = `
          <div class="info-content">
            <span class="info-text">${markerData.data?.title || '未知事件'}</span>
          </div>
        `;

        console.log('Created marker elements with color:', markerColor);

        dotContainer.appendChild(outerRing);
        dotContainer.appendChild(mainDot);
        markerContainer.appendChild(dotContainer);
        markerContainer.appendChild(infoContainer);
        markerElement.appendChild(markerContainer);

        const marker = new mapboxgl.Marker({
          element: markerElement,
          anchor: 'center'
        })
          .setLngLat(markerData.position)
          .addTo(newMap);

        console.log('Added marker to map at position:', markerData.position);

        customMarkers.push(marker);
      });
    });

    return () => {
      cleanupMap();
      unsubscribe();
      unsubscribeMarkers();
    };
  }

  onMount(() => {
    cleanup = initMap();
    return () => {
      if (cleanup) cleanup();
      cleanupMap();
    };
  });

  onDestroy(() => {
    cleanupMap();
    if (cleanup) cleanup();
  });

  afterUpdate(() => {
    if (map) {
      map.resize();
      if (marker) {
        marker.setLngLat([locationData?.longitude || 104.06, locationData?.latitude || 30.67]);
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

  // 添加自定义标记
  export function addMarker({ position, color, size, className, data }: { 
    position: [number, number]; 
    color: string; 
    size: number;
    className?: string;
    data?: any;
  }) {
    if (!map) {
      console.error('Map not initialized');
      return null;
    }

    console.log('Adding marker at position:', position);

    const markerElement = document.createElement('div');
    markerElement.className = className || 'custom-marker';
    markerElement.style.width = `${size}px`;
    markerElement.style.height = `${size}px`;
    markerElement.style.backgroundColor = color;
    markerElement.style.borderRadius = '50%';
    markerElement.style.border = '2px solid white';
    markerElement.style.boxShadow = `0 0 0 2px ${color}40`;
    markerElement.style.cursor = 'pointer';
    markerElement.style.transition = 'all 0.2s ease';
    markerElement.style.zIndex = '1'; // 确保标记在最上层

    const marker = new mapboxgl.Marker({
      element: markerElement,
      anchor: 'center'
    })
      .setLngLat(position)
      .addTo(map);

    // 存储数据
    if (data) {
      markerElement.dataset.eventData = JSON.stringify(data);
    }

    // 添加事件监听器
    markerElement.addEventListener('mouseenter', () => {
      markerElement.style.transform = 'scale(1.2)';
      markerElement.style.boxShadow = `0 0 0 4px ${color}40`;
    });

    markerElement.addEventListener('mouseleave', () => {
      markerElement.style.transform = 'scale(1)';
      markerElement.style.boxShadow = `0 0 0 2px ${color}40`;
    });

    customMarkers.push(marker);
    return marker;
  }

  // 移除所有自定义标记
  export function removeAllMarkers() {
    console.log('Removing all markers');
    customMarkers.forEach(marker => {
      marker.remove();
      console.log('Marker removed');
    });
    customMarkers = [];
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

  @keyframes pulse {
    0%, 100% {
      transform: scale(0.9);
      opacity: 0.8;
    }
    50% {
      transform: scale(1.1);
      opacity: 1;
    }
  }

  :global(.marker-amount) {
    background: rgba(255, 255, 255, 0.95);
    color: #111827;
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    white-space: nowrap;
    letter-spacing: -0.01em;
  }

  :global(.marker-dot) {
    position: relative;
    width: 12px;
    height: 12px;
    margin-top: 24px;
    display: block;
  }

  :global(.main-dot) {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: currentColor;
    box-shadow: 
      0 0 10px currentColor,
      0 0 20px currentColor;
    animation: pulse 2s infinite;
    display: block;
  }

  :global(.outer-ring) {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 200%;
    height: 200%;
    border: 1.5px solid currentColor;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    opacity: 0.3;
    animation: ripple 2s infinite;
    display: block;
  }

  :global(.amount-display) {
    position: absolute;
    top: -4px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(13, 18, 30, 0.95);
    color: currentColor;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: -0.01em;
  }

  :global(.marker-info) {
    position: absolute;
    top: -24px;
    left: 50%;
    transform: translateX(-50%);
    padding: 2px 8px;
    border-radius: 12px;
    white-space: nowrap;
    text-shadow: 
      0 0 8px currentColor;
    opacity: 1;
    pointer-events: none;
    z-index: 2;
    display: block;
  }

  :global(.info-content) {
    color: currentColor;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: block;
  }

  :global(.info-text) {
    font-weight: 500;
    display: block;
  }

  :global(.marker-container) {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    transform-origin: center bottom;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  :global(.custom-marker) {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
  }

  :global(.marker-container:hover) {
    z-index: 10;
  }

  :global(.marker-container:hover .marker-info) {
    transform: translateX(-50%) translateY(-2px);
  }

  @keyframes ripple {
    0% {
      transform: translate(-50%, -50%) scale(0.9);
      opacity: 0.3;
    }
    100% {
      transform: translate(-50%, -50%) scale(1.8);
      opacity: 0;
    }
  }
</style> 