<script lang="ts">
  import { onMount } from "svelte";
  import { UserAvatar } from "$lib/components/ui/avatar";
  import { cn } from "$lib/utils";

  let {
    src,
    fallback,
    userName = "Anakin", // Default user name
    time = "12:46", // Default time
    message = "I hate you!", // Default message
    footerText = "Seen at 12:46", // Default footer text
  }: {
    src: string | null;
    fallback: string;
    userName?: string;
    time?: string;
    message?: string;
    footerText?: string;
  } = $props();
</script>

<div class="chat chat-end">
  <div class="chat-image avatar">
    <UserAvatar class="w-10" {src} {fallback}></UserAvatar>
  </div>
  <div class="chat-header">
    {userName}
    <time class="text-xs opacity-50">{time}</time>
  </div>
  <div class="chat-bubble">{message}</div>
  <div class="chat-footer opacity-50">{footerText}</div>
</div>
