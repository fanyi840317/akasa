<!--
/**
 * @component MapPicker
 * @description 地图位置选择器组件，支持搜索地址、选择位置和获取当前位置
 * 
 * @prop {string} value - 当前选中的地址
 * @prop {string} placeholder - 占位文本
 * @event {CustomEvent<LocationChangeEvent>} locationChange - 位置变更事件
 */
-->
<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import * as Command from "$lib/components/ui/command";
  import * as Popover from "$lib/components/ui/popover";
  import { MapPin, Locate, Check, ChevronsUpDown } from "lucide-svelte";
  import { cn } from "$lib/utils";
  import { createEventDispatcher, tick, onDestroy, onMount } from "svelte";
  import MapBase from "./map-base.svelte";
  import type { LocationData, LocationChangeEvent } from ".";
  import { PUBLIC_MAPBOX_TOKEN } from "$env/static/public";
  import { getCurrentLocation, reverseGeocode, getLocationData } from '$lib/services/location';

  interface Props {
    locationData?: LocationData;
    placeholder?: string;
    isLocating?: boolean;
    autoRequest?: boolean;
    shouldRequest?: boolean;
  }

  let { locationData = $bindable({ longitude: 104.06, latitude: 30.67 }), placeholder = "选择位置", isLocating = false, autoRequest = true, shouldRequest = false } = $props();

  const dispatch = createEventDispatcher<{
    locationChange: LocationChangeEvent;
  }>();

  // 状态管理
  let isError = $state(false);
  let isSearching = $state(false);
  let mapComponent: MapBase;
  let searchResults = $state<
    Array<{ value: string; label: string; lat: number; lon: number }>
  >([
    { value: "成都市", label: "成都市", lat: 30.67, lon: 104.06 },
    {
      value: "成都市天府广场",
      label: "成都市天府广场",
      lat: 30.6578,
      lon: 104.0657,
    },
    {
      value: "成都市春熙路",
      label: "成都市春熙路",
      lat: 30.6543,
      lon: 104.0819,
    },
    {
      value: "成都市锦里古街",
      label: "成都市锦里古街",
      lat: 30.6427,
      lon: 104.0433,
    },
  ]);
  let isOpen = $state(false);
  let triggerRef = $state<HTMLButtonElement>(null!);
  let searchValue = $state("");
  let searchTimeout: number | undefined;
  let currentController: AbortController | null = null;

  // 监听 shouldRequest 变化
  $effect(() => {
    if (shouldRequest && !locationData) {
      handleGetCurrentLocation();
    }
  });

  // 在组件销毁时清理
  onDestroy(() => {
    if (searchTimeout) {
      clearTimeout(searchTimeout);
    }
    if (currentController) {
      currentController.abort();
    }
  });

  // 计算属性
  const selectedValue = $derived(
    locationData ? searchResults.find((r) => r.value === `${locationData.latitude.toFixed(6)}, ${locationData.longitude.toFixed(6)}`)?.label ?? placeholder : placeholder
  );

  // 事件处理函数
  function handleCloseAndFocus() {
    isOpen = false;
    tick().then(() => {
      triggerRef.focus();
    });
  }

  // 防抖处理的搜索函数
  async function debouncedSearch(search: string) {
    if (searchTimeout) {
      clearTimeout(searchTimeout);
    }
    if (currentController) {
      currentController.abort();
    }

    if (!search.trim()) {
      isSearching = false;
      searchResults = [
        { value: "成都市", label: "成都市", lat: 30.67, lon: 104.06 },
        {
          value: "成都市天府广场",
          label: "成都市天府广场",
          lat: 30.6578,
          lon: 104.0657,
        },
        {
          value: "成都市春熙路",
          label: "成都市春熙路",
          lat: 30.6543,
          lon: 104.0819,
        },
        {
          value: "成都市锦里古街",
          label: "成都市锦里古街",
          lat: 30.6427,
          lon: 104.0433,
        },
      ];
      return;
    }

    isSearching = true;
    try {
      currentController = new AbortController();

      // 创建超时控制
      const timeoutId = setTimeout(() => {
        if (currentController) {
          currentController.abort();
        }
      }, 5000); // 5秒超时

      try {
        const response = await fetch(
          `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(search)}.json?access_token=${PUBLIC_MAPBOX_TOKEN}&country=cn&bbox=103.6,30.2,104.5,31.2&language=zh`,
          {
            signal: currentController.signal,
          },
        );

        clearTimeout(timeoutId);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.features && data.features.length > 0) {
          searchResults = data.features.map((item: any) => ({
            value: item.place_name,
            label: item.text,
            lat: item.center[1],
            lon: item.center[0],
          }));
        } else {
          searchResults = [];
        }
      } finally {
        clearTimeout(timeoutId);
      }
    } catch (error: unknown) {
      if (error instanceof Error) {
        if (error.name === "AbortError") {
          console.log("请求已取消或超时");
          searchResults = [
            { value: "成都市", label: "成都市", lat: 30.67, lon: 104.06 },
            {
              value: "成都市天府广场",
              label: "成都市天府广场",
              lat: 30.6578,
              lon: 104.0657,
            },
            {
              value: "成都市春熙路",
              label: "成都市春熙路",
              lat: 30.6543,
              lon: 104.0819,
            },
            {
              value: "成都市锦里古街",
              label: "成都市锦里古街",
              lat: 30.6427,
              lon: 104.0433,
            },
          ];
        } else {
          console.error("搜索地址失败:", error.message);
          isError = true;
          searchResults = [
            { value: "成都市", label: "成都市", lat: 30.67, lon: 104.06 },
            {
              value: "成都市天府广场",
              label: "成都市天府广场",
              lat: 30.6578,
              lon: 104.0657,
            },
            {
              value: "成都市春熙路",
              label: "成都市春熙路",
              lat: 30.6543,
              lon: 104.0819,
            },
            {
              value: "成都市锦里古街",
              label: "成都市锦里古街",
              lat: 30.6427,
              lon: 104.0433,
            },
          ];
        }
      }
    } finally {
      isSearching = false;
      currentController = null;
    }
  }

  function handleSearchInput(e: Event) {
    const input = e.target as HTMLInputElement;
    searchValue = input.value;
    void debouncedSearch(searchValue);
  }

  // 更新处理地图点击的函数
  async function handleMapClick(e: { lngLat: { lng: number; lat: number } }) {
    const { lng, lat } = e.lngLat;
    try {
      const address = await reverseGeocode(lat, lng);
      locationData = { longitude: lng, latitude: lat };
      handleLocationUpdate(address, lng, lat);
      searchResults = [
        {
          value: `${lat.toFixed(6)}, ${lng.toFixed(6)}`,
          label: address.split(",")[0],
          lat: lat,
          lon: lng,
        },
      ];
    } catch (error) {
      console.error("处理点击位置失败:", error);
      // 如果反向地理编码失败，使用坐标作为地址
      const address = `${lat.toFixed(6)}, ${lng.toFixed(6)}`;
      locationData = { longitude: lng, latitude: lat };
      handleLocationUpdate(address, lng, lat);
      searchResults = [
        {
          value: address,
          label: address,
          lat: lat,
          lon: lng,
        },
      ];
    }
  }

  // 更新获取当前位置的函数
  async function handleGetCurrentLocation() {
    try {
      const result = await getCurrentLocation();
      locationData = result.location;
      handleLocationUpdate(result.address, result.location.longitude, result.location.latitude);
      
      if (mapComponent) {
        mapComponent.setLocation(result.location.longitude, result.location.latitude);
      }
    } catch (error) {
      console.error("获取位置失败:", error);
      isError = true;
      locationData = { longitude: 104.06, latitude: 30.67 }; // 设置默认值
    }
  }

  function handleLocationUpdate(
    address: string,
    longitude: number,
    latitude: number,
  ) {
    dispatch("locationChange", {
      address,
      location: {
        longitude,
        latitude,
      },
    });
  }

  function handleSelect(result: {
    value: string;
    label: string;
    lat: number;
    lon: number;
  }) {
    locationData = {
      longitude: result.lon,
      latitude: result.lat,
    };
    if (mapComponent) {
      mapComponent.setLocation(result.lon, result.lat);
    }
    handleLocationUpdate(result.label, result.lon, result.lat);
    handleCloseAndFocus();
  }

  // 初始化位置数据
  onMount(async () => {
    if (!autoRequest) return;
    
    try {
        const data = await getLocationData();
        locationData = data;
    } catch (error) {
        console.error("初始化位置失败:", error);
        locationData = { longitude: 104.06, latitude: 30.67 }; // 设置默认值
    }
  });
