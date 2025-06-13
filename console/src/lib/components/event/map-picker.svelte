<script lang="ts">
	import * as Popover from '$lib/components/ui/popover';
	import type { Snippet } from 'svelte';
	import * as Card from '$lib/components/ui/card';
	import Button from '../ui/button/button.svelte';
	import Map from '../map/map.svelte';
	import { Input } from '../ui/input';
	import { MapIcon, MapPinHouse, Loader2 } from '@lucide/svelte';
	import { toast } from 'svelte-sonner';
	import { PUBLIC_MAPBOX_TOKEN } from '$env/static/public';
	import { DEFAULT_LOCATION } from '$lib/constants';
	import Mask from './mask.svelte';

	let {
		value = '',
		onSave,
		isSaving = $bindable(false),
		isOpen = $bindable(false),
		children
	} = $props<{
		value?: string;
		isOpen?: boolean;
		isSaving?: boolean;
		onSave?: (locationData: any) => void;
		children?: Snippet;
	}>();

	// 状态管理
	let isLocating = $state(false);
	let isSearching = $state(false);

	// 地址搜索相关
	let searchInput = $state('');
	let searchResults = $state<any[]>([]);
	let showResults = $state(false);

	// 地图数据
	let locationData = $state(value ? JSON.parse(value) : DEFAULT_LOCATION);
	let mapRef: any;

	// 搜索地址
	async function searchAddress(query: string) {
		if (!query.trim() || query.length < 3) {
			searchResults = [];
			showResults = false;
			return;
		}

		isSearching = true;
		try {
			const response = await fetch(
				`https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(query)}.json?access_token=${PUBLIC_MAPBOX_TOKEN}&limit=5&language=zh`
			);
			const data = await response.json();

			if (data.features) {
				searchResults = data.features;
				showResults = true;
			} else {
				searchResults = [];
				showResults = false;
			}
		} catch (error) {
			console.error('搜索地址失败:', error);
			toast.error('搜索地址失败');
			searchResults = [];
			showResults = false;
		} finally {
			isSearching = false;
		}
	}

	// 选择搜索结果
	function selectSearchResult(feature: any) {
		const [lng, lat] = feature.center;
		locationData = {
			coordinates: { lng, lat },
			address: feature.place_name,
			name: feature.text
		};
		searchInput = feature.place_name;
		showResults = false;

		// 更新地图位置
		if (mapRef) {
			mapRef.flyTo(lng, lat, { zoom: 15 });
		}
	}

	// 获取用户当前位置
	async function getCurrentLocation() {
		if (!navigator.geolocation) {
			toast.error('浏览器不支持定位功能');
			return;
		}

		isLocating = true;
		try {
			const position = await new Promise<GeolocationPosition>((resolve, reject) => {
				navigator.geolocation.getCurrentPosition(resolve, reject, {
					enableHighAccuracy: true,
					timeout: 10000,
					maximumAge: 300000
				});
			});

			const { latitude: lat, longitude: lng } = position.coords;

			// 反向地理编码获取地址
			try {
				const response = await fetch(
					`https://api.mapbox.com/geocoding/v5/mapbox.places/${lng},${lat}.json?access_token=${PUBLIC_MAPBOX_TOKEN}&language=zh`
				);
				const data = await response.json();

				if (data.features && data.features.length > 0) {
					const feature = data.features[0];
					locationData = {
						coordinates: { lng, lat },
						address: feature.place_name,
						name: feature.text
					};
					searchInput = feature.place_name;
				} else {
					locationData = {
						coordinates: { lng, lat },
						address: `${lat.toFixed(6)}, ${lng.toFixed(6)}`,
						name: '当前位置'
					};
					searchInput = locationData.address;
				}
			} catch (error) {
				console.error('反向地理编码失败:', error);
				locationData = {
					coordinates: { lng, lat },
					address: `${lat.toFixed(6)}, ${lng.toFixed(6)}`,
					name: '当前位置'
				};
				searchInput = locationData.address;
			}

			// 更新地图位置
			if (mapRef) {
				mapRef.flyTo(lng, lat, { zoom: 15 });
			}

			toast.success('定位成功');
		} catch (error) {
			console.error('定位失败:', error);
			toast.error('定位失败，请检查定位权限');
		} finally {
			isLocating = false;
		}
	}

	// 地图点击处理
	function handleMapClick(e: { lngLat: { lng: number; lat: number } }) {
		const { lng, lat } = e.lngLat;

		// 反向地理编码获取地址
		fetch(
			`https://api.mapbox.com/geocoding/v5/mapbox.places/${lng},${lat}.json?access_token=${PUBLIC_MAPBOX_TOKEN}&language=zh`
		)
			.then((response) => response.json())
			.then((data) => {
				if (data.features && data.features.length > 0) {
					const feature = data.features[0];
					locationData = {
						coordinates: { lng, lat },
						address: feature.place_name,
						name: feature.text
					};
					searchInput = feature.place_name;
				} else {
					locationData = {
						coordinates: { lng, lat },
						address: `${lat.toFixed(6)}, ${lng.toFixed(6)}`,
						name: '选中位置'
					};
					searchInput = locationData.address;
				}
			})
			.catch((error) => {
				console.error('反向地理编码失败:', error);
				locationData = {
					coordinates: { lng, lat },
					address: `${lat.toFixed(6)}, ${lng.toFixed(6)}`,
					name: '选中位置'
				};
				searchInput = locationData.address;
			});
	}

	// 保存位置数据
	function saveLocationData() {
		const locationString = JSON.stringify(locationData);
		onSave?.(locationString);
	}

	// 取消编辑
	function cancelEdit() {
		isOpen = false;
		// 重置为原始值
		locationData = value ? JSON.parse(value) : DEFAULT_LOCATION;
		searchInput = locationData.address || '';
		showResults = false;
	}

	// 搜索输入处理
	function handleSearchInput(event: Event) {
		const target = event.target as HTMLInputElement;
		searchInput = target.value;
		searchAddress(searchInput);
	}

	// 点击外部关闭搜索结果
	function handleClickOutside() {
		setTimeout(() => {
			showResults = false;
		}, 200);
	}
