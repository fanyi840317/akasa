<script lang="ts">
    import type { PageData } from './$types';
    import Map from '$lib/components/Map.svelte';
    import EventList from '$lib/components/EventList.svelte';
    import { _ } from 'svelte-i18n';
    import * as Card from "$lib/components/ui/card";
    import { theme } from '$lib/stores/theme';
    import { onMount } from 'svelte';
    import { get } from 'svelte/store';
    import { Input } from "$lib/components/ui/input";
    import { Button } from "$lib/components/ui/button";
    import { PlusCircle, Search, MapPin } from "lucide-svelte";
    import { getUserLocation } from '$lib/services/location';

    let { data }: { data: PageData } = $props();

    const categories = [
        { name: $_('events.categories.urban'), icon: "/icons/urban.svg", type: "urban" },
        { name: $_('events.categories.paranormal'), icon: "/icons/paranormal.svg", type: "paranormal" },
        { name: $_('events.categories.supernatural'), icon: "/icons/supernatural.svg", type: "supernatural" },
        { name: $_('events.categories.mysterious'), icon: "/icons/mysterious.svg", type: "mysterious" },
        { name: $_('events.categories.unexplained'), icon: "/icons/unexplained.svg", type: "unexplained" },
        { name: $_('events.categories.phenomena'), icon: "/icons/phenomena.svg", type: "phenomena" }
    ];

    let searchQuery = '';
    let map: any;

    onMount(() => {
      
    });

    async function locateUser() {
        try {
            const userLocation = await getUserLocation();
            const mapComponent = document.querySelector('div[data-map]');
            if (mapComponent) {
                const mapInstance = (mapComponent as any).__svelte?.type?.instance;
                if (mapInstance?.map) {
                    mapInstance.map.flyTo({
                        center: [userLocation.longitude, userLocation.latitude],
                        zoom: 12,
                        duration: 2000
                    });
                }
            }
        } catch (error) {
            console.error('定位失败:', error);
        }
    }
</script>

<div class="relative w-full" style="height: calc(100vh - 9.6rem)">
    <div class="absolute inset-0">
        <Map data-map />
    </div>
    <div class="absolute top-4 left-4 z-20 w-64 space-y-4">
        <div class="bg-background/95 backdrop-blur p-4 rounded-lg">
            <h1 class="text-xl font-bold">{$_('site.events')}</h1>
            <h2 class="text-sm text-muted-foreground mb-4">{$_('events.subtitle')}</h2>
            <Button variant="outline" class="w-full gap-2">
                <PlusCircle class="h-4 w-4" />
                <span>{$_('events.share')}</span>
            </Button>
        </div>
        <div class="flex flex-wrap gap-2">
            {#each categories as category}
                <div class="bg-background/95 backdrop-blur p-2 rounded-lg flex items-center gap-2 cursor-pointer hover:bg-accent/50 transition-colors">
                    <div class="w-6 h-6 bg-gradient-to-br from-cyan-400/20 to-purple-400/20 rounded-full p-1 group-hover:from-cyan-400/30 group-hover:to-purple-400/30 transition-all">
                        <img src={category.icon} alt={category.name} class="w-full h-full text-cyan-400" />
                    </div>
                    <span class="text-xs text-primary">{category.name}</span>
                </div>
            {/each}
        </div>
    </div>
    <div class="absolute top-4 right-4 z-20 space-y-4">
        <div class="bg-background/95  backdrop-blur rounded-lg w-80">
            <div class="relative w-full flex gap-2 p-4 ">
                <div class="relative flex-1">
                    <Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                    <Input placeholder="Search Location" class="pl-10" />
                </div>
                <Button variant="outline" size="icon" on:click={locateUser} class="shrink-0">
                    <MapPin class="h-4 w-4" />
                </Button>
            </div>
        </div>
        <div class="bg-background/95 backdrop-blur rounded-lg w-80" >
            <div class="p-4 mb-20">
                <h2 class="text-lg font-semibold mb-6">{$_('events.latest')}</h2>
                <EventList />
            </div>
        </div>
    </div>
</div>

<style>
    :global(body) {
        margin: 0;
        padding: 0;
        background: #0a0a0f;
        color: white;
    }

    :global(.mapboxgl-ctrl-bottom-right) {
        display: none;
    }
</style>
