<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Separator } from "$lib/components/ui/separator";
  import {
    Popover,
    PopoverContent,
    PopoverTrigger,
  } from "$lib/components/ui/popover";
  import { Calendar } from "$lib/components/ui/calendar";
  import EditableInput from "../../ui/editable-input/editable-input.svelte";
  import {
    DateFormatter,
    getLocalTimeZone,
    parseDate,
  } from "@internationalized/date";
  import { Calendar as CalendarIcon } from "lucide-svelte";
    import { cn } from "$lib/utils";


  let {
    eventDate = $bindable(undefined),
    className = "",
  } = $props<{
    eventDate?: string;
    className?: string;
  }>();

  // 导出 class
  export { className as class };

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
    if (originalDate) {
      try {
        eventDate = df.format(originalDate.toDate(getLocalTimeZone()));
      } catch (error) {
        console.error("日期解析错误:", error);
      }
    }
  });
</script>

<div class={cn(className)}>
  <div class="flex items-center justify-between mb-3">
    <div class="text-sm font-bold flex items-center text-muted-foreground gap-2">
      <CalendarIcon class="h-4 w-4 " />
      <span>事件时间</span>
    </div>
    <Popover>
      <PopoverTrigger>
        <Button variant="outline" size="sm" class="h-8">
          <span class:opacity-50={!eventDate}>选择日期</span>
        </Button>
      </PopoverTrigger>
      <PopoverContent class="flex flex-col w-auto p-0 gap-2" align="start">
        <div class="flex items-center gap-2 pt-2 px-2 bg-muted/10 rounded-sm">
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

  <div class="flex flex-col items-center justify-center h-[140px]">
    {#if eventDate}
      <div class="text-4xl font-bold text-primary">
        {formatDate(eventDate)}
      </div>
      <div class="text-sm text-muted-foreground mt-2">
        事件发生时间
      </div>
    {:else}
      <div class="text-center text-muted-foreground">
        <CalendarIcon
          class="h-16 w-16 mx-auto mb-2 text-muted-foreground/40"
        />
        <p class="text-foreground font-medium">
          未设置事件时间
        </p>
        <p class="text-xs mt-1">点击右上角的按钮设置时间</p>
      </div>
    {/if}
  </div>
</div>
