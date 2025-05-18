<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { cn } from "$lib/utils";

  const dispatch = createEventDispatcher<{ fileChange: FileList | null }>();

  let { coverUrl = '' ,class:className } = $props<{ coverUrl?: string ,class?: string }>();

  let isDragging = false;

  function handleFileSelect(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files) {
      dispatch('fileChange', input.files);
    }
  }

  function handleDragOver(event: DragEvent) {
    event.preventDefault();
    isDragging = true;
  }

  function handleDragLeave() {
    isDragging = false;
  }

  function handleDrop(event: DragEvent) {
    event.preventDefault();
    isDragging = false;
    if (event.dataTransfer?.files) {
      dispatch('fileChange', event.dataTransfer.files);
    }
  }

  function handleRemoveCover() {
    dispatch('fileChange', null);
  }
</script>

<div class={cn("card rounded-md shadow-4xl bg-base-100 card-border border-base-300 p-4",className)}>
  {#if coverUrl}
    <div class="relative w-full h-48 overflow-hidden rounded-md">
      <img src={coverUrl} alt="Cover" class="w-full h-full object-cover" />
      <button
        class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1"
        onclick={handleRemoveCover}
      >
        <!-- Icon for remove, e.g., an X -->
        X
      </button>
    </div>
  {:else}
    <label
      class="flex flex-col items-center justify-center w-full h-48 border-2 border-dashed rounded-md cursor-pointer"
      class:border-blue-500={isDragging}
      ondragover={handleDragOver}
      ondragleave={handleDragLeave}
      ondrop={handleDrop}
    >
      <div class="flex flex-col items-center justify-center pt-5 pb-6">
        <svg
          class="w-8 h-8 mb-4 text-gray-500 dark:text-gray-400"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 20 16"
        >
          <path
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L7.6 8.3M10 6l2.4 2.3"
          />
        </svg>
        <p class="mb-2 text-sm text-gray-500 dark:text-gray-400">
          <span class="font-semibold">点击上传</span> 或拖放文件
        </p>
        <p class="text-xs text-gray-500 dark:text-gray-400">SVG, PNG, JPG or GIF (MAX. 800x400px)</p>
      </div>
      <input type="file" class="hidden" onchange={handleFileSelect} accept="image/*" />
    </label>
  {/if}
</div>


