<script lang="ts">
    import * as Card from "$lib/components/ui/card";
    import { Button } from "$lib/components/ui/button";
    import type { Event } from '$lib/types/event';
    import { mockEvents } from '$lib/data/mock-events';

    const events = mockEvents;
    let showAll = false;
    $: displayEvents = showAll ? events : events.slice(0, 3);
</script>

<div>
    <div class="flex flex-col gap-3">
        {#each displayEvents as event}
            <Card.Root class="cursor-pointer hover:bg-accent/50 transition-colors flex items-start p-3 gap-3">
                <div class="w-16 h-16 rounded-lg overflow-hidden bg-muted flex-shrink-0">
                    <img src={event.image} alt={event.title} class="w-full h-full object-cover" />
                </div>
                <div class="flex-1 min-w-0">
                    <h3 class="text-primary text-sm font-medium mb-1 truncate">{event.title}</h3>
                    <p class="text-muted-foreground text-xs mb-2 line-clamp-1">{event.description}</p>
                    <div class="flex items-center justify-between text-xs text-muted-foreground">
                        <span class="flex items-center gap-1 truncate">
                            <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
                            </svg>
                            {event.location.name}
                        </span>
                        <span class="flex-shrink-0">{event.occurredAt.toLocaleDateString()}</span>
                    </div>
                </div>
            </Card.Root>
        {/each}
        {#if events.length > 3 && !showAll}
            <Button variant="outline" class="w-full text-sm py-2" on:click={() => showAll = true}>
                查看更多
            </Button>
        {/if}
    </div>
</div>
