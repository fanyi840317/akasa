<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import {
    Eye,
    Share2,
    Image,
    Twitter,
    Facebook,
    QrCode,
    Copy,
  } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";
  import { toast } from "svelte-sonner";

  export let title: string = "";
  export let onPreview: () => void;
  export let onCoverUpload: (event: { currentTarget: EventTarget & HTMLInputElement }) => void;

  const dispatch = createEventDispatcher();

  async function handleShare(type: "copy" | "twitter" | "facebook" | "wechat") {
    const url = window.location.href;

    switch (type) {
      case "copy":
        await navigator.clipboard.writeText(url);
        toast.success("链接已复制到剪贴板");
        break;
      case "twitter":
        window.open(
          `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`,
        );
        break;
      case "facebook":
        window.open(
          `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`,
        );
        break;
      case "wechat":
        dispatch("wechatShare");
        break;
    }
  }
</script>

<div class="flex items-center gap-2">
  <Button variant="ghost" size="icon" onclick={onPreview} class="h-9 w-9">
    <Eye class="h-4 w-4" strokeWidth={3} />
  </Button>
  <Button variant="ghost" size="icon" onclick={() => handleShare("copy")} class="h-9 w-9">
    <Copy class="h-4 w-4" strokeWidth={3} />
  </Button>
  <Button variant="ghost" size="icon" onclick={() => handleShare("twitter")} class="h-9 w-9">
    <Twitter class="h-4 w-4" strokeWidth={3} />
  </Button>
  <Button variant="ghost" size="icon" onclick={() => handleShare("facebook")} class="h-9 w-9">
    <Facebook class="h-4 w-4" strokeWidth={3} />
  </Button>
  <Button variant="ghost" size="icon" onclick={() => handleShare("wechat")} class="h-9 w-9">
    <QrCode class="h-4 w-4" strokeWidth={3} />
  </Button>
  <label class="cursor-pointer">
    <input
      type="file"
      accept="image/*"
      class="hidden"
      on:change={onCoverUpload}
    />
    <Button variant="ghost" size="icon" class="h-9 w-9">
      <Image class="h-4 w-4" strokeWidth={3} />
    </Button>
  </label>
</div> 