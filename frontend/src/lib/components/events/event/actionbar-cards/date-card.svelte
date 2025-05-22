<script lang="ts">
  import ActionBarCard from "./actionbar-card.svelte";
  import { Clock } from "lucide-svelte";
  import { formatDistanceToNow } from 'date-fns';
  import { zhCN } from 'date-fns/locale';
  import { cn } from "$lib/utils";

  let { eventDate = $bindable(undefined), class: className = "" } = $props<{ eventDate?: string; class?: string }>();

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
      relativeTime = "发生时间";
    }
  });
</script>

<ActionBarCard class={cn("w-auto", className)}>
  <div class="flex items-center text-xs px-2 text-gray-500 ">
    <Clock class="w-3 h-3 mr-1" />
    <span class="font-semibold">{relativeTime}</span>
  </div>
</ActionBarCard>