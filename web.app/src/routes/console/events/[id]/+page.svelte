<script lang="ts">
  import { Separator } from "$lib/components/ui/separator";
  import {
    Avatar,
    AvatarFallback,
    AvatarImage,
  } from "$lib/components/ui/avatar";
  import { Badge } from "$lib/components/ui/badge";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import { Input } from "$lib/components/ui/input";
  import { onMount, onDestroy, setContext } from "svelte";
  import { browser } from "$app/environment";
  import { writable } from "svelte/store";
  import AffineEditor from "$lib/components/ui/editor/affine-editor.svelte";
  import {
    User,
    MapPin,
    Clock,
    Calendar as CalendarIcon,
    ChevronsUpDown,
    Save,
    Send,
  } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";
  import * as Popover from "$lib/components/ui/popover";
  import * as Collapsible from "$lib/components/ui/collapsible";
  import { cn } from "$lib/utils";
  import {
    DateFormatter,
    type DateValue,
    getLocalTimeZone,
    parseDate,
  } from "@internationalized/date";
  import { RangeCalendar } from "$lib/components/ui/range-calendar";
  import MapFloat from "$lib/components/ui/map/map-float.svelte";
  import { page } from "$app/stores";
  import { eventStore } from "$lib/stores/event";
  import { toast } from "svelte-sonner";
  import type { Event } from "$lib/types/event";
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";
  import {
    LocationPicker,
    type LocationData,
    type LocationChangeEvent,
  } from "$lib/components/ui/map";
  import type { Html } from "@blocksuite/blocks";
  import type { HtmlDoc } from "$lib/types/types";
  import { Skeleton } from "$lib/components/ui/skeleton";
  import Header from "$lib/components/layout/header.svelte";
  import type { Snippet } from "svelte";
  import { Calendar } from "$lib/components/ui/calendar";

  // 事件数据
  let event: Event | null = null;
  let eventData = {
    title: "",
    location: "",
    date: "",
    status: "",
    creator: {
      name: "",
      avatar: "https://github.com/shadcn.png",
    },
  };

  // 编辑器数据
  let htmlDoc: HtmlDoc = { content: "" };
  let editorLoaded = $state(false);
  let shouldResetEditor = $state(false);

  // 日期相关
  let dateValue: DateValue | undefined;
  const df = new DateFormatter("zh-CN", { dateStyle: "long" });

  // 位置数据
  let locationData: LocationData = {
    longitude: 104.06,
    latitude: 30.67,
  };

  // 状态管理
  let isLoading = $state(false);
  let isOpen = $state(true); // 默认展开属性面板

  // 面包屑数据
  let titles = [
    { name: "事件", path: "/console/events" },
    { name: eventData.title || "无标题", path: `/console/events/${$page.params.id}` }
  ];

  // 加载事件数据
  async function loadEventData(eventId: string) {
    if (!eventId) return;
    
    try {
      editorLoaded = false;
      shouldResetEditor = true;
      htmlDoc = { content: "" };
      await eventStore.fetchEvent(eventId);
    } catch (error) {
      toast.error(
        error instanceof Error ? error.message : "获取事件详情失败",
      );
    }
  }

  // 监听 URL 变化
  $effect(() => {
    const eventId = $page.params.id;
    if (eventId) {
      loadEventData(eventId);
    }
  });

  // 订阅事件数据变化
  const unsubscribe = eventStore.subscribe((state) => {
    event = state.currentEvent;
    isLoading = state.eventLoading;
    if (event) {
      eventData = {
        title: event.title || "",
        location: event.location || "",
        date: event.date || "",
        status: event.status || "",
        creator: {
          name: event.creator_name || get(auth).user?.name || "",
          avatar: event.creator_avatar || "https://github.com/shadcn.png",
        },
      };

      // 更新编辑器内容
      if (event.content) {
        htmlDoc = { content: event.content };
      }
      
      setTimeout(() => {
        editorLoaded = true;
        shouldResetEditor = false;
      }, 100);

      // 设置日期
      if (eventData.date) {
        try {
          dateValue = parseDate(eventData.date);
        } catch (error) {
          console.error("日期转换错误:", error);
        }
      }

      // 设置位置数据（如果有）
      if (event.location_data) {
        locationData = event.location_data;
      }
    }
  });

  onDestroy(() => {
    unsubscribe();
    clearTimeout(updateTimeout);
    // 清理状态
    eventStore.setCurrentEvent(null);
  });

  // 事件处理函数
  async function handleSave() {
    if (!event?.$id) return;

    try {
      await eventStore.updateEvent(event.$id, {
        title: eventData.title,
        location: eventData.location,
        date: eventData.date,
        status: eventData.status,
        location_data: locationData,
        user_id: get(auth).user?.$id || "",
      });
      toast.success("事件已更新");
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "更新事件失败");
    }
  }

  function handleDateChange(date: DateValue) {
    dateValue = date;
    if (date) {
      eventData.date = date.toString();
    }
  }

  function handleLocationChange(e: CustomEvent<LocationChangeEvent>) {
    const { address, location } = e.detail;
    eventData.location = address;
    locationData = location;
  }

  // 编辑器内容变化处理
  let updateTimeout: NodeJS.Timeout;
  function handleEditorChange(content: string) {
    if (!event?.$id) return;
    
    clearTimeout(updateTimeout);
    updateTimeout = setTimeout(() => {
      try {
        eventStore.updateEvent(event?.$id, {
          ...eventData,
          content,
          location_data: locationData,
          user_id: get(auth).user?.$id || "",
        });
      } catch (error) {
        console.error('更新编辑器内容失败:', error);
      }
    }, 500);
  }

  // 更新面包屑标题
  $effect(() => {
    if (eventData.title) {
      titles = [
        { name: "事件", path: "/console/events" },
        { name: eventData.title, path: `/console/events/${$page.params.id}` }
      ];
    }
  });
