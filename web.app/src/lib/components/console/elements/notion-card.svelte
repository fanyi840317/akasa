<script lang="ts">
  import * as Card from "$lib/components/ui/card";
  import { cn } from "$lib/utils";
  
  /**
   * Notion风格的卡片容器
   * 提供符合Notion设计规范的卡片布局
   */
  let {
    title = '',
    subtitle = '',
    withBlur = true,
    transparent = false,
    class: className = '',
  } = $props();
</script>

<Card.Root 
  class={cn(
    withBlur && "backdrop-blur-sm",
    transparent && "bg-opacity-80 border-none",
    "shadow-sm transition-all duration-200",
    className
  )}
>
  {#if title || subtitle}
    <Card.Header class="p-4 pb-2">
      {#if title}
        <Card.Title class="text-lg font-inter font-medium text-foreground">
          {title}
        </Card.Title>
      {/if}
      {#if subtitle}
        <Card.Description class="text-sm font-inter font-normal text-muted-foreground">
          {subtitle}
        </Card.Description>
      {/if}
    </Card.Header>
  {/if}
  
  <Card.Content class="p-4 font-inter">
    <slot />
  </Card.Content>
  
  {#if $$slots.footer}
    <Card.Footer class="p-4 pt-2 font-inter">
      <slot name="footer" />
    </Card.Footer>
  {/if}
</Card.Root>

<style>
  /* Notion风格的动画和过渡效果 */
  :global(.card-hover) {
    transition: all 0.2s ease;
  }
  
  :global(.card-hover:hover) {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  }
</style>
