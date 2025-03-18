<script lang="ts">
    import { onMount } from "svelte";
    import { getContext } from "svelte";
    import type { Writable } from "svelte/store";
    import type { AppState } from "./affine-editor";
    import "@blocksuite/presets/themes/affine.css";

    const appState = getContext<Writable<AppState>>("appState");
    let editorContainer: HTMLDivElement;

    onMount(() => {
        const unsubscribe = appState.subscribe(({ editor }) => {
            if (editorContainer && editor) {
                editorContainer.innerHTML = "";
                editorContainer.appendChild(editor);
            }
        });

        return () => {
            unsubscribe();
        };
    });
</script>
<style>
    :root{
        
    }
</style>
<div bind:this={editorContainer} class="editor-container"></div>
