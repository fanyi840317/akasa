<script lang="ts">
  import { fade, fly, slide } from "svelte/transition";
  import { backInOut, cubicOut } from "svelte/easing";
  import { createEventDispatcher, onDestroy, onMount } from "svelte";
  import {
    X,
    MapPin,
    Save,
    Clock,
    Tag,
    Calendar,
    Image as ImageIcon,
    Eye,
    Share2,
    Twitter,
    Facebook,
    QrCode,
    Copy,
    Sparkles,
  } from "lucide-svelte";
  import * as Tabs from "$lib/components/ui/tabs";
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import { Separator } from "$lib/components/ui/separator";
  import { Label } from "$lib/components/ui/label";
  import AffineEditor from "$lib/components/editor/affine-editor.svelte";
  import AICard from "$lib/components/ai/ai-card.svelte";
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

  let cursorPosition = $state({ top: 0, left: 0 });
  let showAICard = $state(false);

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

  let showAICardTimer: ReturnType<typeof setTimeout>;

  function handleCursorPosition(
    event: CustomEvent<{ top: number; left: number }>,
  ) {
    console.log("ai-card 位置:");
    console.log(event.detail);
    cursorPosition = {
      top: event.detail.top + 40,
      left: event.detail.left + 40,
    };
    showAICardTimer = setTimeout(() => {
      showAICard = true;
    }, 200);
  }

  // onDestroy(() => {
  //   if (showAICardTimer) {
  //     clearTimeout(showAICardTimer);
  //   }
  //   console.log("EventCreatorWindow 销毁");
  // });
  function handleAIAction(action: string) {
    console.log("AI action:", action);
    // TODO: 实现 AI 操作
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
  >
    <!-- 关闭按钮 -->
    <Button variant="ghost" class="absolute left-4 top-4" onclick={handleClose}>
      <X class="h-4 w-4 stroke-[3]" />
    </Button>

    <!-- 事件操作按钮 -->
    <div class="absolute right-4 top-4 flex gap-2">
      <Button variant="ghost" onclick={() => {}}>
        <Eye class="h-4 w-4 stroke-[3]" />
      </Button>
      <Button variant="ghost" onclick={() => {}}>
        <Copy class="h-4 w-4 stroke-[3]" />
      </Button>
      <Button variant="ghost" onclick={() => {}}>
        <Twitter class="h-4 w-4 stroke-[3]" />
      </Button>
      <Button variant="ghost" onclick={() => {}}>
        <Facebook class="h-4 w-4 stroke-[3]" />
      </Button>
      <Button variant="ghost" onclick={() => {}}>
        <QrCode class="h-4 w-4 stroke-[3]" />
      </Button>
      <Button variant="ghost" onclick={handleCoverUpload}>
        <ImageIcon class="h-4 w-4 stroke-[3]" />
      </Button>
    </div>

    <!-- 窗口容器 -->
    <div
      class="fixed left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] flex gap-2 p-8"
    >
      <!-- 左侧窗口容器 -->
      <div class="flex flex-col gap-2 hidden">
        <!-- 地图窗口 -->
        <div
          class="w-[220px] overflow-hidden"
          in:fly={{ duration: 500, x: -100, delay: 200, easing: backInOut }}
          out:fly={{ duration: 400, x: -100, easing: cubicOut }}
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

      <!-- 右侧编辑器窗口 -->
      <div
        class="w-[800px] h-[80vh] bg-white dark:bg-neutral-900 border border-neutral-200/50 dark:border-neutral-800/50 shadow-[0_4px_12px_rgba(0,0,0,0.05)] dark:shadow-[0_4px_12px_rgba(0,0,0,0.2)] duration-300 rounded-xl overflow-hidden"
        in:fly={{ duration: 500, x: 100, delay: 0, easing: backInOut }}
        out:fly={{ duration: 400, x: 100, easing: cubicOut }}
      >
        <div class="w-full h-full">
          <AffineEditor
            htmlDoc={newDoc}
            on:cursorPosition={handleCursorPosition}
          />
          {#if showAICard}
            <AICard position={cursorPosition} onAction={handleAIAction} />
          {/if}
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  :global(.event-creator-window .affine-editor) {
    min-height: 100%;
    height: 100%;
    position: relative;
  }
</style>
