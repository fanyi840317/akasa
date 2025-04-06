<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Clock, Calendar, MapPin, Tag, FileText, Image as ImageIcon } from "lucide-svelte";
  import * as Select from "$lib/components/ui/select";
  import { Popover, PopoverContent, PopoverTrigger } from "$lib/components/ui/popover";
  import { auth } from "$lib/stores/auth";
  import { createEventDispatcher } from "svelte";
  import type { Category } from "$lib/types/category";
  import type { LocationData } from "$lib/components/map";

  const dispatch = createEventDispatcher();

  let { 
    createdAt = new Date().toISOString(),
    lastModified = new Date().toISOString(),
    eventDate = undefined,
    locationData = null,
    selectedCategories = [],
    categories = [],
    evidenceCount = 0,
    timelinePointsCount = 0
  } = $props<{
    createdAt: string;
    lastModified: string;
    eventDate?: Date;
    locationData: LocationData | null;
    selectedCategories: string[];
    categories: Category[];
    evidenceCount: number;
    timelinePointsCount: number;
  }>();

  // 格式化日期
  function formatDate(date: Date | undefined) {
    if (!date) return "未设置";
    return date.toLocaleDateString("zh-CN", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    });
  }

  // 处理日期选择
  function handleDateSelect(date: Date | undefined) {
    dispatch("dateSelect", { date });
  }

  // 处理分类选择
  function handleCategorySelect(value: string) {
    if (!value) return;
    dispatch("categorySelect", { value });
  }

  // 处理位置选择
  function handleLocationSelect() {
    dispatch("locationSelect");
  }
</script>

<div class="w-[80px] h-[80vh] flex flex-col justify-start">
  <div class="space-y-4 py-20">
    <!-- 基本信息 -->
    <div class="space-y-2">
      <div class="flex flex-col items-end gap-1">
        <span class="text-xs text-muted-foreground">创建时间</span>
        <Button
          variant="ghost"
          class="w-full justify-end gap-2 h-auto py-2 px-0"
        >
          <div class="flex items-center gap-2 text-sm">
            <Clock class="h-4 w-4 text-muted-foreground" />
            <span>{formatDate(new Date(createdAt))}</span>
          </div>
        </Button>
      </div>
      <div class="flex flex-col items-end gap-1">
        <span class="text-xs text-muted-foreground">最后修改</span>
        <Button
          variant="ghost"
          class="w-full justify-end gap-2 h-auto py-2 px-0"
        >
          <div class="flex items-center gap-2 text-sm">
            <Clock class="h-4 w-4 text-muted-foreground" />
            <span>{formatDate(new Date(lastModified))}</span>
          </div>
        </Button>
      </div>
      <div class="flex flex-col items-end gap-1">
        <span class="text-xs text-muted-foreground">创建者</span>
        <Button
          variant="ghost"
          class="w-full justify-end gap-2 h-auto py-2 px-0"
        >
          <div class="flex items-center gap-2 text-sm">
            {#if $auth.user?.prefs?.avatar}
              <img
                src={$auth.user.prefs.avatar as string}
                alt={$auth.user.name}
                class="h-4 w-4 rounded-full"
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
            <span>{$auth.user?.name || "神秘探索者"}</span>
          </div>
        </Button>
      </div>
    </div>

    <!-- 事件信息 -->
    <div class="space-y-2 py-4">
      <div class="flex flex-col items-end gap-1">
        <span class="text-xs text-muted-foreground">发生时间</span>
        <Popover>
          <PopoverTrigger>
            <Button
              variant="ghost"
              class="w-full justify-end gap-2 h-auto py-2 px-0"
            >
              <div class:opacity-50={!eventDate}>
                <Calendar class="h-4 w-4 text-muted-foreground" />
              </div>
              <span class:opacity-50={!eventDate}
                >{formatDate(eventDate)}</span
              >
            </Button>
          </PopoverTrigger>
          <PopoverContent class="w-auto p-0" align="end">
            <!-- <CalendarPicker
              value={eventDate ? [eventDate] : undefined}
              onValueChange={(dates) => handleDateSelect(dates?.[0])}
              initialFocus
            /> -->
          </PopoverContent>
        </Popover>
      </div>
      <div class="flex flex-col items-end gap-1">
        <span class="text-xs text-muted-foreground">发生地点</span>
        <Popover>
          <PopoverTrigger>
            <Button
              variant="ghost"
              class="w-full justify-end gap-2 h-auto py-2 px-0"
              on:click={handleLocationSelect}
            >
              <div class:opacity-50={!locationData?.address}>
                <MapPin class="h-4 w-4 text-muted-foreground" />
              </div>
              <span class:opacity-50={!locationData?.address}
                >{locationData?.address || "未设置"}</span
              >
            </Button>
          </PopoverTrigger>
          <PopoverContent class="w-[400px] p-0" align="end">
            <div class="w-full h-[300px] bg-muted rounded-lg">
              <!-- 这里可以添加地图组件 -->
              <div class="p-4 text-center text-muted-foreground">
                地图选择器
              </div>
            </div>
          </PopoverContent>
        </Popover>
      </div>
      <div class="flex flex-col items-end gap-1">
        <span class="text-xs text-muted-foreground">事件分类</span>
        <Select.Root
          type="single"
          value={selectedCategories.length ? selectedCategories[0] : ""}
          onValueChange={(value) => handleCategorySelect(value)}
        >
          <Select.Trigger
            class="w-full justify-end gap-2 h-auto py-2 px-0"
          >
            <div class:opacity-50={!selectedCategories.length}>
              <Tag class="h-4 w-4 text-muted-foreground" />
            </div>
            <span class:opacity-50={!selectedCategories.length}
              >{selectedCategories.join(",") || "未分类"}</span
            >
          </Select.Trigger>
          <Select.Content>
            {#each categories as category}
              <Select.Item value={category.$id || ""}>
                {category.name.zh}
              </Select.Item>
            {/each}
          </Select.Content>
        </Select.Root>
      </div>
    </div>

    <!-- 统计信息 -->
    <div class="space-y-2">
      <div class="flex flex-col items-end gap-1">
        <span class="text-xs text-muted-foreground">字数统计</span>
        <Button
          variant="ghost"
          class="w-full justify-end gap-2 h-auto py-2 px-0"
        >
          <div class="flex items-center gap-2 text-sm">
            <FileText class="h-4 w-4 text-muted-foreground" />
            <span>{0} 字</span>
          </div>
        </Button>
      </div>
      <div class="flex flex-col items-end gap-1">
        <span class="text-xs text-muted-foreground">证据数量</span>
        <Button
          variant="ghost"
          class="w-full justify-end gap-2 h-auto py-2 px-0"
        >
          <div class:opacity-50={evidenceCount === 0}>
            <ImageIcon class="h-4 w-4 text-muted-foreground" />
          </div>
          <span class:opacity-50={evidenceCount === 0}
            >{evidenceCount} 个</span
          >
        </Button>
      </div>
      <div class="flex flex-col items-end gap-1">
        <span class="text-xs text-muted-foreground">时间点数量</span>
        <Button
          variant="ghost"
          class="justify-end gap-2 h-auto py-1 px-2"
        >
          <div class:opacity-50={timelinePointsCount === 0}>
            <Clock class="h-4 w-4 text-muted-foreground" />
          </div>
          <span class:opacity-50={timelinePointsCount === 0}
            >{timelinePointsCount} 个</span
          >
        </Button>
      </div>
    </div>
  </div>
</div> 