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
  import { appStore } from "$lib/stores/app-state";
  // import "@toeverything/theme/style.css";
  import type { ExtensionType } from "@blocksuite/block-std";
  import { Block, Slot } from "@blocksuite/store";
  import type { Disposable } from "@blocksuite/global/utils";

//   import { effects as blocksEffects } from "@blocksuite/blocks/effects";
// import { effects as presetsEffects } from "@blocksuite/presets/effects";
// blocksEffects();
// presetsEffects();
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
  const createDocModeProvider = (
    editor: AffineEditorContainer,
  ): DocModeProvider => {
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
        doc_id: string,
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
    return service;
  };

  onMount(async () => {
    const doc = createEmptyDoc().init();
    console.log(doc);
    const editor = new AffineEditorContainer();

    let surface = doc.getBlocksByFlavour("affine:surface")[0];
    alert(surface.id);
    if (surface) {
      doc.addBlock(
      'affine:embed-github',
      {
        url: 'https://github.com/Milkdown/milkdown/pull/1215',
        xywh: '[500, 400, 752, 116]',
      },
      (surface as Block)?.id
    );
    }
    editor.doc = doc;

    editor.mode = "edgeless";
    // 应用主题扩展到编辑器
    if (editor.edgelessSpecs) {
      const edgelessSpecs = SpecProvider.getInstance().getSpec("edgeless");
      edgelessSpecs.extend([
        OverrideThemeExtension(themeExtension),
        DocModeExtension(createDocModeProvider(editor)),
      ]);
      editor.edgelessSpecs = edgelessSpecs.value;
    }

    
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
