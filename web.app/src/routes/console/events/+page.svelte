<script lang="ts">
    import type { PageData } from "./$types";
    import { Input } from "$lib/components/ui/input";
    import { Search, Star, Map } from "lucide-svelte";
    import EventCard from "$lib/components/ui/notion-cards/event-card.svelte";
    import TagNav from "$lib/components/ui/tag-nav/tag-nav.svelte";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";
    import { eventStore } from "$lib/stores/event";
    import { categoryStore } from "$lib/stores/category";
    import type { Event } from "$lib/types/event";
    import type { Category } from "$lib/types/category";
    import { fly } from "svelte/transition";
    import { onMount } from "svelte";
    import { ModeWatcher } from "mode-watcher";
    import { NotionPanel } from "$lib/components/layout";
    import EventView from "$lib/components/events/event-view.svelte";
    import { Motion } from "svelte-motion";
    import Globe from "$lib/components/ui/globe/Globe.svelte";
    import GlobeLeftContent from "$lib/components/ui/globe/GlobeLeftContent.svelte";
    import EventSidebarCards from "$lib/components/events/event-sidebar-cards.svelte";
    import EventStatsSidebar from "$lib/components/events/event-stats-sidebar.svelte";
    import { Sparkles } from "lucide-svelte";
    import BorderBeam from "$lib/components/ui/background/border-beam.svelte";
    import Marquee from "$lib/components/ui/marquee/Marquee.svelte";
    import DarkTiles from "$lib/components/ui/background/dark-tiles.svelte";

    let events = $state<Event[]>([]);
    let categories = $state<Category[]>([]);
    let loading = $state(true);
    let selectedCategory = $state("all");

    // Panel 状态
    let showEventPanel = $state(false);
    let selectedEvent = $state<Event | null>(null);

    // 分类标签

    // 过滤后的事件列表
    let filteredEvents = $derived(
        selectedCategory === "all"
            ? events
            : events.filter(
                  (event) =>
                      event.categories &&
                      event.categories.includes(selectedCategory),
              ),
    );

    // 获取事件和分类数据
    async function fetchData() {
        try {
            loading = true;
            const [eventsResponse, categoriesResponse] = await Promise.all([
                eventStore.fetchEvents(),
                categoryStore.fetchCategories(),
            ]);

            events = eventsResponse as unknown as Event[];
            categories = categoriesResponse;
        } catch (error) {
            console.error("Failed to fetch data:", error);
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
        // 直接添加模拟数据以确保显示
        addMockEvents();

        // 然后尝试从服务器获取数据
        // fetchData();
        console.log("Fetching data...");
    });

    // 监听事件数据变化
    $effect(() => {
        console.log("Events loaded:", events.length);
        console.log("Filtered events:", filteredEvents.length);

        // 直接添加模拟数据以确保显示
        if (!loading && events.length === 0) {
            addMockEvents();
        }
    });

    // 添加模拟数据函数，确保有事件显示
    function addMockEvents() {
        if (events.length === 0) {
            console.log("Adding mock events...");
            const mockEvents = [
                {
                    $id: "mock1",
                    title: "神秘森林事件",
                    content: "在深山密林中发现的不明现象，多人目击光怪物体。",
                    cover: "https://images.unsplash.com/photo-1448375240586-882707db888b",
                    tags: ["森林", "超自然"],
                    categories: ["all"],
                    date: new Date().toISOString(),
                    user_id: "user1",
                    creator_name: "探索者",
                    creator_avatar:
                        "https://api.dicebear.com/7.x/bottts/svg?seed=explorer",
                },
                {
                    $id: "mock2",
                    title: "海底异常信号",
                    content:
                        "深海探测器捕捉到的不明声波信号，可能来自未知生物。",
                    cover: "https://images.unsplash.com/photo-1551244072-5d12893278ab",
                    tags: ["海洋", "信号"],
                    categories: ["all"],
                    date: new Date().toISOString(),
                    user_id: "user2",
                    creator_name: "海洋学家",
                    creator_avatar:
                        "https://api.dicebear.com/7.x/bottts/svg?seed=ocean",
                },
                {
                    $id: "mock3",
                    title: "沙漠奇异光点",
                    content: "沙漠中出现的不明光点，夜间移动并改变形状。",
                    cover: "https://images.unsplash.com/photo-1509316785289-025f5b846b35",
                    tags: ["沙漠", "光点"],
                    categories: ["all"],
                    date: new Date().toISOString(),
                    user_id: "user3",
                    creator_name: "沙漠向导",
                    creator_avatar:
                        "https://api.dicebear.com/7.x/bottts/svg?seed=desert",
                },
                {
                    $id: "mock4",
                    title: "古城府密室发现",
                    content:
                        "考古队在古城府遗址发现的密室，内有不明文字和图案。",
                    cover: "https://images.unsplash.com/photo-1461988320302-91bde64fc8e4",
                    tags: ["古迹", "密室"],
                    categories: ["all"],
                    date: new Date().toISOString(),
                    user_id: "user4",
                    creator_name: "考古学家",
                    creator_avatar:
                        "https://api.dicebear.com/7.x/bottts/svg?seed=ancient",
                },
                {
                    $id: "mock5",
                    title: "天空不明飞行物",
                    content:
                        "多人目击的天空不明飞行物，移动速度超过已知飞行器。",
                    cover: "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a",
                    tags: ["天空", "UFO"],
                    categories: ["all"],
                    date: new Date().toISOString(),
                    user_id: "user5",
                    creator_name: "天文爱好者",
                    creator_avatar:
                        "https://api.dicebear.com/7.x/bottts/svg?seed=sky",
                },
                {
                    $id: "mock6",
                    title: "山洞古老符文",
                    content: "山洞中发现的不明符文，与已知文字系统不符。",
                    cover: "https://images.unsplash.com/photo-1496275068113-fff8c90750d1",
                    tags: ["山洞", "符文"],
                    categories: ["all"],
                    date: new Date().toISOString(),
                    user_id: "user6",
                    creator_name: "语言学家",
                    creator_avatar:
                        "https://api.dicebear.com/7.x/bottts/svg?seed=cave",
                },
            ];

            events = [...mockEvents];
        }
    }
    // 获取随机默认封面图
    function getRandomDefaultCover(): string {
        const defaultCovers = [
            "/images/cover/c1.webp",
            "/images/cover/c2.webp",
            "/images/cover/c3.webp",
        ];
        const randomIndex = Math.floor(Math.random() * defaultCovers.length);
        return defaultCovers[randomIndex];
    }

    // 处理封面图片
    function getCoverUrl(event: Event): string {
        if (!event.cover) return getRandomDefaultCover();

        return event.cover || getRandomDefaultCover();
    }
