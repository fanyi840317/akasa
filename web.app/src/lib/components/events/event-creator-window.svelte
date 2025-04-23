<script lang="ts">
  import { fade, fly } from "svelte/transition";
  import { createEventDispatcher, onDestroy, onMount } from "svelte";
  import {
    Plus,
    Sparkles,
    Save,
    Network,
    Clock,
    Lightbulb,
    Search,
    Type,
    FileText,
    Tag,
    MessageSquare,
  } from "lucide-svelte";
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
    exportDocToJson,
    createDocByJson,
  } from "$lib/components/editor/affine-editor";
  import { ID } from "appwrite";
  import type { Doc } from "@blocksuite/store";
  import EventSidePanel from "./event-side-panel.svelte";
  import EventEditorArea from "./event-editor-area.svelte";
  import EventCoverArea from "./event-cover-area.svelte";
  import CoverSelector from "./cover-selector.svelte";
  import EventCommentsPanel from "./event-comments-panel.svelte";
  import { alertDialog } from "$lib/stores/alert-dialog";
  import EventActionsWidget from "./event-actions-widget.svelte";
  // TimelineHypothesisPanel 已集成到 EventSidePanel 中
  import { reverseGeocodeLocation } from "$lib/services/location";
  import { uploadToImgBB } from "$lib/services/image";

  const dispatch = createEventDispatcher();

  let {
    open = $bindable(false),
    event,
    mode = "window",
    isSidebarOpen = $bindable(true),
  } = $props<{
    open?: boolean;
    event?: import("$lib/types/event").Event;
    mode?: "window" | "embedded";
    isSidebarOpen?: boolean;
  }>();

  // 编辑器文档
  let newDoc = $state<Doc | null>(null);
  let locationData: Location | null = $state(null);
  let title = $state("");
  let coverImage = $state("");
  let coverFileId = "";
  let selectedCategories: string[] = $state([]);
  let eventDate = $state("");
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

  // 时间线和假说状态
  let timelineEvents = $state([]);
  let hypotheses = $state([]);

  // 评论状态
  let comments = $state([
    {
      id: "1",
      author: {
        name: "张三",
        avatar: "/images/avatars/user1.png",
      },
      content: "这个事件非常有趣，我想了解更多细节。",
      timestamp: new Date(Date.now() - 3600000 * 24),
      likes: 5,
      replies: [
        {
          id: "1-1",
          author: {
            name: "李四",
            avatar: "/images/avatars/user2.png",
          },
          content: "我同意，特别是关于时间线的部分很精彩。",
          timestamp: new Date(Date.now() - 3600000 * 12),
          likes: 2,
        },
      ],
    },
    {
      id: "2",
      author: {
        name: "王五",
        avatar: "/images/avatars/user3.png",
      },
      content: "我有一些补充资料可以分享，希望对研究有帮助。",
      timestamp: new Date(Date.now() - 3600000 * 48),
      likes: 3,
      replies: [],
    },
  ]);

  let isUploading = $state(false);
  let uploadProgress = $state(0);

  // 封面选择器状态
  let isCoverSelectorOpen = $state(false);
  let coverSelectorTab = $state("my-images");
  let coverLink = $state("");

  // 添加封面按钮显示状态
  let showCoverButton = $state(false);
  let showEditor = $state(event?.content ? false : true);

  let isLocation = $state(false);
  // 初始化事件数据
  async function initializeEventData(event: any) {
    if (event) {
      title = event.title || "";
      if (event.location_data) {
        // 检查 location_data 是否已经是对象
        if (typeof event.location_data === "object") {
          locationData = event.location_data;
        } else {
          // 尝试解析 JSON 字符串
          locationData = JSON.parse(event.location_data);
        }
      }
      selectedCategories = event.categories || [];
      eventDate = event.date;

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

      // 初始化时间线和假说数据
      if (event.entities_data) {
        try {
          // 如果 entities_data 是字符串数组，取第一个元素
          const entitiesDataStr = Array.isArray(event.entities_data)
            ? event.entities_data[0]
            : event.entities_data;
          const entities = JSON.parse(entitiesDataStr);

          // 如果有时间线数据，则提取并转换为 TimelineEvent 格式
          if (
            entities &&
            entities.timeline &&
            Array.isArray(entities.timeline)
          ) {
            timelineEvents = entities.timeline.map(
              (item: any, index: number) => ({
                id: `timeline-${index}`,
                timestamp: new Date(item.time),
                description: item.event,
                evidenceIds: [],
                witnessIds: [],
              }),
            );
            timelinePointsCount = timelineEvents.length;
          }
        } catch (e) {
          console.error("解析 entities_data 失败:", e);
          timelineEvents = [];
        }
      } else if (event.timeline_data) {
        try {
          timelineEvents = JSON.parse(event.timeline_data);
          timelinePointsCount = timelineEvents.length;
        } catch (e) {
          console.error("解析时间线数据失败:", e);
          timelineEvents = [];
        }
      }

      if (event.hypothesis_data) {
        try {
          hypotheses = JSON.parse(event.hypothesis_data);
        } catch (e) {
          console.error("解析假说数据失败:", e);
          hypotheses = [];
        }
      }
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
  function handleAIGenerate() {}

  // AI 操作列表
  const aiActions = [
    { icon: Type, label: "生成标题", action: "title", group: "generate" },
    { icon: FileText, label: "生成内容", action: "content", group: "generate" },
    { icon: Network, label: "提取关系图谱", action: "graph", group: "analyze" },
    { icon: Clock, label: "生成时间线", action: "timeline", group: "analyze" },
    {
      icon: Lightbulb,
      label: "生成假设",
      action: "hypothesis",
      group: "analyze",
    },
    { icon: Search, label: "提取线索", action: "clues", group: "analyze" },
    { icon: Tag, label: "提取实体", action: "entities", group: "analyze" },
  ];

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
  $effect(() => {
    if (locationData) {
      isLocation = true;
      if (
        locationData.coordinates?.lat === 0 &&
        locationData.coordinates?.lng === 0
      ) {
        isLocation = false;
        return;
      }
      if (locationData.coordinates && !locationData.name) {
        reverseGeocodeLocation(
          locationData.coordinates.lat,
          locationData.coordinates.lng,
        ).then((address) => {
          // 创建一个新的对象而不是修改原来的对象
          locationData = {
            ...locationData,
            name: address
          };
          isLocation = false;
        });
      }
    }
  });
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
          coverImage = localPreviewUrl;

          // 强制更新 UI
          await new Promise((resolve) => setTimeout(resolve, 0));

          // 使用封装的上传服务
          const result = await uploadToImgBB(file, (progress) => {
            uploadProgress = progress.percentage;
          });

          if (result.success) {
            coverImage = result.data!.url;
            hasChanges = true;
            toast.success("封面上传成功");
          } else {
            throw new Error(result.error?.message || "上传失败");
          }
        } catch (error: any) {
          console.error("上传封面失败:", error);
          const errorMessage =
            error.message || error.response?.message || "上传封面失败";
          toast.error(`上传失败: ${errorMessage}`);
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
      location: locationData?.name || "",
      categories: selectedCategories,
      date: eventDate ? eventDate.toString() : "",
      user_id: $auth.user?.$id || "",
      cover: JSON.stringify({
        fileId: coverFileId,
        url: coverImage,
      }),
      location_data: locationData || undefined,
      // 添加时间线和假说数据
      timeline_data: timelineEvents.length ? JSON.stringify(timelineEvents) : "",
      hypothesis_data: hypotheses.length ? JSON.stringify(hypotheses) : "",
    };
    let obj = null;
    try {
      let updatedEvent;
      if (event?.$id) {
        updatedEvent = await eventStore.updateEvent(event.$id, eventData);
      } else {
        updatedEvent = await eventStore.createEvent(eventData);
      }
      hasChanges = false;

      // 只在窗口模式下关闭
      if (obj && mode === "window") {
        open = false;
        dispatch("close");
      }
    } catch (e) {
      alert(e);
      console.error(e);
    }
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

  // 处理评论相关操作
  function handleCommentAdded(event: CustomEvent<{ comment: any }>) {
    hasChanges = true;
    // 这里可以添加将评论保存到数据库的逻辑
  }

  function handleCommentLiked(event: CustomEvent<{ commentId: string }>) {
    hasChanges = true;
    // 这里可以添加将点赞保存到数据库的逻辑
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
      class="fixed inset-0 top-12 left-0 z-0"
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
      class={mode === "window"
        ? "absolute left-[50%] top-[50%] translate-y-[-50%] translate-x-[-50%] flex z-50 event-creator-window"
        : "flex item-center justify-center event-creator-window"}
      in:fly={{ y: 20, duration: 500, delay: 300 }}
      out:fly={{ y: 20, duration: 500 }}
    >
      <!-- 属性和时间线区域 -->
      {#if isSidebarOpen}
      <div
        class="py-[48px]"
        in:fly={{ x: -20, duration: 300 }}
        out:fly={{ x: -20, duration: 300 }}
      >
        <!-- 左侧面板内容已移动到右侧 -->
      </div>
      {/if}

      <!-- 主要内容区域 -->
      <div
        class="flex gap-4 overflow-hidden flex-1 item-center justify-center transition-all duration-300"
        style="width: {isSidebarOpen ? 'auto' : '100%'};"
        in:fly={{ x: 20, duration: 500, delay: 500 }}
        out:fly={{ x: 20, duration: 500 }}
      >
        <!-- 编辑器工具栏 -->
        <div class="min-w-[800px] w-full h-[100vh] border border-l-0 rounded-tr-xl relative">
          {#if showEditor}
            <EventEditorArea
              bind:title
              bind:doc={newDoc}
              {showAICard}
              onEditorClick={handleEditorClick}
              onEditorInput={handleEditorInput}
              onCursorPosition={handleCursorPosition}
              onTitleHover={handleTitleHover}
              onSave={handleSave}
            />
          {/if}

          <!-- 保存按钮 -->
          <div class="absolute top-0 right-0 z-10 border-b border-l rounded-tr-xl rounded-bl-xl bg-background
          flex items-center px-6 py-4 text-xs text-muted-foreground cursor-pointer hover:bg-muted/50 transition-colors">
            <Save class="h-4 w-4 mr-2" />
              保存
          </div>
        </div>
      </div>

      <!-- 评论区域 -->
      {#if isSidebarOpen}
      <div
        class="h-full"
        in:fly={{ x: 20, duration: 300 }}
        out:fly={{ x: 20, duration: 300 }}
      >
        <EventSidePanel
          bind:eventDate
          bind:locationData
          bind:isLocation
          bind:selectedCategories
          {categories}
          bind:timelineEvents
          bind:hypotheses
          entitiesData={event?.entities_data?.[0]}
          onToggleSidebar={() => {
            isSidebarOpen = !isSidebarOpen;
          }}
        />
        <!-- <EventCommentsPanel
          bind:comments
          eventId={event?.$id || eventId}
        /> -->
      </div>
      {/if}
      <!-- 时间线和假说操作区域已移动到左侧面板 -->
      <!-- 已删除 -->
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
  :global(.event-creator-window) {
    /* max-height: 90vh; */
    overflow: hidden;
  }
</style>
