<script lang="ts">
  import { Sparkles } from "lucide-svelte";
  import { fade, scale } from "svelte/transition";

  export let position = { top: 0, left: 0 };
  export let visible = false;
  export let onAction: (action: string) => void = () => {};

  function handleAction(action: string) {
    onAction(action);
  }
</script>

<div
  class="fixed bg-white dark:bg-neutral-800 border border-neutral-200/50 dark:border-neutral-700/50 rounded-lg shadow-lg p-2 flex flex-col gap-2 z-50"
  style="top: {position.top}px; left: {position.left}px;"
  in:scale={{
    duration: 150,
    start: 0.95,
    opacity: 0,
  }}
  out:fade={{ duration: 100 }}
>
  <div class="flex items-center gap-1.5">
    <Sparkles class="h-3 w-3 stroke-[2.5] text-primary" />
    <p class="text-xs font-medium">AI 写作助手</p>
  </div>
  <p class="text-xs text-muted-foreground leading-5 px-0.5">
    让我帮你优化内容...
  </p>
  <div class="flex gap-2">
    <button
      class="text-xs px-2 py-1 rounded-md bg-primary/10 text-primary hover:bg-primary/20 transition-colors"
      on:click={() => handleAction("optimize")}
    >
      优化内容
    </button>
    <button
      class="text-xs px-2 py-1 rounded-md bg-primary/10 text-primary hover:bg-primary/20 transition-colors"
      on:click={() => handleAction("expand")}
    >
      扩展内容
    </button>
  </div>
</div>
