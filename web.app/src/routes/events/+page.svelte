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
    import { PlusCircle, Search } from "lucide-svelte";

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

    onMount(() => {
      
    });
</script>

<div class="container flex flex-col ">
    <main class="flex-1 py-6">
        <div class="flex justify-between items-center mb-4">
            <div class="space-y-1">
                <h1 class="text-3xl font-bold">{$_('site.events')}</h1>
                <h2 class="text-sm text-muted-foreground">{$_('events.subtitle')}</h2>
            </div>
            <Button variant="outline" class="gap-2">
                <PlusCircle class="h-4 w-4" />
                <span>{$_('events.share')}</span>
            </Button>
        </div>
        <!-- 地图区域 -->
        <div class="relative rounded-lg overflow-hidden h-[70vh]">
            <div class="absolute top-4 right-4 z-10 w-64">
                <div class="relative w-full">
                    <Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                    <Input placeholder="Search Location" class="bg-background/95 backdrop-blur pl-10" />
                </div>
            </div>
            <div class="absolute top-4 left-4 z-20 w-64 flex flex-wrap gap-2">
                {#each categories as category}
                    <div class="bg-background/95 backdrop-blur p-2 rounded-lg flex items-center gap-2 cursor-pointer hover:bg-accent/50 transition-colors">
                        <div class="w-6 h-6 bg-gradient-to-br from-cyan-400/20 to-purple-400/20 rounded-full p-1 group-hover:from-cyan-400/30 group-hover:to-purple-400/30 transition-all">
                            <img src={category.icon} alt={category.name} class="w-full h-full text-cyan-400" />
                        </div>
                        <span class="text-xs text-cyan-400">{category.name}</span>
                    </div>
                {/each}
            </div>
            <Map />
        </div>
        <!-- 事件列表区域 -->
        <!-- <h1 class="text-3xl font-bold py-10">{$_('events.mysterious')}</h1>
        <div class="mt-6 rounded-xl bg-background/40 backdrop-blur">
            <EventList />
        </div> -->
    </main>
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
