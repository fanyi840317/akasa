<script lang="ts">
  import { createEmptyDoc, AffineEditorContainer } from "@blocksuite/presets";
  import {
    ColorScheme,
    OverrideThemeExtension,
    ParagraphBlockService,
    SpecProvider,
    type ThemeExtension,
  } from "@blocksuite/blocks";
  import { onMount, onDestroy } from "svelte";
  import { appStore } from "$lib/stores/appState";
  let editorContainer: HTMLDivElement;

 
  appStore.setHeaderFloatingEnabled(true);
    appStore.setShowFloatingHeader(false);
  onMount(async () => {
    // document.documentElement.dataset.theme = "dark"
    const doc = createEmptyDoc().init();

    console.log(doc);
    const editor = new AffineEditorContainer();
    editor.doc = doc;
    editor.mode = 'edgeless';
    editorContainer.appendChild(editor);
    await editor.updateComplete


    // const handleMouseMove = (event: MouseEvent) => {
    //   if (event.clientY < 50) {
    //     appStore.setShowFloatingHeader(true);
    //   } else {
    //     appStore.setShowFloatingHeader(false);
    //   }
    // };

    // document.body.addEventListener('mousemove', handleMouseMove);

    onDestroy(() => {
      // appStore.setHeaderFloatingEnabled(false);
      // appStore.setShowFloatingHeader(true); // 恢复默认显示
      // document.body.removeEventListener('mousemove', handleMouseMove);
    });
  });
</script>
<div class="w-full h-full">
  <div class="h-[calc(100vh)]" bind:this={editorContainer}></div>
</div>
