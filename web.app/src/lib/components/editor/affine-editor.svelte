<script lang="ts">
    import { onMount } from "svelte";
    import { getContext } from "svelte";
    import type { Writable } from "svelte/store";
    import type { AppState } from "./affine-editor";
    import { initEditor } from "./affine-editor";
    import { cn } from "$lib/utils.js";
    import './affine-editor.css'

    let { docId = 'page1', class: className = '' } = $props();
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

<div bind:this={editorContainer} class={cn("w-[40vh]", className)}></div>

