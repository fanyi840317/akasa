<script lang="ts">
  import {
    AffineEditorContainer,
    createEmptyDoc,
    EdgelessEditor,
  } from "@blocksuite/presets";
  import { signal } from "@preact/signals-core";
  import {
    ColorScheme,
    DocModeExtension,
    DocModeProvider,
    OverrideThemeExtension,
    ParagraphBlockService,
    SpecProvider,
    type DocMode,
    type ThemeExtension,
  } from "@blocksuite/blocks";
  import { onMount, onDestroy } from "svelte";
  import { appStore } from "$lib/stores/appState";
  import "@toeverything/theme/style.css";
  import type { ExtensionType } from "@blocksuite/block-std";
  import { Slot } from "@blocksuite/store";
  import type { Disposable } from '@blocksuite/global/utils';

  let editorContainer: HTMLDivElement;
  appStore.setShowHeader(false);
  const currentTheme = document.documentElement.dataset.theme;
  const colorScheme =
    currentTheme === "black" ? ColorScheme.Dark : ColorScheme.Light;
  const themeExtension: ThemeExtension = {
    getAppTheme: () => {
      return signal(colorScheme);
    },
    getEdgelessTheme: () => {
      return signal(colorScheme);
    },
  };
  const override_doc_mode_extension = (
    editor: AffineEditorContainer
  ): ExtensionType => {
    const DOC_MODE = "edgeless"; // fixed to edgeless mode
    const doc_slots = new Map<string, Slot<DocMode>>();
    const service: DocModeProvider = {
      setPrimaryMode: (_mode: DocMode, doc_id: string): void => {
        doc_slots.get(doc_id)?.emit(DOC_MODE);
      },
      getPrimaryMode: (_doc_id: string): DocMode => {
        return DOC_MODE;
      },
      togglePrimaryMode: (_doc_id: string): DocMode => {
        return DOC_MODE;
      },
      onPrimaryModeChange: (
        handler: (mode: DocMode) => void,
        doc_id: string
      ): Disposable => {
        if (!doc_slots.has(doc_id)) {
          doc_slots.set(doc_id, new Slot<DocMode>());
        }
        return doc_slots.get(doc_id)!.on(handler);
      },
      setEditorMode: (_mode: DocMode): void => {
        editor.switchEditor(DOC_MODE);
      },
      getEditorMode: (): DocMode | null => editor.mode,
    };
    return DocModeExtension(service);
  };

  onMount(async () => {
    const doc = createEmptyDoc().init();
    doc;
    console.log(doc);
    const editor = new AffineEditorContainer();
    editor.doc = doc;
    

    editor.mode = "edgeless";
    // 应用主题扩展到编辑器
    if (editor.edgelessSpecs) {
      const edgelessSpecs = SpecProvider.getInstance().getSpec("edgeless");
      edgelessSpecs.extend([OverrideThemeExtension(themeExtension), override_doc_mode_extension(editor)]);
      editor.edgelessSpecs = edgelessSpecs.value;
    }

    // const paragraphService: ParagraphBlockService | null =
    //   editor.std.getService("affine:paragraph");
    // if (paragraphService) {
    //   paragraphService.placeholderGenerator = (model) => {
    //     const placeholders = {
    //       text: "输入 '/' 使用命令，或按 'Enter' 创建新段落",
    //       h1: "标题 1",
    //       h2: "标题 2",
    //       h3: "标题 3",
    //       h4: "标题 4",
    //       h5: "标题 5",
    //       h6: "标题 6",
    //       quote: "",
    //     };
    //     return placeholders[model.type];
    //   };
    // }
    editorContainer.appendChild(editor);
    await editor.updateComplete;
  });
  onDestroy(() => {
    appStore.setShowHeader(true);
  });
</script>

<div class="w-full">
  <div class="h-[calc(100vh)]" bind:this={editorContainer}></div>
</div>
