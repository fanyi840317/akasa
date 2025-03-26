<script lang="ts">
  import { Calendar } from "$lib/components/ui/calendar";
  import * as Popover from "$lib/components/ui/popover";
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { CalendarIcon } from "lucide-svelte";
  import { cn } from "$lib/utils";
  import { createEventDispatcher } from "svelte";
  import type { DateValue } from "@internationalized/date";
  import {
    DateFormatter,
    getLocalTimeZone,
    parseDate,
  } from "@internationalized/date";

  export let value: DateValue | undefined = undefined;
  export let placeholder = "选择日期";

  const dispatch = createEventDispatcher();
  
  // 日期格式化
  const df = new DateFormatter("zh-CN", {
    dateStyle: "long",
  });

  // 日期字符串格式化
  const dateStrFormatter = new DateFormatter("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });

  let inputValue = "";
  let showError = false;

  // 当日期通过日历选择时
  function handleCalendarSelect(date: DateValue) {
    value = date;
    if (date) {
      inputValue = dateStrFormatter.format(date.toDate(getLocalTimeZone()));
      showError = false;
    }
    dispatch("dateChange", { date });
  }

  // 当输入框值改变时
  function handleInputChange() {
    try {
      // 尝试解析输入的日期字符串
      const parts = inputValue.split(/[-/.]/);
      if (parts.length === 3) {
        const [year, month, day] = parts.map(p => parseInt(p));
        if (!isNaN(year) && !isNaN(month) && !isNaN(day)) {
          const date = parseDate(`${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`);
          value = date;
          showError = false;
          dispatch("dateChange", { date });
          return;
        }
      }
      showError = true;
    } catch (e) {
      showError = true;
    }
  }
</script>

<div class="relative">
  <Popover.Root>
    <Popover.Trigger>
      <Button
        variant="outline"
        class={cn(
          "justify-start text-left font-normal w-full",
          !value && "text-muted-foreground"
        )}
      >
        <CalendarIcon class="mr-2 h-4 w-4" />
        {#if value}
          {df.format(value.toDate(getLocalTimeZone()))}
        {:else}
          {placeholder}
        {/if}
      </Button>
    </Popover.Trigger>
    <Popover.Content class="w-auto p-0" align="start">
      <Calendar
        type="single"
        bind:selected={value}
        onSelect={handleCalendarSelect}
        initialFocus
      />
    </Popover.Content>
  </Popover.Root>

  <div class="mt-2">
    <Input
      type="text"
      placeholder="YYYY-MM-DD"
      bind:value={inputValue}
      on:blur={handleInputChange}
      class={cn(showError && "border-red-500")}
    />
    {#if showError}
      <p class="text-sm text-red-500 mt-1">请输入有效的日期格式：YYYY-MM-DD</p>
    {/if}
  </div>
</div> 