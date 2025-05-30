<script lang="ts">
  import { cn } from "$lib/utils";
  import { fade } from "svelte/transition";
  import { UserAvatar } from "$lib/components/ui";
  import type { Event } from "$lib/types/event";
  import { Calendar, Clock, Image } from "lucide-svelte";

  let {
    event,
    onClick = undefined,
    size = "sm", // Default to 'sm'
    class: className = "",
  } = $props<{
    event: Event;
    onClick?: (event: Event) => void;
    size?: "xs" | "sm";
    class?: string;
  }>();

  // 格式化日期
  function formatDate(dateString: string): string {
    if (!dateString) return "未知日期";
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString("zh-CN", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    } catch (e) {
      return "日期格式错误";
    }
  }
</script>

<div
  class={cn(
    "card bg-base-100 card-border border-base-200 overflow-hidden hover:shadow-md transition-all card-hover",
    size === "sm" && "card-sm",
    size === "xs" && "p-0",
    className
  )}
  in:fade={{ duration: 200 }}
  out:fade={{ duration: 200 }}
  on:click={() => onClick?.(event)}
  on:keydown={(e) => e.key === "Enter" && onClick?.(event)}
  role="button"
  tabindex="0"
>
  <!-- 卡片封面图 -->
  <figure class="relative w-full h-32 overflow-hidden">
    {#if event.cover}
      <img 
        src={event.cover} 
        alt={event.title} 
        class="w-full h-full object-cover transition-transform hover:scale-105"
      />
    {:else}
      <div class="w-full h-full bg-gradient-to-br from-base-200 to-base-300 flex items-center justify-center">
        <Image class="size-10 opacity-30" />
      </div>
    {/if}
  </figure>

  <div
    class={cn(
      "card-body relative bg-base-200",
      size === "sm" && "gap-3 p-4",
      size === "xs" && "p-2 gap-1"
    )}
  >
    <div class="flex justify-between items-start ">
      <h3 class="font-semibold text-base text-base-content/80 line-clamp-1">{event.title}</h3>
      {#if event.categories && event.categories.length > 0}
        <div class="shrink-0 flex-none">
          <span
            class={cn(
              "badge badge-neutral whitespace-nowrap",
              size === "sm" && "badge-sm",
              size === "xs" && "badge-xs"
            )}
          >
            {event.categories[0]}
          </span>
        </div>
      {/if}
    </div>
    
    <div class="text-xs text-base-content/70 line-clamp-2">
      {event.summary || "无摘要"}
    </div>
  </div>
  

</div>

<!-- <div
class={cn(
  "bg-base-200 flex items-center justify-between px-4",
  size === "sm" && "py-3",
  size === "xs" && "py-2 px-2"
)}
>
<div class="flex items-center gap-2">
  
  <UserAvatar
    fallback={event.creator_name || "?"}
    class="bg-secondary size-6"
    fallbackClass="text-secondary text-xs"
  />
  <span class="text-xs opacity-70">{event.creator_name || "未知用户"}</span>
</div>

<div class="flex items-center gap-1 text-xs opacity-60">
  <Clock class="size-3" />
  <span>{formatDate(event.date)}</span>
</div>
</div> -->