<script lang="ts">
  import { MapBase } from "$lib/components/map";
  import ActionbarCard from "./actionbar-card.svelte";
  import type { Location } from "$lib/types/map";
  import { cn } from "$lib/utils";
  // 这里可以引入地图相关依赖
  // import MapBase from "$lib/components/map/map-base.svelte";
  let {
    class: className = "",
    locationData = $bindable(null),
    ...restProps
  } = $props<{ mapData?: any; class?: string; locationData?: Location }>();
</script>

<ActionbarCard class={cn("border-neutral", className)} {...restProps}>
  <div class="relative w-full h-full">
    <MapBase bind:locationData showUserLocation={false} clickable={false}
    ></MapBase>
    <div class="absolute top-0 right-0 w-full h-full z-1000"></div>
  </div>
  {#snippet rightContent()}
    <div
      class="flex flex-col gap-0 pe-2 text-left text-[0.625rem] text-gray-500 font-semibold"
    >
      <span class="">{locationData?.name || "发生地点"}</span>
      {locationData?.coordinates
        ? `${locationData.coordinates.lng.toFixed(2)}, ${locationData.coordinates.lat.toFixed(2)}`
        : "未设置地点"}
    </div>
  {/snippet}
</ActionbarCard>
