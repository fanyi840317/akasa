<script lang="ts">
    import type { PageData } from './$types';
    import Map from '$lib/components/Map.svelte';
    import EventList from '$lib/components/EventList.svelte';
    import { _ } from 'svelte-i18n';
    import * as Card from "$lib/components/ui/card";
    import { theme } from '$lib/stores/theme';
    import { onMount } from 'svelte';
    import { get } from 'svelte/store';

    let { data }: { data: PageData } = $props();

    const categories = [
        { name: $_('events.categories.urban'), icon: "/icons/urban.svg", type: "urban" },
        { name: $_('events.categories.paranormal'), icon: "/icons/paranormal.svg", type: "paranormal" },
        { name: $_('events.categories.supernatural'), icon: "/icons/supernatural.svg", type: "supernatural" },
        { name: $_('events.categories.mysterious'), icon: "/icons/mysterious.svg", type: "mysterious" },
        { name: $_('events.categories.unexplained'), icon: "/icons/unexplained.svg", type: "unexplained" },
        { name: $_('events.categories.phenomena'), icon: "/icons/phenomena.svg", type: "phenomena" }
    ];


    onMount(() => {
      
    });
</script>

<div class="container flex flex-col min-h-screen">
    <!-- 主要内容区域 -->
    <main class="flex-1">
        
        <!-- 地图和标题区域 -->
        <div class="relative h-[70vh] rounded-lg overflow-hidden">
            <!-- 地图层 -->
            <div class="absolute inset-0 z-10 rounded-lg">
                <Map />
            </div>
            
            <!-- 雷达图覆盖层 -->
            <!-- <div class="absolute top-4 right-4 w-48 h-48 opacity-80">
                <img src="/images/radar.svg" alt="radar" class="w-full h-full" />
            </div> -->

            <!-- 标题层 - 只在顶部添加渐变遮罩 -->
            <div class="absolute inset-0 z-20 pointer-events-none">
                <div class="h-1/2 bg-gradient-to-b from-black/50 to-transparent">
                    <div class="container mx-auto px-4 py-16">
                        <div class="max-w-2xl pointer-events-auto">
                            <h1 class="text-5xl font-bold text-white mb-4 drop-shadow-lg">
                                {$_('events.mysterious')}
                            </h1>
                            <p class="text-cyan-400/80 text-lg mb-8 drop-shadow-md">
                                {$_('events.discover')}
                            </p>
                            <button class="bg-cyan-400/20 text-cyan-400 px-6 py-2 rounded-full 
                                hover:bg-cyan-400/30 transition-colors backdrop-blur-sm">
                                Discover More
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 分类卡片网格 -->
        <div class="mx-auto py-8">
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
                {#each categories as category}
                    <Card.Root>
                        <Card.Header class="text-center p-6">
                            <div class="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-cyan-400/20 
                                to-purple-400/20 rounded-full p-3 group-hover:from-cyan-400/30 
                                group-hover:to-purple-400/30 transition-all">
                                <img src={category.icon} alt={category.name} class="w-full h-full text-cyan-400" />
                            </div>
                            <Card.Title class="text-cyan-400 text-lg">
                                {category.name}
                            </Card.Title>
                        </Card.Header>
                    </Card.Root>
                {/each}
            </div>
        </div>
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
