<script lang="ts">
  import { Image, Link } from "lucide-svelte";
  import { onMount } from "svelte";
  import { userImagesStore } from "$lib/stores/userImages"; // 导入用户图片 store
  import { fade } from "svelte/transition";
  import {ScrollArea} from "$lib/components/ui/scroll-area";

  // 使用 $props() 定义组件属性，接收回调函数
  let { onSelect, onLinkSubmit, onFileUpload, userId } = $props<{
    onSelect: (url: string) => void;
    onLinkSubmit: (url: string) => void;
    onFileUpload: (file: File) => void; // 新增属性用于传递文件
    userId: string; // 添加 userId 属性
  }>();

  let coverSelectorTab = $state("my-images");
  let coverLink = $state("");
  let showValidationError = $state(false); // 控制是否显示验证错误信息

  // 使用 store 中的数据
  // 修改为包含缩略图 URL 的数据结构
  // 使用 store 中的数据并按提供者分组

  let groupedCoverImages = $derived(
    $userImagesStore.images && $userImagesStore.images.length > 0
      ? $userImagesStore.images.reduce(
          (
            acc: Record<
              string,
              { imageUrl: string; thumbnailUrl?: string; provider?: string }[]
            >,
            image,
          ) => {
            const provider = image.provider || "未知提供者";
            if (!acc[provider]) {
              acc[provider] = [];
            }
            acc[provider].push(image);
            return acc;
          },
          {} as Record<
            string,
            { imageUrl: string; thumbnailUrl?: string; provider?: string }[]
          >,
        )
      : {},
  );
  let isLoading = $derived($userImagesStore.listLoading);

  // 在组件挂载或 userId 变化时加载用户图片
  onMount(() => {
    if (userId) {
      userImagesStore.loadUserImages(userId);
    }
  });

  // 处理选择已有图片
  function handleSelectExistingImage(imageUrl: string) {
    onSelect(imageUrl);
  }

  // 处理文件选择
  function handleFileSelect(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      onFileUpload(input.files[0]); // 将文件传递给父组件
      input.value = ""; // 清空文件输入，以便再次选择同一文件
    }
  }

  // 验证链接格式
  function isValidUrl(url: string): boolean {
    try {
      new URL(url);
      return true;
    } catch (e) {
      return false;
    }
  }

  // 处理链接提交
  function handleLinkSubmit() {
    const trimmedLink = coverLink.trim();
    if (!trimmedLink) {
      showValidationError = true;
      return;
    }
    // 使用更严格的URL验证，并检查是否是图片链接（简单判断后缀）
    const imageRegex = /\.(jpg|jpeg|png|gif|webp|bmp)$/i;
    if (!isValidUrl(trimmedLink) || !imageRegex.test(trimmedLink)) {
      showValidationError = true;
      return;
    }

    showValidationError = false;
    onLinkSubmit(trimmedLink);
    coverLink = ""; // 提交后清空输入框
  }

  // 检查链接是否有效以控制按钮状态
  let isSubmitButtonEnabled = $derived(() => {
    const trimmedLink = coverLink.trim();
    if (!trimmedLink) return false;
    const imageRegex = /\.(jpg|jpeg|png|gif|webp|bmp)$/i;
    return isValidUrl(trimmedLink) && imageRegex.test(trimmedLink);
  });
</script>

<div class="w-[400px] h-[360px]">
  <div role="tablist" class="tabs tabs-border">
    <button
      role="tab"
      class="tab gap-1 [--tab-bg:var(--color-base-200)]"
      class:tab-active={coverSelectorTab === "my-images"}
      onclick={() => (coverSelectorTab = "my-images")}
    >
      <span>我的图片</span>
    </button>

    <button
      role="tab"
      class="tab gap-1 [--tab-bg:var(--color-base-200)]"
      class:tab-active={coverSelectorTab === "link"}
      onclick={() => (coverSelectorTab = "link")}
    >
      <span>填写链接</span>
    </button>
  </div>

  {#if coverSelectorTab === "my-images"}
    <div class="p-4 border-t border-secondary">
      <ScrollArea class="h-[240px]">
        {#if isLoading}
          <div class="col-span-3 flex items-center justify-center h-full">
            <div
              class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"
            ></div>
          </div>
        {:else if Object.keys(groupedCoverImages).length === 0}
          <div
            class="col-span-3 flex items-center justify-center h-full text-muted-foreground"
          >
            暂无可用图片
          </div>
        {:else}
          {#each Object.entries(groupedCoverImages) as [provider, images]}
            <div class="mb-4">
              <h3 class="text-sm font-semibold mb-2">{provider}</h3>
              <div class="grid grid-cols-3 gap-2">
                {#each images as image}
                  <button
                    class="aspect-video overflow-hidden rounded-lg cursor-pointer hover:border-1
                       hover:border-primary"
                    onclick={() => handleSelectExistingImage(image.imageUrl)}
                  >
                    <img
                      src={image.thumbnailUrl || image.imageUrl}
                      alt="封面图片"
                      class="w-full h-full object-cover"
                    />
                  </button>
                {/each}
              </div>
            </div>
          {/each}
        {/if}
      </ScrollArea>
      <!-- 添加文件选择输入框 -->
      <input
        type="file"
        accept="image/*"
        class="hidden size-0 opacity-0 text-transparent"
        onchange={handleFileSelect}
        id="file-upload-input"
      />
      <!-- 添加一个按钮作为文件选择的触发器 -->
      <div class="flex justify-center mt-4">
        <label
          for="file-upload-input"
          class="btn btn-outline btn-primary btn-sm"
        >
          上传图片
        </label>
      </div>
    </div>
  {/if}

  {#if coverSelectorTab === "link"}
  <div class="py-6 px-4 border-t border-secondary pb-1 space-y-1 w-full ">
    <label class="input input-border input-neutral w-full">
      <Link class="h-4 w-4" />
      <input
        type="url"
        class="editor-fix-input input-neutral"
        bind:value={coverLink}
        oninput={() => (showValidationError = false)}
        placeholder="在此粘贴图片的链接..."
      />
    </label>
    {#if showValidationError}
      <p
        in:fade={{ duration: 200 }}
        out:fade={{ duration: 200 }}
        class="ml-1 validator-hint text-error m-0"
      >
        请输入有效的图片链接 (需包含图片文件后缀)
      </p>
    {/if}
    <div class="flex flex-col items-center justify-center gap-2 mt-6">
      <button
        class="btn  btn-neutral btn-sm btn-wide"
        onclick={handleLinkSubmit}
        disabled={!isSubmitButtonEnabled}>确认</button
      >
      <p class="label text-xs">适合任何的网络图片</p>
    </div>
  </div>
  {/if}
</div>
