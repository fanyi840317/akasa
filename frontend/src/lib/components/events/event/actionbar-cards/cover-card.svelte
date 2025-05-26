<script lang="ts">
  import { cn } from "$lib/utils";
  import type { Snippet } from "svelte";
  import ActionbarCard from "./actionbar-card.svelte";
  import { Image, Camera, X } from "lucide-svelte"; // Import Lucide icons
  import CoverSelector from "../cover-selector.svelte";
  import { uploadToImgBB } from "$lib/services/image"; // 导入上传函数
  import { userImagesStore } from "$lib/stores/userImages"; // 导入用户图片 store
  import InfoCard from "$lib/components/ui/card/info-card.svelte";
  import { Card } from "$lib/components/ui/card"; // Keep Card for dropdown content
  import ProgressContainer from "$lib/components/ui/progress-container/progress-container.svelte";
  import type { HTMLAttributes } from "svelte/elements";

  let {
    class: className = "",
    dropdownClass = "",
    coverUrl = $bindable(undefined),
    userId,
    ...restProps
  }: HTMLAttributes<HTMLDivElement> & {
    coverUrl?: string;
    class?: string;
    userId?: string;
    dropdownClass?: string;
	} = $props(); 

  let isUploading = $state(false);
  let uploadProgress = $state(0);
  let imageLoading = $state(false);
  let showInfoTooltip = $state(false);
  let isDropdownOpen = $state(false); // To control dropdown visibility on click
  let oldCoverUrl: string | undefined = undefined;

  $effect(() => {
    if (coverUrl && coverUrl !== oldCoverUrl) {
      imageLoading = true;
    }
    oldCoverUrl = coverUrl;
  });

  async function handleFileUpload(file: File) {
    isUploading = true;
    uploadProgress = 0;
    try {
      const result = await uploadToImgBB(file, (progress) => {
        uploadProgress = progress.percentage;
      });
      if (result.success && result.data?.url) {
        coverUrl = result.data.url;
        console.log("图片上传成功:", userId, result.data.url);
        if (userId) {
          userImagesStore.addUserImage(
            userId,
            result.data.url,
            "imgbb",
            result.data.thumb?.url,
            { delete_url: result.data.delete_url }
          );
        }
      } else {
        console.error("图片上传失败:", result.error?.message || "未知错误");
        alert("图片上传失败: " + (result.error?.message || "未知错误"));
      }
    } catch (error) {
      console.error("图片上传出错:", error);
      alert("图片上传出错");
    } finally {
      isUploading = false;
      uploadProgress = 0;
      // isDropdownOpen = false; // Optionally close dropdown after upload
    }
  }

  function toggleDropdown() {
    if (isUploading) return;
    isDropdownOpen = !isDropdownOpen;
    if (isDropdownOpen) {
      showInfoTooltip = false; // Hide tooltip when dropdown opens
    }
  }

  function handleMouseEnterTrigger() {
    if (isUploading || isDropdownOpen) return; // Don't show tooltip if dropdown is open
    showInfoTooltip = true;
  }

  function handleMouseLeaveTrigger() {
    showInfoTooltip = false;
  }
</script>

<div class={cn("dropdown",dropdownClass)}>
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <ActionbarCard
  onmouseenter={handleMouseEnterTrigger}
  onmouseleave={handleMouseLeaveTrigger}
  disabled={isUploading}
  class={cn("h-[60px] min-w-18 relative", className)}
  {...restProps}
 >
  <div
    role="button"
    class="w-full h-full flex items-center justify-center"
    tabindex="0"
    onclick={toggleDropdown}
  >
    {#if isUploading}
      <ProgressContainer progress={uploadProgress} size="xxs" />
    {:else if coverUrl}
      <ProgressContainer
        class="bg-transparent"
        size="xs"
        isLoading={imageLoading}
      >
        <img
          src={coverUrl}
          alt="Event Cover"
          class:opacity-0={imageLoading}
          class="max-w-full max-h-full object-contain"
          onload={() => {
            imageLoading = false;
          }}
          onerror={() => (imageLoading = false)}
        />
      </ProgressContainer>
    {:else}
      <div class="flex items-center text-xs px-2">
        <Image class="w-3 h-3 mr-1" />
      </div>
    {/if}
  </div>
  {#snippet content()}
    <span
      class="badge badge-xs badge-neutral bg-base-200/20
      p-2 max-w-[62px] text-left truncate
      text-[10px] -mt-2"
      >{coverUrl || "未设置封面"}
    </span>
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    {#if coverUrl}
      <button
        class="absolute -top-2 -right-2 btn btn-xs btn-circle btn-ghost text-error
        pointer-events-auto
        bg-base-100 shadow-md z-10"
        onclick={(e) => {
          e.stopPropagation(); // Prevent dropdown from opening
          coverUrl = undefined;
        }}
      >
        <X class="w-3 h-3" />
      </button>
    {/if}
  {/snippet}
 </ActionbarCard>
 {#if showInfoTooltip && !isUploading && !isDropdownOpen}
  <div
    class="absolute z-50 top-full left-1/2 -translate-x-1/2 pointer-events-none"
  >
    <InfoCard
      class={coverUrl
        ? "shadow-xl w-[200px] min-w-64 min-h-48 rounded-lg"
        : "min-w-30 rounded-lg"}
      size="xs"
      contentClass="p-0"
      title={coverUrl ? coverUrl : "当前暂无封面"}
      description={coverUrl ? undefined : "点击打开设置封面"}
    >
      {#if coverUrl}
        <img
          alt=""
          src={coverUrl}
          class="absolute inset-0 w-full h-full object-cover"
        />
      {/if}
    </InfoCard>
  </div>
 {/if}
 <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
  {#if isDropdownOpen}
  
 <div class="absolute z-50 top-full left-1/2 -translate-x-1/2 p-4 ml-10 z-50 -mt-2">
   <Card class="p-0 ">
     <CoverSelector
       onSelect={(url) => {
         coverUrl = url;
         isDropdownOpen = false; // Close dropdown after selection
       }}
       onLinkSubmit={(url) => {
         coverUrl = url;
         isDropdownOpen = false; // Close dropdown after submission
       }}
       onFileUpload={handleFileUpload}
       {userId}
     />
   </Card>
  </div>
  {/if}
</div>


