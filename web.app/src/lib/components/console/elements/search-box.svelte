<script lang="ts">
  import { Input } from "$lib/components/ui/input";
  import { Button } from "$lib/components/ui/button";
  import { Search, MapPin } from "lucide-svelte";
  import { createEventDispatcher } from "svelte";
  import type { HTMLInputAttributes } from "svelte/elements";

  /**
   * Notion风格的搜索框组件
   * 提供标准的搜索界面和操作
   */
  let {
    placeholder = "Search...",
    value = $bindable(''),
    showLocationButton = true,
    class: className = "",
  } = $props();

  const dispatch = createEventDispatcher<{
    search: { query: string };
    locationSearch: void;
  }>();

  function handleKeyPress(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      dispatch('search', { query: value });
    }
  }

  function handleLocationSearch() {
    dispatch('locationSearch');
  }
</script>

<div class="relative w-full flex gap-2 {className}">
  <div class="relative flex-1">
    <Search
      class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground"
    />
    <Input
      {placeholder}
      class="pl-10 font-inter"
      bind:value
      on:keypress={handleKeyPress}
    />
  </div>
  {#if showLocationButton}
    <Button
      variant="outline"
      size="icon"
      class="shrink-0"
      on:click={handleLocationSearch}
    >
      <MapPin class="h-4 w-4" />
    </Button>
  {/if}
</div>

<style>
  /* 确保使用Inter字体，符合Notion设计风格 */
  :global(input.font-inter) {
    font-family: 'Inter', sans-serif;
    font-weight: 400;
  }
  
  :global(input.font-inter::placeholder) {
    color: rgb(120, 119, 116);
    opacity: 0.75;
  }
</style>
