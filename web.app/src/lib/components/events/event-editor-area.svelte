<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Sparkles, Save, MapPin } from "lucide-svelte";
  import AffineEditor from "$lib/components/editor/affine-editor.svelte";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import type { Doc } from "@blocksuite/store";
  import MapBase from "$lib/components/map/map-base.svelte";
  import type { LocationData } from "$lib/components/map/types";

  let {
    title = $bindable(""),
    doc = $bindable(null),
    showAICard = false,
    onContentChange = (content: { content: string }) => {},
    onAIGenerate = () => {},
    onSave = () => {},
    onEditorClick = () => {},
    onEditorInput = () => {},
    onCursorPosition = (position: { top: number; left: number }) => {},
    onTitleHover = (isHovering: boolean) => {},
    locationData = $bindable(null),
    onLocationChange = (event: CustomEvent<LocationData>) => {},
  } = $props<{
    title: string;
    content?: string;
    doc: Doc | null;
    showAICard: boolean;
    onContentChange?: (content: { content: string }) => void;
    onAIGenerate?: () => void;
    onSave?: () => void;
    onEditorClick?: () => void;
    onEditorInput?: () => void;
    onCursorPosition?: (position: { top: number; left: number }) => void;
    onTitleHover?: (isHovering: boolean) => void;
    locationData?: LocationData | null;
    onLocationChange?: (event: CustomEvent<LocationData>) => void;
  }>();

  // 处理内容变化
  function handleContentChange(event: CustomEvent<{ content: string }>) {
    onContentChange({ content: event.detail.content });
  }

  // 处理AI生成
  function handleAIGenerate() {
    onAIGenerate();
  }

  // 处理保存
  function handleSave() {
    onSave();
  }

  // 处理编辑器点击
  function handleEditorClick() {
    onEditorClick();
  }

  // 处理编辑器输入
  function handleEditorInput() {
    onEditorInput();
  }

  // 处理光标位置变化
  function handleCursorPosition(
    event: CustomEvent<{ top: number; left: number }>,
  ) {
    onCursorPosition(event.detail);
  }

  // 处理按键事件
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Enter") {
      // 处理回车键
    }
  }

  // 处理标题悬停
  function handleTitleMouseEnter() {
    onTitleHover(true);
  }

  // 处理标题离开悬停
  function handleTitleMouseLeave() {
    onTitleHover(false);
  }
</script>

<div
  class="w-full py-4 sm:py-6 md:py-10 h-[60vh] sm:h-[70vh] md:h-[80vh] bg-white dark:bg-neutral-900 border border-neutral-200/50 dark:border-neutral-800/50 shadow-[0_4px_12px_rgba(0,0,0,0.05)] dark:shadow-[0_4px_12px_rgba(0,0,0,0.2)] duration-300 rounded-xl overflow-hidden flex flex-col"
>
  <!-- 标题输入框 -->
  <div
    class="py-3 sm:py-4 md:py-6 px-4 sm:px-8 md:px-14 flex items-center gap-2 sm:gap-3 md:gap-4"
    role="button"
    tabindex="0"
    onmouseenter={handleTitleMouseEnter}
    onmouseleave={handleTitleMouseLeave}
  >
    <div class="flex-1">
      <input
        type="text"
        placeholder="为你的神秘事件命名..."
        bind:value={title}
        class="event-title-input w-full bg-transparent text-2xl sm:text-3xl md:text-4xl font-semibold border-0 outline-none shadow-none focus:ring-0 px-0 py-0 h-auto placeholder:text-muted-foreground/40"
      />
    </div>
    <div class="flex items-center gap-1 sm:gap-2 border-l border-border/40 pl-2 sm:pl-3 md:pl-4">
      <Button
        variant="ghost"
        size="icon"
        class="h-6 w-6 sm:h-7 sm:w-7 md:h-8 md:w-8"
        onclick={handleAIGenerate}
      >
        <Sparkles class="h-3 w-3 sm:h-3.5 sm:w-3.5 md:h-4 md:w-4" />
      </Button>
      <Button
        variant="ghost"
        size="icon"
        class="h-6 w-6 sm:h-7 sm:w-7 md:h-8 md:w-8"
        onclick={handleSave}
      >
        <Save class="h-3 w-3 sm:h-3.5 sm:w-3.5 md:h-4 md:w-4" />
      </Button>
    </div>
  </div>

  <!-- 编辑器区域 -->
  <div class="flex-1 relative overflow-hidden">
    <ScrollArea class="w-full h-full pr-4 sm:pr-8 md:pr-20">
      <div
        role="button"
        tabindex="0"
        onkeydown={handleKeydown}
        class="w-full h-full -ml-4 sm:-ml-6 md:-ml-10"
        onclick={handleEditorClick}
        oninput={handleEditorInput}
      >
        <AffineEditor bind:doc on:cursorPosition={handleCursorPosition} />
      </div>
    </ScrollArea>
  </div>
</div>

<style>
  :global(.event-editor-area .scroll-area-viewport) {
    height: 100%;
  }

  :global(.event-editor-area .scroll-area-scrollbar) {
    z-index: 10;
  }
  
  :global(.mapboxgl-map) {
    border-radius: 2px !important;
  }
  
  :global(.map-container .mapboxgl-canvas) {
    border-radius: 2px !important;
  }
  
  :global(.map-container .mapboxgl-canvas-container) {
    border-radius: 2px !important;
  }

  /* 响应式样式 */
  @media (max-width: 640px) {
    :global(.event-editor-area .affine-editor) {
      font-size: 14px;
      line-height: 1.5;
    }
  }

  @media (min-width: 641px) and (max-width: 768px) {
    :global(.event-editor-area .affine-editor) {
      font-size: 15px;
      line-height: 1.6;
    }
  }

  @media (min-width: 769px) {
    :global(.event-editor-area .affine-editor) {
      font-size: 16px;
      line-height: 1.7;
    }
  }
</style>
