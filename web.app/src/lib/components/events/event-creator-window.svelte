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
    class="fixed inset-0 z-50 bg-background"
    transition:fade={{ duration: 400, delay: 0, easing: cubicOut }}
    on:click={handleClose}
  >
    <!-- 关闭按钮 -->
    <div
      class="fixed left-4 top-4 z-50"
      in:fly={{ duration: 300, x: -20, delay: 100, easing: backInOut }}
      out:fly={{ duration: 200, x: -20, easing: cubicOut }}
      on:click|stopPropagation
    >
      <Button
        variant="ghost"
        size="icon"
        class="h-9 w-9"
        onclick={handleClose}
      >
        <X class="h-4 w-4" strokeWidth={3}/>
      </Button>
    </div>

    <!-- 操作按钮 -->
    <div 
      class="fixed right-4 top-4 z-50"
      in:fly={{ duration: 300, x: 20, delay: 200, easing: backInOut }}
      out:fly={{ duration: 200, x: 20, easing: cubicOut }}
    >
      <EventActions
        {title}
        onPreview={() => {}}
        onCoverUpload={handleCoverUpload}
      />
    </div>

    <!-- 窗口容器 -->
    <div 
      class="fixed left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] flex gap-2 p-8"
      on:click|stopPropagation
    >
      <!-- 左侧窗口容器 -->
      <div class="flex flex-col gap-2">
        <!-- AI 窗口 -->
        <div
          class="w-[220px] bg-white dark:bg-neutral-900 border border-neutral-200/50 dark:border-neutral-800/50 shadow-[0_4px_12px_rgba(0,0,0,0.05)] dark:shadow-[0_4px_12px_rgba(0,0,0,0.2)] duration-300 rounded-xl overflow-hidden"
          in:fly={{ duration: 500, x: -100, delay: 300, easing: backInOut }}
          out:fly={{ duration: 400, x: -100, easing: cubicOut }}
        >
          <div class="flex flex-col h-[180px]">
            <!-- AI 头部 -->
            <div class="flex items-center gap-2 p-3 border-b border-neutral-200/50 dark:border-neutral-800/50">
              <div class="relative">
                <div class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                  <div class="w-3 h-3 rounded-full bg-white animate-pulse"></div>
                </div>
                <div class="absolute -bottom-1 -right-1 w-3 h-3 rounded-full bg-green-500 border-2 border-white dark:border-neutral-900"></div>
              </div>
              <div class="flex-1">
                <div class="text-sm font-medium">AI 助手</div>
                <div class="text-xs text-muted-foreground">正在思考...</div>
              </div>
            </div>

            <!-- 对话内容 -->
            <div class="flex-1 overflow-y-auto p-3 space-y-3">
              <!-- AI 消息 -->
              <div class="flex gap-2">
                <div class="w-6 h-6 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex-shrink-0"></div>
                <div class="flex-1">
                  <div class="bg-neutral-100 dark:bg-neutral-800 rounded-lg p-2 text-sm">
                    你好！我是你的 AI 助手。我可以帮你：
                    <ul class="mt-1 space-y-1 text-xs text-muted-foreground">
                      <li>• 优化文章内容</li>
                      <li>• 提供写作建议</li>
                      <li>• 回答你的问题</li>
                    </ul>
                  </div>
                </div>
              </div>

              <!-- 用户消息 -->
              <div class="flex gap-2 justify-end">
                <div class="flex-1"></div>
                <div class="w-6 h-6 rounded-full bg-neutral-200 dark:bg-neutral-700 flex-shrink-0"></div>
                <div class="flex-1">
                  <div class="bg-blue-50 dark:bg-blue-950/50 rounded-lg p-2 text-sm">
                    请帮我优化这篇文章
                  </div>
                </div>
              </div>
            </div>

            <!-- 输入框 -->
            <div class="p-3 border-t border-neutral-200/50 dark:border-neutral-800/50">
              <div class="relative">
                <input
                  type="text"
                  placeholder="输入你的问题..."
                  class="w-full bg-neutral-100 dark:bg-neutral-800 rounded-lg pl-3 pr-10 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button class="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 2L11 13"></path>
                    <path d="M22 2L15 22L11 13L2 9L22 2Z"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 新窗口 -->
        <div
          class="w-[220px] bg-white dark:bg-neutral-900 border border-neutral-200/50 dark:border-neutral-800/50 shadow-[0_4px_12px_rgba(0,0,0,0.05)] dark:shadow-[0_4px_12px_rgba(0,0,0,0.2)] duration-300 rounded-xl overflow-hidden"
          in:fly={{ duration: 500, x: -100, delay: 400, easing: backInOut }}
          out:fly={{ duration: 400, x: -100, easing: cubicOut }}
        >
          <div class="flex flex-col h-[180px]">
            <div class="flex-1 overflow-hidden">
              <div class="h-full p-4">
                <!-- 新窗口内容 -->
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 中间窗口容器 -->
      <div class="flex flex-col gap-2">
        <!-- 编辑器窗口 -->
        <div
          class="w-[800px] bg-white dark:bg-neutral-900 border border-neutral-200/50 dark:border-neutral-800/50 shadow-[0_4px_12px_rgba(0,0,0,0.05)] dark:shadow-[0_4px_12px_rgba(0,0,0,0.2)] duration-300 rounded-xl overflow-hidden"
          in:fly={{ duration: 500, x: 100, delay: 500, easing: backInOut }}
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

      <!-- 右侧窗口容器 -->
      <div class="flex flex-col gap-2">
        <!-- 地图窗口 -->
        <div
          class="w-[220px] overflow-hidden"
          in:fly={{ duration: 500, x: 100, delay: 600, easing: backInOut }}
          out:fly={{ duration: 400, x: 100, easing: cubicOut }}
        >
          <div class="flex flex-col h-[220px]">
            <div class="flex-1 overflow-hidden">
              <div class="h-full">
                <MapPicker on:locationChange={handleLocationChange} />
              </div>
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
