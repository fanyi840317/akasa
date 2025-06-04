<script lang="ts">
  import type { ComponentType } from "svelte";
  import { cn } from "$lib/utils";
  import { fly } from "svelte/transition";

  let {
    href,
    icon,
    label,
    color,
    isActive = false,
    class: className = "",
  } = $props<{
    href: string;
    icon: ComponentType;
    label: string;
    color: string;
    isActive?: boolean;
    class?: string;
  }>();
  
  // 悬停状态
  let isHovered = $state(false);
</script>

<a
    {href}
    class={cn(
      "flex items-center gap-3 py-2 px-3 rounded-lg relative overflow-hidden transition-all duration-300",
      isActive
        ? "bg-base-300 text-base-content font-medium shadow-sm"
        : "hover:bg-base-300/50",
      className
    )}
    on:mouseenter={() => isHovered = true}
    on:mouseleave={() => isHovered = false}
  >
    {#if isHovered && !isActive}
      <div 
        class="absolute inset-0 bg-primary/5" 
        in:fly={{ y: 10, duration: 200 }}
        out:fly={{ y: 10, duration: 150 }}
      ></div>
    {/if}
    
    <div class="relative z-10 flex items-center gap-3 w-full text-sm">
      <div class={cn(
        "w-5 h-5 rounded-md flex text-sm items-center justify-center transition-all duration-300",
        color,
        (isHovered || isActive) && "scale-110 shadow-sm"
      )}>
        <svelte:component
          this={icon}
          class="w-3 h-3 text-base-content/70"
        />
      </div>
      <span class={cn(
        "transition-all duration-300 ",
        (isHovered || isActive) && "translate-x-0.5"
      )}>{label}</span>
    </div>
  </a>