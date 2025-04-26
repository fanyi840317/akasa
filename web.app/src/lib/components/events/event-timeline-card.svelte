<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
  } from "$lib/components/ui/card";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import {
    Popover,
    PopoverContent,
    PopoverTrigger,
  } from "$lib/components/ui/popover";
  import { Input } from "$lib/components/ui/input";
  import { Textarea } from "$lib/components/ui/textarea";
  import { fade } from "svelte/transition";
  import { createEventDispatcher } from "svelte";
  import type { TimelineEvent } from "$lib/types/timeline";
  import { Layers, Plus, X } from "lucide-svelte";

  const dispatch = createEventDispatcher();

  let {
    timelineEvents = $bindable([]),
  } = $props<{
    timelineEvents: TimelineEvent[];
  }>();

  // 时间线相关
  let newTimelineDate = $state("");
  let newTimelineDescription = $state("");

  // 处理添加时间线条目
  function handleAddTimeline() {
    if (newTimelineDate && newTimelineDescription) {
      const newEntry: TimelineEvent = {
        id: crypto.randomUUID(),
        timestamp: new Date(newTimelineDate),
        description: newTimelineDescription,
        evidenceIds: [],
        witnessIds: [],
      };

      timelineEvents = [...timelineEvents, newEntry];
      dispatch("timelineChange", { timelineEvents });

      // 重置表单
      newTimelineDate = "";
      newTimelineDescription = "";
    }
  }

  // 取消添加时间线
  function cancelAddTimeline() {
    newTimelineDate = "";
    newTimelineDescription = "";
  }

  // 删除时间线条目
  function removeTimelineEntry(id: string) {
    timelineEvents = timelineEvents.filter(
      (entry: TimelineEvent) => entry.id !== id,
    );
    dispatch("timelineChange", { timelineEvents });
  }

  // 格式化时间线日期
  function formatTimelineDate(date: Date | string | undefined): string {
    if (!date) return "未设置日期";

    const d = typeof date === "string" ? new Date(date) : date;
    return d.toLocaleDateString("zh-CN", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }
</script>

<Card class="shadow-sm bg-neutral-900 h-[320px]">
  <CardHeader class="p-3 pb-1">
    <CardTitle class="text-xs font-bold flex items-center justify-between">
      <div class="flex items-center gap-2 font-bold">
        <Layers class="h-3 w-3" />
        <span>时间线</span>
      </div>
      <Popover>
        <PopoverTrigger>
          <Button variant="outline" size="sm" class="h-7 px-2 py-0 gap-0">
            <Plus class="h-3 w-3" />
            <span class="text-xs">添加时间点</span>
          </Button>
        </PopoverTrigger>
        <PopoverContent class="w-80">
          <div class="space-y-3">
            <h4 class="text-sm font-medium">添加时间点</h4>
            <div class="space-y-2">
              <div class="flex items-center gap-2">
                <Input
                  type="datetime-local"
                  placeholder="选择日期和时间"
                  bind:value={newTimelineDate}
                />
              </div>
              <Textarea
                placeholder="描述这个时间点发生了什么..."
                bind:value={newTimelineDescription}
                rows={3}
              />
            </div>
            <div class="flex justify-end gap-2">
              <Button variant="outline" size="sm" onclick={cancelAddTimeline}>
                取消
              </Button>
              <Button size="sm" onclick={handleAddTimeline}>添加</Button>
            </div>
          </div>
        </PopoverContent>
      </Popover>
    </CardTitle>
  </CardHeader>
  <CardContent class="p-3 pt-1">
    <ScrollArea class="h-[260px]">
      <div class="space-y-4 my-2">
        {#each [...timelineEvents].sort((a: TimelineEvent, b: TimelineEvent) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()) as entry (entry.id)}
          <div class="flex gap-3 group" in:fade={{ duration: 200 }}>
            <div class="flex flex-col items-center">
              <div class="w-px h-3 bg-border"></div>
              <div class="w-2 h-2 rounded-full bg-primary"></div>
              <div class="flex-1 w-px bg-border"></div>
            </div>
            <div class="flex-1 pb-3 relative">
              <Button
                variant="ghost"
                size="icon"
                class="absolute right-0 top-0 opacity-0 group-hover:opacity-100 transition-opacity h-5 w-5"
                onclick={() => removeTimelineEntry(entry.id)}
              >
                <X class="h-2 w-2" />
              </Button>
              <p class="text-xs text-muted-foreground">
                {formatTimelineDate(entry.timestamp)}
              </p>
              <p class="text-xs mt-1 break-words line-clamp-2">
                {entry.description}
              </p>
            </div>
          </div>
        {:else}
          <div class="text-xs text-center text-muted-foreground py-4">
            暂无时间线数据
          </div>
        {/each}
      </div>
    </ScrollArea>
  </CardContent>
</Card>
