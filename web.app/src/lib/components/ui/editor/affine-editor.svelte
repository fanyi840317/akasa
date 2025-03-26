<script lang="ts">
  import { onDestroy, onMount, createEventDispatcher } from "svelte";
  import { signal } from "@preact/signals-core";
  import { mode } from "mode-watcher";
  import { createEmptyDoc, AffineEditorContainer } from "@blocksuite/presets";
  import {
    ColorScheme,
    OverrideThemeExtension,
    ParagraphBlockSchema,
    ParagraphBlockService,
    SpecProvider,
    type ThemeExtension,
  } from "@blocksuite/blocks";
  import { get } from "svelte/store";
  import { createDocByHtml, exportDoc } from "./affine-editor";

  const dispatch = createEventDispatcher();

  let { htmlDoc, shouldReset = false, class: className = "" } = $props();
  let editorContainer: HTMLDivElement;
  let editor: AffineEditorContainer | null = null;
  let isInitialized = false;
  let contentUpdateTimeout: NodeJS.Timeout;

  const themeExtension: ThemeExtension = {
    getAppTheme: () => {
      const currentTheme = get(mode);
      return signal(
        currentTheme === "dark" ? ColorScheme.Dark : ColorScheme.Light,
      );
    },
  };

  async function setupEditor() {
    if (!editorContainer) return;

    cleanup(); // 确保清理旧的编辑器

    try {
      // 创建新的编辑器实例
      editor = new AffineEditorContainer();

      // 创建文档
      let doc = createEmptyDoc().init();
      if (htmlDoc.content) {
        const existingDoc = await createDocByHtml(htmlDoc.content);
        if (existingDoc) {
          doc = existingDoc;
        }
      }
      editor.doc = doc;
      htmlDoc.doc = doc;

      // 设置编辑器变化监听
      editor.doc.slots.historyUpdated.on(async () => {
        clearTimeout(contentUpdateTimeout);
        contentUpdateTimeout = setTimeout(async () => {
          if (editor?.doc) {
            const content = await exportDoc(editor.doc);
            if (content) {
              dispatch("contentChange", content);
            }
          }
        }, 300);
      });

      // 应用主题扩展到编辑器
      if (editor.pageSpecs) {
        const pageSpecs = SpecProvider.getInstance().getSpec("page");
        pageSpecs.extend([OverrideThemeExtension(themeExtension)]);
        editor.pageSpecs = pageSpecs.value;
        const paragraphService: ParagraphBlockService | null =
          editor.std.getService("affine:paragraph");
        if (paragraphService) {
          paragraphService.placeholderGenerator = (model) => {
            const placeholders = {
              text: "输入 '/' 使用命令，或按 'Enter' 创建新段落",
              h1: "标题 1",
              h2: "标题 2",
              h3: "标题 3",
              h4: "标题 4",
              h5: "标题 5",
              h6: "标题 6",
              quote: "",
            };
            return placeholders[model.type];
          };
        }
      }

      // 添加编辑器到容器
      editorContainer.appendChild(editor);
      isInitialized = true;

      // 等待编辑器完全挂载后更新内容
      await editor.updateComplete;

      setTimeout(() => {
        const richText = editor?.host?.querySelector("rich-text");
        if (richText) {
          const inlineEditor = (richText as any).inlineEditor;
          if (inlineEditor) {
            inlineEditor.focusEnd();
          }
        }
      }, 200);
    } catch (error) {
      console.error("Editor initialization failed:", error);
      cleanup();
    }
  }

  function cleanup() {
    clearTimeout(contentUpdateTimeout);
    if (editor) {
      try {
        editor.doc?.dispose();
        editor.disposables?.dispose();
        if (editorContainer?.contains(editor)) {
          editorContainer.removeChild(editor);
        }
      } catch (error) {
        console.error("Editor cleanup error:", error);
      }
      editor = null;
    }
    isInitialized = false;
  }

  // 监听属性变化
  $effect(() => {
    if (shouldReset) {
      cleanup();
      setupEditor();
    }
  });

  // 监听内容变化
  // $effect(() => {
  //   if (htmlDoc.content !== undefined && isInitialized && editor?.doc) {
  //     const currentEditor = editor;
  //     createDocByHtml(htmlDoc.content).then(doc => {
  //       if (doc && currentEditor) {
  //         currentEditor.doc = doc;
  //         htmlDoc.doc = doc;
  //       }
  //     });
  //   }
  // });

  onMount(() => {
    setupEditor();
  });

  onDestroy(() => {
    cleanup();
  });
</script>

<div bind:this={editorContainer} class={className}></div>

<style>
  :global(embed-card-create-modal .embed-card-modal-mask) {
    z-index: 200000;
  }
  :global(embed-card-create-modal .embed-card-modal-wrapper) {
    z-index: 200001;
  }
  /* 隐藏文档标题 */
  /* :global(doc-title) {
    display: none !important;
  } */
</style>
