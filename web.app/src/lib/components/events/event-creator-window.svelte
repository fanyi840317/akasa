<script lang="ts">
  import { fade, fly } from "svelte/transition";
  import { createEventDispatcher, onDestroy, onMount } from "svelte";
  import { Plus } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";
  import type { Location } from "$lib/types/map";
  import { categoryStore } from "$lib/stores/category";
  import { toast } from "svelte-sonner";
  import type { Category } from "$lib/types/category";
  import { auth } from "$lib/stores/auth";
  import {
    Popover,
    PopoverContent,
    PopoverTrigger,
  } from "$lib/components/ui/popover";
  import { eventStore } from "$lib/stores/event";
  import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
    DialogDescription,
  } from "$lib/components/ui/dialog";
  import {
    exportDocToJson,
    createDocByJson,
  } from "$lib/components/editor/affine-editor";
  import { ID } from "appwrite";
  import type { Doc } from "@blocksuite/store";
  import { createEmptyDoc } from "@blocksuite/presets";
  import EventPropertiesArea from "./event-properties-area.svelte";
  import EventEditorArea from "./event-editor-area.svelte";
  import EventCoverArea from "./event-cover-area.svelte";
  import CoverSelector from "./cover-selector.svelte";
  import { alertDialog } from "$lib/stores/alert-dialog";
  import EventActionsWidget from "./event-actions-widget.svelte";
  import { parseDate, getLocalTimeZone } from "@internationalized/date";
  import type { DateValue } from "@internationalized/date";

  const dispatch = createEventDispatcher();

  let {
    open = $bindable(false),
    event,
    mode = "window",
  } = $props<{
    open?: boolean;
    event?: import("$lib/types/event").Event;
    mode?: "window" | "embedded";
  }>();

  // 编辑器文档
  let newDoc = $state<Doc | null>(null);
  let locationData: Location | null = $state(null);
  let title = $state("");
  let coverImage = $state("");
  let coverFileId = "";
  let selectedCategories: string[] = $state([]);
  let eventDate = $state<DateValue | undefined>();
  let categories = $state<Category[]>([]);
  let activeTab = $state("content");
  let isPublishing = $state(false);
  let hasChanges = $state(false);
  let showSaveDialog = $state(false);
  let eventId = $state(ID.unique()); // 生成事件ID
  let localPreviewUrl = $state(""); // 添加本地预览 URL 状态
  let showContent = $state(false);

  // 事件属性状态
  let createdAt = $state(new Date().toISOString());
  let lastModified = $state(new Date().toISOString());
  let creator = $state(
    $auth.user || {
      name: "神秘探索者",
      avatar: null,
    },
  );
  let evidenceCount = $state(0);
  let timelinePointsCount = $state(0);

  let isUploading = $state(false);
  let uploadProgress = $state(0);

  // 封面选择器状态
  let isCoverSelectorOpen = $state(false);
  let coverSelectorTab = $state("my-images");
  let coverLink = $state("");

  // 添加封面按钮显示状态
  let showCoverButton = $state(false);
  let showEditor = $state(event?.content ? false : true);

  // 初始化事件数据
  async function initializeEventData(event: any) {
    if (event) {
      title = event.title || "";
      locationData = event.location_data
        ? JSON.parse(event.location_data)
        : null;
      selectedCategories = event.categories || [];
      eventDate = event.date ? parseDate(event.date.split('T')[0]) : undefined;

      // 解析封面信息
      if (event.cover) {
        try {
          const coverData = JSON.parse(event.cover);
          coverImage = coverData.url || "";
          coverFileId = coverData.fileId || "";
        } catch (e) {
          console.error("解析封面数据失败:", e);
          coverImage = "";
          coverFileId = "";
        }
      }

      // 初始化编辑器文档
      if (event.content) {
        try {
          console.log("正在从JSON初始化文档内容");
          const doc = await createDocByJson(event.content);
          if (doc) {
            console.log("文档初始化成功");
            newDoc = doc;
            showEditor = true;
          }
        } catch (e) {
          console.error("初始化编辑器文档失败:", e);
        }
      }

      createdAt = event.$createdAt || new Date().toISOString();
      lastModified = event.$updatedAt || new Date().toISOString();
    }
  }

  // 格式化日期
  function formatDate(date: Date | undefined) {
    if (!date) return "未设置";
    return date.toLocaleDateString("zh-CN", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    });
  }

  // 处理 AI 生成
  function handleAIGenerate(event: CustomEvent<void>) {
    showAICard = !showAICard;
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

  // 处理关闭
  function handleClose() {
    if (isUploading) {
      toast.error("请等待封面上传完成");
      return;
    }

    if (hasChanges) {
      alertDialog.confirm({
        title: "保存更改",
        message: "您有未保存的更改，是否要保存？",
        confirmText: "保存",
        cancelText: "放弃",
        onConfirm: handleSave,
        onCancel: handleDiscard,
      });
    } else {
      open = false;
      dispatch("close");
    }
  }

  function handleCursorPosition(position: { top: number; left: number }) {
    console.log("ai-card 位置:");
    console.log(position);
    if (position && position.top > 0 && position.left > 0) {
      // 直接使用传入的top和left属性
      cursorPosition = {
        top: position.top,
        left: position.left,
      };
      showAICard = true;
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

  // 处理封面上传
  async function handleCoverUpload() {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";
    input.onchange = async (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        isUploading = true;
        uploadProgress = 0;
        try {
          // 清理之前的预览 URL
          if (localPreviewUrl) {
            URL.revokeObjectURL(localPreviewUrl);
          }

          // 创建新的本地预览
          localPreviewUrl = URL.createObjectURL(file);
          console.log("Local preview URL created:", localPreviewUrl);

          // 确保 coverImage 被正确设置
          coverImage = localPreviewUrl;
          console.log("Cover image set to:", coverImage);

          // 强制更新 UI
          await new Promise((resolve) => setTimeout(resolve, 0));

          // 准备上传到 ImgBB
          const formData = new FormData();
          formData.append("image", file);

          // 使用 XMLHttpRequest 来获取上传进度
          const xhr = new XMLHttpRequest();

          // 创建一个 Promise 来处理 XHR 请求
          const uploadPromise = new Promise<{
            success: boolean;
            data: { url: string };
            error?: { message: string };
          }>((resolve, reject) => {
            xhr.open(
              "POST",
              "https://api.imgbb.com/1/upload?key=dc1398dd7ba5dc154d50c82c42bf18c6",
              true,
            );

            // 监听上传进度
            xhr.upload.addEventListener("progress", (event) => {
              if (event.lengthComputable) {
                uploadProgress = Math.round((event.loaded / event.total) * 100);
                console.log(`Upload progress: ${uploadProgress}%`);
              }
            });

            // 监听请求完成
            xhr.addEventListener("load", () => {
              if (xhr.status >= 200 && xhr.status < 300) {
                try {
                  const result = JSON.parse(xhr.responseText);
                  resolve(result);
                } catch (e) {
                  reject(new Error("Failed to parse response"));
                }
              } else {
                reject(
                  new Error(`HTTP error: ${xhr.status} ${xhr.statusText}`),
                );
              }
            });

            // 监听请求错误
            xhr.addEventListener("error", () => {
              reject(new Error("Network error"));
            });

            // 发送请求
            xhr.send(formData);
          });

          // 等待上传完成
          const result = await uploadPromise;
          console.log("ImgBB upload result:", result);

          if (result.success) {
            // 使用 ImgBB 返回的 URL
            coverImage = result.data.url;
            console.log("Cover image set to ImgBB URL:", coverImage);

            // 标记有更改
            hasChanges = true;

            toast.success("封面上传成功");
          } else {
            throw new Error(result.error?.message || "上传失败");
          }
        } catch (error: any) {
          console.error("上传封面失败:", error);
          // 显示更详细的错误信息
          const errorMessage =
            error.message || error.response?.message || "上传封面失败";
          toast.error(`上传失败: ${errorMessage}`);
          // 如果上传失败，清除本地预览
          if (localPreviewUrl) {
            URL.revokeObjectURL(localPreviewUrl);
            localPreviewUrl = "";
            coverImage = "";
          }
        } finally {
          isUploading = false;
          uploadProgress = 0;
        }
      }
    };
    input.click();
  }

  // 处理保存
  async function handleSave() {
    // 检查文档内容
    let exportedDoc = newDoc ? await exportDocToJson(newDoc) : { content: "" };
    const eventData = {
      title: title.trim(),
      content: exportedDoc.content.trim(),
      location: locationData?.address || "",
      categories: selectedCategories,
      date: eventDate ? eventDate.toString() : "",
      user_id: $auth.user?.$id || "",
      cover: JSON.stringify({
        fileId: coverFileId,
        url: coverImage,
      }),
      location_data: locationData ? JSON.stringify(locationData) : "",
    };
    if (event?.$id) {
      await eventStore.updateEvent(event.$id, eventData);
    } else {
      await eventStore.createEvent(eventData);
    }
    hasChanges = false;
    open = false;
    dispatch("close");
  }

  // 处理放弃保存
  function handleDiscard() {
    // 清理本地预览 URL
    if (localPreviewUrl) {
      URL.revokeObjectURL(localPreviewUrl);
      localPreviewUrl = "";
    }
    hasChanges = false;
    open = false;
    dispatch("close");
  }

  // 处理选择已有图片
  function handleSelectExistingImage(event: CustomEvent<{ url: string }>) {
    coverImage = event.detail.url;
    hasChanges = true;
    isCoverSelectorOpen = false;
    toast.success("封面已设置");
  }

  // 处理上传图片
  function handleCoverUploadFromSelector() {
    handleCoverUpload();
    isCoverSelectorOpen = false;
  }

  // 处理链接提交
  function handleCoverLinkSubmit(event: CustomEvent<{ url: string }>) {
    coverImage = event.detail.url;
    hasChanges = true;
    isCoverSelectorOpen = false;
    toast.success("封面链接已设置");
  }

  // 处理标题悬停
  function handleTitleHover(isHovering: boolean) {
    showCoverButton = isHovering;
  }

  // 处理操作事件
  function handleAction(event: CustomEvent<{ type: string }>) {
    const { type } = event.detail;
    switch (type) {
      case "addRelatedEvent":
        // 处理添加相关事件
        break;
      case "addEvidence":
        // 处理添加证据
        break;
      case "addTimelinePoint":
        // 处理添加时间点
        break;
      case "addDimension":
        // 处理添加维度
        break;
    }
  }

  onMount(async () => {
    showContent = true;
    loadCategories();

    // 如果是在编辑模式下，初始化事件数据
    if (event) {
      await initializeEventData(event);
    }
    
  });

  // 组件销毁时清理
  onDestroy(() => {
    if (localPreviewUrl) {
      URL.revokeObjectURL(localPreviewUrl);
      localPreviewUrl = "";
    }
  });
</script>

{#snippet child()}
  {#if showContent}
    <!-- 使用封面区域组件 -->
    <div
      class="flex"
      in:fly={{ y: 20, duration: 500, delay: 200 }}
      out:fly={{ y: 20, duration: 500 }}
    >
      <EventCoverArea
        {coverImage}
        {isUploading}
        {uploadProgress}
        hideCloseButton={mode === "embedded"}
        hideActionButtons={mode === "embedded"}
        onClose={handleClose}
        on:coverUpload={handleCoverUpload}
        on:imageError={() => {
          console.error("Image load error");
          console.log("Failed image src:", coverImage);
          coverImage = "";
        }}
      />
    </div>

    <!-- 窗口容器 -->
    <div
      class="fixed left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] flex p-8"
      in:fly={{ y: 20, duration: 500, delay: 300 }}
      out:fly={{ y: 20, duration: 500 }}
    >
      <!-- 属性区域 -->
      <div
        in:fly={{ x: -20, duration: 500, delay: 400 }}
        out:fly={{ x: -20, duration: 500 }}
      >
        <EventPropertiesArea
          {createdAt}
          {lastModified}
          bind:eventDate
          bind:locationData
          bind:selectedCategories
          {categories}
          {evidenceCount}
          {timelinePointsCount}
        />
      </div>

      <!-- 使用新创建的组件 -->
      <div
        class="flex h-[80vh] gap-4"
        in:fly={{ x: 20, duration: 500, delay: 500 }}
        out:fly={{ x: 20, duration: 500 }}
      >
        <!-- 编辑器区域（包含标题和封面） -->
        <div class="w-[800px] relative">
          {#if showEditor}
            <EventEditorArea
              bind:title
              bind:doc={newDoc}
              {showAICard}
              onAIGenerate={() => (showAICard = !showAICard)}
              onEditorClick={handleEditorClick}
              onEditorInput={handleEditorInput}
              onCursorPosition={handleCursorPosition}
              onSave={handleSave}
              onTitleHover={handleTitleHover}
            />
          {/if}
          <div
          class="fixed right-[calc(50%-400px)] top-[calc(50%)] translate-y-[-50%] flex flex-col gap-4 z-10"
          in:fly={{ y: 100, duration: 500, delay: 600 }}
          out:fly={{ y: 100, duration: 500 }}
        >
        <EventActionsWidget
          {locationData}
          on:action={handleAction}
        />
          
        </div>
          <!-- 添加封面按钮 - 悬停时显示 -->
          <div
            role="banner"
            class="absolute -top-2 left-4 opacity-0 transition-opacity duration-200"
            class:opacity-100={showCoverButton}
            onmouseenter={() => (showCoverButton = true)}
            onmouseleave={() => (showCoverButton = false)}
          >
            <Popover bind:open={isCoverSelectorOpen}>
              <PopoverTrigger>
                <Button
                  variant="outline"
                  size="sm"
                  class="gap-1 bg-background/80 backdrop-blur-sm"
                >
                  <Plus class="h-3 w-3" />
                  <span class="text-xs">添加封面</span>
                </Button>
              </PopoverTrigger>
              <PopoverContent class="w-auto p-0" align="start">
                <CoverSelector
                  on:select={handleSelectExistingImage}
                  on:upload={handleCoverUploadFromSelector}
                  on:linkSubmit={handleCoverLinkSubmit}
                />
              </PopoverContent>
            </Popover>
          </div>
        </div>
      </div>
      <!-- 操作区域 -->
      <div
        class="w-[80px]"
        in:fly={{ x: 20, duration: 500, delay: 600 }}
        out:fly={{ x: 20, duration: 500 }}
      ></div>
    </div>
  {/if}
{/snippet}
{#if open}
  {#if mode === "window"}
    <div
      class="fixed inset-0 z-50 bg-background"
      in:fade={{ duration: 400 }}
      out:fade={{ duration: 400 }}
    >
      {@render child()}
    </div>
  {:else}
    {@render child()}
  {/if}
{/if}

<style>
  :global(.event-creator-window .affine-editor) {
    min-height: 100%;
    height: 100%;
    position: relative;
  }
</style>
