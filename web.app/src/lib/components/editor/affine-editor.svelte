<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { AffineEditorContainer } from "@blocksuite/presets";
    import { Doc, Schema, DocCollection } from "@blocksuite/store";
    import { AffineSchemas } from "@blocksuite/blocks";
    import "@blocksuite/presets/themes/affine.css";

    interface Props {
        docId?: string;
    }

    let { docId = "default-doc" }: Props = $props();

    let editorContainer: HTMLDivElement;
    let editor: AffineEditorContainer;
    let collection: DocCollection;

    onMount(async () => {
        // 初始化编辑器
        const schema = new Schema().register(AffineSchemas);
        collection = new DocCollection({ schema });
        collection.meta.initialize();

        // 创建文档
        const doc = collection.createDoc({ id: docId });

        // 初始化文档结构
        await doc.load();
        const pageBlockId = doc.addBlock("affine:page", {});
        const noteId = doc.addBlock("affine:note", {}, pageBlockId);
        doc.addBlock("affine:paragraph", {}, noteId);

        // 创建编辑器实例
        editor = new AffineEditorContainer();
        editor.doc = doc;

        // 配置编辑器
        editor.slots.docLinkClicked.on(({ docId }) => {
            const target = collection.getDoc(docId) as Doc;
            editor.doc = target;
        });

        // 将编辑器挂载到容器
        if (editorContainer && editor) {
            editorContainer.appendChild(editor as unknown as Node);
        }
    });

    onDestroy(() => {
        if (editor) {
            editor.remove?.();
        }
        if (collection) {
            (collection as any).dispose?.();
        }
    });

    // 暴露编辑器实例和集合实例
    export function getEditor() {
        return editor;
    }

    export function getCollection() {
        return collection;
    }
</script>

<div bind:this={editorContainer} class="h-full w-full" />

<style>
    :root {
        --affine-background-color: hsl(var(--card));
        --affine-text-color: hsl(var(--card-foreground));
        --affine-editor-text-color: hsl(var(--card-foreground));
        --affine-link-color: hsl(var(--primary));
        --affine-primary-color: hsl(var(--primary));
        --affine-hover-color: hsl(var(--accent));
        --affine-icon-color: hsl(var(--card-foreground));
        --affine-background-primary-color: hsl(var(--card));
    }
</style>
