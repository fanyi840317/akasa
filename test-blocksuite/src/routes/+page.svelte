<script lang="ts">

    // import { createEmptyDoc, EdgelessEditor } from "@blocksuite/presets";
    // import { signal } from "@preact/signals-core";
    // import {
    //     ColorScheme,
    //     OverrideThemeExtension,
    //     ParagraphBlockService,
    //     SpecProvider,
    //     type ThemeExtension,
    // } from "@blocksuite/blocks";
    import { onMount, onDestroy } from "svelte";
    // import "@toeverything/theme/style.css";

    // let editorContainer: HTMLDivElement;
    // const currentTheme = document.documentElement.dataset.theme;
    // const colorScheme =
    //     currentTheme === "black" ? ColorScheme.Dark : ColorScheme.Light;
    // const themeExtension: ThemeExtension = {
    //     getAppTheme: () => {
    //         return signal(colorScheme);
    //     },
    //     getEdgelessTheme: () => {
    //         return signal(colorScheme);
    //     },
    // };
    //   function OverrideToolsExtension(service: ThemeExtension): ExtensionType {
    //   return {
    //     setup: di => {
    //       di.override(ThemeExtensionIdentifier, () => service);
    //     },
    //   };
    // }
    onMount(() => {
        console.log("onMount");
        // const doc = createEmptyDoc().init();
        // doc;
        // console.log(doc);
        // const editor = new EdgelessEditor();
        // editor.doc = doc;

        // // editor.mode = "edgeless";
        // // 应用主题扩展到编辑器
        // if (editor.specs) {
        //     const edgelessSpecs =
        //         SpecProvider.getInstance().getSpec("edgeless");
        //     edgelessSpecs.extend([OverrideThemeExtension(themeExtension)]);
        //     editor.specs = edgelessSpecs.value;
        // }

        // editorContainer.appendChild(editor);
        // await editor.updateComplete;
    });
    onDestroy(() => {});
</script>

<div style="width:100% height: 100%;">
    <div style="width:100% height: 100%;" bind:this={editorContainer}></div>
</div>
