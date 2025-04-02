<script lang="ts">
    import type { PageData } from "./$types";
    import { Input } from "$lib/components/ui/input";
    import {
        Search,
        Star,
        Map,
    } from "lucide-svelte";
    import EventCard from "$lib/components/ui/notion-cards/event-card.svelte";
    import TagNav from "$lib/components/ui/tag-nav/tag-nav.svelte";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";
    import { eventStore } from "$lib/stores/event";
    import { categoryStore } from "$lib/stores/category";
    import type { Event } from "$lib/types/event";
    import type { Category } from "$lib/types/category";
    import { fade, slide } from 'svelte/transition';
    import { GridBackground } from "$lib/components/ui/grid-background";
    import LightGridBackground from "$lib/components/ui/grid-background/light-grid-background.svelte";
    import { onMount } from 'svelte';
    import { ModeWatcher, mode } from "mode-watcher";
    import { NotionPanel } from "$lib/components/layout";
    import EventView from "$lib/components/events/event-view.svelte";
    import { goto } from "$app/navigation";
    import './styles.css';

    let { data }: { data: PageData } = $props();
    let events = $state<Event[]>([]);
    let categories = $state<Category[]>([]);
    let loading = $state(true);
    let selectedCategory = $state("all");
    let searchQuery = "";
    let currentPage = 1;
    const itemsPerPage = 6;
    
    // Panel 状态
    let showEventPanel = $state(false);
    let selectedEvent = $state<Event | null>(null);

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

    // 处理卡片点击
    function handleEventClick(event: Event) {
        selectedEvent = event;
        showEventPanel = true;
    }

    // 处理面板关闭
    function handlePanelClose() {
        showEventPanel = false;
        selectedEvent = null;
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

<ModeWatcher />
<ScrollArea class="h-[calc(100vh-1rem)] relative">
    <!-- 粒子效果容器 -->
    <div class="particle-container">
        {#each Array(20) as _, i}
            <div
                class="particle"
                style="
                    left: {Math.random() * 100}%;
                    animation-delay: {Math.random() * 2}s;
                "
            />
        {/each}
    </div>

    <!-- Hero 区域 -->
    <div class="relative w-full">
        <!-- 背景 -->
        <div class="absolute inset-0">
            {#if $mode === 'dark'}
                <GridBackground />
            {:else}
                <!-- <LightGridBackground /> -->
            {/if}
        </div>

        <!-- 页面标题和搜索栏 -->
        <div class="relative container mx-auto px-20 pointer-events-none pt-10 pb-10">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-20">
                <div class="space-y-4">
                    <div class="inline-flex items-center gap-2">
                        <span class="mysterious-badge px-2 py-1 rounded-md text-sm text-foreground/70">
                            神秘事件
                        </span>
                        
                    </div>
                    <h1 class="mysterious-title text-4xl font-medium tracking-tight">探索未知</h1>
                    <p class="text-sm text-muted-foreground max-w-[600px]">
                        发现并参与各种神秘事件，每一个事件都可能改变你对这个世界的认知...
                    </p>
                </div>
                <div class="flex items-center gap-2 w-full md:w-auto">
                    <div class="relative w-full md:w-[300px] pointer-events-auto">
                        <Search class="absolute left-2.5 top-2.5 h-4 w-4 text-foreground/30" />
                        <Input
                            type="search"
                            placeholder="搜寻神秘..."
                            class="mysterious-search pl-8"
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
    <div class="container mx-auto px-20 space-y-10">
        <div class="space-y-6">
            <!-- 精选区域标题 -->
            <div class="featured-title-container">
                <div class="featured-title-content">
                    <Star class="featured-title-icon h-4 w-4" />
                    <span class="featured-title-text">精选神秘事件</span>
                </div>
                <div class="featured-divider"></div>
            </div>

            <!-- 事件卡片网格 -->
            <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-3 gap-6">
                {#if loading}
                    {#each Array(6) as _}
                        <div class="hover-lift">
                            <div class="glow-effect">
                                <EventCard loading={true} title="" />
                            </div>
                        </div>
                    {/each}
                {:else if filteredEvents.length === 0}
                    <div class="col-span-full flex items-center justify-center py-20">
                        <div class="text-center space-y-4">
                            <div class="mysterious-badge w-12 h-12 rounded-full mx-auto flex items-center justify-center">
                                <Star class="h-6 w-6 text-foreground/70" />
                            </div>
                            <div class="space-y-2">
                                <p class="text-lg font-medium">暂无神秘事件</p>
                                <p class="text-sm text-muted-foreground">敬请期待更多神秘事件的出现...</p>
                            </div>
                        </div>
                    </div>
                {:else}
                    {#each filteredEvents as event (event.$id)}
                        <div
                            in:fade={fadeConfig}
                            out:slide={slideConfig}
                            on:click={() => handleEventClick(event)}
                            class="hover-lift"
                        >
                            <div class="glow-effect">
                                <EventCard
                                    title={event.title || ''}
                                    image={event.cover_image || ''}
                                    avatarSrc={event.creator_avatar}
                                    tags={event.category ? [event.category] : []}
                                    rating={0}
                                />
                            </div>
                        </div>
                    {/each}
                {/if}
            </div>
        </div>
    </div>
</ScrollArea>

<!-- 事件详情面板 -->
<NotionPanel 
    open={showEventPanel}
    width={45}
    maxWidth={60}
    showHeader={false}
    showFooter={false}
    component={EventView}
    componentProps={{
        event: selectedEvent
    }}
    on:close={handlePanelClose}
/>

<style>
    /* 移除旧的网格样式 */
    :global(.bg-grid-white) {
        display: none;
    }

    .light-grid-background,
    .light-grid {
        display: none;
    }
</style>