</script>

<!-- <ModeWatcher /> -->
<div class="w-full h-full flex flex-col relative bg-card">
    
    <div class="flex flex-row h-full items-center justify-center">
       
        <!-- 左侧：新增内容区域 -->
        <div class="w-2/5 h-full flex items-center justify-end pr-8">
            <GlobeLeftContent />
        </div>

        <!-- 中间：地球组件 -->
        <div
            class="relative w-[400px] h-[400px] md:w-[400px] md:h-[400px] flex items-center justify-center"
        >
            <div
                class="absolute inset-0 rounded-full bg-blue-500/5 dark:bg-blue-500/10 blur-2xl"
            ></div>
            <Globe class="w-full h-full text-blue-500 dark:text-blue-400" />
        </div>

        <!-- 右侧：事件跑马灯 -->
    </div>
    <div class="flex flex-row mb-20 mx-40 relative">
        <Marquee>
            {#each events.slice(0, 5) as event}
                <article
                    class="flex flex-row items-start justify-center relative gap-x-4 p-4"
                >
                    <div
                        class="flex flex-col items-center justify-center gap-y-1"
                    >
                        <img
                            src={getCoverUrl(event)}
                            placeholder="blur"
                            alt="don corleone"
                            class="w-[100px] h-[60px] object-cover rounded-sm"
                        />
                        <div class="text-gray-300 z-10 text-xs">
                            {event.date.split("T")[0]}
                        </div>
                    </div>

                    <!-- <div
                class="absolute inset-0 from-neutral-900/90 via-neutral-900/80 to-neutral-900/50
    rounded-xl bg-gradient-to-t backdrop-blur-[4px] transition-all duration-300"
            ></div> -->

                    <!-- <BorderBeam size={150} duration={12} /> -->
                    <div
                        class="flex flex-col flex-1 items-start gap-y-2 mt-0.5"
                    >
                        <!-- <div class="flex items-center gap-x-4 text-xs">
                <div class="text-gray-300 z-10">Mar 16, 2020</div>

            </div> -->
                        <div class="group relative">
                            <h3
                                class=" text-md font-semibold leading-6
                break-words line-clamp-1
                text-gray-200 group-hover:text-gray-50"
                            >
                                <a href="/">
                                    {event.title.substring(0, 10)}
                                </a>
                            </h3>
                        </div>
                        <div class="relative flex items-center gap-x-2">
                            <div class="text-[8px]">
                                <p class="text-white">
                                    <a href="https://github.com/SikandarJODD">
                                        <span class="absolute inset-0"></span>
                                        {event.creator_name}
                                    </a>
                                </p>
                                <p class="text-gray-500">Developer</p>
                            </div>
                            <img
                                src="https://avatars.githubusercontent.com/u/93428946?v=4"
                                alt="bhide"
                                class="h-4 w-4 rounded-full bg-gray-50"
                            />
                        </div>
                    </div>
                </article>
            {/each}
        </Marquee>
        <div
            class="pointer-events-none absolute inset-y-0 left-0 w-1/3 h-full bg-gradient-to-r from-white dark:from-card"
        ></div>
        <div
            class="pointer-events-none absolute inset-y-0 right-0 w-1/3 h-full bg-gradient-to-l from-white dark:from-card"
        ></div>
    </div>
</div>

<!-- 事件详情面板 -->
<NotionPanel
    open={showEventPanel}
    width={45}
    maxWidth={60}
    showHeader={false}
    showFooter={false}
    component={EventView}
    componentProps={{
        event: selectedEvent,
    }}
    on:close={handlePanelClose}
/>

<style>
    /* 移除旧的网格样式 */
    :global(.bg-grid-white) {
        display: none;
    }
</style>
