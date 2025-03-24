<script lang="ts">
    import { onDestroy, onMount } from "svelte";
    import "@toeverything/theme/style.css";
    import { signal, type Signal } from '@preact/signals-core';
    import {ModeWatcher,mode} from "mode-watcher";

    import {
        createEmptyDoc,
        AffineEditorContainer,
    } from "@blocksuite/presets";
    import { ColorScheme, OverrideThemeExtension, SpecProvider, type ThemeExtension } from "@blocksuite/blocks";
    import { get } from "svelte/store";

    let { docId = "page1", class: className = "" } = $props();
    let editorContainer: HTMLDivElement;
    let doc = createEmptyDoc().init();
    let editor: AffineEditorContainer | null = null;
    
    // 创建编辑器实例
    editor = new AffineEditorContainer();
    editor.doc = doc;
    editor.autofocus = true;


    const themeExtension: ThemeExtension = {
        getAppTheme: () => {
            const currentTheme = get(mode);
            return signal(currentTheme === 'dark' ? ColorScheme.Dark : ColorScheme.Light);
        }
    };

    onMount(() => {
        if (editorContainer && editor) {
            // // 设置暗色主题7
            
            // 应用主题扩展到编辑器
            if (editor.pageSpecs) {
                const pageSpecs = SpecProvider.getInstance().getSpec('page');
                pageSpecs.extend([OverrideThemeExtension(themeExtension)]);
                editor.pageSpecs = pageSpecs.value;
            }
            
            // 添加编辑器到容器
            editorContainer.appendChild(editor);
            
            // 等待编辑器完全挂载后尝试聚焦
            // editor.updateComplete.then(() => {
            //     // 简化的聚焦逻辑
            //     setTimeout(() => {
            //         const richText = editor?.host?.querySelector("rich-text");
            //         if (richText) {
            //             const inlineEditor = (richText as any).inlineEditor;
            //             if (inlineEditor) {
            //                 inlineEditor.focusEnd();
            //             }
            //         }
            //     }, 200);
            // });
        }
    });

    onDestroy(() => {
        if (editorContainer && editor && editorContainer.contains(editor)) {
            editorContainer.removeChild(editor);
            editor.disposables?.dispose();
        }
    });
</script>

<div
    bind:this={editorContainer}
    data-theme="dark"
    style="width: 100%; height: 100%; position: relative;"
></div>

<style>
    :global(embed-card-create-modal .embed-card-modal-mask) {
        z-index: 200000;
    }
    :global(embed-card-create-modal .embed-card-modal-wrapper) {
        z-index: 200001;
    }
    /* 隐藏文档标题 */
    /* :global(doc-title) {
        display: none !important;
    } */
</style>
