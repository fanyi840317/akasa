<script lang="ts">
  import { cn } from "$lib/utils";
  import type { Snippet } from "svelte";
  import ActionbarCard from "./actionbar-card.svelte";
  import CoverSelector from "../cover-selector.svelte";
  import { uploadToImgBB } from "$lib/services/image"; // 导入上传函数
  import { userImagesStore } from "$lib/stores/userImages"; // 导入用户图片 store

  let {
    class: className = "",
    coverUrl = $bindable(undefined),
    userId, // 添加 userId 属性
    ...restProps
  } = $props<{
    // children: Snippet;
    coverUrl?: string;
    class?: string;
    userId: string; // 声明 userId 属性类型
  }>();

  let isUploading = $state(false); // 添加上传状态变量
  let uploadProgress = $state(0); // 添加上传进度变量

  // 处理文件上传
  async function handleFileUpload(file: File) {
    isUploading = true;
    uploadProgress = 0;

    try {
      const result = await uploadToImgBB(file, (progress) => {
        uploadProgress = progress.percentage;
      });

      if (result.success && result.data?.url) {
        coverUrl = result.data.url; // 更新封面 URL
        console.log("图片上传成功:", userId, result.data.url);
        // 上传成功后，将图片添加到用户图片列表中
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
      uploadProgress = 0; // 重置进度
    }
  }
</script>

<div class="dropdown dropdown-center">
  <ActionbarCard
    role="button"
    tabindex="0"
    disabled={isUploading}
    class={cn("", className)}
    {...restProps}
  >
    {#if isUploading}
      <!-- Display progress directly inside ActionbarCard -->
      <div
        class="absolute top-0 right-0 w-full h-full z-1000
   flex flex-col items-center justify-between bg-base-200/50 -mb-2"
      >
        <p class="text-muted-foreground mt-2 font-semibold text-[0.625rem]">
          {uploadProgress}%
        </p>
        <progress
          class="progress w-full h-[3px]"
          value={uploadProgress}
          max="100"
        ></progress>
      </div>
    {/if}
    {#if coverUrl}
      <img src={coverUrl} alt="Event Cover" />
    {:else}
      <span class="animate-bounce text-gray-400 -rotate-10 text-xs font-black">
        no cover
      </span>
    {/if}
  </ActionbarCard>
  <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
  {#if !isUploading}
    <div
      tabindex="0"
      class="dropdown-content card bg-base-300 mt-2 ml-10
   border border-neutral shadow-xl"
    >
      <ul class="menu w-full">
        <CoverSelector
          onSelect={(url) => (coverUrl = url)}
          onLinkSubmit={(url) => (coverUrl = url)}
          onFileUpload={handleFileUpload}
          {userId}
        />
      </ul>
    </div>
  {/if}
</div>
