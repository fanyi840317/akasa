<script lang="ts">
  import { Calendar } from "$lib/components/ui/calendar";
  import * as Popover from "$lib/components/ui/popover";
  import { Button } from "$lib/components/ui/button";
  import { CalendarIcon } from "lucide-svelte";
  import { cn } from "$lib/utils";
  import { createEventDispatcher } from "svelte";
  import type { DateValue } from "@internationalized/date";
  import Input from "../input/input.svelte";
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

  // 当 value 变化时，更新输入框的值
  $: if (value) {
    inputValue = dateStrFormatter.format(value.toDate(getLocalTimeZone()));
  }

  let showError = false;

  // 当日期通过日历选择时
  function handleCalendarSelect(newValue: DateValue | undefined) {
    if (newValue) {
      value = newValue;
      inputValue = dateStrFormatter.format(newValue.toDate(getLocalTimeZone()));
      showError = false;
      dispatch("dateChange", { date: newValue });
    }
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
          "justify-start text-left font-normal w-full h-7 py-1 px-2",
          !value && "text-muted-foreground"
        )}
      >
        <CalendarIcon class="h-3 w-3" />
        {#if value}
          {df.format(value.toDate(getLocalTimeZone()))}
        {:else}
          {placeholder}
        {/if}
      </Button>
    </Popover.Trigger>
    <Popover.Content class="w-auto p-0" align="start">
      <div class="p-3">
        <Input
          type="text"
          placeholder="YYYY-MM-DD"
          bind:value={inputValue}
          onkeydown={e => e.key === 'Enter' && handleInputChange()}
          class={showError ? "border-red-500" : ""}
        />
        {#if showError}
          <p class="text-sm text-red-500 mb-3">请输入有效的日期格式：YYYY-MM-DD</p>
        {/if}
        <Calendar
          type="single"
          bind:value
          onValueChange={handleCalendarSelect}
          initialFocus
        />
      </div>
    </Popover.Content>
  </Popover.Root>
</div> 