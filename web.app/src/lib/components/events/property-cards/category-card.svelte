<script lang="ts">

  import * as Select from "$lib/components/ui/select";
  import type { Category } from "$lib/types/category";
  import { cn } from "$lib/utils";
  import { ListFilter, Tag, X } from "lucide-svelte";
  import { onMount } from "svelte";

  let {
    selectedCategories = $bindable([]),
    categories = [],
    className = "",
  } = $props<{
    selectedCategories: string[];
    categories: Category[];
    className?: string;
  }>();

  // 导出 class
  export { className as class };

  // 标签颜色
  let tagColors = $state<Record<string, string>>({});

  // 颜色列表 - 发光线框样式
  const colors = [
    "border-red-500/30 text-red-500 hover:shadow-[0_0_15px_rgba(239,68,68,0.5)]",
    "border-blue-500/30 text-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.3)] hover:shadow-[0_0_15px_rgba(59,130,246,0.5)]",
    "border-green-500/30 text-green-500 shadow-[0_0_10px_rgba(34,197,94,0.3)] hover:shadow-[0_0_15px_rgba(34,197,94,0.5)]",
    "border-yellow-500/30 text-yellow-500 shadow-[0_0_10px_rgba(234,179,8,0.3)] hover:shadow-[0_0_15px_rgba(234,179,8,0.5)]",
    "border-purple-500/30 text-purple-500 shadow-[0_0_10px_rgba(168,85,247,0.3)] hover:shadow-[0_0_15px_rgba(168,85,247,0.5)]",
    "border-pink-500/30 text-pink-500 shadow-[0_0_10px_rgba(236,72,153,0.3)] hover:shadow-[0_0_15px_rgba(236,72,153,0.5)]",
    "border-indigo-500/30 text-indigo-500 shadow-[0_0_10px_rgba(99,102,241,0.3)] hover:shadow-[0_0_15px_rgba(99,102,241,0.5)]",
    "border-orange-500/30 text-orange-500 shadow-[0_0_10px_rgba(249,115,22,0.3)] hover:shadow-[0_0_15px_rgba(249,115,22,0.5)]",
  ];

  // 为每个标签分配颜色
  function assignColors() {
    const newColors: Record<string, string> = {};

    selectedCategories.forEach((id: string, index: number) => {
      if (!tagColors[id]) {
        // 为新标签分配颜色
        const colorIndex = index % colors.length;
        newColors[id] = colors[colorIndex];
      } else {
        // 保留现有标签的颜色
        newColors[id] = tagColors[id];
      }
    });

    // 更新标签颜色
    tagColors = newColors;
  }

  // 当选中的分类变化时，更新颜色
  $effect(() => {
    if (selectedCategories.length > 0) {
      assignColors();
    }
  });

  onMount(() => {
    if (selectedCategories.length > 0) {
      assignColors();
    }
  });
</script>

<div class={cn(className)}>
  <div class="flex items-center justify-between mb-3">
    <div class="text-sm font-bold flex items-center text-muted-foreground gap-2">
      <Tag class="h-4 w-4 " />
      <span>分类标签</span>
    </div>
    <div class="px-1">
      <Select.Root type="multiple" bind:value={selectedCategories}>
        <Select.Trigger
          class="justify-end gap-2 h-auto py-1 px-2 border-none"
        >
          <span class:opacity-50={!selectedCategories.length}
            >{selectedCategories.length || "0"}</span
          >
        </Select.Trigger>
        <Select.Content align="start">
          {#each categories as category}
            <Select.Item value={category.$id || ""}
              >{category.name.zh}</Select.Item
            >
          {/each}
        </Select.Content>
      </Select.Root>
    </div>
  </div>

  <div class="h-[140px] overflow-y-auto pr-1">
    {#if selectedCategories.length === 0}
      <div class="flex items-center justify-center h-full">
        <div class="text-sm text-muted-foreground text-center">
          <ListFilter class="h-10 w-10 mx-auto mb-2 text-muted-foreground/50" />
          <p class="text-foreground font-medium">未选择任何分类</p>
          <p class="text-xs mt-1">点击右上角的数字添加分类</p>
        </div>
      </div>
    {:else}
      <div class="flex flex-wrap gap-2">
        {#each selectedCategories as categoryId}
          {@const category = categories.find((c: Category) => c.$id === categoryId)}
          {#if category && tagColors[categoryId]}
            <div
              class="flex items-center gap-1 px-2 py-1 rounded-full border border-opacity-30 text-xs font-medium bg-background/30 backdrop-blur-sm transition-all duration-300 {tagColors[categoryId]}"
            >
              <span>{category.name.zh}</span>
              <button
                class="h-4 w-4 rounded-full flex items-center justify-center hover:opacity-100"
                onclick={() => {
                  selectedCategories = selectedCategories.filter(
                    (id: string) => id !== categoryId,
                  );
                }}
              >
                <X class="h-3 w-3" />
              </button>
            </div>
          {/if}
        {/each}
      </div>
    {/if}
  </div>
</div>
