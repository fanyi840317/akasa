<script lang="ts">
  import { fade, fly, slide } from 'svelte/transition';
  import { backInOut, cubicOut } from 'svelte/easing';
  import { createEventDispatcher, onMount } from 'svelte';
  import { X, MapPin, Save, Clock, Tag, Calendar, Image as ImageIcon } from 'lucide-svelte';
  import * as Tabs from '$lib/components/ui/tabs';
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
  import { ScrollArea } from '$lib/components/ui/scroll-area';
  import { Separator } from '$lib/components/ui/separator';
  import { Label } from '$lib/components/ui/label';
  import AffineEditor from '$lib/components/editor/affine-editor.svelte';
  import MapPicker from '$lib/components/map/map-picker.svelte';
  import type { LocationData, LocationChangeEvent } from '$lib/components/map';
  import * as Select from '$lib/components/ui/select';
  import { cn } from '$lib/utils';
  import { categoryStore } from '$lib/stores/category';
  import { toast } from 'svelte-sonner';
  import type { Category } from '$lib/types/category';

  const dispatch = createEventDispatcher();

  let { open = false } = $props();

  // 编辑器文档
  let newDoc = { content: "", doc: null };
  let locationData: LocationData | null = null;
  let title = "";
  let coverImage = "";
  let selectedCategory = "";
  let eventDate = "";
  let categories = $state<Category[]>([]);
  let activeTab = $state("content");
  let isPublishing = $state(false);

  // 加载分类数据
  async function loadCategories() {
    try {
      const result = await categoryStore.fetchCategories();
      categories = result;
    } catch (error) {
      console.error('无法加载分类数据:', error);
      toast.error('无法加载分类数据');
    }
  }

  function handleClose() {
    open = false;
    dispatch("close");
  }

  function handleLocationChange(event: CustomEvent<LocationChangeEvent>) {
    const { location } = event.detail;
    locationData = location;
  }

  async function handleSave() {
    if (!title.trim()) {
      toast.error('请输入事件标题');
      return;
    }

    isPublishing = true;
    try {
      // 提交事件数据
      const eventData = {
        title,
        content: newDoc.content,
        location: locationData,
        category: selectedCategory,
        date: eventDate,
        cover_image: coverImage
      };
      
      dispatch("save", eventData);
      handleClose();
    } catch (error) {
      console.error('保存事件失败:', error);
      toast.error('保存事件失败');
    } finally {
      isPublishing = false;
    }
  }

  function handleCoverUpload() {
    // 实现封面上传功能
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          coverImage = e.target?.result as string;
        };
        reader.readAsDataURL(file);
      }
    };
    input.click();
  }

  onMount(() => {
    loadCategories();
  });

  // 动画配置
  const backdropTransition = { duration: 300, opacity: 0 };
  const modalTransition = { duration: 400, y: 30, opacity: 0, easing: cubicOut };
</script>

