<script lang="ts">
  import { cn } from "$lib/utils";
  import type { Snippet } from "svelte";
  import ActionbarCard from "./actionbar-card.svelte";
  import CoverSelector from "../cover-selector.svelte";
  import { uploadToImgBB } from "$lib/services/image"; // 导入上传函数
  import { userImagesStore } from "$lib/stores/userImages"; // 导入用户图片 store
  import { Card } from "$lib/components/ui/card";

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
  let imageLoading = $state(false);
  let showCoverSelector = $state(false); // 控制 CoverSelector 的显示

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

<div class="dropdown dropdown-hover dropdown-center">
  <div role="button" tabindex="0">
    <ActionbarCard
      disabled={isUploading}
      class={cn("", className)}
      {...restProps}
    >
      {#if isUploading}
        <!-- Display progress directly inside ActionbarCard -->
        <div
          class="absolute top-0 right-0 w-full h-full z-1000 flex flex-col items-center justify-between bg-base-200/50 -mb-2"
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
        <div class="relative w-full h-full flex items-center justify-center">
          {#if imageLoading}
            <div
              class="absolute inset-0 flex items-center justify-center bg-base-200/60 z-10"
            >
              <span
                class="loading loading-spinner loading-lg text-primary"
                aria-label="图片加载中"
              ></span>
            </div>
          {/if}
          <img
            src={coverUrl}
            alt="Event Cover"
            class:opacity-0={imageLoading}
            onload={() => (imageLoading = false)}
            onloadstart={() => (imageLoading = true)}
            onerror={() => (imageLoading = false)}
            style="max-width:100%;max-height:100%;"
          />
        </div>
      {:else}
        <span
          class="animate-bounce text-gray-400 -rotate-10 text-xs font-black"
        >
          no cover
        </span>
      {/if}
    </ActionbarCard>
  </div>
  {#if !isUploading}
    <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
    <div tabindex="0" class="dropdown-content p-4 ml-10">
      <Card class="p-0">
        {#if showCoverSelector}
          <div class="p-2">
            <CoverSelector
              onSelect={(url) => {
                coverUrl = url;
                showCoverSelector = false;
              }}
              onLinkSubmit={(url) => {
                coverUrl = url;
                showCoverSelector = false;
              }}
              onFileUpload={handleFileUpload}
              {userId}
            />
          </div>
        {:else if coverUrl}
          <div class="relative flex items-center justify-end h-60  w-100">
            <img
              src={coverUrl}
              alt="封面大图"
              class=" w-full h-full object-cover rounded-lg"
            />
            <button
              class="btn  btn-primary btn-sm absolute top-2 right-2"
              onclick={() => (showCoverSelector = true)}
            >
              更改封面
            </button>
          </div>
        {:else}
          <div class="flex flex-col items-center justify-center h-20 mb-4 w-60">
            <span class="text-neutral-content/50 text-sm font-semibold"
              >暂无封面</span
            >
          </div>
          <button
            class="btn btn-outline btn-sm mb-4"
            onclick={() => (showCoverSelector = true)}
          >
            更改封面
          </button>
        {/if}
      </Card>
    </div>
  {/if}
</div>
