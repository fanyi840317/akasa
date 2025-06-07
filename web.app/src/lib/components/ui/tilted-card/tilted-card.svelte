<script lang="ts">
  import { cn } from "$lib/utils";

  let {
    tiltAngle = -5,
    bgClass = "bg-gray-200 dark:bg-zinc-800",
    scaleX = 0.95,
    class: className = "",
    cardClass = "px-6 py-10 relative mx-auto rounded-lg shadow dark:bg-zinc-900/90 backdrop-blur-xl",
    ...rest
  } = $props<{
    tiltAngle?: number;
    bgClass?: string;
    scaleX?: number;
    class?: string;
    cardClass?: string;
    [key: string]: any;
  }>();
</script>

<div class="py-8" {...rest}>
  <div class="relative max-w-xl">
    <div
      class={cn("absolute inset-0 rounded-lg", bgClass)}
      style:transform={`rotate(${tiltAngle}deg) scaleX(${scaleX})`}
    />
    <!-- 卡片内容 -->
    <div class={cn(cardClass, className)}>
      <slot />
    </div>
  </div>
</div>
