<script lang="ts">
    import { SpecProvider } from "@blocksuite/affine-shared/utils";
    import { AffineSchemas } from "@blocksuite/affine/schemas";
    import {
        createAutoIncrementIdGenerator,
        type DocCollectionOptions,
        TestWorkspace,
    } from "@blocksuite/affine/store/test";
    import { TestAffineEditorContainer } from "@blocksuite/integration-test";
    import { onDestroy, onMount } from "svelte";

    let editorContainer: HTMLDivElement;

    function createTestOptions() {
        const idGenerator = createAutoIncrementIdGenerator();
        return { id: "test-collection", idGenerator };
    }
    const collection = new TestWorkspace(createTestOptions());
    collection.meta.initialize();
    collection.storeExtensions = SpecProvider._.getSpec("store").value;
    const doc = collection.createDoc("home");


    console.log(collection.storeExtensions);

    const editor = new TestAffineEditorContainer();
    editor.doc = doc.getStore();
    // editor.edgelessSpecs = testSpecs;

    // document.body.append(editorContainer);
    onMount(async () => {
        editorContainer.appendChild(editor);
        await editor.updateComplete;
    });
    onDestroy(() => {});
</script>

<div class="fullscreen-editor" bind:this={editorContainer}></div>

<style>
    :global(html, body, #svelte) {
        width: 100vw;
        height: 100vh;
        margin: 0;
        padding: 0;
        overflow: hidden;
    }
    :global(body) {
        background: #18181b;
    }
    .dg > ul {
        overflow: scroll;
    }
    .fullscreen-editor {
        width: 100vw;
        height: 100vh;
        position: fixed;
        top: 0;
        left: 0;
        background: #18181b;
    }
</style>
