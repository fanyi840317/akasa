<script lang="ts">
  import { cn } from "$lib/utils";
  import type { Snapshot } from "@sveltejs/kit";

  let {
    cancelText = "取消",
    confirmText = "保存",
    onCancel = () => {},
    onConfirm = () => {},
    class: className = "",
    leftContent,
  } = $props<{
    cancelText?: string;
    confirmText?: string;
    onCancel?: () => void;
    onConfirm?: () => void;
    class?: string;
    leftContent?: ()=>any;
  }>();

  function handleCancel() {
    onCancel();
  }

  function handleConfirm() {
    onConfirm();
  }
</script>

<div class={cn("flex gap-2 items-center justify-between my-4 px-6", className)}>
  <div class="">
    {@render leftContent?.()}
  </div>
  <div>
    <button class="btn btn-sm btn-ghost" onclick={handleCancel}
      >{cancelText}</button
    >
    <button class="btn btn-sm btn-primary" onclick={handleConfirm}>
      {confirmText}
    </button>
  </div>
</div>
