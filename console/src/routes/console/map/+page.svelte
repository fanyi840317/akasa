<script lang="ts">
	import { onMount } from 'svelte';
	import { appStore } from '$lib/stores/app-state';
	import { eventStore } from '$lib/stores/event.svelte';
	import PageHeader from '$lib/components/ui/page-header.svelte';
	import Map from '$lib/components/map/map.svelte';
	import { DEFAULT_LOCATION } from '$lib/constants';
	import type { Event } from '$lib/types/event';

	appStore.setSidebarCollapsed(false);

	let allEvents: Event[] = $state([]);
	let mapComponent: Map;
	let selectedEvent: Event | null = $state(null);

	// 获取所有事件数据
	onMount(async () => {
		try {
			allEvents = await eventStore.getEvents();
			console.log('Loaded events:', allEvents);
			// 等待地图加载完成后添加事件标记
			setTimeout(() => {
				updateEventMarkers();
			}, 1000);
		} catch (error) {
			console.error('Failed to load events:', error);
		}
	});

	// 更新地图上的事件标记
	function updateEventMarkers() {
		if (!mapComponent) return;
		
		const eventMarkersData = allEvents
			.filter(event => event.location_data && typeof event.location_data === 'object')
			.map(event => {
				const locationData = event.location_data as any;
				if (locationData.coordinates) {
					return {
						id: event.$id || '',
						lng: locationData.coordinates.lng,
						lat: locationData.coordinates.lat,
						title: event.name || 'Unnamed Event',
						color: '#3b82f6'
					};
				}
				return null;
			})
			.filter(Boolean) as Array<{id: string, lng: number, lat: number, title: string, color: string}>;
		
		mapComponent.updateEventMarkers(eventMarkersData);
	}

	// 处理地图点击事件
	function handleMapClick(e: { lngLat: { lng: number; lat: number } }) {
		console.log('Map clicked at:', e.lngLat);
		// 可以在这里添加创建新事件的逻辑
	}

	// 飞行到事件位置
	function flyToEvent(event: Event) {
		if (event.location_data && typeof event.location_data === 'object') {
			const locationData = event.location_data as any;
			if (locationData.coordinates) {
				const { lng, lat } = locationData.coordinates;
				mapComponent?.flyTo(lng, lat, { zoom: 15 });
				selectedEvent = event;
			}
		}
	}

	// 监听事件数据变化，自动更新标记
	$effect(() => {
		if (allEvents.length > 0 && mapComponent) {
			updateEventMarkers();
		}
	});
</script>

<div class="h-content bg-base-200 flex flex-col rounded-2xl border overflow-hidden">
	<PageHeader title="Map" description="Visualize and explore your events on the map">
		{#snippet rightContent()}
			<div class="flex items-center gap-2">
				<span class="text-sm text-muted-foreground">
					{allEvents.length} events loaded
				</span>
			</div>
		{/snippet}
	</PageHeader>
	
	<div class="flex-1 flex">
		<!-- 地图区域 -->
		<div class="flex-1 relative">
			<Map 
				bind:this={mapComponent}
				zoom={10}
				showUserLocation={false}
				clickable={true}
				onClick={handleMapClick}
				class="h-full"
			/>
		</div>
		
		<!-- 侧边栏 - 事件列表 -->
		<div class="w-80 bg-background border-l flex flex-col">
			<div class="p-4 border-b">
				<h3 class="font-semibold text-lg">Events</h3>
				<p class="text-sm text-muted-foreground">Click on events to view on map</p>
			</div>
			
			<div class="flex-1 overflow-y-auto">
				{#each allEvents as event}
					<div 
						class="p-4 border-b hover:bg-muted/50 cursor-pointer transition-colors {selectedEvent?.$id === event.$id ? 'bg-muted' : ''}"
						onclick={() => flyToEvent(event)}
					>
						<h4 class="font-medium text-sm mb-1">{event.name || 'Unnamed Event'}</h4>
						{#if event.summary}
							<p class="text-xs text-muted-foreground mb-2 line-clamp-2">{event.summary}</p>
						{/if}
						{#if event.location_data && typeof event.location_data === 'object'}
							{@const locationData = event.location_data as any}
							{#if locationData.address || locationData.name}
								<p class="text-xs text-muted-foreground flex items-center gap-1">
									<svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
									</svg>
									{locationData.address || locationData.name}
								</p>
							{/if}
						{:else}
							<p class="text-xs text-muted-foreground">No location data</p>
						{/if}
						{#if event.date}
							<p class="text-xs text-muted-foreground mt-1">
								{new Date(event.date).toLocaleDateString()}
							</p>
						{/if}
					</div>
				{/each}
				
				{#if allEvents.length === 0}
					<div class="p-8 text-center">
						<p class="text-muted-foreground">No events found</p>
						<p class="text-sm text-muted-foreground mt-1">Create some events to see them on the map</p>
					</div>
				{/if}
			</div>
		</div>
	</div>
</div>
