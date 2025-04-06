<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Sparkles, Save } from "lucide-svelte";
  import AffineEditor from "$lib/components/editor/affine-editor.svelte";
  import type { Doc } from "@blocksuite/store";

  const dispatch = createEventDispatcher();

  let { 
    title = "",
    content = "",
    doc = null,
    showAICard = false,
    coverImage = ""
  } = $props<{
    title: string;
    content?: string;
    doc: Doc | null;
    showAICard: boolean;
    coverImage: string;
  }>();

  // 处理标题变化
  function handleTitleChange(event: Event) {
    const target = event.target as HTMLInputElement;
    dispatch("titleChange", { title: target.value });
  }

  // 处理内容变化
  function handleContentChange(event: CustomEvent<{ content: string }>) {
    dispatch("contentChange", { content: event.detail.content });
  }

  // 处理AI生成
  function handleAIGenerate() {
    dispatch("aiGenerate");
  }

  // 处理保存
  function handleSave() {
    dispatch("save");
  }

  // 处理编辑器点击
  function handleEditorClick() {
    dispatch("editorClick");
  }

  // 处理编辑器输入
  function handleEditorInput() {
    dispatch("editorInput");
  }

  // 处理光标位置变化
  function handleCursorPosition(event: CustomEvent<{ top: number; left: number }>) {
    dispatch("cursorPosition", event.detail);
  }
  
  // 处理输入事件
  function handleInput(event: Event) {
    const target = event.target as HTMLInputElement;
    dispatch("titleChange", { title: target.value });
  }
  
  // 处理按键事件
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Enter") {
      // 处理回车键
    }
  }
</script>

<div class="w-[800px] h-[80vh] bg-white dark:bg-neutral-900 border border-neutral-200/50 dark:border-neutral-800/50 shadow-[0_4px_12px_rgba(0,0,0,0.05)] dark:shadow-[0_4px_12px_rgba(0,0,0,0.2)] duration-300 rounded-xl overflow-hidden flex flex-col">
  <!-- 封面区域 -->
  {#if coverImage}
    <div class="relative h-[200px] overflow-hidden">
      <img
        src={coverImage}
        alt="封面"
        class="w-full h-full object-cover"
      />
    </div>
  {/if}

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
            oninput={(e) => {
              const target = e.target as HTMLInputElement;
              dispatch("titleChange", target.value);
            }}
          />
        </div>
        <div class="flex items-center gap-2 border-l border-border/40 pl-4">
          <Button
            variant="ghost"
            size="icon"
            class="h-8 w-8"
            onclick={() => dispatch("aiGenerate")}
          >
            <Sparkles class="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            class="h-8 w-8"
            onclick={() => dispatch("save")}
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