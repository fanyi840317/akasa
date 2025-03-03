<script lang="ts">
    import { _ } from 'svelte-i18n';
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import { type EditorType, Editor } from "$lib/components/editor";
    import { cn } from "$lib/utils.js";
    import { fade } from 'svelte/transition';
    
    export let title = "";
    export let description = "";
    let editor: EditorType;
    let titleFocused = false;
    let descriptionFocused = false;
    
    function handleEditorChange() {
        if (editor) {
            description = editor.getHTML();
        }
    }
    
    function handleEditorFocus() {
        descriptionFocused = true;
    }
    
    function handleEditorBlur() {
        descriptionFocused = false;
    }
</script>

<div class="notion-page max-w-4xl mx-auto px-4 py-10 md:py-16 md:px-0">
    <div class="space-y-1">
        <!-- Notion-style title field -->
        <div class="relative group">
            <input 
                type="text" 
                id="title" 
                bind:value={title} 
                placeholder={$_('events.create.title') || "Untitled"} 
                on:focus={() => titleFocused = true} 
                on:blur={() => titleFocused = false}
                class={cn(
                    "w-full px-0 py-1 text-4xl font-bold border-0 focus:outline-none focus:ring-0 bg-transparent transition-colors",
                    !title ? "text-gray-400" : "text-gray-800"
                )}
            />
            {#if !title && !titleFocused}
                <div class="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity">
                    Click to edit
                </div>
            {/if}
        </div>

        <!-- Light divider -->
        <div class="h-px w-full bg-gray-200 my-4"></div>
        
        <!-- Notion-style editor -->
        <div class="notion-editor relative group {descriptionFocused ? 'is-focused' : ''}">
            <div class="relative">
                <Editor
                    bind:editor
                    defaultValue={description}
                    onUpdate={handleEditorChange}
                    on:focus={handleEditorFocus}
                    on:blur={handleEditorBlur}
                    class="min-h-[70vh] border-0 bg-transparent prose prose-sm sm:prose-base transition-colors"
                >
                    <div class="p-1 text-base text-gray-400">
                        {$_('events.create.description_placeholder') || '输入"/"查看命令菜单...'}
                    </div>
                </Editor>
                
                {#if !description && !descriptionFocused}
                    <div class="absolute right-2 top-4 text-xs text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity">
                        Click to edit
                    </div>
                {/if}
            </div>
        </div>
    </div>
</div>

<style>
    /* Notion-style styling */
    .notion-page {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, "Apple Color Emoji", Arial, sans-serif, "Segoe UI Emoji", "Segoe UI Symbol";
        color: rgb(55, 53, 47);
    }
    
    .notion-editor {
        position: relative;
        border-radius: 3px;
        transition: background-color 100ms ease-in;
    }
    
    .notion-editor:hover {
        background-color: rgba(55, 53, 47, 0.03);
    }
    
    .notion-editor.is-focused {
        background-color: transparent;
    }
    
    /* Remove the default prose max-width constraint */
    :global(.notion-editor .prose) {
        max-width: none;
    }
    
    /* Style the editor placeholder text */
    :global(.notion-editor .ProseMirror p.is-editor-empty:first-child::before) {
        color: rgba(55, 53, 47, 0.4);
        font-style: normal;
    }
</style>