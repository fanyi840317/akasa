<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Label } from "$lib/components/ui/label";
  import * as Tabs from "$lib/components/ui/tabs";
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

<div class="w-[400px] p-4">
  <Tabs.Root value={coverSelectorTab} onValueChange={(value) => coverSelectorTab = value}>
    <Tabs.List class="grid w-full grid-cols-3">
      <Tabs.Trigger value="my-images" class="gap-1">
        <Image class="h-4 w-4" />
        <span>我的图片</span>
      </Tabs.Trigger>
      <Tabs.Trigger value="upload" class="gap-1">
        <Upload class="h-4 w-4" />
        <span>上传图片</span>
      </Tabs.Trigger>
      <Tabs.Trigger value="link" class="gap-1">
        <Link class="h-4 w-4" />
        <span>填写链接</span>
      </Tabs.Trigger>
    </Tabs.List>
    
    <Tabs.Content value="my-images" class="mt-4">
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
    </Tabs.Content>
    
    <Tabs.Content value="upload" class="mt-4">
      <div class="flex flex-col items-center justify-center h-[200px] border-2 border-dashed rounded-md">
        <Upload class="h-10 w-10 text-muted-foreground mb-2" />
        <p class="text-sm text-muted-foreground mb-2">拖放图片到此处或点击上传</p>
        <Button variant="outline" onclick={handleUpload}>选择图片</Button>
      </div>
    </Tabs.Content>
    
    <Tabs.Content value="link" class="mt-4">
      <div class="space-y-4">
        <div class="space-y-2">
          <Label for="cover-link">图片链接</Label>
          <Input id="cover-link" placeholder="https://example.com/image.jpg" bind:value={coverLink} />
        </div>
        <div class="flex justify-end">
          <Button onclick={handleLinkSubmit}>确认</Button>
        </div>
      </div>
    </Tabs.Content>
  </Tabs.Root>
</div> 