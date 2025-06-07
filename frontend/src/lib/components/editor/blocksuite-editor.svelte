<script lang="ts">
  import { AffineEditorContainer, createEmptyDoc } from "@blocksuite/presets";
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
  import { onMount, onDestroy, createEventDispatcher } from "svelte";
  
  const dispatch = createEventDispatcher();

  import "@toeverything/theme/style.css";
  import { Doc, Slot } from "@blocksuite/store"; // Added Doc
  import type { Disposable } from "@blocksuite/global/utils";
  import { createDocByJson, exportDocToJson } from "./editor-doc";

  // Import effects if they are not globally initialized elsewhere
  import { effects as blocksEffects } from "@blocksuite/blocks/effects";
  import { effects as presetsEffects } from "@blocksuite/presets/effects";

  import { EdgelessCoverToolButton } from "./toolbar/cover/cover-button";
  import { EdgelessAIToolButton } from "./toolbar/ai/ai-button";
  import { auth } from "$lib/stores/auth";
  import CoverSelector from "./toolbar/cover/cover-selector.svelte";
  import AIModal from "./toolbar/ai/ai-modal.svelte";
  import AIFeatureHandler from "./toolbar/ai/ai-feature-handler.svelte";
  import { Card } from "../ui";

  import { EdgelessMapToolButton } from "./toolbar/map/map-button";
  import { cn } from "$lib/utils";
  // Ensure effects are initialized only once globally
  if (!(window as any).__blocksuite_effects_initialized) {
    blocksEffects();
    presetsEffects();
    customElements.define(
      "edgeless-cover-tool-button",
      EdgelessCoverToolButton
    );

    customElements.define("edgeless-map-tool-button", EdgelessMapToolButton);
    customElements.define("edgeless-ai-tool-button", EdgelessAIToolButton);
    (window as any).__blocksuite_effects_initialized = true;
  }

  // export let docId: string | undefined = undefined; // Optional prop to load an existing doc
  // export let initialJsonContent: string | undefined = undefined; // New prop for initial JSON content
  let { initialJsonContent = undefined, class: className, readonly = $bindable(false) } = $props<{
    initialJsonContent: string | undefined;
    class: string;
    readonly?: boolean;
  }>();
  let editorContainer: HTMLDivElement;
  let editor: AffineEditorContainer;
  let resizeObserver: ResizeObserver | null = null;

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
  function removeTemporaryElements() {
    const toolbarWidget = document.querySelector("edgeless-toolbar-widget");
      if (!toolbarWidget) {
        return;
      }

      const templateButton = toolbarWidget.shadowRoot?.querySelector(
        "edgeless-template-button"
      );
      // const cover = document.createElement("edgeless-cover-tool-button");

      templateButton?.parentElement?.remove();
  }
  onMount(async () => {
    let doc: Doc | undefined = undefined;

    if (initialJsonContent) {
      try {
        const jsonData = initialJsonContent;
        // User is expected to provide `createDocByJson` function.
        // This function should take a docId and the parsed custom JSON,
        // and return an initialized BlockSuite Doc instance.
        // The `declare function createDocByJson` above is a placeholder.
        // Ensure this function is properly imported and available in scope.
        doc = await createDocByJson(jsonData);

        if (!(doc instanceof Doc)) {
          console.error(
            "createDocByJson did not return a Doc instance, falling back."
          );
          throw new Error("createDocByJson did not return a Doc instance");
        }
        // Assuming createDocByJson returns an initialized/loaded Doc.
        // If not, doc.load() or similar might be needed here.
      } catch (e) {
        console.error(
          "Failed to create document using createDocByJson or provided JSON is invalid:",
          e
        );
        // Fallback to an empty doc with the given ID
        doc = createEmptyDoc().init();
      }
    } else {
      // If no initial content, create a new empty doc
      doc = createEmptyDoc().init();
    }

    editor = new AffineEditorContainer();
    editor.doc = doc;
    editor.mode = "edgeless";
    
    // 设置编辑器的只读模式
    if (readonly) {
      editor.doc.awarenessStore.setReadonly(doc.blockCollection,true);
    }

    const edgelessSpecs = SpecProvider.getInstance().getSpec("edgeless");
    edgelessSpecs.extend([
      OverrideThemeExtension(themeExtension),
      DocModeExtension(createDocModeProvider(editor)),
    ]);
    editor.edgelessSpecs = edgelessSpecs.value;

    // Example: Add a block to the surface
    // let surface = doc.getBlocksByFlavour("affine:surface")[0];
    // if (surface) {
    //   doc.addBlock(
    //     'affine:embed-github',
    //     {
    //       url: 'https://github.com/Milkdown/milkdown/pull/1215',
    //       xywh: '[500, 400, 752, 116]',
    //     },
    //     (surface as Block)?.id
    //   );
    // }

    editorContainer.appendChild(editor);
    await editor.updateComplete;
    // <div class="full-divider"></div>
    setTimeout(() => {
      removeTemporaryElements();
    }, 100);

    // 创建 ResizeObserver 监听容器大小变化
    resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        // 当容器大小变化时，延迟调用 removeTemporaryElements
        setTimeout(() => {
          removeTemporaryElements();
        }, 100);
      }
    });

    // 开始观察编辑器容器
    resizeObserver.observe(editorContainer);
  });

  // 监听readonly属性变化，动态切换编辑器的只读模式
  $effect(() => {
    if (editor && editor.doc) {
      editor.doc.awarenessStore.setReadonly(editor.doc.blockCollection,readonly);
    }
  });

  onDestroy(() => {
    // 清理 ResizeObserver
    if (resizeObserver) {
      resizeObserver.disconnect();
      resizeObserver = null;
    }
    // editor?.dispose(); // Consider disposing the editor if necessary
  });
  export async function getContent() {
    return await exportDocToJson(editor.doc);
  }
  
</script>

<div class={cn("w-full h-full ",className)} bind:this={editorContainer}>

</div>


