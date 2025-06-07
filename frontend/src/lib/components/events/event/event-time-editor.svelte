<script lang="ts">
  import { Clock } from "lucide-svelte";
  import * as Popover from "$lib/components/ui/popover";

  let {
    eventTime = $bindable<Date | null>(null),
    onTimeChange = (newTime: Date | null) => {},
    class: className = ""
  } = $props<{
    eventTime?: Date | null;
    onTimeChange?: (newTime: Date | null) => void;
    class?: string;
  }>();

  let isTimePopoverOpen = $state(false);
  let timeInputValue = $state("");

  // 修复时区问题：使用本地时间而不是UTC时间
  function formatDateTimeLocal(date: Date | null): string {
    if (!date) return "";
    try {
      // 创建本地时间的ISO字符串，避免时区转换问题
      const localDate = new Date(date.getTime() - date.getTimezoneOffset() * 60000);
      return localDate.toISOString().slice(0, 16);
    } catch (error) {
      console.error("Date formatting error:", error);
      return "";
    }
  }

  // 格式化显示日期
  function formatDisplayDate(date: Date | null): string {
    if (!date) return "设置时间";
    try {
      return new Date(date).toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch (error) {
      console.error("Date display formatting error:", error);
      return "设置时间";
    }
  }

  // 更新时间输入值
  $effect(() => {
    timeInputValue = formatDateTimeLocal(eventTime);
  });

  function handleTimeChange(newTime: Date | null) {
    eventTime = newTime;
    onTimeChange(newTime);
    isTimePopoverOpen = false;
  }

  function handleTimeInputChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const value = target.value;
    
    if (value) {
      try {
        // 创建本地时间，避免时区问题
        const newTime = new Date(value);
        if (!isNaN(newTime.getTime())) {
          handleTimeChange(newTime);
        }
      } catch (error) {
        console.error("Time parsing error:", error);
      }
    } else {
      handleTimeChange(null);
    }
  }
</script>

<Popover.Root bind:open={isTimePopoverOpen}>
  <Popover.Trigger>
    <button class="text-sm font-medium hover:bg-base-200 px-2 py-1 rounded transition-colors {className}">
      <Clock class="w-3 h-3 inline mr-1" />
      {formatDisplayDate(eventTime)}
    </button>
  </Popover.Trigger>
  <Popover.Content class="w-80">
    <div class="space-y-4">
      <h4 class="font-medium">设置活动时间</h4>
      <input
        type="datetime-local"
        class="input input-bordered w-full"
        value={timeInputValue}
        onchange={handleTimeInputChange}
        oninput={(e) => {
          timeInputValue = (e.target as HTMLInputElement).value;
        }}
      />
      <div class="flex gap-2 justify-end">
        <button class="btn btn-sm btn-ghost" onclick={() => isTimePopoverOpen = false}>
          取消
        </button>
        <button class="btn btn-sm btn-primary" onclick={() => handleTimeChange(null)}>
          清除
        </button>
      </div>
    </div>
  </Popover.Content>
</Popover.Root>