<script lang="ts">

  import { Image, Upload, Link } from "lucide-svelte";
  import { createEventDispatcher, onMount } from "svelte";

  const dispatch = createEventDispatcher<{
    select: { url: string };
    upload: void;
    linkSubmit: { url: string };
  }>();

  let coverSelectorTab = "my-images";
  let coverLink = "";
  let coverImages: string[] = [];
  let isLoading = true;

  // 加载封面图片
  async function loadCoverImages() {
    try {
      isLoading = true;
      // 使用 fetch 获取图片列表
      const response = await fetch('/api/cover-images');
      if (response.ok) {
        const data = await response.json();
        coverImages = data.images;
      } else {
        console.error('加载封面图片失败:', response.statusText);
        // 如果API不可用，使用默认图片
        coverImages = [
          '/images/cover/c1.webp',
          '/images/cover/c2.webp',
          '/images/cover/c3.webp'
        ];
      }
    } catch (error) {
      console.error('加载封面图片出错:', error);
      // 出错时使用默认图片
      coverImages = [
        '/images/cover/c1.webp',
        '/images/cover/c2.webp',
        '/images/cover/c3.webp'
      ];
    } finally {
      isLoading = false;
    }
  }

  onMount(() => {
    loadCoverImages();
  });

  // 处理选择已有图片
  function handleSelectExistingImage(imageUrl: string) {
    dispatch("select", { url: imageUrl });
  }

  // 处理上传图片
  function handleUpload() {
    dispatch("upload");
  }

  // 处理链接提交
  function handleLinkSubmit() {
    if (coverLink.trim()) {
      dispatch("linkSubmit", { url: coverLink.trim() });
      coverLink = "";
    }
  }
</script>

<div class="w-[400px]">
  <div role="tablist" class="tabs tabs-lift">
    <button role="tab" class="tab  gap-1" class:tab-active={coverSelectorTab === 'my-images'} onclick={() => coverSelectorTab = 'my-images'}>
      <Image class="h-4 w-4" />
      <span>我的图片</span>
    </button>
    <div class="p-4 tab-content bg-base-100 border-base-300">
      <div class="grid grid-cols-3 gap-2 h-[200px] overflow-y-auto">
        {#if isLoading}
          <div class="col-span-3 flex items-center justify-center h-full">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
        {:else if coverImages.length === 0}
          <div class="col-span-3 flex items-center justify-center h-full text-muted-foreground">
            暂无可用图片
          </div>
        {:else}
          {#each coverImages as imageUrl}
            <div 
              class="aspect-video overflow-hidden rounded-lg cursor-pointer hover:border-1 hover:border-primary" 
              onclick={() => handleSelectExistingImage(imageUrl)}
            >
              <img src={imageUrl} alt="封面图片" class="w-full h-full object-cover" />
            </div>
          {/each}
        {/if}
      </div>
    </div>
    <button role="tab" class="tab gap-1" class:tab-active={coverSelectorTab === 'upload'} onclick={() => coverSelectorTab = 'upload'}>
      <Upload class="h-4 w-4" />
      <span>上传图片</span>
    </button>
    <div class="p-4 tab-content bg-base-100 border-base-300">
      <div class="flex flex-col items-center justify-center h-[200px] border-2 border-dashed rounded-md">
        <!-- <Upload class="h-10 w-10 text-muted-foreground mb-2" /> -->
        <p class="text-sm text-muted-foreground mb-2">拖放图片到此处或点击上传</p>
        <button class="btn btn-outline" onclick={handleUpload}>选择图片</button>
      </div>
    </div>
    <button role="tab" class="tab gap-1" class:tab-active={coverSelectorTab === 'link'} onclick={() => coverSelectorTab = 'link'}>
      <Link class="h-4 w-4" />
      <span>填写链接</span>
    </button>
    <div class="p-4 tab-content bg-base-100 border-base-300">
      <div class="space-y-4">
        <div class="space-y-2">
          <label for="cover-link" class="label"><span class="label-text">图片链接</span></label>
          <input id="cover-link" type="text" placeholder="https://example.com/image.jpg" class="editor-fix-input w-full" bind:value={coverLink} />
        </div>
        <div class="flex justify-end">
          <button class="btn btn-primary" onclick={handleLinkSubmit}>确认</button>
        </div>
      </div>
    </div>
  </div>
</div>