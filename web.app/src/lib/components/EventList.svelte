<script lang="ts">
    import * as Card from "$lib/components/ui/card";
    import { Button } from "$lib/components/ui/button";
    import type { Event } from '$lib/types/event';
    import { mockEvents } from '$lib/data/mock-events';
    import { onMount } from 'svelte';
    import Badge from "./ui/badge/badge.svelte";

    const events = mockEvents;
    let showAll = false;
    let userLocation: { latitude: number; longitude: number } | null = null;
    $: displayEvents = showAll ? events : events.slice(0, 3);

    // 计算两点之间的距离（使用Haversine公式）
    function calculateDistance(lat1: number, lon1: number, lat2: number, lon2: number): number {
        const R = 6371; // 地球半径（公里）
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                Math.sin(dLon/2) * Math.sin(dLon/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return Math.round(R * c);
    }

    // 格式化距离显示
    function formatDistance(distance: number): string {
        if (distance < 1) {
            return '< 1公里';
        }
        return `${distance}公里`;
    }

</script>

<div>
    <div class="flex flex-col gap-3">
        {#each displayEvents as event}
            <Card.Root class="cursor-pointer hover:bg-accent/50 transition-colors flex items-start p-3 gap-3">
                    <div class="w-16 h-16 rounded-lg overflow-hidden bg-muted flex-shrink-0">
                    <img src={event.image} alt={event.title} class="w-full h-full object-cover" />
                </div>
                    <div class="flex-1 min-w-0 relative">
                    <div class="flex justify-between items-start mb-1">
                        <h3 class="text-primary text-sm font-medium truncate">{event.title}</h3>
                        <Badge variant="outline" class="text-xs ml-2">{event.occurredAt.getFullYear()}</Badge>
                    </div>

                    <p class="text-muted-foreground text-xs mb-2 line-clamp-1">{event.description}</p>
                    <div class="items-center text-xs text-muted-foreground">
                        <span class="flex items-center gap-1 truncate">
                            <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
                            </svg>
                            {#if userLocation && event.location}
                                <span class="ml-1">{formatDistance(calculateDistance(
                                    userLocation.latitude,
                                    userLocation.longitude,
                                    event.location.latitude,
                                    event.location.longitude
                                ))}</span>
                            {/if}
                            {event.location.name}
                        </span>
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
