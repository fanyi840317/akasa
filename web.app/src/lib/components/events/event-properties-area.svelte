<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { PUBLIC_MAPBOX_TOKEN } from "$env/static/public";
  import * as Command from "$lib/components/ui/command";
  import {
    Clock,
    Calendar as CalendarIcon,
    MapPin,
    Tag,
    FileText,
    Image as ImageIcon,
    User,
    X,
    Search,
    Undo2,
    Redo2,
    Pencil,
    Check,
  } from "lucide-svelte";
  import { LoadingCircle } from "$lib/components/icons";
  import * as Select from "$lib/components/ui/select";
  import * as Accordion from "$lib/components/ui/accordion";
  import {
    Popover,
    PopoverContent,
    PopoverTrigger,
  } from "$lib/components/ui/popover";
  import { auth } from "$lib/stores/auth";
  import { createEventDispatcher, onMount } from "svelte";
  import type { Category } from "$lib/types/category";
  import { MapBase } from "$lib/components/map";
  import DimensionPicker from "./dimension-picker.svelte";
  import { Calendar } from "$lib/components/ui/calendar";
  import { fromDate, getLocalTimeZone, parseDate } from "@internationalized/date";
  import type { DateValue } from "@internationalized/date";
  import { DateFormatter } from "@internationalized/date";
  import { formatSystemDate } from "$lib/utils";
  import Separator from "../ui/separator/separator.svelte";
  import type { Location } from "$lib/types/map";
  import { fade, fly, scale } from "svelte/transition";
  import { Card } from "$lib/components/ui/card";
  import { cn } from "$lib/utils";
  import { map } from "leaflet";
  import Input from "../ui/input/input.svelte";
  import EditableInput from "../ui/editable-input/editable-input.svelte";

  const dispatch = createEventDispatcher();

  // 定义维度类型
  type Dimension = {
    title: string;
    questions: string[];
    findings: string[];
    hypotheses: string[];
  };

  let {
    createdAt = new Date().toISOString(),
    lastModified = new Date().toISOString(),
    eventDate = $bindable(undefined),
    locationData = $bindable(null),
    selectedCategories = $bindable([]),
    categories = [],
    evidenceCount = 0,
    timelinePointsCount = 0,
    dimensions = [],
    onCategorySelect = (value: string) => {},
    onLocationSelect = () => {},
    onDimensionsChange = (dimensions: Dimension[]) => {},
    isLocation = $bindable(false),
  } = $props<{
    createdAt: string;
    lastModified: string;
    eventDate?: string;
    locationData: Location | null;
    selectedCategories: string[];
    categories: Category[];
    evidenceCount: number;
    timelinePointsCount: number;
    dimensions?: Dimension[];
    onCategorySelect?: (value: string) => void;
    onLocationSelect?: () => void;
    onDimensionsChange?: (dimensions: Dimension[]) => void;
    isLocation?: boolean;
  }>();

  let showFullMap = $state(false);
  let mapContainer: HTMLElement;
  let mapPosition = $state({ top: 0, left: 0, width: 0, height: 0 });

  let originalAddress = $state(locationData?.address || "");

  const df = new DateFormatter("zh-CN", {
    dateStyle: "long",
  });

  const shortDf = new DateFormatter("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });

  let originalDate = $state(toDate(eventDate));
  // let selectedDate = $state(
  //   eventDate ? formatDate(eventDate).toString() : undefined,
  // );
  
  function toDate(date: string | undefined) {
    if (!date) return undefined;
    try {
      return parseDate(date);
    } catch (error) {
      return undefined
    }
  }  
  function formatDate(date: string | undefined) {
    if (!date|| date==="") return "未设置发生时间";
    try {
      return df.format(parseDate(date.split("T")[0]).toDate(getLocalTimeZone()));
    } catch (error) {
      // console.error("格式化日期时发生错误:", error);
      return date;
    }
  }

  onMount(() => {
    if (mapContainer) {
      const windowContainer = document.querySelector(".event-creator-window");
      const windowRect = windowContainer?.getBoundingClientRect();
      const rect = mapContainer.getBoundingClientRect();
      if (windowRect) {
        mapPosition = {
          top: rect.top - windowRect.top,
          left: rect.left - windowRect.left,
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
    if (originalDate) {
      try {
        // const parsedDate = parseDate(originalDate);
        eventDate = df.format(originalDate.toDate(getLocalTimeZone()));
      } catch (error) {
        console.error("日期解析错误:", error);
      }
    }
    if(locationData){
      originalAddress=locationData.address;
    }
    // if (selectedDate) {
    //   eventDate = formatDate(selectedDate);
    // }
  });
</script>

<div
  class="h-[80vh] py-12 sm:py-8 md:py-14 flex flex-col justify-start w-full min-w-[120px] sm:min-w-[140px] md:min-w-[160px]"
>
  <div class="space-y-4 py-4 bg-background rounded-l-lg">
    <!-- 事件信息 -->
    <div class="w-full bg-background px-2 rounded-l-lg">
      <div class="space-y-4">
        <div class="flex flex-col items-end gap-1">
          <div class="flex items-center gap-2">
            <span class="text-xs text-muted-foreground">事件分类</span>
          </div>
          <div class="px-1">
            <Select.Root type="multiple" bind:value={selectedCategories}>
              <Select.Trigger
                class="justify-end gap-2 h-auto py-1 px-2 border-none"
              >
                <Tag class="h-3 w-3 text-muted-foreground" />
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
        <div class="flex flex-col items-end gap-1">
          <div class="flex items-center gap-2">
            <CalendarIcon class="h-3 w-3 text-muted-foreground" />
            <span class="text-xs text-muted-foreground">发生时间</span>
          </div>
          <Popover>
            <PopoverTrigger>
              <Button variant="link" class="justify-end gap-2 h-auto py-1 px-0">
                <span class:opacity-50={!eventDate}
                  >{formatDate(eventDate)}</span
                >
              </Button>
            </PopoverTrigger>
            <PopoverContent class="w-auto p-0" align="start">
              <div class="p-3">
                <div class="flex items-center gap-2 px-2">
                  <EditableInput
                    value={eventDate}
                    placeholder="未设置发生时间"
                    class="h-9"
                    on:change={(e) => {
                      eventDate = e.detail.value;
                    }}
                  />
                </div>
                <Calendar type="single" bind:value={originalDate} />
              </div>
            </PopoverContent>
          </Popover>
        </div>

        <div class="flex flex-col items-end gap-1">
          <div class="flex items-center gap-2">
            <MapPin class="h-3 w-3 text-muted-foreground" />
            <span class="text-xs text-muted-foreground">发生地点</span>
          </div>
          <div class="overflow-hidden w-[130px] h-[110px]">
            <div
              role="tooltip"
              bind:this={mapContainer}
              class={cn(
                "rounded-sm h-full transition-all border-[0.5px] duration-500 ease-in-out p-1",
                showFullMap
                  ? "absolute z-50 bg-card border rounded-lg shadow-md"
                  : "bg-muted/40",
              )}
              onmouseenter={() => (showFullMap = true)}
              onmouseleave={(e) => {
                // alert(e.relatedTarget);
                // 检查事件目标是否为EditableInput或其子元素
                const target = e.relatedTarget as Element;
                if (target && target.closest('.editable-input')) {
                  return;
                }
                showFullMap = false;
              }}
            >
              <div
                class="w-full h-[60%] rounded-t-sm overflow-hidden cursor-pointer"
              >
                <MapBase
                  zoom={6}
                  bind:locationData
                  showUserLocation={true}
                  clickable={showFullMap}
                  showLocateButton={showFullMap}
                />
              </div>
              <div
                class="flex flex-col items-start gap-1"
                class:p-6={showFullMap}
              >
                {#if showFullMap}
                  <div
                    class="flex-clos items-center gap-2 w-full pointer-events-auto"
                  >
                    <div
                      class="flex py-4 items-center gap-2 w-full justify-start"
                    >
                      {#if isLocation}
                        <LoadingCircle dimensions="h-3 w-3" />
                      {/if}
                      <EditableInput
                        bind:value={originalAddress}
                        placeholder="未设置事件发生位置"
                        class="h-9 editable-input"
                        on:change={(e) => {
                          locationData.address = e.detail.value;
                        }}
                      />
                    </div>
                  </div>
                {:else}
                  <div
                    class={cn(
                      "flex p-2 items-center gap-2 w-full justify-start text-xs",
                    )}
                  >
                    {#if isLocation}
                      <LoadingCircle dimensions="h-3 w-3" />
                    {/if}
                    {#if locationData?.address}
                      <span
                        class="text-muted-foreground/90 break-words line-clamp-2"
                      >
                        {locationData.address}
                      </span>
                    {:else}
                      <span class="text-muted-foreground/80"
                        >未设置事件发生位置</span
                      >
                    {/if}
                  </div>
                {/if}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 基本信息 -->
    <Separator></Separator>
    <div class="w-full px-2">
      <div class="space-y-4">
        <div class="flex flex-col items-end gap-1">
          <div class="flex items-center gap-2">
            <Clock class="h-3 w-3 text-muted-foreground/50" />
            <span class="text-xs text-muted-foreground/50">创建时间</span>
          </div>
          <span class="text-sm text-muted-foreground/50"
            >{formatSystemDate(createdAt)}</span
          >
        </div>
        <div class="flex flex-col items-end gap-1">
          <div class="flex items-center gap-2">
            <Clock class="h-3 w-3 text-muted-foreground/50" />
            <span class="text-xs text-muted-foreground/50">最后修改</span>
          </div>
          <span class="text-sm text-muted-foreground/50"
            >{formatSystemDate(lastModified)}</span
          >
        </div>
        <div class="flex flex-col items-end gap-1">
          <div class="flex items-center gap-2">
            <User class="h-3 w-3 text-muted-foreground/50" />
            <span class="text-xs text-muted-foreground/50">创建者</span>
          </div>
          <div class="flex items-center gap-2 text-sm">
            {#if $auth.user?.prefs?.avatar}
              <img
                src={$auth.user.prefs.avatar as string}
                alt={$auth.user.name}
                class="h-6 w-6 rounded-full"
              />
            {:else}
              <div
                class="h-6 w-6 rounded-full bg-primary/10 flex items-center justify-center"
              >
                <span class="text-[10px] text-primary"
                  >{$auth.user?.name?.[0] || "?"}</span
                >
              </div>
            {/if}
            <span class="text-sm text-muted-foreground/50"
              >{$auth.user?.name || "神秘探索者"}</span
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
