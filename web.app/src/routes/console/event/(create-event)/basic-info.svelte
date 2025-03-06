<script lang="ts">
    import { _ } from 'svelte-i18n';
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import { browser } from '$app/environment';
    import ShadEditor from '$lib/components/shad-editor/shad-editor.svelte';
    import { cn } from "$lib/utils.js";
    import { fade } from 'svelte/transition';
    import { writable } from 'svelte/store';
    
    export let title = "";
    export let description = "";
    let titleFocused = false;
    
    let localStorageContent = '';
    
    if (browser) {
        localStorageContent = localStorage.getItem('event_description') || '';
        description = localStorageContent;
    }
    
    const content = writable(description);
    
    content.subscribe((value) => {
        if (!browser) return;
        description = value;
        localStorage.setItem('event_description', value);
    });
</script>

<div class="notion-page max-w-5xl mx-auto px-4 py-6 md:py-8 md:px-0">
    <div class="space-y-2">
        <!-- Notion-style title field -->
        <div class="relative group px-6 mb-10">
            <input 
                type="text" 
                id="title" 
                bind:value={title} 
                placeholder={$_('events.create.title') || "Untitled"} 
                on:focus={() => titleFocused = true} 
                on:blur={() => titleFocused = false}
                class={cn(
                    "w-full px-0 py-2 text-4xl font-bold border-0 focus:outline-none focus:ring-0 bg-transparent transition-colors",
                    !title ? "text-gray-400" : "text-gray-800"
                )}
            />
            {#if !title && !titleFocused}
                <div class="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity">
                    Click to edit
                </div>
            {/if}
        </div>
        
        <!-- Notion-style editor with ShadEditor -->
        <div class="notion-editor relative group">
            <ShadEditor showToolbar={false}
                    class="min-h-[80vh] border-0" 
                    content={$content}
                />
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
    
</style>