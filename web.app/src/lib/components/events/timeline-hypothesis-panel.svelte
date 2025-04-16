<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { fade, fly } from "svelte/transition";
  import { Plus, Clock, Lightbulb, X, Calendar, Check } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Textarea } from "$lib/components/ui/textarea";
  import * as Tabs from "$lib/components/ui/tabs";
  import * as Accordion from "$lib/components/ui/accordion";
  import * as Popover from "$lib/components/ui/popover";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import { Separator } from "$lib/components/ui/separator";
  import type { TimelineEvent, Hypothesis } from "$lib/types/event";

  const dispatch = createEventDispatcher();

  // 模拟数据
  const mockTimelineEvents: TimelineEvent[] = [
    {
      id: "1",
      timestamp: new Date("2024-01-15T09:30:00"),
      description: "发现可疑人员在案发现场附近徘徊",
      evidenceIds: [],
      witnessIds: []
    },
    {
      id: "2",
      timestamp: new Date("2024-01-15T10:15:00"),
      description: "接到报警电话，报案人称听到可疑声响",
      evidenceIds: [],
      witnessIds: []
    },
    {
      id: "3",
      timestamp: new Date("2024-01-15T11:00:00"),
      description: "警方到达现场开始初步调查",
      evidenceIds: [],
      witnessIds: []
    }
  ];

  const mockHypotheses: Hypothesis[] = [
    {
      id: "1",
      title: "预谋作案假说",
      description: "根据现场痕迹分析，嫌疑人可能提前踩点并精心策划了这起案件。现场未发现明显的强行闯入痕迹，说明嫌疑人对现场环境非常熟悉。",
      evidence: [],
      createdAt: new Date("2024-01-15T14:30:00")
    },
    {
      id: "2",
      title: "内部人员作案假说",
      description: "考虑到案发时间和地点的特殊性，不排除内部人员作案的可能。需要重点调查近期离职或与受害者有矛盾的相关人员。",
      evidence: [],
      createdAt: new Date("2024-01-15T16:45:00")
    }
  ];

  let {
    timelineEvents = mockTimelineEvents,
    hypotheses = $bindable(mockHypotheses),
  } = $props<{
    timelineEvents?: TimelineEvent[];
    hypotheses?: Hypothesis[];
  }>();

  // Active tab state
  let activeTab = $state("timeline");

  // New timeline entry state
  let newTimelineDate = $state("");
  let newTimelineDescription = $state("");
  let isAddingTimeline = $state(false);

  // New hypothesis state
  let newHypothesisTitle = $state("");
  let newHypothesisDescription = $state("");
  let isAddingHypothesis = $state(false);

  // Handle adding a new timeline entry
  function handleAddTimeline() {
    if (newTimelineDate && newTimelineDescription) {
      const newEntry: TimelineEvent = {
        id: crypto.randomUUID(),
        timestamp: new Date(newTimelineDate),
        description: newTimelineDescription,
        evidenceIds: [],
        witnessIds: []
      };

      timelineEvents = [...timelineEvents, newEntry];
      dispatch("timelineChange", { timelineEvents });

      // Reset form
      newTimelineDate = "";
      newTimelineDescription = "";
      isAddingTimeline = false;
    }
  }

  // Handle adding a new hypothesis
  function handleAddHypothesis() {
    if (newHypothesisTitle && newHypothesisDescription) {
      const newHypothesis: Hypothesis = {
        id: crypto.randomUUID(),
        title: newHypothesisTitle,
        description: newHypothesisDescription,
        evidence: [],
        createdAt: new Date()
      };

      hypotheses = [...hypotheses, newHypothesis];
      dispatch("hypothesisChange", { hypotheses });

      // Reset form
      newHypothesisTitle = "";
      newHypothesisDescription = "";
      isAddingHypothesis = false;
    }
  }

  // Format date for display
  function formatDate(date: Date | string | undefined): string {
    if (!date) return "未设置日期";

    const d = typeof date === "string" ? new Date(date) : date;
    return d.toLocaleDateString("zh-CN", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    });
  }

  // Cancel adding timeline
  function cancelAddTimeline() {
    isAddingTimeline = false;
    newTimelineDate = "";
    newTimelineDescription = "";
  }

  // Cancel adding hypothesis
  function cancelAddHypothesis() {
    isAddingHypothesis = false;
    newHypothesisTitle = "";
    newHypothesisDescription = "";
  }

  // Remove timeline entry
  function removeTimelineEntry(id: string) {
    timelineEvents = timelineEvents.filter((entry: TimelineEvent) => entry.id !== id);
    dispatch("timelineChange", { timelineEvents });
  }

  // Remove hypothesis
  function removeHypothesis(id: string) {
    hypotheses = hypotheses.filter((hypo: Hypothesis) => hypo.id !== id);
    dispatch("hypothesisChange", { hypotheses });
  }
</script>

<div class="h-full w-full w-[300px] flex flex-col bg-card py-4 rounded-r-lg py-4 px-2">
  <!-- <div class="p-4 border-b border-border/30">
    <h3 class="text-lg font-medium">操作区</h3>
    <p class="text-sm text-muted-foreground">添加时间线和假说</p>
  </div> -->

      <!-- Add Timeline Entry Button -->
      <Popover.Root>
        <Popover.Trigger>
          <Button variant="outline" class="flex items-center gap-2 text-sm text-muted-foreground">
            <Plus class="h-4 w-4" />
            <span>添加时间点</span>
          </Button>
        </Popover.Trigger>
        <Popover.Content class="w-80">
          <div class="space-y-3">
            <h4 class="text-sm font-medium">添加时间点</h4>
            <div class="space-y-2">
              <div class="flex items-center gap-2">
                <!-- <Calendar class="h-4 w-4 text-muted-foreground" /> -->
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
              <Button size="sm" onclick={handleAddTimeline}>
                添加
              </Button>
            </div>
          </div>
        </Popover.Content>
      </Popover.Root>
  <ScrollArea >
    <div class="space-y-4 my-4">
      {#each timelineEvents.sort((a: TimelineEvent, b: TimelineEvent) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()) as entry (entry.id)}
        <div class="flex gap-4 group" in:fade={{ duration: 200 }}>
          <div class="flex flex-col items-center">
            <div class="w-px h-3 bg-border" />
            <div class="w-2 h-2 rounded-full bg-primary" />
            <div class="flex-1 w-px bg-border" />
          </div>
          <div class="flex-1 pb-4 relative">
            <Button
              variant="ghost"
              size="icon"
              class="absolute right-0 top-0 opacity-0 group-hover:opacity-100 transition-opacity h-6 w-6"
              onclick={() => removeTimelineEntry(entry.id)}
            >
              <X class="h-3 w-3" />
            </Button>
            <p class="text-xs text-muted-foreground">
              {formatDate(entry.timestamp)}
            </p>
            <p class="text-sm mt-1 break-words line-clamp-2">{entry.description}</p>
          </div>
        </div>
      {/each}
    </div>
  </ScrollArea>
</div>
