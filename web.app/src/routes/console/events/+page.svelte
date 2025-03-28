<script lang="ts">
    import type { PageData } from "./$types";
    import { Input } from "$lib/components/ui/input";
    import { Button } from "$lib/components/ui/button";
    import {
        Search,
        Filter,
        Calendar,
        MapPin,
        Users,
        Star,
    } from "lucide-svelte";
    import EventCard from "$lib/components/ui/notion-cards/event-card.svelte";
    import TagNav from "$lib/components/ui/tag-nav/tag-nav.svelte";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";
    import ShareButton from "$lib/components/ui/share/share-button.svelte";
    import SharePanel from "$lib/components/ui/share/share-panel.svelte";
    import { eventStore } from "$lib/stores/event";
    import { categoryStore } from "$lib/stores/category";
    import { Query } from "appwrite";
    import type { Event } from "$lib/types/event";
    import type { Category } from "$lib/types/category";
    import { fade, slide, scale } from 'svelte/transition';
    import { GridBackground } from "$lib/components/ui/grid-background";
    import { onMount } from 'svelte';

    let { data }: { data: PageData } = $props();
    let showSharePanel = $state(false);
    let events = $state<Event[]>([]);
    let categories = $state<Category[]>([]);
    let loading = $state(true);
    let selectedCategory = $state("all");
    let searchQuery = "";
    let currentPage = 1;
    const itemsPerPage = 6;

    // 分类标签
    let categoryItems = $derived([
        { id: "all", name: "全部" },
        ...categories.map(cat => ({
            id: cat.$id,
            name: cat.name.zh,
            color: cat.color
        }))
    ]);

    // 过滤后的事件列表
    let filteredEvents = $derived(
        selectedCategory === 'all'
            ? events
            : events.filter(event => event.category === selectedCategory)
    );

    const totalPages = $derived(Math.ceil(events.length / itemsPerPage));

    // 获取事件和分类数据
    async function fetchData() {
        try {
            loading = true;
            const [eventsResponse, categoriesResponse] = await Promise.all([
                eventStore.fetchEvents(),
                categoryStore.fetchCategories()
            ]);
            
            events = eventsResponse as unknown as Event[];
            categories = categoriesResponse;
        } catch (error) {
            console.error('Failed to fetch data:', error);
        } finally {
            loading = false;
        }
    }

    // 页面加载时获取数据
    onMount(() => {
        fetchData();
    });

    function formatDate(dateString: string) {
        const date = new Date(dateString);
        return date.toLocaleDateString("zh-CN", {
            year: "numeric",
            month: "long",
            day: "numeric",
        });
    }

    // 添加过渡动画配置
    const fadeConfig = { duration: 300 };
    const slideConfig = { duration: 300 };
    const scaleConfig = { duration: 200 };
</script>

<ScrollArea class="h-[calc(100vh-1rem)] relative">
    <!-- Hero 区域 -->
    <div class="relative w-full">
        <!-- 网格背景 -->
        <div class="absolute inset-0 bg-background/80">
            <GridBackground className="w-full h-full" />
        </div>

        <!-- 页面标题和搜索栏 -->
        <div class="relative container mx-auto px-20 pointer-events-none pt-20 pb-10">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-20">
                <div >
                    <h1 class="text-3xl font-bold mb-2">活动与事件</h1>
                    <p class="text-sm text-muted-foreground">发现并参与各种精彩活动</p>
                </div>
                <div class="flex items-center gap-2 w-full md:w-auto">
                    <div class="relative w-full md:w-[300px] pointer-events-auto">
                        <Search class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                        <Input
                            type="search"
                            placeholder="搜索活动..."
                            class="pl-8"
                            bind:value={searchQuery}
                        />
                    </div>
                </div>
            </div>

            <!-- 分类标签 -->
            <div class="mt-6 pointer-events-auto">
                <TagNav bind:selectedId={selectedCategory} items={categoryItems} />
            </div>
        </div>
    </div>

    <!-- 内容区域 -->
    <div class="container mx-auto px-20 space-y-10 `">
        <div class="space-y-4">
            <!-- 精选模板区域 -->
            <div class="flex items-center gap-2 px-2 text-muted-foreground">
                <Star class="h-3 w-3" />
                <span class="text-xs">精选模板</span>
            </div>

            <!-- 事件卡片网格 -->
            <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-3 gap-6">
                {#if loading}
                    <div class="col-span-full text-center py-8">加载中...</div>
                {:else}
                    {#each filteredEvents as event (event.$id)}
                        <div
                            in:fade={fadeConfig}
                            out:slide={slideConfig}
                        >
                            <EventCard
                                title={event.title || ''}
                                image={event.creator_avatar || ''}
                                tags={[event.category || '']}
                                rating={0}
                            />
                        </div>
                    {/each}
                {/if}
            </div>
        </div>
    </div>
</ScrollArea>

<style>
    :global(.bg-grid-white) {
        background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    }
</style>
