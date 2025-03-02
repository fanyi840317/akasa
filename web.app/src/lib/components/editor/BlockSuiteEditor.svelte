<script lang="ts">
    import { onMount, onDestroy, createEventDispatcher } from 'svelte';
    import { EditorContainer } from '@blocksuite/editor';
    import '@blocksuite/editor/themes/affine.css';
    import { AffineSchemas } from '@blocksuite/blocks/schemas';
    import { DocCollection } from '@blocksuite/store';
    import { nanoid } from '@blocksuite/store';

    export let content = "";
    export let placeholder = "请输入内容...";
    export let readonly = false;

    let editorContainer: HTMLDivElement;
    let editor: EditorContainer;
    let docCollection: DocCollection;
    let pageId: string;
    const dispatch = createEventDispatcher<{ change: string }>(); 

    onMount(async () => {
        // 创建文档集合
        docCollection = new DocCollection({
            id: nanoid(),
            schema: AffineSchemas,
        });

        // 创建页面
        pageId = docCollection.createDoc({ flavour: 'page' });
        const page = docCollection.getDoc(pageId);
        if (!page) return;

        // 如果有初始内容，尝试解析并设置
        if (content) {
            try {
                const parsedContent = JSON.parse(content);
                if (parsedContent && typeof parsedContent === 'object') {
                    page.load(parsedContent);
                }
            } catch (e) {
                // 如果不是有效的JSON，则创建一个新的段落块并设置文本内容
                const rootBlockId = page.addBlock('affine:page', {});
                page.addBlock('affine:surface', {}, rootBlockId);
                const noteId = page.addBlock('affine:note', {}, rootBlockId);
                const paragraphId = page.addBlock('affine:paragraph', { text: content }, noteId);
            }
        } else {
            // 创建默认的页面结构
            const rootBlockId = page.addBlock('affine:page', {});
            page.addBlock('affine:surface', {}, rootBlockId);
            const noteId = page.addBlock('affine:note', {}, rootBlockId);
            page.addBlock('affine:paragraph', { text: '' }, noteId);
        }

        // 创建编辑器
        editor = new EditorContainer();
        editor.page = page;
        editor.readonly = readonly;

        // 设置占位符
        if (placeholder) {
            const style = document.createElement('style');
            style.textContent = `
                .affine-paragraph-block-container:first-child .affine-paragraph-block:empty::before {
                    content: "${placeholder}";
                    color: #aaa;
                    position: absolute;
                    pointer-events: none;
                }
            `;
            document.head.appendChild(style);
        }

        // 监听内容变化
        page.slots.blockUpdated.on(() => {
            try {
                const serialized = JSON.stringify(page.serialize());
                content = serialized;
                dispatch('change', serialized);
            } catch (e) {
                console.error('Failed to serialize page', e);
            }
        });

        // 挂载编辑器
        editorContainer.appendChild(editor);
    });

    onDestroy(() => {
        if (editor) {
            editor.remove();
        }
        if (docCollection) {
            docCollection.dispose();
        }
    });
</script>

<div class="blocksuite-editor" bind:this={editorContainer}></div>

<style>
    .blocksuite-editor {
        width: 100%;
        min-height: 300px;
        border-radius: 0.375rem;
        border: 1px solid var(--border, #e2e8f0);
        overflow: hidden;
    }

    :global(.affine-default-page) {
        padding: 0 !important;
    }

    :global(.affine-note-block-container) {
        padding: 0.5rem !important;
    }
</style>