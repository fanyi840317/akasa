<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import * as Popover from "$lib/components/ui/popover";
  import { MapPin, Locate } from "lucide-svelte";
  import { cn } from "$lib/utils";
  import { createEventDispatcher } from "svelte";
  import MapBase from "./map-base.svelte";
  import type { LocationData, LocationChangeEvent } from '.';

  export let value = "";
  export let placeholder = "选择位置";

  const dispatch = createEventDispatcher<{
    locationChange: LocationChangeEvent;
  }>();

  let addressInput = "";
  let showError = false;
  let isSearching = false;
  let mapComponent: MapBase;
  let locationData: LocationData = {
    longitude: 104.06,
    latitude: 30.67
  };

  // 获取当前位置
  async function getCurrentLocation() {
    if ("geolocation" in navigator) {
      try {
        const position = await new Promise<GeolocationPosition>((resolve, reject) => {
          navigator.geolocation.getCurrentPosition(resolve, reject);
        });
        
        const { latitude, longitude } = position.coords;
        locationData = { longitude, latitude };
        
        // 获取地址信息
        const response = await fetch(
          `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`
        );
        const data = await response.json();
        addressInput = data.display_name;
        updateLocation(data.display_name, longitude, latitude);
      } catch (error) {
        console.error("获取位置失败:", error);
      }
    }
  }

  // 搜索地址
  async function searchAddress() {
    if (!addressInput.trim()) return;
    
    isSearching = true;
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(addressInput)}`
      );
      const data = await response.json();
      
      if (data.length > 0) {
        const { lat, lon, display_name } = data[0];
        locationData = {
          longitude: parseFloat(lon),
          latitude: parseFloat(lat)
        };
        addressInput = display_name;
        updateLocation(display_name, parseFloat(lon), parseFloat(lat));
      }
    } catch (error) {
      console.error("搜索地址失败:", error);
    } finally {
      isSearching = false;
    }
  }

  function handleMapClick(e: { lngLat: { lng: number; lat: number } }) {
    const { lng, lat } = e.lngLat;
    locationData = {
      longitude: lng,
      latitude: lat
    };
    
    // 获取点击位置的地址
    fetch(
      `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`
    )
      .then(response => response.json())
      .then(data => {
        addressInput = data.display_name;
        updateLocation(data.display_name, lng, lat);
      })
      .catch(error => {
        console.error("获取地址失败:", error);
        updateLocation(`${lat.toFixed(6)}, ${lng.toFixed(6)}`, lng, lat);
      });
  }

  function updateLocation(address: string, longitude: number, latitude: number) {
    value = address;
    dispatch("locationChange", { 
      address,
      location: {
        longitude,
        latitude
      }
    });
  }

  let searchTimeout: NodeJS.Timeout;
  function handleAddressInput() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(searchAddress, 500);
  }
</script>

<div class="relative">
  <Popover.Root>
    <Popover.Trigger>
      <Button
        variant="outline"
        class={cn(
          "justify-start text-left font-normal w-full",
          !value && "text-muted-foreground"
        )}
      >
        <MapPin class="mr-2 h-4 w-4" />
        {#if value}
          {value}
        {:else}
          {placeholder}
        {/if}
      </Button>
    </Popover.Trigger>
    <Popover.Content class="w-[400px] p-2" sideOffset={5}>
      <div class="flex gap-2 mb-2">
        <div class="flex-1">
          <Input
            type="text"
            placeholder="搜索地址"
            bind:value={addressInput}
            on:input={() => handleAddressInput()}
          />
        </div>
        <Button
          variant="outline"
          size="icon"
          on:click={() => getCurrentLocation()}
          title="获取当前位置"
        >
          <Locate class="h-4 w-4" />
        </Button>
      </div>
      
      <div class="w-full h-[300px] mb-2 rounded-md overflow-hidden">
        <MapBase
          bind:this={mapComponent}
          bind:locationData
          onClick={handleMapClick}
          zoom={13}
        />
      </div>
    </Popover.Content>
  </Popover.Root>
</div> 