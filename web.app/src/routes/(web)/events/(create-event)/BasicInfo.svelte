<script lang="ts">
    import { _ } from 'svelte-i18n';
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    // import { BlockSuiteEditor } from "$lib/components/editor";
    export let title = "";
    export let description = "";

    function handleEditorChange(event: CustomEvent<string>) {
        description = event.detail;
    }
</script>

<div class="min-h-screen w-full max-w-3xl mx-auto px-4 py-8">
    <div class="space-y-6">
        <div class="space-y-2">
            <Label for="title">{$_('events.create.title')}</Label>
            <Input type="text" id="title" bind:value={title} placeholder={$_('events.create.title_placeholder')} />
        </div>

        <div class="space-y-2">
            <Label for="description">{$_('events.create.description')}</Label>
            <!-- <BlockSuiteEditor 
                bind:content={description} 
                placeholder={$_('events.create.description_placeholder') || '请输入详细描述...'} 
                on:change={handleEditorChange} 
            /> -->
        </div>
    </div>
</div>