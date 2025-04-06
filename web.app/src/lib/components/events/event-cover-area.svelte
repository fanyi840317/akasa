<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { Button } from "$lib/components/ui/button";
  import { X, Eye, Copy, Twitter, Facebook, QrCode, Image as ImageIcon } from "lucide-svelte";

  const dispatch = createEventDispatcher<{
    coverUpload: void;
    imageError: void;
  }>();

  let { 
    coverImage = "",
    isUploading = false,
    uploadProgress = 0,
    onClose = () => {}
  } = $props<{
    coverImage: string;
    isUploading: boolean;
    uploadProgress: number;
    onClose: () => void;
  }>();

  // 处理封面上传
  function handleCoverUpload() {
    dispatch("coverUpload");
  }

  // 处理图片加载错误
  function handleImageError() {
    dispatch("imageError");
  }
  
  // 处理关闭按钮点击
  function handleCloseClick() {
    onClose();
  }
  
  // 处理空操作按钮点击
  function handleEmptyAction() {
    // 空操作，仅用于避免事件错误
  }
</script>

<!-- 封面区域 -->
<div class="absolute top-0 left-0 right-0 h-[200px] overflow-hidden">
  {#if coverImage}
    <img
      src={coverImage}
      alt="封面"
      class="w-full h-full object-cover"
      onerror={handleImageError}
    />
  {/if}

  <!-- 上传进度指示器 - 封面区右下角 -->
  {#if isUploading}
    <div
      class="absolute bottom-4 right-4 bg-background/90 backdrop-blur-sm border border-border rounded-lg shadow-lg p-3 flex items-center gap-2 z-50"
    >
      <div class="relative w-6 h-6">
        <svg class="w-full h-full" viewBox="0 0 100 100">
          <circle
            class="text-muted-foreground/20"
            stroke-width="6"
            stroke="currentColor"
            fill="transparent"
            r="40"
            cx="50"
            cy="50"
          />
          <circle
            class="text-primary"
            stroke-width="6"
            stroke-dasharray={251.2}
            stroke-dashoffset={251.2 - (251.2 * uploadProgress) / 100}
            stroke-linecap="round"
            stroke="currentColor"
            fill="transparent"
            r="40"
            cx="50"
            cy="50"
          />
        </svg>
        <div class="absolute inset-0 flex items-center justify-center">
          <span class="text-[10px] font-medium"
            >{Math.round(uploadProgress)}%</span
          >
        </div>
      </div>
      <div class="text-xs font-medium">上传中...</div>
    </div>
  {/if}
</div>

<!-- 关闭按钮 -->
<Button
  variant="ghost"
  size="icon"
  class="absolute left-4 top-4"
  onclick={handleCloseClick}
  disabled={isUploading}
>
  <X class="h-4 w-4 stroke-[3]" />
</Button>

<!-- 事件操作按钮 -->
<div class="absolute right-4 top-4 flex gap-2">
  <Button variant="ghost" onclick={handleEmptyAction}>
    <Eye class="h-4 w-4 stroke-[3]" />
  </Button>
  <Button variant="ghost" onclick={handleEmptyAction}>
    <Copy class="h-4 w-4 stroke-[3]" />
  </Button>
  <Button variant="ghost" onclick={handleEmptyAction}>
    <Twitter class="h-4 w-4 stroke-[3]" />
  </Button>
  <Button variant="ghost" onclick={handleEmptyAction}>
    <Facebook class="h-4 w-4 stroke-[3]" />
  </Button>
  <Button variant="ghost" onclick={handleEmptyAction}>
    <QrCode class="h-4 w-4 stroke-[3]" />
  </Button>
  <Button variant="ghost" onclick={handleCoverUpload}>
    <ImageIcon class="h-4 w-4 stroke-[3]" />
  </Button>
</div> 