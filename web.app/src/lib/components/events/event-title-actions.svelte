<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Sparkles, Save, Network, Clock, Lightbulb, Search, Type, FileText } from "lucide-svelte";
  import * as Popover from "$lib/components/ui/popover";

  let {
    onAIGenerate = () => {},
    onSave = () => {},
  } = $props<{
    onAIGenerate?: () => void;
    onSave?: () => void;
  }>();

  const aiActions = [
    { icon: Type, label: "生成标题", action: "title", group: "generate" },
    { icon: FileText, label: "生成内容", action: "content", group: "generate" },
    { icon: Network, label: "提取关系图谱", action: "graph", group: "analyze" },
    { icon: Clock, label: "生成时间线", action: "timeline", group: "analyze" },
    { icon: Lightbulb, label: "生成假设", action: "hypothesis", group: "analyze" },
    { icon: Search, label: "提取线索", action: "clues", group: "analyze" },
  ];

  function handleAIAction(action: string) {
    onAIGenerate({ action });
  }
</script>

<div class="flex items-center gap-2 border-l border-border/40 pl-4">
  <Popover.Root>
    <Popover.Trigger>
      <Button
        variant="ghost"
        size="icon"
        class="h-8 w-8"
      >
        <Sparkles class="h-4 w-4" />
      </Button>
    </Popover.Trigger>
    <Popover.Content class="p-1 w-[200px]" align="start">
      <div class="flex flex-col gap-0.5">
        {#each aiActions.filter(a => a.group === "generate") as action}
          <Button
            variant="ghost"
            class="w-full justify-start gap-1.5 px-2 py-1.5"
            onclick={() => handleAIAction(action.action)}
          >
            <svelte:component this={action.icon} class="h-4 w-4" />
            {action.label}
          </Button>
        {/each}
        <div class="h-px bg-border/40 my-1" />
        {#each aiActions.filter(a => a.group === "analyze") as action}
          <Button
            variant="ghost"
            class="w-full justify-start gap-1.5 px-2 py-1.5"
            onclick={() => handleAIAction(action.action)}
          >
            <svelte:component this={action.icon} class="h-4 w-4" />
            {action.label}
          </Button>
        {/each}
      </div>
    </Popover.Content>
  </Popover.Root>
  <Button variant="ghost" size="icon" class="h-8 w-8" onclick={onSave}>
    <Save class="h-4 w-4" />
  </Button>
</div>