</script>

<Mask bind:show={isOpen} onCancel={cancelEdit} />
<Popover.Root bind:open={isOpen}>
	<Popover.Trigger class={isOpen ? 'relative z-50' : ''}>
		{@render children()}
	</Popover.Trigger>
	<Popover.Content class="w-[500px] h-[400px] p-0 border-0 bg-transparent z-50" align="start">
		<Card.Root class="w-full h-full pb-0">
			<Card.Header>
				<Card.Title>Event location</Card.Title>
				<Card.Description>Event happens on this location</Card.Description>
				<Card.Action class="gap-2">
					<Button variant="ghost" onclick={getCurrentLocation} disabled={isLocating}>
						{#if isLocating}
							<Loader2 class="size-4 animate-spin" />
						{:else}
							<MapPinHouse class="size-4 text-foreground/50" />
						{/if}
					</Button>
					<Button
						variant="ghost"
						class="text-foreground/50"
						onclick={cancelEdit}
						disabled={isSaving}
					>
						cancel
					</Button>
					<Button variant="secondary" onclick={saveLocationData} disabled={isSaving}>
						{#if isSaving}
							<Loader2 class="size-4 animate-spin mr-2" />
						{/if}
						Save
					</Button>
				</Card.Action>
			</Card.Header>
			<Card.Content>
				<div class="w-full relative">
					<Input
						class="placeholder:text-xs w-full pl-8 relative"
						placeholder="you can select a location or type in an address"
						bind:value={searchInput}
						oninput={handleSearchInput}
						onblur={handleClickOutside}
					/>
					{#if isSearching}
						<Loader2
							class="text-foreground/50 absolute right-2 top-1/2 transform -translate-y-1/2 size-4 animate-spin"
						/>
					{:else}
						<MapIcon
							class="text-foreground/50 absolute left-2 top-1/2 transform -translate-y-1/2 size-4"
						/>
					{/if}

					<!-- 搜索结果下拉列表 -->
					{#if showResults && searchResults.length > 0}
						<div
							class="absolute top-full left-0 right-0 bg-background border border-border rounded-[16px] shadow-lg z-50 max-h-40 overflow-y-auto"
						>
							{#each searchResults as result}
								<button
									class="w-full text-left px-3 py-2 hover:bg-muted text-sm border-b border-border last:border-b-0"
									onclick={() => selectSearchResult(result)}
								>
									<div class="font-medium">{result.text}</div>
									<div class="text-xs text-muted-foreground truncate">{result.place_name}</div>
								</button>
							{/each}
						</div>
					{/if}
				</div>
			</Card.Content>
			<Map
				class="rounded-b-3xl"
				bind:this={mapRef}
				bind:locationData
				onClick={handleMapClick}
				clickable={true}
				showUserLocation={true}
				showLocateButton={false}
			/>
		</Card.Root>
	</Popover.Content>
</Popover.Root>
