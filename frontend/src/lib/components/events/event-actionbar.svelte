<script lang="ts">
  import {
    X as XIcon,
    Save as SaveIcon,
    Pencil,
    Settings2,
  } from "lucide-svelte";
  import * as Modal from "$lib/components/ui/modal";
  import {UserAvatar } from "$lib/components/ui/avatar";

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
  let isPropertiesPanelOpen = $state(false);

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
  <button class="btn btn-sm btn-circle btn-ghost" onclick={onClose}>
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
  <div>
    <button
      class="btn btn-sm btn-ghost"
      onclick={() => {
        // isPropertiesPanelOpen =!isPropertiesPanelOpen;
      }}
    >
      
    <UserAvatar class="size-6"></UserAvatar>
    +添加评论
      </button>

    <button
      class="btn btn-sm btn-ghost"
      onclick={() => {
        isPropertiesPanelOpen = !isPropertiesPanelOpen;
      }}
    >
      <!-- {#if isPropertiesPanelOpen}
        <XIcon class="w-4 h-4 mr-1" />
        关闭属性
      {:else}
       
      {/if} -->
      <Settings2 class="w-4 h-4 mr-1" />
      属性
      <label class="toggle toggle-xs text-base-content ml-2">
        <input type="checkbox" bind:checked={isPropertiesPanelOpen} />
        <svg
          aria-label="enabled"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
        >
          <g
            stroke-linejoin="round"
            stroke-linecap="round"
            stroke-width="4"
            fill="none"
            stroke="currentColor"
          >
            <path d="M20 6 9 17l-5-5"></path>
          </g>
        </svg>
        <svg
          aria-label="disabled"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="4"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M18 6 6 18" />
          <path d="m6 6 12 12" />
        </svg>
      </label>
    </button>
    {#if showSaveButton}
      <button class="btn btn-sm btn-ghost" onclick={handleSaveDocument}>
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
    class="editor-fix-input px-4 mx-2"
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
