<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Eye, Copy, Twitter, Facebook, QrCode, ImageIcon } from "lucide-svelte";

  export let onCoverUpload: () => void = () => {};
  export let onShare: () => void = () => {};
  export let onCopy: () => void = () => {};
  export let onTwitter: () => void = () => {};
  export let onFacebook: () => void = () => {};
  export let onQrCode: () => void = () => {};
</script>

<div class="flex gap-2">
  <Button variant="ghost" size="icon" onclick={onShare}>
    <Eye class="h-4 w-4 stroke-[3]" />
  </Button>
  <Button variant="ghost" size="icon" onclick={onCopy}>
    <Copy class="h-4 w-4 stroke-[3]" />
  </Button>
  <Button variant="ghost" size="icon" onclick={onTwitter}>
    <Twitter class="h-4 w-4 stroke-[3]" />
  </Button>
  <Button variant="ghost" size="icon" onclick={onFacebook}>
    <Facebook class="h-4 w-4 stroke-[3]" />
  </Button>
  <Button variant="ghost" size="icon" onclick={onQrCode}>
    <QrCode class="h-4 w-4 stroke-[3]" />
  </Button>
  <Button variant="ghost" size="icon" onclick={onCoverUpload}>
    <ImageIcon class="h-4 w-4 stroke-[3]" />
  </Button>
</div> 