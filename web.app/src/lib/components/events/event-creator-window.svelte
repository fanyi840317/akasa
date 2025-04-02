<script lang="ts">
  import { fade, fly, slide } from "svelte/transition";
  import { backInOut, cubicOut } from "svelte/easing";
  import { createEventDispatcher, onMount } from "svelte";
  import {
    X,
    MapPin,
    Save,
    Clock,
    Tag,
    Calendar,
    Image as ImageIcon,
  } from "lucide-svelte";
  import * as Tabs from "$lib/components/ui/tabs";
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import { Separator } from "$lib/components/ui/separator";
  import { Label } from "$lib/components/ui/label";
  import AffineEditor from "$lib/components/editor/affine-editor.svelte";
  import MapPicker from "$lib/components/map/map-picker.svelte";
  import type { LocationData, LocationChangeEvent } from "$lib/components/map";
  import * as Select from "$lib/components/ui/select";
  import { cn } from "$lib/utils";
  import { categoryStore } from "$lib/stores/category";
  import { toast } from "svelte-sonner";
  import type { Category } from "$lib/types/category";
  import { appStore } from "$lib/stores/appState";
  import * as Modal from "$lib/components/ui/modal";
  import EventDetail from "./event-detail.svelte";

  const dispatch = createEventDispatcher();

  let { open = $bindable(false) } = $props();

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
  let currentEvent = $state({
    title: "",
    content: "",
    location: "",
    date: "",
    user_id: "",
    cover: "",
  });

  // 加载分类数据
  async function loadCategories() {
    try {
      const result = await categoryStore.fetchCategories();
      categories = result;
    } catch (error) {
      console.error("无法加载分类数据:", error);
      toast.error("无法加载分类数据");
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
      toast.error("请输入事件标题");
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
        cover_image: coverImage,
      };

      dispatch("save", eventData);
      handleClose();
    } catch (error) {
      console.error("保存事件失败:", error);
      toast.error("保存事件失败");
    } finally {
      isPublishing = false;
    }
  }

  function handleCoverUpload() {
    // 实现封面上传功能
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";
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
  const modalTransition = {
    duration: 400,
    y: 30,
    opacity: 0,
    easing: cubicOut,
  };
</script>

{#if open}
  <div
    class="fixed inset-0 z-50 bg-neutral-900/10 backdrop-blur-[2px] dark:bg-neutral-900/50"
    transition:fade={backdropTransition}
  >
    <div
      class="fixed left-[50%] top-[50%] z-50 grid w-full max-w-[1200px] translate-x-[-50%] translate-y-[-50%] bg-white dark:bg-neutral-900 border border-neutral-200/50 dark:border-neutral-800/50 shadow-[0_0_0_1px_rgba(0,0,0,0.03)] dark:shadow-[0_0_0_1px_rgba(255,255,255,0.03)] duration-200 sm:rounded-lg overflow-hidden"
      transition:fly={modalTransition}
    >
      <div class="flex flex-col h-[80vh]">
        <!-- 顶部工具栏 -->
        <div class="flex items-center justify-between p-2 bg-white dark:bg-neutral-900 z-10 border-b border-neutral-200/50 dark:border-neutral-800/50">
          <div class="flex items-center gap-2">
            <Button variant="ghost" size="icon" onclick={handleClose}>
              <X class="h-4 w-4" />
            </Button>
            <Input
              placeholder="输入事件标题..."
              bind:value={title}
              class="w-[300px]"
            />
          </div>
          <div class="flex items-center gap-2">
            <Button variant="outline" onclick={handleCoverUpload}>
              <ImageIcon class="h-4 w-4 mr-2" />
              上传封面
            </Button>
            <Button onclick={handleSave} disabled={isPublishing}>
              <Save class="h-4 w-4 mr-2" />
              {isPublishing ? "保存中..." : "保存"}
            </Button>
          </div>
        </div>

        <!-- 主要内容区域 -->
        <div class="flex-1 flex overflow-hidden">
          <!-- 左侧编辑器 -->
          <div class="flex-1 overflow-hidden border-r border-neutral-200/50 dark:border-neutral-800/50">
            <div class="h-full">
              <AffineEditor htmlDoc={newDoc} />
            </div>
          </div>

          <!-- 右侧地图选择器 -->
          <div class="w-[400px] overflow-hidden">
            <div class="h-full">
              <MapPicker on:locationChange={handleLocationChange} />
            </div>
          </div>
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
