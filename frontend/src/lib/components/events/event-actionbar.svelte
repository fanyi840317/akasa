<script lang="ts">
  import { X as XIcon, Save as SaveIcon, Pencil } from "lucide-svelte";
  import * as Modal from "$lib/components/ui/modal";

  let {
    title = $bindable("Untitled Event"),
    showSaveButton = true,
    editableTitle = true,
    onClose = () => {},
    onSaveDocument = () => {},
    onTitleChange = (newTitle: string) => {},
  } = $props<{
    title?: string;
    showSaveButton?: boolean;
    editableTitle?: boolean;
    onClose?: () => void;
    onSaveDocument?: () => void;
    onTitleChange?: (newTitle: string) => void;
  }>();

  let isEditingModalVisible = $state(false);
  let originalModalTitle = title;
  let currentModalTitle = $state(title);

  let inputElement: HTMLInputElement; // Variable to hold the input element reference

  function startEditing() {
    if (!editableTitle) return;
    originalModalTitle = title;
    currentModalTitle = title;
    isEditingModalVisible = true;
  }

  function confirmSaveChanges() {
    isEditingModalVisible = false;
    onTitleChange(currentModalTitle);
  }

  function cancelEditing() {
    currentModalTitle = originalModalTitle; // Revert to title when modal opened
    isEditingModalVisible = false;
  }

  function handleClose() {
    onClose();
  }

  function handleSaveDocument() {
    onSaveDocument();
  }

  $effect(() => {
    if (isEditingModalVisible && inputElement) {
      inputElement.focus(); // Focus the input when the modal becomes visible
    }
  });
</script>

<div
  class="p-4 flex justify-between items-center absolute top-0 left-0 right-0 z-10"
>
  <button class="btn btn-sm btn-circle" onclick={handleClose}>
    <XIcon class="w-4 h-4" />
  </button>

  <div class="flex items-center">
    <h1 class="text-lg font-semibold mr-2">{title}</h1>
    {#if editableTitle}
      <button
        class="btn btn-circle btn-sm p-1 btn-ghost"
        onclick={startEditing}
      >
        <Pencil class="w-4 h-4" />
      </button>
    {/if}
  </div>

  {#if showSaveButton}
    <button class="btn btn-sm btn-primary" onclick={handleSaveDocument}>
      <SaveIcon class="w-4 h-4 mr-1" />
      保存
    </button>
  {:else}
    <!-- Placeholder for alignment if save button is hidden -->
    <div
      class="w-[calc(theme(spacing.btn-sm)+theme(spacing.4)+theme(spacing.1))]"
    ></div>
    <!-- Adjusted width to match button + icon + margin -->
  {/if}
</div>

<!-- Modal for title editing -->
<Modal.Root bind:open={isEditingModalVisible} class="w-[500px]">
  <Modal.Title
    onClose={() => {
      isEditingModalVisible = false;
    }}>编辑标题</Modal.Title
  >

  <input
    type="text"
    placeholder="输入标题"
    bind:value={currentModalTitle}
    bind:this={inputElement} 
    class="editor-fix-input px-4 w-full mx-4"
  />
  <Modal.Foot
      cancelText="取消"
      confirmText="保存"
      onCancel={cancelEditing}
      onConfirm={confirmSaveChanges}
    />
</Modal.Root>

<style>
  .editor-fix-input {
    color: white;
    padding-left: 10px;
    font-size: medium;
  }
</style>
