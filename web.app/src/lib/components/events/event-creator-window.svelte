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
  import EventActions from "./event-actions.svelte";

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
  const backdropTransition = { duration: 400, opacity: 0 };
  const modalTransition = {
    duration: 500,
    y: 30,
    opacity: 0,
    easing: cubicOut,
  };
</script>

{#if open}
  <div
    class="fixed inset-0 z-50 bg-neutral-900/10 backdrop-blur-[2px] dark:bg-neutral-900/50"
    transition:fade={{ duration: 400, delay: 0, easing: cubicOut }}
    on:click={handleClose}
  >
    <!-- 窗口容器 -->
    <div 
      class="fixed left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] flex gap-2 p-8"
      on:click|stopPropagation
    >
      <!-- 事件操作按钮 -->
      <div class="absolute right-0 top-0 p-4">
        <EventActions
          {title}
          onPreview={() => {}}
          onCoverUpload={handleCoverUpload}
        />
      </div>

      <!-- 左侧窗口容器 -->
      <div class="flex flex-col gap-2 py-10">
        <!-- AI 窗口 -->
        <div
          class="w-[200px] bg-white dark:bg-neutral-900 border border-neutral-200/50 dark:border-neutral-800/50 shadow-[0_4px_12px_rgba(0,0,0,0.05)] dark:shadow-[0_4px_12px_rgba(0,0,0,0.2)] duration-300 rounded-xl overflow-hidden"
          in:fly={{ duration: 500, x: -100, delay: 100, easing: backInOut }}
          out:fly={{ duration: 400, x: -100, easing: cubicOut }}
        >
          <div class="flex flex-col h-[200px]">
            <div class="flex-1 overflow-hidden">
              <div class="h-full p-4">
                <!-- <p class="text-sm text-muted-foreground">AI 助手将帮助你优化内容...</p> -->
              </div>
            </div>
          </div>
        </div>

        <!-- 地图窗口 -->
        <div
          class="w-[200px] bg-white dark:bg-neutral-900 border border-neutral-200/50 dark:border-neutral-800/50 shadow-[0_4px_12px_rgba(0,0,0,0.05)] dark:shadow-[0_4px_12px_rgba(0,0,0,0.2)] duration-300 rounded-xl overflow-hidden"
          in:fly={{ duration: 500, x: -100, delay: 200, easing: backInOut }}
          out:fly={{ duration: 400, x: -100, easing: cubicOut }}
        >
          <div class="flex flex-col h-[200px]">
            <div class="flex-1 overflow-hidden">
              <div class="h-full">
                <MapPicker on:locationChange={handleLocationChange} />
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 右侧编辑器窗口 -->
      <div
        class="w-[800px] bg-white dark:bg-neutral-900 border border-neutral-200/50 dark:border-neutral-800/50 shadow-[0_4px_12px_rgba(0,0,0,0.05)] dark:shadow-[0_4px_12px_rgba(0,0,0,0.2)] duration-300 rounded-xl overflow-hidden"
        in:fly={{ duration: 500, x: 100, delay: 0, easing: backInOut }}
        out:fly={{ duration: 400, x: 100, easing: cubicOut }}
      >
        <div class="flex flex-col h-[80vh]">
          <div class="flex-1 overflow-hidden">
            <div class="h-full">
              <AffineEditor htmlDoc={newDoc} />
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
