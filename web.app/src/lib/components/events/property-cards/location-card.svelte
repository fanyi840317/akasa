<script lang="ts">
  import { MapBase } from "$lib/components/map";
  import { cn } from "$lib/utils";
  import type { Location } from "$lib/types/map";
  import { MapPin } from "lucide-svelte";
  import { onMount } from "svelte";

  let { locationData = $bindable(null), className = "" } = $props<{
    locationData: Location | null;
    className?: string;
  }>();

  // 导出 class
  export { className as class };

  // 地图相关
  let mapContainer: HTMLElement;
  let mapPosition = $state({ top: 0, left: 0, width: 0, height: 0 });
  let originalAddress = $state(locationData?.name || "");

  $effect(() => {
    if (locationData) {
      originalAddress = locationData.name || "";
    }
  });

  onMount(() => {
    if (mapContainer) {
      const windowContainer = document.querySelector(".event-creator-window");
      const rect = mapContainer?.getBoundingClientRect();
      if (windowContainer && rect) {
        mapPosition = {
          top: rect.top - windowContainer.getBoundingClientRect().top,
          left: rect.left - windowContainer.getBoundingClientRect().left,
          width: rect.width,
          height: rect.height,
        };
      }
    }
  });
</script>

<div bind:this={mapContainer} class="absolute p-1 pt-16 rounded-lg inset-0 w-full h-full z-0">
  <div class="w-full h-full rounded-lg overflow-hidden">
    <MapBase
      zoom={6}
      bind:locationData
      showUserLocation={true}
      clickable={true}
      showLocateButton={true}
    />
  </div>
</div>
<div class={cn("relative w-full h-full overflow-hidden", className)}>
  <!-- 地图容器 -->

  <!-- 内容层 -->
  <div class="relative h-full flex flex-col rounded-lg overflow-hidden">
    <!-- 标题栏 -->
    <div class="flex items-center justify-between">
      <div class="text-sm font-bold flex items-center text-muted-foreground gap-2">
        <MapPin class="h-4 w-4" />
        <span>地理位置</span>
      </div>
      
    </div>

    <!-- 位置信息 -->
    {#if locationData}
      <div class="mt-24 p-4 bg-card/30 rounded-lg shadow-sm">
        <div class="flex items-center gap-2 mb-1">
          <!-- <MapPin class="h-4 w-4 text-primary flex-shrink-0" /> -->
          <div class="text-sm font-medium text-foreground truncate">
            {locationData.name || "未命名位置"}
          </div>
        </div>

        {#if locationData.description}
          <div class="text-xs text-muted-foreground mb-1">
            {locationData.description}
          </div>
        {/if}

        {#if locationData.coordinates && locationData.coordinates.lat !== undefined && locationData.coordinates.lng !== undefined}
          <div class="flex items-center gap-2">
            <div class="w-4 h-4 flex-shrink-0"></div>
            <div
              class="flex items-center gap-1 text-xs text-foreground font-medium bg-background/50 px-2 py-1 rounded-md"
            >
              <span>{locationData.coordinates.lat.toFixed(4)}</span>
              <span class="text-muted-foreground">|</span>
              <span>{locationData.coordinates.lng.toFixed(4)}</span>
            </div>
          </div>
        {/if}
      </div>
    {:else}
      <div class="flex-1 flex items-center justify-center">
        <div
          class="bg-background/80 backdrop-blur-sm p-4 rounded-lg text-center"
        >
          <p
            class="text-foreground font-medium flex items-center gap-2 justify-center"
          >
            <MapPin class="h-5 w-5 text-primary/80" />
            未设置位置信息
          </p>
          <p class="text-xs text-muted-foreground mt-1">点击地图选择位置</p>
        </div>
      </div>
    {/if}
  </div>
</div>
