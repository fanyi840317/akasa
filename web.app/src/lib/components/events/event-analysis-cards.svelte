<script lang="ts">
  import { CalendarIcon } from "lucide-svelte";

  let { 
    hypothesisContent = $bindable(""),
    clueContent = $bindable(""),
  } = $props<{
    hypothesisContent?: string;
    clueContent?: string;
  }>();
</script>

<div class="flex w-[140px] flex-col gap-4">
  <div class="h-[100px] p-1 rounded-sm bg-card/40">
    <div class="w-full rounded-t-sm h-[60%] bg-muted/10 font-bold items-center justify-center flex">
      {#if hypothesisContent}
        <h1>{hypothesisContent}</h1>
      {/if}
    </div>
    <div class="flex items-center gap-1 p-1 mt-2 text-xs text-muted-foreground/50">
      <CalendarIcon class="h-3 w-3" />
      假设
    </div>
  </div>

  <div class="h-[100px] p-1 rounded-sm bg-muted/40">
    <div class="w-full rounded-t-sm h-[60%] bg-muted/10 font-bold items-center justify-center flex">
      {#if clueContent}
        <h1>{clueContent}</h1>
      {/if}
    </div>
    <div class="flex items-center gap-1 p-1 mt-2 text-xs text-muted-foreground/50">
      <CalendarIcon class="h-3 w-3" />
      线索
    </div>
  </div>
</div>