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
  } from "@internationalized/date";
  import { RangeCalendar } from "$lib/components/ui/range-calendar";
  import MapFloat from "$lib/components/console/map-float.svelte";
  import { page } from "$app/stores";
  import { eventStore } from "$lib/stores/event";
  import { toast } from "svelte-sonner";
  import type { Event } from "$lib/types/event";
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";

  // 当前事件数据
  let current_event: Event | null = null;
  let eventTitle = "";
  let eventLocation = "";
  let eventDate = "";
  let eventStatus = "";
  let creator = {
    name: "",
    avatar: "https://github.com/shadcn.png",
  };
  
  let titleInput: HTMLInputElement;
  let dateValue: DateValue | undefined = undefined;

  // 日期格式化器
  const df = new DateFormatter("zh-CN", {
    dateStyle: "long",
  });

  // 自动聚焦函数
  const autofocus = (node: HTMLInputElement) => {
    titleInput = node;
    return {
      destroy: () => {},
    };
  };

  // 处理日期变化
  function handleDateChange(date: DateValue) {
    dateValue = date;
    if (date) {
      const jsDate = date.toDate(getLocalTimeZone());
      eventDate = jsDate.toISOString().split("T")[0]; // 转换为YYYY-MM-DD格式
    } else {
      eventDate = "";
    }
  }

  // 地图位置数据
  let locationCoords = $state({
    longitude: 104.06,
    latitude: 30.67,
  });

  // 在组件挂载时获取事件数据
  onMount(async () => {
    const eventId = $page.params.id;
    if (eventId) {
      try {
        // 获取事件详情
        await eventStore.fetchEvent(eventId);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : '获取事件详情失败';
        toast.error(errorMessage);
      }
    }
  });

  // 订阅事件数据变化
  const unsubscribe = eventStore.subscribe((state) => {
    current_event = state.currentEvent;
    if (current_event) {
      eventTitle = current_event.title || "";
      eventLocation = current_event.location || "";
      eventDate = current_event.date || "";
      eventStatus = current_event.status || "";
      
      // 设置创建者信息
      creator = {
        name: current_event.creator_name || get(auth).user?.name || "",
        avatar: current_event.creator_avatar || "https://github.com/shadcn.png",
      };

      // 如果有日期，转换为DateValue对象
      if (eventDate) {
        try {
          const dateParts = eventDate.split('-');
          if (dateParts.length === 3) {
            const year = parseInt(dateParts[0]);
            const month = parseInt(dateParts[1]);
            const day = parseInt(dateParts[2]);
            // 使用internationalized-date库创建日期对象
            // 注意：月份从1开始，不需要减1
            dateValue = new Date(year, month - 1, day);
          }
        } catch (error) {
          console.error('日期转换错误:', error);
        }
      }
    }
  });

  // 组件销毁时取消订阅
  onDestroy(() => {
    unsubscribe();
  });

  // 保存事件更新
  async function saveEventChanges() {
    if (!current_event?.$id) return;
    
    try {
      await eventStore.updateEvent(current_event.$id, {
        title: eventTitle,
        location: eventLocation,
        date: eventDate,
        status: eventStatus,
        user_id: get(auth).user?.$id || "",
      });
      toast.success("事件已更新");
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : '更新事件失败';
      toast.error(errorMessage);
    }
  }
</script>

<ScrollArea class="h-[calc(100vh-4rem)] py-4">
  <div class="space-y-6 flex flex-col h-full mx-auto max-w-4xl">
    <div class="px-24 space-y-4">
      <!-- 标题区域 -->
      <div class="pt-6 mb-10 space-y-2">
        <input
          type="text"
          placeholder="无标题"
          class="text-4xl font-bold bg-transparent border-none outline-none w-full placeholder:text-muted-foreground/50"
          bind:value={eventTitle}
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
                  <AvatarImage src={creator.avatar} alt={creator.name} />
                  <AvatarFallback>{creator.name[0]}</AvatarFallback>
                </Avatar>
                <span class="text-sm">{creator.name}</span>
              </div>
            </div>

            <!-- 位置输入 -->
            <div class="flex items-center gap-6 w-full">
              <div class="flex items-center gap-2 w-24">
                <MapPin class="h-3 w-3 text-muted-foreground" />
                <span class="text-sm text-muted-foreground">位置</span>
              </div>
              <div class="flex-1">
                <Button
                  variant="ghost"
                  class={cn(
                    " justify-start text-left  font-normal h-9 px-2 py-1",
                    !eventLocation && "text-muted-foreground/70"
                  )}
                  size="sm"
                  onclick={() => {
                    // 如果有位置信息，显示地图浮窗
                    if (eventLocation) {
                      // 这里可以添加显示地图浮窗的逻辑
                    }
                  }}
                >
                  <!-- <MapPin class="h-4 w-4 mr-2" /> -->
                  {eventLocation || "添加位置"}
                </Button>
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
                        " justify-start text-left  font-normal h-9 px-2 py-1",
                        !dateValue && "text-muted-foreground/70"
                      )}
                      size="sm"
                    >
                      <!-- <CalendarIcon class="h-4 w-4 mr-2" /> -->
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
        <Button variant="outline" class="gap-2" on:click={saveEventChanges}>
          <Save class="h-4 w-4" />
          保存更改
        </Button>
      </div>
    </div>

    <!-- 描述区域 -->
    <div class="flex-1 flex flex-col">
      <AffineEditor docId="event-doc" class="flex-1" />
    </div>
  </div>
</ScrollArea>

<!-- 地图浮窗 -->
{#if eventLocation}
  <MapFloat
    locationName={eventLocation}
    locationData={locationCoords}
    showUserLocation={true}
  />
{/if}
