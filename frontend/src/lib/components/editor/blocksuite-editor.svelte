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
  import { onMount, onDestroy } from "svelte";

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
  let { initialJsonContent = undefined, class: className, readonly = false } = $props<{
    initialJsonContent: string | undefined;
    class: string;
    readonly?: boolean;
  }>();
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
      const toolbarWidget = document.querySelector("edgeless-toolbar-widget");
      if (!toolbarWidget) {
        return;
      }

      const templateButton = toolbarWidget.shadowRoot?.querySelector(
        "edgeless-template-button"
      );
      // const cover = document.createElement("edgeless-cover-tool-button");
      if (coverRef) {
        templateButton?.parentElement?.append(coverRef);
      }
      templateButton?.remove();

      const shapeButton = toolbarWidget.shadowRoot?.querySelector(
        "edgeless-shape-tool-button"
      );

      // if (mindmapButton) {
      //   // 获取父节点
      //   const parent = mindmapButton.parentNode;

      //   // 获取父节点的父节点（祖父节点）
      //   const grandParent = parent?.parentNode;

      //   // 在祖父节点中向上移动父节点（交换位置）
      //   if (grandParent && (parent as Element).previousElementSibling) {
      //     grandParent.insertBefore(parent, (parent as Element).previousElementSibling);
      //   }
      //   const aiNode = document.createElement("div");
      //   aiNode.className="senior-tool-item";
      //   grandParent?.appendChild(aiNode);
      // }

      if (mapButtonRef) {
        shapeButton?.parentElement?.append(mapButtonRef);
      }
      shapeButton?.remove();
      // const toolsNode =
      //   toolbarWidget.shadowRoot?.querySelector(".senior-tools");
      // if (toolsNode) {
      //   toolsNode?.appendChild(aiButtonRef);
      // }
    }, 100);
  });

  // 监听readonly属性变化，动态切换编辑器的只读模式
  $effect(() => {
    if (editor && editor.doc) {
      editor.doc.awarenessStore.setReadonly(editor.doc.blockCollection,readonly);
    }
  });

  onDestroy(() => {
    // editor?.dispose(); // Consider disposing the editor if necessary
  });
  export async function getContent() {
    return await exportDocToJson(editor.doc);
  }
  let coverRef = $state<HTMLDivElement>();
  let mapButtonRef = $state<HTMLDivElement>();
  let coverUrl = $state(
    "https://images.unsplash.com/photo-1448375240586-882707db888b"
  );
  let showCoverSelector = $state(false);
  let coverSelectorRef = $state<HTMLDivElement>();
  let uploadProgress = $state(0);
  let showUploadProgress = $state(false);

  // AI相关状态
  let aiButtonRef: HTMLDivElement;
  let showAIModal = $state(false);
  let aiModalPosition = $state({ x: 0, y: 0 });
  let activeAIFeature = $state("");

  function handleFileUpload(file: File) {
    showUploadProgress = true;
    uploadProgress = 0;
    showCoverSelector = false;

    // 模拟上传进度
    const interval = setInterval(() => {
      uploadProgress += 10;
      if (uploadProgress >= 100) {
        clearInterval(interval);
        showUploadProgress = false;
        // 实际上传完成后设置url
        coverUrl = URL.createObjectURL(file);
      }
    }, 300);
  }

  // AI按钮处理函数
  // function handleAIClick() {
  //   const rect = aiButtonRef?.getBoundingClientRect();
  //   if (rect) {
  //     aiModalPosition = {
  //       x: rect.left + rect.width / 2,
  //       y: rect.top,
  //     };
  //   }
  //   showAIModal = true;
  // }

  function handleAIFeatureSelect(event: { featureId: string }) {
    activeAIFeature = event.featureId;
    showAIModal = false;
  }

  function handleAIModalClose() {
    showAIModal = false;
  }

  function handleAIFeatureClose() {
    activeAIFeature = "";
  }
</script>

<div class={cn("w-full h-full ",className)} bind:this={editorContainer}>
  <edgeless-cover-tool-button
    bind:this={coverRef}
    url={coverUrl}
    {uploadProgress}
    {showUploadProgress}
    onclick={() => (showCoverSelector = true)}
    onkeydown={(e: KeyboardEvent) =>
      e.key === "Enter" && (showCoverSelector = true)}
    role="button"
    tabindex="0"
    aria-label="选择封面"
  ></edgeless-cover-tool-button>

  <edgeless-map-tool-button
    bind:this={mapButtonRef}
    onclick={() => console.log("Map button clicked")}
    onkeydown={(e: KeyboardEvent) =>
      e.key === "Enter" && console.log("Map button clicked")}
    role="button"
    tabindex="0"
    aria-label="地图工具"
  ></edgeless-map-tool-button>

  <!-- <edgeless-ai-tool-button
    bind:this={aiButtonRef}
    onclick={handleAIClick}
    onkeydown={(e: KeyboardEvent) => e.key === "Enter" && handleAIClick()}
    role="button"
    tabindex="0"
    aria-label="AI助手"
  ></edgeless-ai-tool-button> -->

  {#if showCoverSelector}
    <div
      class="absolute z-50"
      bind:this={coverSelectorRef}
      style="top: {(coverRef?.getBoundingClientRect()?.top ?? 0) -
        360}px; left: {(coverRef?.getBoundingClientRect()?.left ?? 0) - 150}px"
    >
      <Card class="p-0 ">
        <CoverSelector
          onSelect={(url) => {
            coverUrl = url;
            // isDropdownOpen = false; // Close dropdown after selection
          }}
          onLinkSubmit={(_url) => {
            // coverUrl = _url;
            // isDropdownOpen = false; // Close dropdown after submission
          }}
          onFileUpload={handleFileUpload}
          userId={$auth.user?.$id || ""}
        ></CoverSelector>
      </Card>
    </div>
  {/if}
</div>

{#if showCoverSelector}
  <div
    class="fixed inset-0 z-40"
    onclick={() => (showCoverSelector = false)}
    oncontextmenu={(e) => {
      e.preventDefault();
      e.stopPropagation();
    }}
    role="button"
    tabindex="0"
    onkeydown={(e) => e.key === "Enter" && (showCoverSelector = false)}
  ></div>
{/if}

<!-- AI模态框 -->
<AIModal
  bind:open={showAIModal}
  position={aiModalPosition}
  onfeatureselect={handleAIFeatureSelect}
  onclose={handleAIModalClose}
/>

<!-- AI功能处理器 -->
<AIFeatureHandler
  bind:activeFeature={activeAIFeature}
  onclose={handleAIFeatureClose}
/>
