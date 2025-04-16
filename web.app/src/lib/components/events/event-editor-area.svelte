<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { Input } from "$lib/components/ui/input";
  import { MapPin, MapPinIcon, CalendarIcon } from "lucide-svelte";
  import EventTitleActions from "./event-title-actions.svelte";
  import AffineEditor from "$lib/components/editor/affine-editor.svelte";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import type { Doc } from "@blocksuite/store";
  import MapBase from "$lib/components/map/map-base.svelte";
  import EventAnalysisCards from "./event-analysis-cards.svelte";

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
  }>();

  // 处理内容变化
  function handleContentChange(event: CustomEvent<{ content: string }>) {
    onContentChange({ content: event.detail.content });
  }

  // 处理AI生成

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
  class="w-full py-8 h-[90vh] bg-white dark:bg-neutral-900 border border-neutral-200/50 dark:border-neutral-800/50 shadow-[0_4px_12px_rgba(0,0,0,0.05)] dark:shadow-[0_4px_12px_rgba(0,0,0,0.2)] duration-300 rounded-xl overflow-hidden flex flex-col"
>
  <!-- 标题输入框 -->
  <div
    class="py-6 px-14 flex items-center gap-4"
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
        class="event-title-input w-full bg-transparent text-4xl font-semibold border-0 outline-none shadow-none focus:ring-0 px-0 py-0 h-auto placeholder:text-muted-foreground/40"
      />
    </div>
    <EventTitleActions {onAIGenerate} onSave={handleSave} />
  </div>

  <!-- 编辑器区域 -->
  <div class="flex-1 relative overflow-hidden">
    <ScrollArea class="w-full h-full pl-12 pr-4">
      <div
        role="button"
        tabindex="0"
        onkeydown={handleKeydown}
        class="w-full h-full flex gap-4"
        onclick={handleEditorClick}
        oninput={handleEditorInput}
      >
        <AffineEditor
          class="flex-1"
          bind:doc
          on:cursorPosition={handleCursorPosition}
        />
        <EventAnalysisCards />
      </div>
    </ScrollArea>
  </div>
</div>

<style>
</style>
