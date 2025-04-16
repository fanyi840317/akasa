<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Sparkles, Save } from "lucide-svelte";

  let {
    onAIGenerate = () => {},
    onSave = () => {},
  } = $props<{
    onAIGenerate?: () => void;
    onSave?: () => void;
  }>();
</script>

<div class="flex items-center gap-2 border-l border-border/40 pl-4">
  <Button
    variant="ghost"
    size="icon"
    class="h-8 w-8"
    onclick={onAIGenerate}
  >
    <Sparkles class="h-4 w-4" />
  </Button>
  <Button variant="ghost" size="icon" class="h-8 w-8" onclick={onSave}>
    <Save class="h-4 w-4" />
  </Button>
</div>