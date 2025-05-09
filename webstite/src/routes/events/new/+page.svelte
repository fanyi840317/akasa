<script lang="ts">
  import { createEmptyDoc, EdgelessEditor } from "@blocksuite/presets";
  import { signal } from "@preact/signals-core";
  import {
    ColorScheme,
    OverrideThemeExtension,
    ParagraphBlockService,
    SpecProvider,
    type ThemeExtension,
  } from "@blocksuite/blocks";
  import { onMount, onDestroy } from "svelte";
  import { appStore } from "$lib/stores/appState";
  import "@toeverything/theme/style.css";

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
  //   function OverrideToolsExtension(service: ThemeExtension): ExtensionType {
  //   return {
  //     setup: di => {
  //       di.override(ThemeExtensionIdentifier, () => service);
  //     },
  //   };
  // }
  onMount(async () => {
    const doc = createEmptyDoc().init();
    doc;
    console.log(doc);
    const editor = new EdgelessEditor();
    editor.doc = doc;

    // editor.mode = "edgeless";
    // 应用主题扩展到编辑器
    if (editor.specs) {
      const edgelessSpecs = SpecProvider.getInstance().getSpec("edgeless");
      edgelessSpecs.extend([OverrideThemeExtension(themeExtension)]);
      editor.specs = edgelessSpecs.value;
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
