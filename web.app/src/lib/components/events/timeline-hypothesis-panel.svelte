<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { fade, fly } from "svelte/transition";
  import { Plus, Clock, Lightbulb, X, Calendar, Check } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Textarea } from "$lib/components/ui/textarea";
  import * as Tabs from "$lib/components/ui/tabs";
  import * as Accordion from "$lib/components/ui/accordion";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import { Separator } from "$lib/components/ui/separator";
  import type { TimelineEvent, Hypothesis } from "$lib/types/event";

  const dispatch = createEventDispatcher();

  let {
    timelineEvents = $bindable([]),
    hypotheses = $bindable([]),
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

<div class="h-[80vh] w-[320px] border-l border-border/30 flex flex-col">
  <div class="p-4 border-b border-border/30">
    <h3 class="text-lg font-medium">操作区</h3>
    <p class="text-sm text-muted-foreground">添加时间线和假说</p>
  </div>

  <Tabs.Root value={activeTab} class="flex-1 flex flex-col" onValueChange={(value) => activeTab = value}>
    <Tabs.List class="px-4 pt-2">
      <Tabs.Trigger value="timeline" class="flex items-center gap-2">
        <Clock class="h-4 w-4" />
        时间线
      </Tabs.Trigger>
      <Tabs.Trigger value="hypothesis" class="flex items-center gap-2">
        <Lightbulb class="h-4 w-4" />
        假说
      </Tabs.Trigger>
    </Tabs.List>

    <ScrollArea class="flex-1">
      <Tabs.Content value="timeline" class="p-4 h-full">
        {#if timelineEvents.length > 0}
          <div class="space-y-4 mb-4">
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
                  <p class="text-sm mt-1">{entry.description}</p>
                </div>
              </div>
            {/each}
          </div>
        {:else}
          <div class="flex flex-col items-center justify-center h-[200px] text-center text-muted-foreground">
            <Clock class="h-8 w-8 mb-2 opacity-50" />
            <p>暂无时间线条目</p>
            <p class="text-xs">点击下方按钮添加</p>
          </div>
        {/if}

        {#if isAddingTimeline}
          <div class="space-y-3 border border-border rounded-md p-3 mb-4" in:fade={{ duration: 200 }}>
            <h4 class="text-sm font-medium">添加时间点</h4>
            <div class="space-y-2">
              <div class="flex items-center gap-2">
                <Calendar class="h-4 w-4 text-muted-foreground" />
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
        {/if}

        <Button
          variant={isAddingTimeline ? "secondary" : "outline"}
          class="w-full"
          onclick={() => isAddingTimeline = !isAddingTimeline}
        >
          {#if isAddingTimeline}
            <X class="h-4 w-4 mr-2" />
            取消添加
          {:else}
            <Plus class="h-4 w-4 mr-2" />
            添加时间点
          {/if}
        </Button>
      </Tabs.Content>

      <Tabs.Content value="hypothesis" class="p-4 h-full">
        {#if hypotheses.length > 0}
          <Accordion.Root type="multiple" class="mb-4">
            {#each hypotheses as hypothesis (hypothesis.id)}
              <Accordion.Item value={hypothesis.id} class="group">
                <Accordion.Trigger class="relative">
                  <Button
                    variant="ghost"
                    size="icon"
                    class="absolute right-8 opacity-0 group-hover:opacity-100 transition-opacity h-6 w-6"
                    onclick={() => removeHypothesis(hypothesis.id)}
                  >
                    <X class="h-3 w-3" />
                  </Button>
                  {hypothesis.title}
                </Accordion.Trigger>
                <Accordion.Content>
                  <div class="pb-4 pt-1 text-sm">
                    <p class="text-muted-foreground text-xs mb-2">
                      创建于 {formatDate(hypothesis.createdAt)}
                    </p>
                    <p>{hypothesis.description}</p>
                  </div>
                </Accordion.Content>
              </Accordion.Item>
            {/each}
          </Accordion.Root>
        {:else}
          <div class="flex flex-col items-center justify-center h-[200px] text-center text-muted-foreground">
            <Lightbulb class="h-8 w-8 mb-2 opacity-50" />
            <p>暂无假说</p>
            <p class="text-xs">点击下方按钮添加</p>
          </div>
        {/if}

        {#if isAddingHypothesis}
          <div class="space-y-3 border border-border rounded-md p-3 mb-4" in:fade={{ duration: 200 }}>
            <h4 class="text-sm font-medium">添加假说</h4>
            <div class="space-y-2">
              <Input
                placeholder="假说标题"
                bind:value={newHypothesisTitle}
              />
              <Textarea
                placeholder="详细描述你的假说..."
                bind:value={newHypothesisDescription}
                rows={4}
              />
            </div>
            <div class="flex justify-end gap-2">
              <Button variant="outline" size="sm" onclick={cancelAddHypothesis}>
                取消
              </Button>
              <Button size="sm" onclick={handleAddHypothesis}>
                添加
              </Button>
            </div>
          </div>
        {/if}

        <Button
          variant={isAddingHypothesis ? "secondary" : "outline"}
          class="w-full"
          onclick={() => isAddingHypothesis = !isAddingHypothesis}
        >
          {#if isAddingHypothesis}
            <X class="h-4 w-4 mr-2" />
            取消添加
          {:else}
            <Plus class="h-4 w-4 mr-2" />
            添加假说
          {/if}
        </Button>
      </Tabs.Content>
    </ScrollArea>
  </Tabs.Root>
</div>
