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

  // 日期相关
  let dateValue: DateValue | undefined;
  const df = new DateFormatter("zh-CN", { dateStyle: "long" });

  // 位置数据
  let locationData: LocationData = {
    longitude: 104.06,
    latitude: 30.67,
  };
  let htmlDoc: HtmlDoc = { content: "" };
  // 初始化事件数据
  onMount(async () => {
    const eventId = $page.params.id;
    if (eventId) {
      try {
        await eventStore.fetchEvent(eventId);
      } catch (error) {
        toast.error(
          error instanceof Error ? error.message : "获取事件详情失败",
        );
      }
    }
  });

  // 订阅事件数据变化
  const unsubscribe = eventStore.subscribe((state) => {
    event = state.currentEvent;
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
      if (event.content) {
        htmlDoc.content = event.content;
        // alert(htmlDoc.content)
      }
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
</script>

<ScrollArea class="h-[calc(100vh-4rem)] py-4">
  <div class="space-y-6 flex flex-col h-full mx-auto max-w-4xl">
    <div class="px-24 space-y-4">
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
      <Collapsible.Root class="w-full space-y-2">
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
                    <RangeCalendar
                      type="single"
                      bind:value={dateValue}
                      on:valueChange={(e) => handleDateChange(e.detail)}
                    />
                  </Popover.Content>
                </Popover.Root>
              </div>
            </div>
          </div>
        </Collapsible.Content>
      </Collapsible.Root>

      <!-- 保存按钮 -->
      <div class="flex justify-end mt-4">
        <Button variant="outline" class="gap-2" on:click={handleSave}>
          <Save class="h-4 w-4" />
          保存更改
        </Button>
      </div>
    </div>

    <!-- 描述区域 -->
    <div class="flex-1 flex flex-col">
      <AffineEditor {htmlDoc} class="flex-1" />
    </div>
  </div>
</ScrollArea>

<!-- 地图浮窗 -->
{#if eventData.location}
  <MapFloat
    locationName={eventData.location}
    {locationData}
    showUserLocation={true}
  />
{/if}
