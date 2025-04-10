<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Clock, Calendar, MapPin, Tag, FileText, Image as ImageIcon } from "lucide-svelte";
  import * as Select from "$lib/components/ui/select";
  import * as Accordion from "$lib/components/ui/accordion";
  import { Popover, PopoverContent, PopoverTrigger } from "$lib/components/ui/popover";
  import { auth } from "$lib/stores/auth";
  import { createEventDispatcher } from "svelte";
  import type { Category } from "$lib/types/category";
  import type { LocationData } from "$lib/components/map";
  import DimensionPicker from "./dimension-picker.svelte";

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
    eventDate = undefined,
    locationData = null,
    selectedCategories = [],
    categories = [],
    evidenceCount = 0,
    timelinePointsCount = 0,
    dimensions = [],
    onDateSelect = (date: Date | undefined) => {},
    onCategorySelect = (value: string) => {},
    onLocationSelect = () => {},
    onDimensionsChange = (dimensions: Dimension[]) => {}
  } = $props<{
    createdAt: string;
    lastModified: string;
    eventDate?: Date;
    locationData: LocationData | null;
    selectedCategories: string[];
    categories: Category[];
    evidenceCount: number;
    timelinePointsCount: number;
    dimensions?: Dimension[];
    onDateSelect?: (date: Date | undefined) => void;
    onCategorySelect?: (value: string) => void;
    onLocationSelect?: () => void;
    onDimensionsChange?: (dimensions: Dimension[]) => void;
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

  // 默认展开事件信息
  let activeAccordion = "event-info";
  
  // 处理维度变化
  function handleDimensionsChange(updatedDimensions: Dimension[]) {
    onDimensionsChange(updatedDimensions);
  }
</script>

<div class="h-[80vh] flex flex-col justify-start">
  <div class="space-y-4 py-16 ">
    <Accordion.Root type="single" value="event-info" class="w-full bg-background px-2 rounded-l-lg" >
   
      <!-- 基本信息 -->
      <Accordion.Item value="basic-info">
        <Accordion.Trigger class="flex flex-col items-end gap-1">
          <span class="text-xs text-muted-foreground">基本信息</span>
        </Accordion.Trigger>
        <Accordion.Content>
          <div class="space-y-2">
            <div class="flex flex-col items-end gap-1">
              <span class="text-xs text-muted-foreground">创建时间</span>
              <Button variant="ghost" class="justify-end gap-2 h-auto py-1 px-2">
                <div class="flex items-center gap-2 text-sm">
                  <Clock class="h-4 w-4 text-muted-foreground" />
                  <span>{formatDate(new Date(createdAt))}</span>
                </div>
              </Button>
            </div>
            <div class="flex flex-col items-end gap-1">
              <span class="text-xs text-muted-foreground">最后修改</span>
              <Button variant="ghost" class="justify-end gap-2 h-auto py-1 px-2">
                <div class="flex items-center gap-2 text-sm">
                  <Clock class="h-4 w-4 text-muted-foreground" />
                  <span>{formatDate(new Date(lastModified))}</span>
                </div>
              </Button>
            </div>
            <div class="flex flex-col items-end gap-1">
              <span class="text-xs text-muted-foreground">创建者</span>
              <Button variant="ghost" class="justify-end gap-2 h-auto py-1 px-2">
                <div class="flex items-center gap-2 text-sm">
                  {#if $auth.user?.prefs?.avatar}
                    <img src={$auth.user.prefs.avatar as string} alt={$auth.user.name} class="h-4 w-4 rounded-full" />
                  {:else}
                    <div class="h-6 w-6 rounded-full bg-primary/10 flex items-center justify-center">
                      <span class="text-[10px] text-primary">{$auth.user?.name?.[0] || "?"}</span>
                    </div>
                  {/if}
                  <span>{$auth.user?.name || "神秘探索者"}</span>
                </div>
              </Button>
            </div>
          </div>
        </Accordion.Content>
      </Accordion.Item>
   <!-- 事件信息 -->
   <Accordion.Item value="event-info">
    <Accordion.Trigger class="flex flex-col items-end gap-1">
      <span class="text-xs text-muted-foreground">事件信息</span>
    </Accordion.Trigger>
    <Accordion.Content>
      <div class="space-y-2">
        <div class="flex flex-col items-end gap-1">
          <span class="text-xs text-muted-foreground">发生时间</span>
          <Popover>
            <PopoverTrigger>
              <Button variant="ghost" class="justify-end gap-2 h-auto py-1 px-2">
                <div class:opacity-50={!eventDate}>
                  <Calendar class="h-4 w-4 text-muted-foreground" />
                </div>
                <span class:opacity-50={!eventDate}>{formatDate(eventDate)}</span>
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
              <Button variant="ghost" class="justify-end gap-2 h-auto py-1 px-2" onclick={onLocationSelect}>
                <div class:opacity-50={!locationData?.address}>
                  <MapPin class="h-4 w-4 text-muted-foreground" />
                </div>
                <span class:opacity-50={!locationData?.address}>{locationData?.address || "未设置"}</span>
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
          <Select.Root type="single" value={selectedCategories.length ? selectedCategories[0] : ""} onValueChange={onCategorySelect}>
            <Select.Trigger class="justify-end gap-2 h-auto py-1 px-2 border-none">
              <div class:opacity-50={!selectedCategories.length}>
                <Tag class="h-4 w-4 text-muted-foreground" />
              </div>
              <span class:opacity-50={!selectedCategories.length}>{selectedCategories.join(",") || "未分类"}</span>
            </Select.Trigger>
            <Select.Content>
              {#each categories as category}
                <Select.Item value={category.$id || ""}>{category.name.zh}</Select.Item>
              {/each}
            </Select.Content>
          </Select.Root>
        </div>
      </div>
    </Accordion.Content>
  </Accordion.Item>

      <!-- 维度信息 -->
      <Accordion.Item value="dimensions">
        <Accordion.Trigger class="flex flex-col items-end gap-1">
          <span class="text-xs text-muted-foreground">维度分析</span>
        </Accordion.Trigger>
        <Accordion.Content>
          <div class="space-y-2">
            <div class="flex flex-col items-end gap-1">
              <DimensionPicker 
                dimensions={dimensions} 
                onDimensionsChange={handleDimensionsChange} 
              />
            </div>
          </div>
        </Accordion.Content>
      </Accordion.Item>

      <!-- 统计信息 -->
      <Accordion.Item value="statistics">
        <Accordion.Trigger class="flex flex-col items-end gap-1">
          <span class="text-xs text-muted-foreground">统计信息</span>
        </Accordion.Trigger>
        <Accordion.Content>
          <div class="space-y-2">
            <div class="flex flex-col items-end gap-1">
              <span class="text-xs text-muted-foreground">字数统计</span>
              <Button variant="ghost" class="justify-end gap-2 h-auto py-1 px-2">
                <div class="flex items-center gap-2 text-sm">
                  <FileText class="h-4 w-4 text-muted-foreground" />
                  <span>{0} 字</span>
                </div>
              </Button>
            </div>
            <div class="flex flex-col items-end gap-1">
              <span class="text-xs text-muted-foreground">证据数量</span>
              <Button variant="ghost" class="justify-end gap-2 h-auto py-1 px-2">
                <div class:opacity-50={evidenceCount === 0}>
                  <ImageIcon class="h-4 w-4 text-muted-foreground" />
                </div>
                <span class:opacity-50={evidenceCount === 0}>{evidenceCount} 个</span>
              </Button>
            </div>
            <div class="flex flex-col items-end gap-1">
              <span class="text-xs text-muted-foreground">时间点数量</span>
              <Button variant="ghost" class="justify-end gap-2 h-auto py-1 px-2">
                <div class:opacity-50={timelinePointsCount === 0}>
                  <Clock class="h-4 w-4 text-muted-foreground" />
                </div>
                <span class:opacity-50={timelinePointsCount === 0}>{timelinePointsCount} 个</span>
              </Button>
            </div>
          </div>
        </Accordion.Content>
      </Accordion.Item>
    </Accordion.Root>
  </div>
</div> 