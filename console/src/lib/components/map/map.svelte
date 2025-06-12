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
	let cleanup: (() => void) | undefined;
	let isLocating = $state(false);

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
				if (onClick) {
					onClick(e);
				}

				map!.setCenter(e.lngLat);
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
</script>

<div bind:this={container} class={cn('size-full relative', className)}></div>
