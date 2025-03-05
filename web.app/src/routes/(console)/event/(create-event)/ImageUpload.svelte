<script lang="ts">
    import { _ } from 'svelte-i18n';
    import { Label } from "$lib/components/ui/label";
    import { Button } from "$lib/components/ui/button";
    import { Image as ImageIcon } from "lucide-svelte";

    export let imageFile: File | null = null;
    export let imagePreview: string | null = null;

    function handleImageSelect(event: Event) {
        const input = event.target as HTMLInputElement;
        if (input.files && input.files[0]) {
            imageFile = input.files[0];
            imagePreview = URL.createObjectURL(imageFile);
        }
    }

    function handleDrop(event: DragEvent) {
        event.preventDefault();
        const file = event.dataTransfer?.files[0];
        if (file && file.type.startsWith('image/')) {
            imageFile = file;
            imagePreview = URL.createObjectURL(file);
        }
    }

    function handleDragOver(event: DragEvent) {
        event.preventDefault();
    }
</script>

<div class="space-y-4">
    <div class="space-y-2">
        <Label>{$_('events.create.image')}</Label>
        <div
            class="flex flex-col items-center justify-center rounded-lg border border-dashed p-8"
            on:drop={handleDrop}
            on:dragover={handleDragOver}
        >
            {#if imagePreview}
                <img
                    src={imagePreview}
                    alt="Preview"
                    class="mb-4 max-h-[200px] w-auto rounded-lg"
                />
            {:else}
                <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-muted">
                    <ImageIcon class="h-6 w-6" />
                </div>
            {/if}
            <div class="space-y-1 text-center">
                <p class="text-sm text-muted-foreground">
                    {$_('events.create.image_upload_desc')}
                </p>
            </div>
            <label class="mt-4">
                <Button variant="outline" type="button">
                    {$_('events.create.select_image')}
                </Button>
                <input
                    type="file"
                    accept="image/*"
                    class="hidden"
                    on:change={handleImageSelect}
                />
            </label>
        </div>
    </div>
</div>