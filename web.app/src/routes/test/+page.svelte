<script lang="ts">
    import AffineEditor from "$lib/components/editor/affine-editor.svelte";
    import { initEditor } from "$lib/components/editor/affine-editor";
    import type { AppState } from "$lib/components/editor/affine-editor";
    import { writable } from "svelte/store";
    import { setContext } from "svelte";

    
</script>

<div class="flex p-6 w-full h-[90vh] bg-card">
    <AffineEditor docId="event-doc" />
</div>