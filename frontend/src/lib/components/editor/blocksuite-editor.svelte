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
  import { appStore } from "$lib/stores/app-state";
  import "@toeverything/theme/style.css";
  import { Doc, Slot, type Block } from "@blocksuite/store"; // Added Doc
  import type { Disposable } from "@blocksuite/global/utils";
  import { createDocByJson, exportDocToJson } from "./editor-doc";

  // Import effects if they are not globally initialized elsewhere
  import { effects as blocksEffects } from "@blocksuite/blocks/effects";
  import { effects as presetsEffects } from "@blocksuite/presets/effects";

  import { EdgelessCoverButton } from "./toolbar/cover/cover-button";
  import { auth } from "$lib/stores/auth";
  import CoverSelector from "./toolbar/cover/cover-selector.svelte";
  import { Card } from "../ui";
  // Ensure effects are initialized only once globally
  if (!(window as any).__blocksuite_effects_initialized) {
    blocksEffects();
    presetsEffects();
    customElements.define("edgeless-cover-button", EdgelessCoverButton);
    (window as any).__blocksuite_effects_initialized = true;
  }

  // export let docId: string | undefined = undefined; // Optional prop to load an existing doc
  // export let initialJsonContent: string | undefined = undefined; // New prop for initial JSON content
  let { initialJsonContent = undefined } = $props<{
    initialJsonContent: string | undefined;
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
    editorInstance: AffineEditorContainer,
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
            "createDocByJson did not return a Doc instance, falling back.",
          );
          throw new Error("createDocByJson did not return a Doc instance");
        }
        // Assuming createDocByJson returns an initialized/loaded Doc.
        // If not, doc.load() or similar might be needed here.
      } catch (e) {
        console.error(
          "Failed to create document using createDocByJson or provided JSON is invalid:",
          e,
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
        "edgeless-template-button",
      );
      // const cover = document.createElement("edgeless-cover-tool-button");
      templateButton?.parentElement?.append(coverRef);

      // templateButton?.parentElement?.parentElement?.after(divider); // Append the divider after the template button
      // Append the divider after the template button
      templateButton?.remove();
    }, 100);
    // setTimeout(() => {
    //   url="";
    // },1000)
  });
  const handCoverClick = () => {
    alert("clickdwq");
    coverRef.getBoundingClientRect();
  };

  onDestroy(() => {
    // editor?.dispose(); // Consider disposing the editor if necessary
  });
  export async function getContent() {
    return await exportDocToJson(editor.doc);
  }
  let dividerRef: HTMLDivElement;
  let coverRef: HTMLDivElement;
  let coverUrl = $state(
    "https://images.unsplash.com/photo-1448375240586-882707db888b",
  );
  let showCoverSelector = $state(false);
  let coverSelectorRef: HTMLDivElement;

  function handleCoverSelect(url: string) {
    url = url;
    showCoverSelector = false;
  }

  function handleFileUpload(file: File) {
    // Handle file upload logic
    showCoverSelector = false;
  }

  function handleLinkSubmit(url: string) {
    url = url;
    showCoverSelector = false;
  }
</script>

<div class="w-full h-full" bind:this={editorContainer}>
  <edgeless-cover-button
    bind:this={coverRef}
    url={coverUrl}
    onclick={() => (showCoverSelector = true)}
  />

  {#if showCoverSelector}
    <div
      class="absolute z-50"
      bind:this={coverSelectorRef}
      style="top: {coverRef?.getBoundingClientRect().top -
        360}px; left: {coverRef?.getBoundingClientRect().left - 150}px"
    >
      <Card class="p-0 ">
        <CoverSelector
          onSelect={(url) => {
            coverUrl = url;
            // isDropdownOpen = false; // Close dropdown after selection
          }}
          onLinkSubmit={(url) => {
            // coverUrl = url;
            // isDropdownOpen = false; // Close dropdown after submission
          }}
          onFileUpload={handleFileUpload}
          userId={$auth.user?.$id || ""}
        />
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
  />
{/if}
