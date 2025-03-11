<script lang="ts">
    export let title: string;
    export let subtitle: string = "";
    export let description: string = "";
    export let icon: any;
    export let url: string = "#";
    export let color: "blue" | "green" | "purple" | "amber" = "blue";
</script>

<style lang="postcss">
    .notion-card {
        @apply relative rounded-lg border bg-card overflow-hidden transition-all duration-200;
        @apply hover:shadow-lg hover:border-primary/50;
    }

    .notion-card-image {
        @apply relative aspect-[1.6] w-full overflow-hidden bg-gradient-to-b from-muted/50 to-muted;
    }

    .notion-card-content {
        @apply p-4 space-y-2;
    }

    .icon-container {
        @apply h-8 w-8 text-gray-500 ;
    }
</style>

<div class="notion-card group">
    <div class="notion-card-image">
        <div class="absolute inset-0 flex items-center justify-center bg-card/50">
            <svelte:component this={icon} class="icon-container " />
        </div>
    </div>
    <div class="notion-card-content">
        <div class="space-y-1">
            <h3 class="font-medium group-hover:text-primary transition-colors">{title}</h3>
            {#if subtitle}
                <p class="text-xs text-muted-foreground">{subtitle}</p>
            {/if}
        </div>
        {#if description}
            <p class="text-sm text-muted-foreground line-clamp-2">{description}</p>
        {/if}
    </div>
</div> 