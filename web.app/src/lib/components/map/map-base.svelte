<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import mapboxgl from "mapbox-gl";
  import "mapbox-gl/dist/mapbox-gl.css";
  import { mode } from "mode-watcher";
  import { get } from "svelte/store";
  import type { Location } from "$lib/types/map";
  import { createEventDispatcher } from "svelte";
  import { PUBLIC_MAPBOX_TOKEN } from "$env/static/public";
  import { DEFAULT_LOCATION } from "$lib/types/map";
  import { Button } from "$lib/components/ui/button";
  import { Locate } from "lucide-svelte";
  import { LoadingCircle } from "$lib/components/icons";

  const dispatch = createEventDispatcher();

  let {
    locationData = $bindable(DEFAULT_LOCATION),
    zoom = 13,
    showUserLocation = true,
    onClick = undefined,
    clickable = $bindable(true),
    showLocateButton = $bindable(true),
  } = $props<{
    locationData?: Location;
    zoom?: number;
    showUserLocation?: boolean;
    onClick?: (e: { lngLat: { lng: number; lat: number } }) => void;
    clickable?: boolean;
    showLocateButton?: boolean;
  }>();

  let container: HTMLDivElement;
  let map: mapboxgl.Map | undefined;
  let resizeObserver: ResizeObserver | undefined;
  let marker: mapboxgl.Marker | undefined;
  let cleanup: (() => void) | undefined;
  let isLocating = $state(false);

  // 设置 Mapbox token
  mapboxgl.accessToken = PUBLIC_MAPBOX_TOKEN;

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
  }

  function initMap() {
    if (!container) return;

    // 清理现有实例
    cleanupMap();

    let newMap;
    try {
      // 如果没有位置数据或坐标数据，使用默认值
      const currentLocation = locationData || DEFAULT_LOCATION;
      // 确保有有效的坐标
      const coordinates = currentLocation.coordinates || DEFAULT_LOCATION.coordinates;
      const lng = coordinates?.lng ?? DEFAULT_LOCATION.coordinates!.lng;
      const lat = coordinates?.lat ?? DEFAULT_LOCATION.coordinates!.lat;

      console.log("Initializing map with location:", { currentLocation, coordinates, lng, lat });

      // 防止无效的经纬度值
      if (isNaN(lng) || isNaN(lat)) {
        console.error("Invalid coordinates:", { lng, lat });
        // 使用北京的坐标作为默认值
        const defaultLng = 116.4074;
        const defaultLat = 39.9042;
        console.log("Using Beijing coordinates:", { lng: defaultLng, lat: defaultLat });

        newMap = new mapboxgl.Map({
          container,
          style: get(mode) === "light" ? "mapbox://styles/mapbox/light-v10" : "mapbox://styles/mapbox/dark-v11",
          zoom,
          center: [defaultLng, defaultLat],
          pitch: 0,
          antialias: true,
        });
      } else {
        newMap = new mapboxgl.Map({
          container,
          style:
            get(mode) === "light"
              ? "mapbox://styles/mapbox/light-v10"
              : "mapbox://styles/mapbox/dark-v11",
          zoom,
          center: [lng, lat],
          pitch: 0,
          antialias: true,
        });
      }
    } catch (error) {
      console.error("Error initializing map:", error);
      // 创建一个带有默认坐标的地图
      const defaultLng = 116.4074;
      const defaultLat = 39.9042;
      newMap = new mapboxgl.Map({
        container,
        style: get(mode) === "light" ? "mapbox://styles/mapbox/light-v10" : "mapbox://styles/mapbox/dark-v11",
        zoom,
        center: [defaultLng, defaultLat],
        pitch: 0,
        antialias: true,
      });
    }

    map = newMap;

    // 等待地图加载完成
    newMap.on("load", () => {
      console.log("Map loaded successfully");
      console.log("Current center:", newMap.getCenter());
      console.log("Current zoom:", newMap.getZoom());
      dispatch("mapLoad", { map: newMap });
    });

    // 添加错误处理
    newMap.on("error", (e) => {
      console.error("Map error:", e);
    });

    if (showUserLocation) {
      try {
        const userMarkerElement = document.createElement("div");
        userMarkerElement.className = "user-location-marker";

        // 获取地图当前中心点的坐标
        const center = newMap.getCenter();
        const markerLng = center.lng;
        const markerLat = center.lat;

        marker = new mapboxgl.Marker({
          element: userMarkerElement,
          anchor: "center",
        })
          .setLngLat([markerLng, markerLat])
          .addTo(newMap);
      } catch (error) {
        console.error("Error creating user location marker:", error);
      }
    }
    // 点击事件处理
    newMap.on("click", (e) => {
      if (!clickable) return;
      console.log("Map clicked at:", e.lngLat);
      if (onClick) {
        onClick(e);
      }
      if (marker) {
        marker.setLngLat(e.lngLat);
      } else {
        const userMarkerElement = document.createElement("div");
        userMarkerElement.className = "user-location-marker";
        marker = new mapboxgl.Marker({
          element: userMarkerElement,
          anchor: "center",
        })
          .setLngLat(e.lngLat)
          .addTo(newMap);
      }
      newMap.setCenter(e.lngLat);
      // 更新位置数据
      locationData = {
        coordinates: {
          lng: e.lngLat.lng,
          lat: e.lngLat.lat
        }
      };
      dispatch("locationDataChange", locationData);
    });

    // 添加鼠标样式
    newMap.on("mouseenter", () => {
      newMap.getCanvas().style.cursor = "crosshair";
    });

    newMap.on("mouseleave", () => {
      newMap.getCanvas().style.cursor = "";
    });
    // 监听主题变化
    const unsubscribe = mode.subscribe((currentMode) => {
      if (newMap) {
        newMap.setStyle(
          currentMode === "light"
            ? "mapbox://styles/mapbox/light-v10"
            : "mapbox://styles/mapbox/dark-v11",
        );
      }
    });

    // 监听容器大小变化
    resizeObserver = new ResizeObserver(() => {
      if (newMap) newMap.resize();
    });

    if (container) {
      resizeObserver.observe(container);
    }

    // 设置清理函数
    cleanup = () => {
      cleanupMap();
      unsubscribe();
    };

    return cleanup;
  }

  onMount(() => {
    initMap();
    return () => {
      if (cleanup) cleanup();
      cleanupMap();
    };
  });

  onDestroy(() => {
    cleanupMap();
    if (cleanup) cleanup();
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

  // 获取用户位置并更新地图
  async function getUserLocation() {
    isLocating = true;
    if (!navigator.geolocation) {
      console.error("浏览器不支持地理位置服务");
      return;
    }

    try {
      const position = await new Promise<GeolocationPosition>((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, {
          enableHighAccuracy: true,
          timeout: 5000,
          maximumAge: 0
        });
      });

      const { latitude, longitude } = position.coords;
      setLocation(longitude, latitude);
      locationData = {
        coordinates: { lat: latitude, lng: longitude }
      };
      dispatch("locationDataChange", locationData);
    } catch (error) {
      console.error("获取位置失败:", error);
    } finally {
      isLocating = false;
    }
  }
</script>

<div bind:this={container} class="map-container">
  {#if showLocateButton}
    <Button
      variant="outline"
      size="icon"
      class="absolute top-2 right-2 z-10"
      onclick={getUserLocation}
      disabled={isLocating}
      title="定位到当前位置"
    >
      {#if isLocating}
        <LoadingCircle />
      {:else}
        <Locate class="h-4 w-4 text-primary/70" />
      {/if}
    </Button>
  {/if}
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
    content: "";
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
