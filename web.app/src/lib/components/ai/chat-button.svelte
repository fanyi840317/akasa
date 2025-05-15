<script lang="ts">
  import { MessageSquare } from "lucide-svelte";
  import ChatDialog from "./chat-dialog.svelte";

  // Props
  let {
    buttonText = "AI 对话",
    buttonVariant = "primary",
    buttonSize = "md",
    buttonClass = "",
    showIcon = true,
    apiKey,
    modelName,
    placeholder,
    initialMessages = [],
  } = $props<{
    buttonText?: string;
    buttonVariant?: "primary" | "secondary" | "accent" | "info" | "success" | "warning" | "error" | "ghost" | "link" | "outline" | "neutral";
    buttonSize?: "lg" | "md" | "sm" | "xs";
    buttonClass?: string;
    showIcon?: boolean;
    apiKey?: string;
    modelName?: string;
    placeholder?: string;
    initialMessages?: any[];
  }>();

  // State
  let dialogOpen = $state(false);

  // Methods
  function openDialog() {
    dialogOpen = true;
  }

  function handleDialogClose() {
    dialogOpen = false;
  }
</script>

<!-- Chat Button -->
<button
  class="btn btn-{buttonVariant} btn-{buttonSize} {buttonClass}"
  onclick={openDialog}
>
  {#if showIcon}
    <MessageSquare class="h-4 w-4 mr-1" />
  {/if}
  {buttonText}
</button>

<!-- Chat Dialog -->
<ChatDialog
  bind:open={dialogOpen}
  {apiKey}
  {modelName}
  {placeholder}
  initialMessages={initialMessages}
  on:close={handleDialogClose}
/>