</script>

<div class="relative w-full h-full">
  <!-- 地图 -->
  <div class="absolute inset-0 w-full h-full">
    <MapBase
      bind:this={mapComponent}
      {locationData}
      on:locationDataChange={(e) => {
        locationData = e.detail;
        if (locationData) {
          handleLocationUpdate(
            `${locationData.latitude.toFixed(6)}, ${locationData.longitude.toFixed(6)}`,
            locationData.longitude,
            locationData.latitude,
          );
        }
      }}
      onClick={handleMapClick}
      zoom={13}
      showUserLocation={true}
    />
  </div>

  <!-- 控件层 -->
  <!-- 顶部搜索框 -->
    <div class="absolute top-0 left-0 right-0 p-1">
      <div class="flex items-center gap-2">
        <!-- 搜索框 -->
        <div class="flex-1 min-w-0">
          <Popover.Root bind:open={isOpen}>
            <Popover.Trigger bind:ref={triggerRef}>
              {#snippet child({ props })}
                <Button
                  variant="outline"
                  class="h-8 py-1 px-2 "
                  {...props}
                  role="combobox"
                  aria-expanded={isOpen}
                >
                  <MapPin class="h-4 text-primary/70 flex-shrink-0" />
                  <span class="truncate text-primary/70 max-w-[200px]">{selectedValue}</span>
                </Button>
              {/snippet}
            </Popover.Trigger>
            <Popover.Content
              class="w-full p-0 shadow-lg bg-background/95 backdrop-blur-sm"
              align="start"
            >
              <Command.Root>
                <Command.Input
                  placeholder="搜索地址..."
                  class="h-9 search-input"
                  oninput={handleSearchInput}
                />
                <Command.List class="max-h-[300px] overflow-y-auto">
                  {#if isSearching}
                    <div
                      class="py-6 text-sm text-muted-foreground text-center flex items-center justify-center gap-2"
                    >
                      <div
                        class="w-4 h-4 border-2 border-primary/30 border-t-primary rounded-full animate-spin"
                      ></div>
                      <span>搜索中...</span>
                    </div>
                  {:else}
                    <Command.Empty
                      class="py-2 px-2 h-7 text-sm text-muted-foreground text-center"
                      >未找到相关地点</Command.Empty
                    >
                    <Command.Group>
                      {#if !searchResults.length}
                        <div
                          class="py-2 px-2 text-sm text-muted-foreground text-center"
                        >
                          推荐地点
                        </div>
                      {/if}
                      {#each searchResults as result (result.value)}
                        <Command.Item
                          value={result.value}
                          onSelect={() => handleSelect(result)}
                          class="search-result-item"
                        >
                          <Check
                            class={cn(
                              "h-4 w-4 text-primary flex-shrink-0",
                              locationData ? `${locationData.latitude.toFixed(6)}, ${locationData.longitude.toFixed(6)}` !== result.value && "text-transparent" : "text-transparent"
                            )}
                          />
                          <span class="text-sm truncate">{result.label}</span>
                        </Command.Item>
                      {/each}
                    </Command.Group>
                  {/if}
                </Command.List>
              </Command.Root>
            </Popover.Content>
          </Popover.Root>
        </div>
      </div>
    </div>

    <!-- 底部定位按钮 -->
    <div class="absolute bottom-0 right-0 p-1">
      <Button
        variant="outline"
        size="icon"
        class="h-8 w-8 hover:bg-background/50 transition-colors bg-muted backdrop-blur-sm"
        onclick={() => handleGetCurrentLocation()}
        title="获取当前位置"
      >
        <Locate class="h-4 w-4 text-primary/70" />
      </Button>
    </div>
</div>

<style>
  :global(.search-input) {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    background: transparent;
    transition: all 0.2s ease;
  }

  :global(.search-input:hover) {
    background: hsl(var(--accent) / 0.05);
  }

  :global(.search-input:focus) {
    background: hsl(var(--accent) / 0.1);
  }

  :global(.search-result-item) {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.375rem 0.5rem;
    cursor: pointer;
    transition: all 0.2s ease;
    border-bottom: 1px solid hsl(var(--border) / 0.1);
  }

  :global(.search-result-item:last-child) {
    border-bottom: none;
  }

  :global(.search-result-item:hover) {
    background: hsl(var(--accent) / 0.05);
    transform: translateX(2px);
  }

  :global(.search-result-item:active) {
    transform: translateX(0);
  }

  :global(.command-list) {
    scrollbar-width: thin;
    scrollbar-color: hsl(var(--muted)) transparent;
  }

  :global(.command-list::-webkit-scrollbar) {
    width: 6px;
  }

  :global(.command-list::-webkit-scrollbar-track) {
    background: transparent;
  }

  :global(.command-list::-webkit-scrollbar-thumb) {
    background-color: hsl(var(--muted));
    border-radius: 3px;
  }
</style>
