<script lang="ts">
  import { createEmptyDoc, AffineEditorContainer } from "@blocksuite/presets";
  import {
    ColorScheme,
    OverrideThemeExtension,
    ParagraphBlockService,
    SpecProvider,
    type ThemeExtension,
  } from "@blocksuite/blocks";
  import { onMount } from "svelte";
  let editorContainer: HTMLDivElement;

 
  onMount(() => {
    document.documentElement.dataset.theme = "dark"
    const doc = createEmptyDoc().init();
    console.log(doc);
    const editor = new AffineEditorContainer();
    editor.doc = doc;
    editor.mode = 'edgeless';
    editorContainer.appendChild(editor);
  });
</script>

<div class="w-full h-full">
  <div class="h-[calc(100vh-4rem)]" bind:this={editorContainer}></div>
</div>
