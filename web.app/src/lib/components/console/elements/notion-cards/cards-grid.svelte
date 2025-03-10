<script lang="ts">
  import { cn } from "$lib/utils";
  
  /**
   * Notion风格的卡片网格容器
   */
  let {
    class: className = '',
    columns = 3,
    gap = 4,
    itemsCenter = true, // 是否将卡片居中
  } = $props();
  
  const getGridClass = (cols: number) => {
    const classes = {
      1: 'grid-cols-1',
      2: 'grid-cols-1 sm:grid-cols-2',
      3: 'grid-cols-1 sm:grid-cols-2 md:grid-cols-3',
      4: 'grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4',
    };
    return classes[cols as keyof typeof classes] || classes[3];
  };
  
  const getGapClass = (g: number) => {
    const classes = {
      2: 'gap-2',
      3: 'gap-3',
      4: 'gap-4',
      5: 'gap-5',
      6: 'gap-6',
    };
    return classes[g as keyof typeof classes] || classes[4];
  };
</script>

<div class={cn(
  "grid", 
  getGridClass(columns), 
  getGapClass(gap),
  itemsCenter && "place-items-center",
  className
)}>
  <slot />
</div> 