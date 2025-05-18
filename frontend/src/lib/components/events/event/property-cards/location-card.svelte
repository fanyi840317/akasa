<script lang="ts">
  import type { Location } from "$lib/types/map";
  import { cn } from "$lib/utils";
  import {MapBase} from "$lib/components/map";

  let { locationData = $bindable(null), isLocation = $bindable(false), class: className = "" } = $props<{
    locationData: Location | null;
    isLocation?: boolean;
    class?: string;
  }>();
</script>
<div
  class={cn("card rounded-md bg-base-100 card-border border-base-300 card-sm overflow-hidden", className)}
>
  <div class="card-body p-0 h-[160px]">
    <MapBase class="h-full rounded-full-t"></MapBase>
  </div>
  <div class="bg-base-300">
    <div class="flex items-center gap-2 p-4">
      <div class="grow">
        <div class="text-sm font-medium">Team Sync Meeting</div>
        <div class="text-xs opacity-60">
          Weekly product review with design and development teams
        </div>
      </div>
      <div class="shrink-0">
        <span class="badge badge-sm badge-neutral">1h</span>
      </div>
    </div>
  </div>
</div>