{#if open}
  <div 
    class="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm" 
    on:click|self={handleClose}
    in:fade={backdropTransition}
    out:fade={backdropTransition}
  >
    <div 
      class="fixed left-[50%] top-[50%] z-50 w-[95vw] h-[90vh] max-w-[1400px] translate-x-[-50%] translate-y-[-50%] bg-background border border-border shadow-xl rounded-lg overflow-hidden flex flex-col"
      in:fly={modalTransition}
      out:fade={{ duration: 200 }}
      on:click|stopPropagation
    >
      <!-- 顶部标题栏 -->
      <div class="flex justify-between items-center px-6 py-3 border-b">
        <h2 class="text-xl font-medium">创建新事件</h2>
        <Button variant="ghost" size="icon" onclick={handleClose}>
          <X class="h-4 w-4" />
        </Button>
      </div>

      <!-- 主体内容 -->
      <div class="flex-1 flex min-h-0">
        <!-- 左侧内容 -->
        <div class="w-[70%] border-r flex flex-col">
          <!-- 标题输入 -->
          <div class="border-b p-4 flex items-center">
            <Input 
              type="text" 
              placeholder="输入事件标题..." 
              class="text-xl border-none focus-visible:ring-0 focus-visible:ring-offset-0 h-12 px-0"
              bind:value={title}
            />
            {#if coverImage}
              <div class="flex items-center gap-2 ml-4">
                <img src={coverImage} alt="封面" class="h-8 w-8 rounded object-cover" />
                <Button variant="outline" size="sm" onclick={handleCoverUpload}>更换</Button>
              </div>
            {:else}
              <Button variant="outline" size="sm" class="ml-4 flex items-center gap-2" onclick={handleCoverUpload}>
                <ImageIcon class="h-4 w-4" />
                <span>添加封面</span>
              </Button>
            {/if}
          </div>

          <!-- 内容编辑 -->
          <div class="flex-1 min-h-0 overflow-hidden">
            <Tabs.Root value={activeTab} onValueChange={(v) => activeTab = v} class="h-full flex flex-col">
              <Tabs.List class="border-b px-4">
                <Tabs.Trigger value="content">内容</Tabs.Trigger>
                <Tabs.Trigger value="location">位置</Tabs.Trigger>
              </Tabs.List>
              <Tabs.Content value="content" class="flex-1 p-4 h-full">
                <AffineEditor htmlDoc={newDoc} class="h-full" />
              </Tabs.Content>
              <Tabs.Content value="location" class="flex-1 p-4 overflow-hidden">
                <div class="h-full w-full rounded-md overflow-hidden border">
                  <MapPicker 
                    locationData={locationData} 
                    on:locationChange={handleLocationChange}
                  />
                </div>
              </Tabs.Content>
            </Tabs.Root>
          </div>
        </div>

        <!-- 右侧属性面板 -->
        <div class="w-[30%]">
          <ScrollArea class="h-full">
            <div class="p-6 space-y-6">
              <div>
                <Label class="text-sm font-medium mb-2 block">分类</Label>
                <Select.Root onValueChange={(value) => selectedCategory = value}>
                  <Select.Trigger class="w-full">
                    <span>{selectedCategory ? categories.find(c => c.$id === selectedCategory)?.name?.zh || '选择事件分类' : '选择事件分类'}</span>
                  </Select.Trigger>
                  <Select.Content>
                    {#each categories as category}
                      <Select.Item value={category.$id}>
                        <div class="flex items-center gap-2">
                          <div class="h-2 w-2 rounded-full" style="background-color: {category.color}"></div>
                          <span>{category.name.zh}</span>
                        </div>
                      </Select.Item>
                    {/each}
                  </Select.Content>
                </Select.Root>
              </div>

              <div>
                <Label class="text-sm font-medium mb-2 block">日期</Label>
                <Input 
                  type="text" 
                  placeholder="具体日期或时间描述..." 
                  bind:value={eventDate}
                />
              </div>

              <div>
                <Label class="text-sm font-medium mb-2 block">位置</Label>
                <div class="text-sm text-muted-foreground flex items-center gap-2">
                  <MapPin class="h-4 w-4" />
                  {#if locationData}
                    <span>已选择位置 ({locationData.latitude.toFixed(4)}, {locationData.longitude.toFixed(4)})</span>
                  {:else}
                    <span>未选择位置</span>
                  {/if}
                </div>
              </div>
              
              <Separator />
              
              <div class="pt-4">
                <Button class="w-full" onclick={handleSave} disabled={isPublishing}>
                  {#if isPublishing}
                    <div class="h-4 w-4 border-2 border-current border-t-transparent rounded-full animate-spin mr-2"></div>
                    保存中...
                  {:else}
                    <Save class="h-4 w-4 mr-2" />
                    发布事件
                  {/if}
                </Button>
              </div>
            </div>
          </ScrollArea>
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  :global(.event-creator-window .affine-editor) {
    min-height: 100%;
    height: 100%;
  }
</style>
