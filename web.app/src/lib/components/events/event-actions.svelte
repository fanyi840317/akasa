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
  import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
  } from "$lib/components/ui/dropdown-menu";
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

<DropdownMenu>
  <DropdownMenuTrigger>
    <Button variant="ghost" size="icon" class="h-8 w-8">
      <Share2 class="h-4 w-4" />
    </Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent align="end" class="w-48">
    <DropdownMenuItem onclick={onPreview}>
      <Eye class="mr-2 h-4 w-4" />
      预览
    </DropdownMenuItem>
    <DropdownMenuItem onclick={() => handleShare("copy")}>
      <Copy class="mr-2 h-4 w-4" />
      复制链接
    </DropdownMenuItem>
    <DropdownMenuItem onclick={() => handleShare("twitter")}>
      <Twitter class="mr-2 h-4 w-4" />
      分享到 Twitter
    </DropdownMenuItem>
    <DropdownMenuItem onclick={() => handleShare("facebook")}>
      <Facebook class="mr-2 h-4 w-4" />
      分享到 Facebook
    </DropdownMenuItem>
    <DropdownMenuItem onclick={() => handleShare("wechat")}>
      <QrCode class="mr-2 h-4 w-4" />
      微信扫码分享
    </DropdownMenuItem>
    <DropdownMenuItem>
      <label class="cursor-pointer w-full flex items-center">
        <input
          type="file"
          accept="image/*"
          class="hidden"
          on:change={onCoverUpload}
        />
        <Image class="mr-2 h-4 w-4" />
        更换封面
      </label>
    </DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu> 