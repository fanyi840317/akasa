<script lang="ts">
  import { cn } from "$lib/utils";
  import type { Snippet } from "svelte";
  import ActionbarCard from "./actionbar-card.svelte";
  import CoverSelector from "../cover-selector.svelte";
  import { uploadToImgBB } from "$lib/services/image"; // 导入上传函数
  import { userImagesStore } from "$lib/stores/userImages"; // 导入用户图片 store
  import InfoCard from '$lib/components/ui/card/info-card.svelte';
  import { Card } from '$lib/components/ui/card'; // Keep Card for dropdown content
  import ProgressContainer from '$lib/components/ui/progress-container.svelte';

  let {
    class: className = "",
    coverUrl = $bindable(undefined),
    userId,
    ...restProps
  } = $props<{
    coverUrl?: string;
    class?: string;
    userId: string;
  }>();

  let isUploading = $state(false);
  let uploadProgress = $state(0);
  let imageLoading = $state(false);
  let showInfoTooltip = $state(false);
  let isDropdownOpen = $state(false); // To control dropdown visibility on click

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

<div class="dropdown dropdown-center">
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <div
    role="button"
    tabindex="0"
    onclick={toggleDropdown}
    onmouseenter={handleMouseEnterTrigger}
    onmouseleave={handleMouseLeaveTrigger}
  >
    <ActionbarCard
      disabled={isUploading}
      class={cn("", className)}
      {...restProps}
    >
      {#if isUploading}
        <ProgressContainer progress={uploadProgress} size="xxs"/>
      {:else if coverUrl}
        <ProgressContainer class="bg-transparent" size="xs">
          <img
            src={coverUrl}
            alt="Event Cover"
            class:opacity-0={imageLoading}
            class="max-w-full max-h-full object-contain"
            onload={() => {alert(2); imageLoading = false;}}
            onloadstart={() => {alert(1); imageLoading = true;}}
            onerror={() => (imageLoading = false)}
          />
        </ProgressContainer>
      {:else}
        <span
          class="animate-bounce text-gray-400 -rotate-10 text-xs font-black"
        >
          no cover
        </span>
      {/if}
    </ActionbarCard>
  </div>
  {#if showInfoTooltip && !isUploading && !isDropdownOpen}
    <div
      class="absolute z-50 top-full left-1/2 -translate-x-1/2 mt-2 pointer-events-none"
    >

      <InfoCard
        class="shadow-xl w-[200px] min-w-64 min-h-48"
        title={coverUrl ? "点击更改封面" : "点击设置封面"}
        description={coverUrl ? undefined : "当前暂无封面"}
      >
      {#if coverUrl}
        <img alt="" src={coverUrl} class="w-full h-full object-cover" />
      {/if}
    </InfoCard>
    </div>
  {/if}
  <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
  <div tabindex="0" class="dropdown-content p-4 ml-10 z-[100]">
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
</div>
