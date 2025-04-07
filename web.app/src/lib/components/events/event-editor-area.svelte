<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Sparkles, Save } from "lucide-svelte";
  import AffineEditor from "$lib/components/editor/affine-editor.svelte";
  import type { Doc } from "@blocksuite/store";

  let { 
    title = "",
    content = "",
    doc = null,
    showAICard = false,
    onTitleChange = (value: string) => {},
    onContentChange = (content: { content: string }) => {},
    onAIGenerate = () => {},
    onSave = () => {},
    onEditorClick = () => {},
    onEditorInput = () => {},
    onCursorPosition = (position: { top: number; left: number }) => {}
  } = $props<{
    title: string;
    content?: string;
    doc: Doc | null;
    showAICard: boolean;
    onTitleChange?: (value: string) => void;
    onContentChange?: (content: { content: string }) => void;
    onAIGenerate?: () => void;
    onSave?: () => void;
    onEditorClick?: () => void;
    onEditorInput?: () => void;
    onCursorPosition?: (position: { top: number; left: number }) => void;
  }>();

  // 处理标题变化
  function handleTitleChange(event: Event) {
    const target = event.target as HTMLInputElement;
    onTitleChange(target.value);
  }

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
  function handleCursorPosition(event: CustomEvent<{ top: number; left: number }>) {
    onCursorPosition(event.detail);
  }
  
  // 处理输入事件
  function handleInput(event: Event) {
    const target = event.target as HTMLInputElement;
    onTitleChange(target.value);
  }
  
  // 处理按键事件
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Enter") {
      // 处理回车键
    }
  }
</script>

<div class="w-[800px] h-[80vh] bg-white dark:bg-neutral-900 border border-neutral-200/50 dark:border-neutral-800/50 shadow-[0_4px_12px_rgba(0,0,0,0.05)] dark:shadow-[0_4px_12px_rgba(0,0,0,0.2)] duration-300 rounded-xl overflow-hidden flex flex-col">
 
  <!-- 标题输入框 -->
  <div class=" py-6 mt-10">
    <div class="px-16 max-w-4xl mx-auto">
      <div class="flex items-center gap-4">
        <div class="flex-1">
          <input
            type="text"
            placeholder="为你的神秘事件命名..."
            bind:value={title}
            class="event-title-input w-full bg-transparent text-4xl font-semibold border-0 outline-none shadow-none focus:ring-0 px-0 py-0 h-auto placeholder:text-muted-foreground/40"
            oninput={handleInput}
          />
        </div>
        <div class="flex items-center gap-2 border-l border-border/40 pl-4">
          <Button
            variant="ghost"
            size="icon"
            class="h-8 w-8"
            onclick={handleAIGenerate}
          >
            <Sparkles class="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            class="h-8 w-8"
            onclick={handleSave}
          >
            <Save class="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  </div>

  <!-- 编辑器区域 -->
  <div class="flex-1 relative">
    <div
      role="button"
      tabindex="0"
      onkeydown={handleKeydown}
      class="w-full h-full -ml-7"
      onclick={handleEditorClick}
      oninput={handleEditorInput}
    >
      <AffineEditor
        bind:doc={doc}
        on:cursorPosition={handleCursorPosition}
      />
    </div>
  </div>
</div> 