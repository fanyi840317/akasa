<script lang="ts">
  import {
    Image,
    Mic,
    Camera,
    Send,
    HelpCircle
  } from "lucide-svelte";
  import ChatDialog from "./chat-dialog.svelte";

  // Props
  let {
    placeholder = "描述你的图片...",
    apiKey,
    modelName = "gemini-1.5-flash",
    showToolbar = true,
    aspectRatio = "2:3",
    mode = "4v"
  } = $props<{
    placeholder?: string;
    apiKey?: string;
    modelName?: string;
    showToolbar?: boolean;
    aspectRatio?: string;
    mode?: string;
  }>();

  // State
  let inputText = $state("");
  let dialogOpen = $state(false);
  let inputElement = $state<HTMLInputElement | null>(null);

  // Methods
  function openDialog() {
    if (inputText.trim()) {
      dialogOpen = true;
    } else {
      // Focus the input if empty
      inputElement?.focus();
    }
  }

  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Enter" && inputText.trim()) {
      openDialog();
    }
  }
</script>

<div class="relative max-w-xl mx-auto">
  <!-- Main Input Container -->
  <div class="card bg-base-100 shadow-sm">
    <!-- Input Field -->
    <div class="card-body p-2">
      <div class="join w-full">
        <input
          type="text"
          bind:value={inputText}
          bind:this={inputElement}
          placeholder={placeholder}
          class="input input-bordered join-item w-full"
          onkeydown={handleKeyDown}
        />

        <button
          class="btn btn-ghost join-item"
          onclick={openDialog}
        >
          <Send class="h-4 w-4" />
        </button>
      </div>

      <!-- Toolbar -->
      {#if showToolbar}
        <div class="flex items-center justify-between pt-2 border-t mt-2">
          <div class="flex items-center gap-2">
            <button class="btn btn-ghost btn-xs">
              <Image class="h-3.5 w-3.5 mr-1" />
              图像
            </button>

            <button class="btn btn-ghost btn-xs">
              <Mic class="h-3.5 w-3.5 mr-1" />
              {aspectRatio}
            </button>

            <button class="btn btn-ghost btn-xs">
              <Camera class="h-3.5 w-3.5 mr-1" />
              {mode}
            </button>
          </div>

          <button class="btn btn-ghost btn-circle btn-xs">
            <HelpCircle class="h-3.5 w-3.5" />
          </button>
        </div>
      {/if}
    </div>
  </div>
</div>

<!-- Chat Dialog -->
<ChatDialog
  bind:open={dialogOpen}
  {apiKey}
  {modelName}
  placeholder="继续对话..."
  initialMessages={inputText ? [
    {
      role: "user",
      content: inputText,
      timestamp: new Date()
    }
  ] : []}
/>

<style>
  /* Add any custom styles here */
</style>
