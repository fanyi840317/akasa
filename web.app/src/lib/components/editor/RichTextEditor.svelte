<script lang="ts">
    import { onMount, onDestroy, createEventDispatcher } from 'svelte';
    import { Editor } from '@tiptap/core';
    import StarterKit from '@tiptap/starter-kit';
    import Placeholder from '@tiptap/extension-placeholder';
    import TaskList from '@tiptap/extension-task-list';
    import TaskItem from '@tiptap/extension-task-item';
    import Image from '@tiptap/extension-image';

    export let content = "";
    export let placeholder = "请输入内容...";
    export let readonly = false;

    let element: HTMLDivElement;
    let editor: Editor;
    const dispatch = createEventDispatcher<{ change: string }>();

    onMount(() => {
        editor = new Editor({
            element,
            extensions: [
                StarterKit,
                Placeholder.configure({
                    placeholder,
                }),
                TaskList,
                TaskItem.configure({
                    nested: true,
                }),
                Image,
            ],
            content,
            editable: !readonly,
            onUpdate: ({ editor }) => {
                content = editor.getHTML();
                dispatch('change', content);
            },
        });
    });

    onDestroy(() => {
        if (editor) {
            editor.destroy();
        }
    });
</script>

<div class="rich-text-editor" bind:this={element}></div>

<style>
    .rich-text-editor {
        width: 100%;
        min-height: 300px;
        border-radius: 0.375rem;
        border: 1px solid var(--border, #e2e8f0);
        padding: 1rem;
    }

    :global(.rich-text-editor .ProseMirror) {
        outline: none;
        min-height: 250px;
    }

    :global(.rich-text-editor .ProseMirror p.is-editor-empty:first-child::before) {
        content: attr(data-placeholder);
        float: left;
        color: #aaa;
        pointer-events: none;
        height: 0;
    }

    :global(.rich-text-editor .ProseMirror ul) {
        list-style-type: disc;
        padding-left: 1.5rem;
    }

    :global(.rich-text-editor .ProseMirror ol) {
        list-style-type: decimal;
        padding-left: 1.5rem;
    }

    :global(.rich-text-editor .ProseMirror h1) {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
    }

    :global(.rich-text-editor .ProseMirror h2) {
        font-size: 1.25rem;
        font-weight: bold;
        margin: 0.75rem 0;
    }

    :global(.rich-text-editor .ProseMirror h3) {
        font-size: 1.125rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }

    :global(.rich-text-editor .ProseMirror blockquote) {
        border-left: 3px solid #ddd;
        padding-left: 1rem;
        margin-left: 0;
        margin-right: 0;
        font-style: italic;
    }

    :global(.rich-text-editor .ProseMirror img) {
        max-width: 100%;
        height: auto;
    }

    :global(.rich-text-editor .ProseMirror hr) {
        border: none;
        border-top: 2px solid #ddd;
        margin: 1rem 0;
    }

    :global(.rich-text-editor .ProseMirror code) {
        background-color: rgba(#616161, 0.1);
        color: #616161;
        padding: 0.25rem;
        border-radius: 0.25rem;
        font-family: monospace;
    }

    :global(.rich-text-editor .ProseMirror pre) {
        background: #0d0d0d;
        color: #fff;
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        font-family: monospace;
        margin: 0.75rem 0;
    }

    :global(.rich-text-editor .ProseMirror pre code) {
        color: inherit;
        background: none;
        padding: 0;
    }

    :global(.rich-text-editor .ProseMirror ul[data-type="taskList"]) {
        list-style: none;
        padding: 0;
    }

    :global(.rich-text-editor .ProseMirror ul[data-type="taskList"] li) {
        display: flex;
        align-items: flex-start;
        margin-bottom: 0.5rem;
    }

    :global(.rich-text-editor .ProseMirror ul[data-type="taskList"] li > label) {
        flex: 0 0 auto;
        margin-right: 0.5rem;
        user-select: none;
    }

    :global(.rich-text-editor .ProseMirror ul[data-type="taskList"] li > div) {
        flex: 1 1 auto;
    }
</style>