<script lang="ts">
  import { Image, Link } from "lucide-svelte";
  import { onMount } from "svelte";
  import { userImagesStore } from "$lib/stores/userImages"; // 导入用户图片 store

  // 使用 $props() 定义组件属性，接收回调函数
  let { onSelect, onLinkSubmit, onFileUpload, userId } = $props<{
    onSelect: (url: string) => void;
    onLinkSubmit: (url: string) => void;
    onFileUpload: (file: File) => void; // 新增属性用于传递文件
    userId: string; // 添加 userId 属性
  }>();

  let coverSelectorTab = $state("my-images");
  let coverLink = $state("");

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
            image
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
          >
        )
      : {}
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

  // 处理链接提交
  function handleLinkSubmit() {
    if (coverLink.trim()) {
      onLinkSubmit(coverLink.trim());
      coverLink = "";
    }
  }
</script>

<div class="w-[400px]">
  <div role="tablist" class="tabs tabs-lift">
    <button
      role="tab"
      class="tab gap-1 [--tab-bg:var(--color-base-200)]"
      class:tab-active={coverSelectorTab === "my-images"}
      onclick={() => (coverSelectorTab = "my-images")}
    >
      <Image class="h-4 w-4" />
      <span>我的图片</span>
    </button>
    <div class="p-4 tab-content bg-base-200 border-base-300">
      <div class="h-[200px]">
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
      </div>
      <!-- 添加文件选择输入框 -->
      <input
        type="file"
        accept="image/*"
        class="hidden"
        onchange={handleFileSelect}
        id="file-upload-input"
      />
      <!-- 添加一个按钮作为文件选择的触发器 -->
      <div class="flex justify-center mt-4">
        <label
          for="file-upload-input"
          class="btn btn-outline btn-sm cursor-pointer"
        >
          上传图片
        </label>
      </div>
    </div>
    <button
      role="tab"
      class="tab gap-1 [--tab-bg:var(--color-base-200)]"
      class:tab-active={coverSelectorTab === "link"}
      onclick={() => (coverSelectorTab = "link")}
    >
      <Link class="h-4 w-4" />
      <span>填写链接</span>
    </button>
    <div class="p-4 tab-content bg-base-200 border-base-300">
      <div class="space-y-4">
        <div class="space-y-2">
          <label for="cover-link" class="label"
            ><span class="label-text">图片链接</span></label
          >
          <input
            id="cover-link"
            type="text"
            placeholder="https://example.com/image.jpg"
            class="editor-fix-input w-full"
            bind:value={coverLink}
          />
        </div>
        <div class="flex justify-end">
          <button class="btn btn-primary btn-sm" onclick={handleLinkSubmit}
            >确认</button
          >
        </div>
      </div>
    </div>
  </div>
</div>
