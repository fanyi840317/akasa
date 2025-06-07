<script lang="ts">
    export let title: string;
    export let icon: any;
    export let url: string = "#";
    export let color: "blue" | "green" | "purple" | "amber" = "blue";
    export let lastEdited: string = "";
    export let coverImage: string = "";
    export let emoji: string = "";
</script>

<style lang="postcss">
    .notion-card {
        @apply relative rounded-lg border bg-card overflow-hidden transition-all duration-200;
        @apply hover:shadow-lg hover:border-primary/50;
    }

    .notion-card-cover {
        @apply relative aspect-video w-full overflow-hidden bg-gradient-to-b from-muted/50 to-muted;
    }

    .notion-card-cover img {
        @apply w-full h-full object-cover;
    }

    .notion-card-content {
        @apply p-3 flex items-center gap-2;
    }

    .icon-container {
        @apply flex items-center justify-center h-5 w-5 rounded bg-primary/10 text-primary shrink-0;
    }

    .emoji-container {
        @apply flex items-center justify-center h-5 w-5 text-sm shrink-0;
    }

    .last-edited {
        @apply absolute bottom-2 right-2 text-xs px-2 py-1 rounded-full bg-background/80 text-muted-foreground;
        @apply opacity-0 group-hover:opacity-100 transition-opacity duration-200;
    }
</style>

<a href={url} class="notion-card group">
    {#if coverImage}
        <div class="notion-card-cover">
            <img src={coverImage} alt={title} />
        </div>
    {/if}
    <div class="notion-card-content">
        {#if emoji}
            <span class="emoji-container">{emoji}</span>
        {:else if icon}
            <div class="icon-container">
                <svelte:component this={icon} class="h-3.5 w-3.5" />
            </div>
        {/if}
        <h3 class="font-medium truncate group-hover:text-primary transition-colors">{title}</h3>
    </div>
    {#if lastEdited}
        <span class="last-edited">{lastEdited}</span>
    {/if}
</a> 