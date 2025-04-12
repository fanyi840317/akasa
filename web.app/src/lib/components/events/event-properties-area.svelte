<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import {
    Clock,
    Calendar as CalendarIcon,
    MapPin,
    Tag,
    FileText,
    Image as ImageIcon,
    User,
    Loader2,
    X,
  } from "lucide-svelte";
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
  import { getLocalTimeZone, parseDate } from "@internationalized/date";
  import type { DateValue } from "@internationalized/date";
  import { DateFormatter } from "@internationalized/date";
  import { formatSystemDate } from "$lib/utils";
  import Separator from "../ui/separator/separator.svelte";
  import type { Location } from "$lib/types/map";
  import { fade, fly, scale } from "svelte/transition";
  import { Card } from "$lib/components/ui/card";
  import { cn } from "$lib/utils";
  import { map } from "leaflet";

  const dispatch = createEventDispatcher();

  const df = new DateFormatter("zh-CN", {
    dateStyle: "long",
  });

  const shortDf = new DateFormatter("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });

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
    eventDate?: DateValue;
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

  // 格式化日期
  function formatDate(date: DateValue | undefined) {
    if (!date) return "未设置发生时间";
    return df.format(date.toDate(getLocalTimeZone()));
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
    if (showFullMap) {
      mapContainer.style =
        +"top: " +
        mapPosition.top +
        "px; left: " +
        mapPosition.left +
        "px; width: " +
        mapPosition.width * 3 +
        "px; height: " +
        mapPosition.height * 3 +
        "px;";
    }
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
              <Select.Content>
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
            <PopoverContent class="w-auto p-0">
              <div class="p-3">
                <Calendar type="single" bind:value={eventDate} />
              </div>
            </PopoverContent>
          </Popover>
        </div>

        <div class="flex flex-col items-end gap-1">
          <div class="flex items-center gap-2">
            <MapPin class="h-3 w-3 text-muted-foreground" />
            <span class="text-xs text-muted-foreground">发生地点</span>
          </div>
          <div
            class="overflow-hidden w-[120px] h-[100px] lg:w-[140px] lg:h-[120px]"
          >
            <div
              bind:this={mapContainer}
              class={cn("rounded-sm h-full"),showFullMap?"bg-muted/40":"")}
              class:absolute={showFullMap}
              class:z-50={showFullMap}
            >
              <div
                class="w-full h-[60%] rounded-t-sm overflow-hidden cursor-pointer"
              >
                <MapBase
                  zoom={6}
                  bind:locationData
                  showUserLocation={true}
                  clickable={false}
                />
              </div>
              <div class="flex flex-col items-end gap-1">
                <button
                  class="flex text-xs p-2 items-center gap-2 w-full justify-start"
                  onclick={() => (showFullMap = true)}
                >
                  {#if isLocation}
                    <Loader2 class="h-3 w-3 animate-spin flex-shrink-0" />
                  {/if}
                  {#if locationData?.address}
                    <span
                      class="text-muted-foreground/90 break-words text-left"
                    >
                      {locationData.address}
                    </span>
                  {:else}
                    <span class="text-muted-foreground/80"
                      >未设置事件发生位置</span
                    >
                  {/if}
                </button>
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
