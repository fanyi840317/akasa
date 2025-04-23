<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
  } from "$lib/components/ui/card";
  import { Separator } from "$lib/components/ui/separator";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import {
    Popover,
    PopoverContent,
    PopoverTrigger,
  } from "$lib/components/ui/popover";
  import * as Select from "$lib/components/ui/select";
  import { Calendar } from "$lib/components/ui/calendar";
  import EditableInput from "../ui/editable-input/editable-input.svelte";
  import { MapBase } from "$lib/components/map";
  import { cn } from "$lib/utils";
  import { onMount } from "svelte";
  import {
    DateFormatter,
    getLocalTimeZone,
    parseDate,
  } from "@internationalized/date";
  import type { Category } from "$lib/types/category";
  import type { Location } from "$lib/types/map";
  import {
    Calendar as CalendarIcon,
    MapPin,
    Settings,
    ListFilter,
  } from "lucide-svelte";

  let {
    eventDate = $bindable(undefined),
    locationData = $bindable(null),
    selectedCategories = $bindable([]),
    categories = [],
    isLocation = $bindable(false),
  } = $props<{
    eventDate?: string;
    locationData: Location | null;
    selectedCategories: string[];
    categories: Category[];
    isLocation?: boolean;
  }>();

  // 地图相关
  let showFullMap = $state(false);
  let mapContainer: HTMLElement;
  let mapPosition = $state({ top: 0, left: 0, width: 0, height: 0 });
  let originalAddress = $state(locationData?.name || "");

  // 日期相关
  const df = new DateFormatter("zh-CN", {
    dateStyle: "long",
  });
  let originalDate = $state(toDate(eventDate));

  // 格式化日期
  function formatDate(date: string | undefined) {
    if (!date || date === "") return "未设置发生时间";
    try {
      return df.format(
        parseDate(date.split("T")[0]).toDate(getLocalTimeZone()),
      );
    } catch (error) {
      return date;
    }
  }

  function toDate(date: string | undefined) {
    if (!date) return undefined;
    try {
      return parseDate(date);
    } catch (error) {
      return undefined;
    }
  }

  $effect(() => {
    if (locationData) {
      originalAddress = locationData.name || "";
    }
  });

  $effect(() => {
    if (originalDate) {
      try {
        eventDate = df.format(originalDate.toDate(getLocalTimeZone()));
      } catch (error) {
        console.error("日期解析错误:", error);
      }
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

  $effect(() => {
    if (mapContainer) {
      if (showFullMap) {
        mapContainer.style.position = "absolute";
        mapContainer.style.top = mapPosition.top + "px";
        mapContainer.style.left = mapPosition.left + "px";
        mapContainer.style.zIndex = "50";
        mapContainer.style.overflow = "hidden";

        // 延迟设置最终尺寸
        setTimeout(() => {
          mapContainer.style.width = mapPosition.width * 3 + "px";
          mapContainer.style.height = mapPosition.height * 3 + "px";
        }, 0);
      } else {
        // 恢复初始状态
        setTimeout(() => {
          mapContainer.style.width = mapPosition.width + "px";
          mapContainer.style.height = mapPosition.height + "px";
        }, 0);

        // 等待动画完成后再移除定位
        setTimeout(() => {
          mapContainer.style.position = "";
          mapContainer.style.top = "";
          mapContainer.style.left = "";
          mapContainer.style.zIndex = "";
          mapContainer.style.overflow = "";
        }, 500);
      }
    }
  });
</script>

<Card class="shadow-sm bg-neutral-900">
 
  <CardContent class="p-3 pb-1">
    <div class="space-y-3">
      <!-- 分类 -->
      <div class="flex items-center justify-between">
        <div class="text-xs text-muted-foreground flex items-center gap-1">
          <ListFilter class="h-3 w-3" />
          <span class="text-xs">分类</span>
        </div>
        <div class="px-1">
          <Select.Root type="multiple" bind:value={selectedCategories}>
            <Select.Trigger
              class="justify-end gap-2 h-auto py-1 px-2 border-none"
            >
              <span class:opacity-50={!selectedCategories.length}
                >{selectedCategories.length || "0"}</span
              >
            </Select.Trigger>
            <Select.Content align="start">
              {#each categories as category}
                <Select.Item value={category.$id || ""}
                  >{category.name.zh}</Select.Item
                >
              {/each}
            </Select.Content>
          </Select.Root>
        </div>
      </div>
  
      <!-- 时间 -->
      <div class="flex items-center justify-between">
        <span class="text-xs text-muted-foreground flex items-center gap-1">
          <CalendarIcon class="h-3 w-3" />
          <span>时间</span>
        </span>
        <Popover>
          <PopoverTrigger>
            <Button variant="link" class="justify-end gap-2 h-auto py-1 px-0">
              <span class:opacity-50={!eventDate}>{formatDate(eventDate)}</span>
            </Button>
          </PopoverTrigger>
          <PopoverContent class="flex flex-col w-auto p-0 gap-2" align="start">
            <div
              class="flex items-center gap-2 pt-2 px-2 bg-muted/10 rounded-sm"
            >
              <EditableInput
                value={eventDate}
                placeholder="未设置发生时间"
                class="h-9"
                on:change={(e) => {
                  eventDate = e.detail.value;
                }}
              />
            </div>
            <Separator></Separator>
            <Calendar type="single" bind:value={originalDate} />
          </PopoverContent>
        </Popover>
      </div>
  
      {#if locationData}
      <div class="flex items-center justify-between gap-2 w-full">
        <MapPin class="h-3 w-3 text-muted-foreground" />
        <div
          class="flex-1 min-w-0 justify-start items-start flex flex-col w-full"
        >
          <div
            class="text-xs font-bold text-white break-words truncate w-full"
          >
            {locationData.name || "未命名位置"}
          </div>
          {#if locationData.description}
            <div class="text-xs text-neutral-400 truncate">
              {locationData.description}
            </div>
          {/if}
          {#if locationData.coordinates && locationData.coordinates.lat !== undefined && locationData.coordinates.lng !== undefined}
            <div class="text-xs text-blue-400 mt-1">
              {locationData.coordinates.lat.toFixed(4)}, {locationData.coordinates.lng.toFixed(4)}
            </div>
          {/if}
        </div>
      </div>
    {:else}
      <div class="flex items-start p-1 py-4 gap-2">
        <MapPin class="h-3 w-3" />
        <div class="text-xs text-muted-foreground">未设置位置信息</div>
      </div>
    {/if}
      <!-- 地图卡片 -->
      <div
        role="tooltip"
        bind:this={mapContainer}
        class={cn(
          "rounded-sm bg-card/10 -mx-2 shadow-lg h-[180px] transition-all duration-500 ease-in-out",
          showFullMap
            ? "absolute z-50 bg-card border rounded-lg shadow-md"
            : "",
        )}
      >
  
        <div
          class="w-full h-full rounded-b-sm border-border overflow-hidden cursor-pointer"
        >
          <MapBase
            zoom={6}
            bind:locationData
            showUserLocation={true}
            clickable={showFullMap}
            showLocateButton={showFullMap}
          />
        </div>
  
      </div>
  </CardContent>
</Card>
