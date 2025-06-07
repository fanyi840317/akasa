<script lang="ts">
  import { MapPin } from "lucide-svelte";
  import * as Popover from "$lib/components/ui/popover";
  import type { Location } from "$lib/types/map";

  let {
    location = $bindable<Location | null>(null),
    onLocationChange = (newLocation: Location | null) => {},
    class: className = "",
  } = $props<{
    location?: Location | null;
    onLocationChange?: (newLocation: Location | null) => void;
    class?: string;
  }>();

  let isLocationPopoverOpen = $state(false);
  let locationInputValue = $state("");

  // 更新地点输入值
  $effect(() => {
    locationInputValue = location?.name || "";
  });

  function handleLocationChange(newLoc: Location | null) {
    location = newLoc;
    onLocationChange(newLoc);
    isLocationPopoverOpen = false;
  }

  function handleLocationInputChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const value = target.value.trim();

    if (value) {
      try {
        // 创建新的地点对象，保留现有坐标或使用默认值
        const newLoc: Location = {
          name: value,
          coordinates: {
            lat: location?.latitude || 0,
            lng: location?.longitude || 0,
          },
        };
        handleLocationChange(newLoc);
      } catch (error) {
        console.error("Location processing error:", error);
      }
    } else {
      handleLocationChange(null);
    }
  }

  function handleLocationInputKeydown(event: KeyboardEvent) {
    if (event.key === "Enter") {
      event.preventDefault();
      handleLocationInputChange(event);
    }
  }

  function clearLocation() {
    locationInputValue = "";
    handleLocationChange(null);
  }
</script>

<Popover.Root bind:open={isLocationPopoverOpen}>
  <Popover.Trigger>
    <button
      class="text-sm font-medium hover:bg-base-200 px-2 py-1 rounded transition-colors {className}"
    >
      <MapPin class="w-3 h-3 inline mr-1" />
      {location?.name || "设置地点"}
    </button>
  </Popover.Trigger>
  <Popover.Content class="w-80">
    <div class="space-y-4">
      <h4 class="font-medium">设置活动地点</h4>
      <input
        type="text"
        class="input input-bordered w-full"
        placeholder="输入地点名称"
        value={locationInputValue}
        oninput={(e) => {
          locationInputValue = (e.target as HTMLInputElement).value;
        }}
        onkeydown={handleLocationInputKeydown}
        onblur={handleLocationInputChange}
      />
      <div class="flex gap-2 justify-end">
        <button
          class="btn btn-sm btn-ghost"
          onclick={() => (isLocationPopoverOpen = false)}
        >
          取消
        </button>
        <button class="btn btn-sm btn-primary" onclick={clearLocation}>
          清除
        </button>
        <button
          class="btn btn-sm btn-primary"
          onclick={handleLocationInputChange}
        >
          保存
        </button>
      </div>
    </div>
  </Popover.Content>
</Popover.Root>