</script>

<div class="flex flex-col h-full">
  <Header {titles}>
    <div slot="actions">
      <Button variant="ghost" size="icon" class="gap-2" onclick={handleSave}>
        <Save class="h-4 w-4" />
        <!-- 保存更改 -->
      </Button>
    </div>
  </Header>

  <ScrollArea class="flex-1">
    <div class="flex flex-col h-full mx-auto max-w-4xl">
      <div class="px-24 space-y-4">
        {#if isLoading}
          <!-- 骨架屏 -->
          <div class="space-y-8">
            <!-- 标题骨架 -->
            <div class="pt-6 mb-10">
              <Skeleton class="h-12 w-[70%]" />
            </div>

            <!-- 属性区域骨架 -->
            <div class="space-y-6">
              <div class="flex items-center justify-between">
                <Skeleton class="h-4 w-24" />
                <Skeleton class="h-8 w-8 rounded-md" />
              </div>
              <Separator />
              <div class="space-y-4">
                <!-- 创作者骨架 -->
                <div class="flex items-center gap-6">
                  <Skeleton class="h-4 w-24" />
                  <div class="flex items-center gap-2">
                    <Skeleton class="h-6 w-6 rounded-full" />
                    <Skeleton class="h-4 w-32" />
                  </div>
                </div>
                <!-- 位置骨架 -->
                <div class="flex items-center gap-6">
                  <Skeleton class="h-4 w-24" />
                  <Skeleton class="h-9 w-[200px]" />
                </div>
                <!-- 日期骨架 -->
                <div class="flex items-center gap-6">
                  <Skeleton class="h-4 w-24" />
                  <Skeleton class="h-9 w-[200px]" />
                </div>
              </div>
            </div>
          </div>
        {:else}
          <!-- 标题区域 -->
          <div class="pt-6 mb-10">
            <input
              type="text"
              placeholder="无标题"
              class="text-4xl font-bold bg-transparent border-none outline-none w-full placeholder:text-muted-foreground/50"
              bind:value={eventData.title}
            />
          </div>

          <!-- 属性区域 -->
          <Collapsible.Root bind:open={isOpen} class="w-full space-y-2">
            <div class="flex items-center justify-between space-x-4">
              <h4 class="text-sm text-muted-foreground font-semibold">事件属性</h4>
              <Collapsible.Trigger>
                <Button variant="ghost" size="sm" class="w-9 p-0">
                  <ChevronsUpDown class="h-4 w-4" />
                  <span class="sr-only">切换属性显示</span>
                </Button>
              </Collapsible.Trigger>
            </div>

            <Separator class="my-4" />
            <Collapsible.Content class="space-y-2">
              <div class="flex flex-col gap-2 py-4 w-full">
                <!-- 创作者 -->
                <div class="flex items-center gap-6 w-full">
                  <div class="flex items-center gap-2 w-24">
                    <User class="h-3 w-3 text-muted-foreground" />
                    <span class="text-sm text-muted-foreground">创作者</span>
                  </div>
                  <div class="flex px-2 items-center gap-2 flex-1">
                    <Avatar class="h-4 w-4">
                      <AvatarImage
                        src={eventData.creator.avatar}
                        alt={eventData.creator.name}
                      />
                      <AvatarFallback>{eventData.creator.name[0]}</AvatarFallback>
                    </Avatar>
                    <span class="text-sm">{eventData.creator.name}</span>
                  </div>
                </div>

                <!-- 位置选择器 -->
                <div class="flex items-center gap-6 w-full">
                  <div class="flex items-center gap-2 w-24">
                    <MapPin class="h-3 w-3 text-muted-foreground" />
                    <span class="text-sm text-muted-foreground">位置</span>
                  </div>
                  <div class="flex-1">
                    <LocationPicker
                      value={eventData.location}
                      on:locationChange={handleLocationChange}
                    />
                  </div>
                </div>

                <!-- 日期选择器 -->
                <div class="flex items-center gap-6 w-full">
                  <div class="flex items-center gap-2 w-24">
                    <Clock class="h-3 w-3 text-muted-foreground" />
                    <span class="text-sm text-muted-foreground">日期</span>
                  </div>
                  <div class="flex-1">
                    <Popover.Root>
                      <Popover.Trigger>
                        <Button
                          variant="ghost"
                          class={cn(
                            "justify-start text-left font-normal h-9 px-2 py-1",
                            !dateValue && "text-muted-foreground/70",
                          )}
                          size="sm"
                        >
                          {dateValue
                            ? df.format(dateValue.toDate(getLocalTimeZone()))
                            : "选择日期"}
                        </Button>
                      </Popover.Trigger>
                      <Popover.Content class="w-auto p-0" align="start">
                        <Calendar
                          mode="single"
                          selected={dateValue}
                          onSelect={handleDateChange}
                          initialFocus
                        />
                      </Popover.Content>
                    </Popover.Root>
                  </div>
                </div>
              </div>
            </Collapsible.Content>
          </Collapsible.Root>
        {/if}
      </div>

      <!-- 描述区域 -->
      <div class="flex-1">
        {#if !editorLoaded}
          <div class="flex-1 space-y-4 p-4">
            <Skeleton class="h-6 w-[40%]" />
            <Skeleton class="h-4 w-[60%]" />
            <Skeleton class="h-4 w-[80%]" />
            <Skeleton class="h-4 w-[70%]" />
            <Skeleton class="h-4 w-[50%]" />
            <div class="mt-8">
              <Skeleton class="h-[300px] w-full" />
            </div>
          </div>
        {:else}
          <AffineEditor
            {htmlDoc}
            shouldReset={shouldResetEditor}
            class="flex-1"
            on:contentChange={(e) => handleEditorChange(e.detail)}
          />
        {/if}
      </div>
    </div>
  </ScrollArea>
</div>

<!-- 地图浮窗 -->
{#if eventData.location}
  <MapFloat
    locationName={eventData.location}
    {locationData}
    showUserLocation={true}
  />
{/if}

<style>
  :global(.affine-editor) {
    padding: 0 !important;
  }
</style>
