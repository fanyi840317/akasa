<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import mapboxgl from "mapbox-gl";
  import "mapbox-gl/dist/mapbox-gl.css";
  // @ts-ignore 暂时忽略类型检查，后续需要安装 @types/mapbox__mapbox-gl-geocoder
  import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder';
  import '@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css';
  import { mode, userPrefersMode } from "mode-watcher";
  // Removed unused 'get' import
  import type { Location } from "$lib/types/map";
  import { createEventDispatcher } from "svelte";
  import { PUBLIC_MAPBOX_TOKEN } from "$env/static/public";
  import { DEFAULT_LOCATION } from "$lib/types/map";
  import { Locate } from "lucide-svelte";
  import { cn } from "$lib/utils";

  let {
    locationData = $bindable(DEFAULT_LOCATION),
    zoom = 13,
    showUserLocation = true,
    class: className = "",
    onClick = undefined,
    clickable = $bindable(true),
    showLocateButton = $bindable(true),
    showGeocoder = false, // Default to false
  } = $props<{
    locationData?: Location|null;
    zoom?: number;
    showUserLocation?: boolean;
    class?: string;
    onClick?: (e: { lngLat: { lng: number; lat: number } }) => void;
    clickable?: boolean;
    showLocateButton?: boolean;
    showGeocoder?: boolean;
  }>();

  let container: HTMLDivElement;
  let map: mapboxgl.Map | undefined;
  let resizeObserver: ResizeObserver | undefined;
  let marker: mapboxgl.Marker | undefined;
  // Removed redundant 'cleanup' variable
  let isLocating = $state(false);

  // 设置 Mapbox token
  mapboxgl.accessToken = PUBLIC_MAPBOX_TOKEN;

  function cleanupMap() {
    marker?.remove();
    marker = undefined;
    map?.remove();
    map = undefined;
    resizeObserver?.disconnect();
    resizeObserver = undefined;
  }

  function createMarker(lngLat: mapboxgl.LngLatLike) {
    if (marker) {
      marker.setLngLat(lngLat);
    } else {
      const userMarkerElement = document.createElement("div");
      userMarkerElement.className = "user-location-marker";
      marker = new mapboxgl.Marker({
        element: userMarkerElement,
        anchor: "center",
      })
        .setLngLat(lngLat)
        .addTo(map!);
    }
  }

  function initMap() {
    if (!container) return;

    // 清理现有实例
    cleanupMap();

    // 获取初始坐标，优先使用 locationData，其次使用 DEFAULT_LOCATION
    let lng =
      locationData?.coordinates?.lng ?? DEFAULT_LOCATION.coordinates!.lng;
    let lat =
      locationData?.coordinates?.lat ?? DEFAULT_LOCATION.coordinates!.lat;

    // 验证坐标有效性，无效则使用默认值
    if (isNaN(lng) || isNaN(lat)) {
      console.error(
        "Invalid or missing coordinates provided, using default location:",
        { lng, lat }
      );
      lng = DEFAULT_LOCATION.coordinates!.lng;
      lat = DEFAULT_LOCATION.coordinates!.lat;
    }

    console.log("Initializing map with coordinates:", { lng, lat });

    try {
      map = new mapboxgl.Map({
        container,
        attributionControl: false,
        
        style:
          mode.current === "light"
            ? "mapbox://styles/mapbox/light-v10"
            : "mapbox://styles/mapbox/dark-v11",
        zoom,
        center: [lng, lat],
        pitch: 0,
        antialias: true,
      });

      // 等待地图加载完成
      map.on("load", () => {
        console.log("Map loaded successfully");
        console.log("Current center:", map!.getCenter());
        console.log("Current zoom:", map!.getZoom());

        if (showUserLocation) {
          try {
            const center = map!.getCenter();
            createMarker([center.lng, center.lat]);
          } catch (error) {
            console.error(
              "Error creating initial user location marker:",
              error
            );
          }
        }

        if (showGeocoder) {
          map!.addControl(
            new MapboxGeocoder({
              accessToken: mapboxgl.accessToken!,
              mapboxgl: mapboxgl
            })
          );
        }
      });

      // 添加错误处理
      map.on("error", (e) => {
        console.error("Map error:", e);
      });

      // 点击事件处理
      map.on("click", (e) => {
        if (!clickable) return;
        console.log("Map clicked at:", e.lngLat);
        if (onClick) {
          onClick(e);
        }

        map!.setCenter(e.lngLat);
        // 更新位置数据
        locationData = {
          coordinates: {
            lng: e.lngLat.lng,
            lat: e.lngLat.lat,
          },
        };
      });

      // 添加鼠标样式
      map.on("mouseenter", () => {
        if (clickable) map!.getCanvas().style.cursor = "crosshair";
      });

      map.on("mouseleave", () => {
        map!.getCanvas().style.cursor = "";
      });

      // 监听主题变化
      $effect(() => {
        if (userPrefersMode && map) {
          map.setStyle(
            userPrefersMode.current === "light"
              ? "mapbox://styles/mapbox/light-v10"
              : "mapbox://styles/mapbox/dark-v11"
          );
        }
      });

      // 监听容器大小变化
      resizeObserver = new ResizeObserver(() => {
        map?.resize();
      });
      resizeObserver.observe(container);
    } catch (error) {
      console.error("Error initializing map:", error);
      cleanupMap(); // Clean up if initialization failed
    }
  }

  onMount(() => {
    initMap();
    // Simplified cleanup call
    return () => cleanupMap();
  });

  // onDestroy already calls cleanupMap
  onDestroy(cleanupMap);

  export function setLocation(lng: number, lat: number) {
    if (map) {
      map.setCenter([lng, lat]);
      createMarker([lng, lat]);
    }
  }

  export function getMap() {
    return map;
  }

  // 平滑飞行到指定位置
  export function flyTo(lng: number, lat: number, options: any = {}) {
    if (map) {
      map.flyTo({
        center: [lng, lat],
        ...options,
      });
      createMarker([lng, lat]);
    }
  }
</script>

<!-- Removed empty div -->
<div bind:this={container} class={cn("size-full relative", className)}></div>

<style>
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
