<script lang="ts">
    import { Editor } from '@blocksuite/affine'; 
    import { onMount } from 'svelte';
    let editorContainer: HTMLDivElement;

    onMount(() => {
        const editor = new Editor();
        editorContainer.appendChild(editor);
    });
</script>


<div>

<div bind:this={editorContainer} ></div>
</div>