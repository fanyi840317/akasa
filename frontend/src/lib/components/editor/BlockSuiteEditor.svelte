<script lang="ts">
  import {
    AffineEditorContainer,
    createEmptyDoc,
  } from "@blocksuite/presets";
  import { signal } from "@preact/signals-core";
  import {
    ColorScheme,
    DocModeExtension,
    DocModeProvider,
    OverrideThemeExtension,
    SpecProvider,
    type DocMode,
    type ThemeExtension,
  } from "@blocksuite/blocks";
  import { onMount, onDestroy } from "svelte";
  import { appStore } from "$lib/stores/app-state";
  import "@toeverything/theme/style.css";
  import { Block, Slot } from "@blocksuite/store";
  import type { Disposable } from "@blocksuite/global/utils";

  // Import effects if they are not globally initialized elsewhere
  // import { effects as blocksEffects } from "@blocksuite/blocks/effects";
  // import { effects as presetsEffects } from "@blocksuite/presets/effects";
  // blocksEffects();
  // presetsEffects();

  export let docId: string | undefined = undefined; // Optional prop to load an existing doc

  let editorContainer: HTMLDivElement;
  let editor: AffineEditorContainer;

  const currentTheme = document.documentElement.dataset.theme;
  const colorScheme =
    currentTheme === "black" ? ColorScheme.Dark : ColorScheme.Light;

  const themeExtension: ThemeExtension = {
    getAppTheme: () => signal(colorScheme),
    getEdgelessTheme: () => signal(colorScheme),
  };

  const createDocModeProvider = (
    editorInstance: AffineEditorContainer
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
        doc_id: string
      ): Disposable => {
        if (!doc_slots.has(doc_id)) {
          doc_slots.set(doc_id, new Slot<DocMode>());
        }
        return doc_slots.get(doc_id)!.on(handler);
      },
      setEditorMode: (_mode: DocMode): void => {
        editorInstance.switchEditor(DOC_MODE);
      },
      getEditorMode: (): DocMode | null => editorInstance.mode,
    };
    return service;
  };

  onMount(async () => {
    // Initialize effects here if they are specific to this component and not globally run
    // This might be necessary if BlockSuite doesn't automatically handle this
    // or if you want to ensure they run before editor initialization.
    // Consider if `blocksEffects()` and `presetsEffects()` need to be called here.

    const doc = createEmptyDoc().init();
    // TODO: Implement logic to load existing doc if docId is provided

    editor = new AffineEditorContainer();
    editor.doc = doc;
    editor.mode = "edgeless";

    // Apply theme and mode extensions
    const edgelessSpecs = SpecProvider.getInstance().getSpec("edgeless");
    edgelessSpecs.extend([
      OverrideThemeExtension(themeExtension),
      DocModeExtension(createDocModeProvider(editor)),
    ]);
    editor.edgelessSpecs = edgelessSpecs.value;

    // Example: Add a block to the surface
    let surface = doc.getBlocksByFlavour("affine:surface")[0];
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

    editorContainer.appendChild(editor);
    await editor.updateComplete;

    // Hide header if appStore is used for global state
    appStore.setShowHeader(false);
  });

  onDestroy(() => {
    // Show header again when component is destroyed
    appStore.setShowHeader(true);
    // Dispose of the editor instance if necessary
    // editor?.dispose();
  });
</script>

<div class="w-full h-full" bind:this={editorContainer}></div>