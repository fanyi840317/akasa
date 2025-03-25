<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import "@toeverything/theme/style.css";
  import { signal, type Signal } from "@preact/signals-core";
  import { ModeWatcher, mode } from "mode-watcher";
  import { HtmlTransformer } from "@blocksuite/blocks";

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
  import { ServiceProvider, ServiceResolver } from "@blocksuite/global/di";
  import { createDocByHtml } from "./affine-editor";

  let { htmlDoc, class: className = "" } = $props();
  let editorContainer: HTMLDivElement;
  let editor: AffineEditorContainer | null = null;
  const themeExtension: ThemeExtension = {
    getAppTheme: () => {
      const currentTheme = get(mode);
      return signal(
        currentTheme === "dark" ? ColorScheme.Dark : ColorScheme.Light
      );
    },
  };
  // 编辑器实例将在onMount中创建

  onMount(async () => {
    // 初始化编辑器
    // 创建编辑器实例
    editor = new AffineEditorContainer();
    
    let doc = await createDocByHtml(htmlDoc.content);
    htmlDoc.doc=doc;    
    if (!doc) {
      doc = createEmptyDoc().init();
    }
    editor.doc = doc;

    if (editorContainer && editor) {
      // // 设置暗色主题7

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
              text: "Type '/' for commands, or type 'Enter' for paragraph",
              h1: "Heading 1",
              h2: "Heading 2",
              h3: "Heading 3",
              h4: "Heading 4",
              h5: "Heading 5",
              h6: "Heading 6",
              quote: "",
            };
            return placeholders[model.type];
          };
        }
        // console.log('pageSpecs', SpecProvider.getInstance().getSpec(ParagraphBlockSchema.model.flavour));
      }

      // 添加编辑器到容器
      editorContainer.appendChild(editor);

      // 等待编辑器完全挂载后尝试聚焦
      editor.updateComplete.then(() => {
        // 简化的聚焦逻辑
        setTimeout(() => {
          const richText = editor?.host?.querySelector("rich-text");
          if (richText) {
            const inlineEditor = (richText as any).inlineEditor;
            if (inlineEditor) {
              inlineEditor.focusEnd();
            }
          }
        }, 200);
      });
    }
  });

  onDestroy(() => {
    if (editorContainer && editor && editorContainer.contains(editor)) {
      editorContainer.removeChild(editor);
      editor.disposables?.dispose();
    }
  });

</script>

<div
  bind:this={editorContainer}
  data-theme="dark"
  style="width: 100%; height: 100%; position: relative; overflow: auto;"
></div>

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
