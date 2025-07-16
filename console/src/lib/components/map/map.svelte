<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import mapboxgl from 'mapbox-gl';
	import 'mapbox-gl/dist/mapbox-gl.css';
	import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder';
	import { mode } from 'mode-watcher';
	import { get } from 'svelte/store';
	import { PUBLIC_MAPBOX_TOKEN } from '$env/static/public';
	import { DEFAULT_LOCATION } from '$lib/constants';
	import { Button } from '$lib/components/ui/button';
	import { Locate, Loader2Icon } from '@lucide/svelte';
	import { cn } from '$lib/utils';

	let {
		locationData = $bindable(DEFAULT_LOCATION),
		zoom = 13,
		showUserLocation = true,
		class: className = '',
		onClick = undefined,
		clickable = $bindable(true),
		showLocateButton = $bindable(true),
		showGeocoder = false
	} = $props<{
		locationData?: Location;
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
	let eventMarkers: Map<string, mapboxgl.Marker> = new Map();
	let cleanup: (() => void) | undefined;
	let isLocating = $state(false);

	mapboxgl.accessToken = PUBLIC_MAPBOX_TOKEN;

	function cleanupMap() {
		marker?.remove();
		marker = undefined;
		// 清理所有事件标记
		eventMarkers.forEach(marker => marker.remove());
		eventMarkers.clear();
		map?.remove();
		map = undefined;
		resizeObserver?.disconnect();
		resizeObserver = undefined;
	}

	function createMarker(lngLat: mapboxgl.LngLatLike) {
		if (marker) {
			marker.setLngLat(lngLat);
		} else {
			const userMarkerElement = document.createElement('div');
			userMarkerElement.className = 'user-location-marker';
			marker = new mapboxgl.Marker({
				element: userMarkerElement,
				anchor: 'center'
			})
				.setLngLat(lngLat)
				.addTo(map!);
		}
	}

	function initMap() {
		if (!container) return;

		// 清理现有实例
		cleanupMap();

		const lng = locationData.coordinates.lng;
		const lat = locationData.coordinates.lat;
		try {
			map = new mapboxgl.Map({
				container,
				attributionControl: false,

				style:
					mode.current === 'light'
						? 'mapbox://styles/mapbox/light-v10'
						: 'mapbox://styles/mapbox/dark-v11',
				zoom,
				center: [lng, lat],
				pitch: 0,
				antialias: true
			});

			// 等待地图加载完成
			map.on('load', () => {
				console.log('Map loaded successfully');
				console.log('Current center:', map!.getCenter());
				console.log('Current zoom:', map!.getZoom());

				if (showUserLocation) {
					try {
						const center = map!.getCenter();
						createMarker([center.lng, center.lat]);
					} catch (error) {
						console.error('Error creating initial user location marker:', error);
					}
				}

				if (showGeocoder) {
					// map!.addControl(
					// 	new MapboxGeocoder({
					// 		accessToken: mapboxgl.accessToken!,
					// 		mapboxgl: mapboxgl
					// 	})
					// );
				}
			});

			// 添加错误处理
			map.on('error', (e) => {
				console.error('Map error:', e);
			});

			// 点击事件处理
			map.on('click', (e) => {
				if (!clickable) return;
				console.log('Map clicked at:', e.lngLat);
				
				// 立即创建或更新标记
				createMarker([e.lngLat.lng, e.lngLat.lat]);
				
				if (onClick) {
					onClick(e);
				}

				// 更新位置数据
				locationData = {
					coordinates: {
						lng: e.lngLat.lng,
						lat: e.lngLat.lat
					}
				};
			});

			// 添加鼠标样式
			map.on('mouseenter', () => {
				if (clickable) map!.getCanvas().style.cursor = 'crosshair';
			});

			map.on('mouseleave', () => {
				map!.getCanvas().style.cursor = '';
			});

			// 监听主题变化
			// $effect(() => {
			// 	if (userPrefersMode && map) {
			// 		map.setStyle(
			// 			userPrefersMode.current === 'light'
			// 				? 'mapbox://styles/mapbox/light-v10'
			// 				: 'mapbox://styles/mapbox/dark-v11'
			// 		);
			// 	}
			// });

			// 监听容器大小变化
			resizeObserver = new ResizeObserver(() => {
				map?.resize();
			});
			resizeObserver.observe(container);
		} catch (error) {
			console.error('Error initializing map:', error);
			cleanupMap(); // Clean up if initialization failed
		}
	}

	onMount(() => {
		setTimeout(() => {
			initMap();
		}, 100);
		// Simplified cleanup call
		return () => cleanupMap();
	});

	// onDestroy already calls cleanupMap
	onDestroy(cleanupMap);

	// 监听locationData变化，自动更新标记
	$effect(() => {
		if (map && locationData?.coordinates) {
			const { lng, lat } = locationData.coordinates;
			createMarker([lng, lat]);
		}
	});

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
				...options
			});
			createMarker([lng, lat]);
		}
	}

	// 添加事件标记
	export function addEventMarker(eventId: string, lng: number, lat: number, title: string, color: string = '#3b82f6') {
		if (!map) return;
		
		// 如果标记已存在，先移除
		if (eventMarkers.has(eventId)) {
			eventMarkers.get(eventId)?.remove();
		}
		
		// 创建自定义标记元素
		const markerElement = document.createElement('div');
		markerElement.className = 'event-marker';
		markerElement.innerHTML = `
			<div class="event-marker-pin" style="background-color: ${color}; width: 24px; height: 24px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; cursor: pointer;">
				<div style="width: 8px; height: 8px; background-color: white; border-radius: 50%;"></div>
			</div>
		`;
		
		// 创建标记
		const eventMarker = new mapboxgl.Marker({
			element: markerElement,
			anchor: 'center'
		})
			.setLngLat([lng, lat])
			.addTo(map);
		
		// 添加点击事件
		markerElement.addEventListener('click', () => {
			// 创建弹窗
			const popup = new mapboxgl.Popup({ offset: 25 })
				.setLngLat([lng, lat])
				.setHTML(`<div style="padding: 8px; font-size: 14px; font-weight: 500;">${title}</div>`)
				.addTo(map!);
		});
		
		// 存储标记
		eventMarkers.set(eventId, eventMarker);
	}

	// 移除事件标记
	export function removeEventMarker(eventId: string) {
		const marker = eventMarkers.get(eventId);
		if (marker) {
			marker.remove();
			eventMarkers.delete(eventId);
		}
	}

	// 清除所有事件标记
	export function clearEventMarkers() {
		eventMarkers.forEach(marker => marker.remove());
		eventMarkers.clear();
	}

	// 更新事件标记
	export function updateEventMarkers(events: Array<{id: string, lng: number, lat: number, title: string, color?: string}>) {
		if (!map) return;
		
		// 清除现有标记
		clearEventMarkers();
		
		// 添加新标记
		events.forEach(event => {
			addEventMarker(event.id, event.lng, event.lat, event.title, event.color);
		});
	}
</script>

<div bind:this={container} class={cn('size-full relative', className)}></div>
