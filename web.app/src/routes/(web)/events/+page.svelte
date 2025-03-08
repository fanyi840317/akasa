<script lang="ts">
    import type { PageData } from './$types';
    import Map from '$lib/components/map.svelte';
    import EventList from '$lib/components/event-list.svelte';
    import { _ } from 'svelte-i18n';
    import * as Card from "$lib/components/ui/card";
    import { theme } from '$lib/stores/theme';
    import { onMount } from 'svelte';
    import { get } from 'svelte/store';
    import { Input } from "$lib/components/ui/input";
    import { Button } from "$lib/components/ui/button";
    import { PlusCircle, Search, MapPin, Image, Loader2, ChevronRight, ChevronLeft } from "lucide-svelte";
    import { auth } from "$lib/stores/auth";
    import { goto } from "$app/navigation";
    import { base } from '$app/paths';

    import { Textarea } from "$lib/components/ui/textarea";
    import { Label } from "$lib/components/ui/label";
    import { databases } from "$lib/appwrite";
    import { ID } from "appwrite";
    // import StepWindow from "$lib/components/StepWindow.svelte";

    let showCreatePanel = writable(false);
    
    let loading = false;
    let title = "";
    let description = "";
    let location = "";
    let imageFile: File | null = null;
    let imagePreview: string | null = null;
    let currentStep = 0;
    const totalSteps = 3;

    const steps = [
        { title: $_('events.create.step1_title'), description: $_('events.create.step1_desc') },
        { title: $_('events.create.step2_title'), description: $_('events.create.step2_desc') },
        { title: $_('events.create.step3_title'), description: $_('events.create.step3_desc') }
    ];

    // 处理分享按钮点击事件
    function handleShare() {
        if (!$auth.user) {
            goto(`${base}/login`);
            return;
        }
        $showCreatePanel = true;
    }
    import { writable } from 'svelte/store';

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

    // 新增一个可写的 store 来存储搜索结果
    const searchResults = writable([]);

    // 搜索位置的函数
    function searchLocation() {
        // if (!data.events) return;
        // const results = data.events.filter(event => 
        //     event.location.toLowerCase().includes(searchQuery.toLowerCase())
        // );
        // searchResults.set(results);
        updateMapLocation(searchQuery);
    }

    // 处理回车事件
    function handleKeyPress(event: KeyboardEvent) {
        if (event.key === 'Enter') {
            searchLocation();
        }
    }

    // 更新地图位置的函数
    async function updateMapLocation(location: string) {
        const response = await fetch(`https://api.example.com/geocode?address=${encodeURIComponent(location)}`);
        const data = await response.json();
        if (data && data.results && data.results.length > 0) {
            const { lat, lng } = data.results[0].geometry.location;
            map.setCenter([lng, lat]);
        } else {
            console.error('未找到该位置');
        }
    }

    onMount(() => {
        // 初始化地图
        // map = ...; // 初始化地图对象
    });
</script>

<div class="relative w-full h-[100%]">
    <div class="absolute inset-0">
        <Map locationData={data.location} />
    </div>
    <div class="absolute top-4 left-4 z-20 w-64 space-y-4">
        <Card.Root class="backdrop-blur-sm border-none shadow-lg">
            <Card.Content class="p-4">
                <h1 class="text-xl font-bold">{$_('site.events')}</h1>
                <h2 class="text-sm text-muted-foreground mb-4">{$_('events.subtitle')}</h2>
                <Button variant="outline" class="w-full gap-2" onclick={handleShare}>
                    <PlusCircle class="h-4 w-4" />
                    <span>{$_('events.share')}</span>
                </Button>
            </Card.Content>
        </Card.Root>
        
        <div class="flex flex-wrap gap-2">
            {#each categories as category}
                <Card.Root class="p-2 flex items-center gap-2 cursor-pointer hover:bg-accent/50 transition-colors border-none shadow-sm backdrop-blur-sm">
                    <div class="w-6 h-6 bg-gradient-to-br from-cyan-400/20 to-purple-400/20 rounded-full p-1 group-hover:from-cyan-400/30 group-hover:to-purple-400/30 transition-all">
                        <img src="{base}{category.icon}" alt="{category.name}" class="w-full h-full text-cyan-400" />
                    </div>
                    <span class="text-xs text-primary">{category.name}</span>
                </Card.Root>
            {/each}
        </div>
    </div>
    <div class="absolute top-4 right-4 z-20 space-y-4">
        <Card.Root class="w-80 backdrop-blur-sm border-none shadow-lg">
            <Card.Content class="p-4">
                <div class="relative w-full flex gap-2">
                    <div class="relative flex-1">
                        <Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                        <Input 
                            placeholder="Search Location" 
                            class="pl-10" 
                            bind:value={searchQuery} 
                            onkeypress={handleKeyPress}
                        />
                    </div>
                    <Button variant="outline" size="icon" class="shrink-0" onclick={searchLocation}>
                        <MapPin class="h-4 w-4" />
                    </Button>
                </div>
            </Card.Content>
        </Card.Root>
        
        <Card.Root class="w-80 backdrop-blur-sm border-none shadow-lg">
            <Card.Content class="p-4">
                <h2 class="text-lg font-semibold mb-6">{$_('events.latest')}</h2>
                <EventList/>
            </Card.Content>
        </Card.Root>
    </div>
    
 
</div>

<!-- <NotionEventCreator isOpen={$showCreatePanel} onClose={()=>{$showCreatePanel = false}} /> -->