<script lang="ts">
    export let title: string;
    export let subtitle: string = "";
    export let description: string = "";
    export let icon: any;
    export let url: string = "#";
    export let color: "blue" | "green" | "purple" | "amber" = "blue";
    export let views: string[] = [];
    export let lastEdited: string = "";
</script>

<style lang="postcss">
    .notion-card {
        @apply relative rounded-lg border bg-card overflow-hidden transition-all duration-200;
        @apply hover:shadow-lg hover:border-primary/50;
    }

    .notion-card-header {
        @apply p-4 border-b;
    }

    .notion-card-content {
        @apply p-4;
    }

    .notion-card-footer {
        @apply px-4 py-3 border-t bg-muted/50;
    }

    .icon-container {
        @apply h-5 w-5 text-muted-foreground;
    }

    .views-list {
        @apply flex gap-2 text-xs text-muted-foreground;
    }

    .views-list::before {
        content: "•";
        @apply text-muted-foreground/50;
    }
</style>

<a href={url} class="notion-card group">
    <div class="notion-card-header">
        <div class="flex items-center gap-3">
            <svelte:component this={icon} class="icon-container" />
            <div>
                <h3 class="font-medium group-hover:text-primary transition-colors">{title}</h3>
                {#if subtitle}
                    <p class="text-xs text-muted-foreground">{subtitle}</p>
                {/if}
            </div>
        </div>
    </div>
    {#if description}
        <div class="notion-card-content">
            <p class="text-sm text-muted-foreground">{description}</p>
        </div>
    {/if}
    <div class="notion-card-footer">
        <div class="flex items-center justify-between text-xs text-muted-foreground">
            <div class="flex items-center gap-2">
                {#if views.length > 0}
                    <span class="views-list">
                        {views.join(", ")}
                    </span>
                {/if}
            </div>
            {#if lastEdited}
                <span>{lastEdited}</span>
            {/if}
        </div>
    </div>
</a> 