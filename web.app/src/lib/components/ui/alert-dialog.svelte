<script lang="ts">
  import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
    DialogDescription,
  } from "$lib/components/ui/dialog";
  import { Button } from "$lib/components/ui/button";
  import { alertDialog } from "$lib/stores/alert-dialog";

  $: ({
    isOpen,
    type,
    title,
    message,
    confirmText,
    cancelText,
    onConfirm,
    onCancel,
  } = $alertDialog);
</script>

<Dialog
  bind:open={isOpen}
  onOpenChange={() => {
    if (!isOpen) alertDialog.close();
  }}
>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>{title}</DialogTitle>
      <DialogDescription>{message}</DialogDescription>
    </DialogHeader>
    <DialogFooter class="gap-2">
      {#if type === "confirm"}
        <Button
          variant="outline"
          onclick={() => {
            onCancel?.();
            alertDialog.close();
          }}>{cancelText}</Button
        >
      {/if}
      <Button
        onclick={() => {
          onConfirm?.();
          alertDialog.close();
        }}>{confirmText}</Button
      >
    </DialogFooter>
  </DialogContent>
</Dialog>
