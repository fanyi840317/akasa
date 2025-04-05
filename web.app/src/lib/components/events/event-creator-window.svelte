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
    CornerDownLeft,
    Circle,
    FileText,
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
  import EventDetailPanel from "./event-detail-panel.svelte";

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

  // 事件属性状态
  let createdAt = $state(new Date().toISOString());
  let lastModified = $state(new Date().toISOString());
  let creator = $state({
    name: "神秘探索者",
    avatar: null
  });
  let evidenceCount = $state(0);
  let timelinePointsCount = $state(0);

  // 监听内容变化，更新最后修改时间
  $effect(() => {
    if (newDoc.content) {
      lastModified = new Date().toISOString();
    }
  });

  // 格式化日期时间
  function formatDateTime(isoString: string) {
    const date = new Date(isoString);
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  let cursorPosition = $state({ top: 0, left: 0 });
  let showAICard = $state(false);
  let isAICardMinimized = $state(false);
  let showEventDetail = $state(false);
  let selectedEvent = $state(null);

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

  function handleCursorPosition(
    event: CustomEvent<{ top: number; left: number }>,
  ) {
    console.log("ai-card 位置:");
    console.log(event.detail);
    if (event.detail && event.detail.top > 0 && event.detail.left > 0) {
      if (cursorPosition.top === 0 && cursorPosition.left === 0) {
        // 计算 AI 面板的位置，考虑右侧面板的影响
        const baseLeft = event.detail.left;
        const adjustedLeft = showEventDetail ? baseLeft - 400 : baseLeft; // 如果右侧面板显示，向左偏移
        cursorPosition = {
          top: event.detail.top + 40,
          left: baseLeft+100,
        };
        showAICard = true;
      }
    }
  }

  function handleAIAction(action: string, data?: any) {
    console.log("AI action:", action);
    if (action === "maximize") {
      isAICardMinimized = false;
    } else if (action === "select-event") {
      selectedEvent = data;
      showEventDetail = true;
      // 这里可以添加将范文插入编辑器的逻辑
    }
  }

  function handleEditorClick() {
    if (showAICard && !isAICardMinimized) {
      isAICardMinimized = true;
    }
  }

  function handleEditorInput() {
    if (showAICard && !isAICardMinimized) {
      isAICardMinimized = true;
    }
  }

  function handleCloseEventDetail() {
    showEventDetail = false;
    selectedEvent = null;
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
  onDestroy(() => {
    // alert();
  });
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
      class="fixed left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] flex gap-4 p-8"
    >
    <!-- 右侧属性按钮 -->
      <div class="w-[80px] h-[80vh] flex flex-col justify-start">
        <div class="space-y-2 py-20">
          <!-- 基本信息 -->
          <div class="space-y-2">
            <Button variant="ghost" class="w-full justify-end gap-2 h-auto py-2">
              <div class="flex flex-col items-end gap-1">
                <Label class="text-xs text-muted-foreground">创建时间</Label>
                <div class="flex items-center gap-2 text-sm">
                  <Clock class="h-4 w-4 text-muted-foreground" />
                  <span>{formatDateTime(createdAt)}</span>
                </div>
              </div>
            </Button>
            <Button variant="ghost" class="w-full justify-end gap-2 h-auto py-2">
              <div class="flex flex-col items-end gap-1">
                <Label class="text-xs text-muted-foreground">最后修改</Label>
                <div class="flex items-center gap-2 text-sm">
                  <Clock class="h-4 w-4 text-muted-foreground" />
                  <span>{formatDateTime(lastModified)}</span>
                </div>
              </div>
            </Button>
            <Button variant="ghost" class="w-full justify-end gap-2 h-auto py-2">
              <div class="flex flex-col items-end gap-1">
                <Label class="text-xs text-muted-foreground">创建者</Label>
                <div class="flex items-center gap-2 text-sm">
                  <Circle class="h-4 w-4 text-primary" />
                  <span>{creator.name}</span>
                </div>
              </div>
            </Button>
          </div>

          <!-- 事件信息 -->
          <div class="space-y-2">
            <Button variant="ghost" class="w-full justify-end gap-2 h-auto py-2">
              <div class="flex flex-col items-end gap-1">
                <Label class="text-xs text-muted-foreground">发生时间</Label>
                <div class="flex items-center gap-2 text-sm">
                  <Calendar class="h-4 w-4 text-muted-foreground" />
                  <span>{eventDate || "未设置"}</span>
                </div>
              </div>
            </Button>
            <Button variant="ghost" class="w-full justify-end gap-2 h-auto py-2">
              <div class="flex flex-col items-end gap-1">
                <Label class="text-xs text-muted-foreground">发生地点</Label>
                <div class="flex items-center gap-2 text-sm">
                  <MapPin class="h-4 w-4 text-muted-foreground" />
                  <span>{locationData?.address || "未设置"}</span>
                </div>
              </div>
            </Button>
            <Button variant="ghost" class="w-full justify-end gap-2 h-auto py-2">
              <div class="flex flex-col items-end gap-1">
                <Label class="text-xs text-muted-foreground">事件分类</Label>
                <div class="flex items-center gap-2 text-sm">
                  <Tag class="h-4 w-4 text-muted-foreground" />
                  <span>{selectedCategory || "未分类"}</span>
                </div>
              </div>
            </Button>
          </div>

          <!-- 统计信息 -->
          <div class="space-y-2">
            <Button variant="ghost" class="w-full justify-end gap-2 h-auto py-2">
              <div class="flex flex-col items-end gap-1">
                <Label class="text-xs text-muted-foreground">字数统计</Label>
                <div class="flex items-center gap-2 text-sm">
                  <FileText class="h-4 w-4 text-muted-foreground" />
                  <span>{newDoc.content.length} 字</span>
                </div>
              </div>
            </Button>
            <Button variant="ghost" class="w-full justify-end gap-2 h-auto py-2">
              <div class="flex flex-col items-end gap-1">
                <Label class="text-xs text-muted-foreground">证据数量</Label>
                <div class="flex items-center gap-2 text-sm">
                  <ImageIcon class="h-4 w-4 text-muted-foreground" />
                  <span>{evidenceCount} 个</span>
                </div>
              </div>
            </Button>
            <Button variant="ghost" class="w-full justify-end gap-2 h-auto py-2">
              <div class="flex flex-col items-end gap-1">
                <Label class="text-xs text-muted-foreground">时间点数量</Label>
                <div class="flex items-center gap-2 text-sm">
                  <Clock class="h-4 w-4 text-muted-foreground" />
                  <span>{timelinePointsCount} 个</span>
                </div>
              </div>
            </Button>
          </div>
        </div>
      </div>
      <!-- 中间编辑器窗口 -->
      <div
        class="w-[800px] h-[80vh] bg-white dark:bg-neutral-900 border border-neutral-200/50 dark:border-neutral-800/50 shadow-[0_4px_12px_rgba(0,0,0,0.05)] dark:shadow-[0_4px_12px_rgba(0,0,0,0.2)] duration-300 rounded-xl overflow-hidden"
        class:translate-x-[-10px]={showEventDetail}
        class:transition-transform={showEventDetail}
        class:duration-500={showEventDetail}
        in:fly={{ duration: 500, x: -100, delay: 0, easing: backInOut }}
        out:fly={{ duration: 400, x: -100, easing: cubicOut }}
      >
        <div class="w-full h-full relative">
          <div
            role="button"
            tabindex="0"
            onkeydown={(e) => e.key === "Enter"}
            class="w-full h-full"
            onclick={handleEditorClick}
            oninput={handleEditorInput}
          >
            <AffineEditor
              htmlDoc={newDoc}
              on:cursorPosition={handleCursorPosition}
            />
          </div>
          {#if showAICard}
            <AICard
              position={cursorPosition}
              onAction={handleAIAction}
              minimized={isAICardMinimized}
            />
          {/if}
        </div>
      </div>

      

      <!-- 右侧事件详情面板 -->
      {#if showEventDetail && selectedEvent}
        <EventDetailPanel
          event={selectedEvent}
          onClose={handleCloseEventDetail}
        />
      {/if}
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
