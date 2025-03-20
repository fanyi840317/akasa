<script lang="ts">
    import { Star } from "lucide-svelte";
    import { Badge } from "$lib/components/ui/badge";
    import {
        Avatar,
        AvatarImage,
        AvatarFallback,
    } from "$lib/components/ui/avatar";

    export let title: string;
    export let image: string = "";
    export let tags: string[] = [];
    export let rating: number = 0;
    export let url: string = "#";
    export let avatarSrc: string = "";
    export let avatarFallback: string = title ? title.slice(0, 2) : "";
</script>

<style lang="postcss">
    .event-card {
        @apply mb-4 transition-all duration-200 hover:-translate-y-1;
    }

    .event-card-image {
        @apply relative h-56 overflow-hidden rounded-lg mb-2;
    }

    .event-card-image img {
        @apply w-full h-full object-cover;
    }

    .event-card-content {
        @apply flex items-center justify-between p-2;
    }

    .event-card-title {
        @apply flex items-center;
    }

    .event-card-tags {
        @apply flex flex-wrap justify-end;
    }

    .event-card-rating {
        @apply flex items-center text-xs text-muted-foreground/40 px-3;
    }
</style>

<a href={url} class="event-card">
    <div class="event-card-image">
        <img src={image} alt={title} />
    </div>
    <div class="event-card-content">
        <div class="event-card-title">
            <div class="flex items-center space-x-2">
                <Avatar class="h-5 w-5">
                    <AvatarImage src={avatarSrc || image} alt={title} />
                    <AvatarFallback>{avatarFallback}</AvatarFallback>
                </Avatar>
                <span class="text-sm text-foreground/90">{title}</span>
            </div>
        </div>
        <div class="event-card-tags">
            {#each tags as tag}
                <Badge variant="outline" class="ml-1 text-muted-foreground/30">{tag}</Badge>
            {/each}
        </div>
    </div>
    {#if rating > 0}
        <div class="event-card-rating gap-1">
            <Star class="h-3 w-3" />
            <span >{rating}</span>
        </div>
    {/if}
</a>