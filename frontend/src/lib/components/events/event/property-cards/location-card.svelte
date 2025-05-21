<script lang="ts">
  import type { Location } from "$lib/types/map";
  import { cn } from "$lib/utils";
  import { MapBase } from "$lib/components/map";
  import * as Modal from "$lib/components/ui/modal";
  import { Pencil } from "lucide-svelte";

  let {
    locationData = $bindable(null),
    isLocation = $bindable(false),
    class: className = "",
    onConfirm = () => {},
    onCancel = () => {},
  } = $props<{
    locationData?: Location | null;
    isLocation?: boolean;
    class?: string;
    onConfirm?: () => void;
    onCancel?: () => void;
  }>();
  let isEditingModalVisible = $state(false);
</script>

<div
  class={cn(
    "card rounded-xl bg-base-100 card-border border-base-200 card-sm overflow-hidden",
    className
  )}
>
  <div class="card-body p-0 h-[160px]">
    <MapBase class="h-full rounded-full-t"></MapBase>
  </div>
  <div class="bg-base-300">
    <div class="flex items-center gap-2 p-4">
      <div class="grow">
        <div class="text-sm font-medium">事件的发生地点</div>
        <div class="text-xs opacity-60">
          {locationData?.name || "未设置"}
        </div>
      </div>
      <div class="shrink-0">
        <button
          class="btn btn-sm"
          onclick={() => {
            isEditingModalVisible = true;
          }}>修改</button
        >
      </div>
    </div>
  </div>
</div>
<!-- Modal for title editing -->
<Modal.Root bind:open={isEditingModalVisible} class="w-[800px] h-[600px]">
  <Modal.Title
    onClose={() => {
      isEditingModalVisible = false;
    }}>设置地点</Modal.Title
  >
  <div class="p-4 w-full h-full">

    <MapBase showGeocoder={true} class="h-full"></MapBase>
  </div>
  <div class="badge m-4">{locationData?.name || "未设置"}</div>
  <Modal.Foot
    onCancel={() => {
      isEditingModalVisible = false;
    }}
    {onConfirm}
  />
</Modal.Root>
