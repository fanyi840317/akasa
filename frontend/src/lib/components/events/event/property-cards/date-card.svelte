<script lang="ts">
  import { cn } from "$lib/utils";
  import { formatDistanceToNow } from 'date-fns';
  import { zhCN } from 'date-fns/locale';
  import { Clock } from 'lucide-svelte';
  let { eventDate = $bindable(undefined), class: className = "" } = $props<{
    eventDate?: string;
    class?: string;
  }>();

  let relativeTime = $derived('');

  $effect(() => {
    if (eventDate) {
      try {
        relativeTime = formatDistanceToNow(new Date(eventDate), { addSuffix: true, locale: zhCN });
      } catch (e) {
        console.error("Error formatting date:", e);
        relativeTime = "日期格式无效";
      }
    } else {
      relativeTime = "未设置";
    }
  });

</script>

<div
  class={cn("card rounded-md bg-base-100 card-border border-base-300 w-full overflow-hidden", className)}
>
  <div class="stats">
    <div class="stat">
      <div class="stat-title">事件发生时间</div>
      <div class="stat-value overflow-hidden">{eventDate || "未设置"}</div>
      <div class="stat-desc flex items-center gap-2">
        <Clock class=" size-3" />
        {relativeTime}
      </div>
    </div>
  </div>
</div>
