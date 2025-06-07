<script lang="ts">
  import { onMount } from "svelte";
  import { setMode } from "mode-watcher";
  onMount(() => {
    setMode("dark");
  });
</script>

<div class="bg-background w-full h-[100vh] flex">
    <div class="bg-primary text-primary-foreground">Hello</div>
  <div class="flex flex-col gap-2">
    <div class="flex flex-col gap-1">
      <span class="text-sm text-muted-foreground">经度</span>
      <span class="text-sm text-muted-foreground">纬度</span>
    </div>
    <div class="flex flex-col gap-1">
      <span class="text-sm text-muted-foreground">
        
      </span>
    </div>
  </div>
</div>