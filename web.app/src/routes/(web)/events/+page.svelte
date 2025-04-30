<script lang="ts">
    import MapBase from "$lib/components/map/map-base.svelte";
    import { Input } from "$lib/components/ui/input";
    import { Search, ChevronDown, User } from "lucide-svelte";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";
    import { eventStore } from "$lib/stores/event";
    import { categoryStore } from "$lib/stores/category";
    import type { Event } from "$lib/types/event";
    import type { Category } from "$lib/types/category";
    import { fly } from "svelte/transition";
    import { onMount } from "svelte";
    import { Motion } from "svelte-motion";
    import { cn } from "$lib/utils";
    import * as Select from "$lib/components/ui/select";
    import * as Avatar from "$lib/components/ui/avatar";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
    import { auth } from "$lib/stores/auth";

    // 状态变量
    let events = $state<Event[]>([]);
    let categories = $state<Category[]>([]);
    let loading = $state(true);
    let searchQuery = $state("");
    let selectedCategory = $state("all");
    let sortOption = $state("newest"); // newest, oldest, alphabetical

    // 过滤后的事件列表
    let filteredEvents = $state<Event[]>([]);

    // 更新过滤后的事件列表
    $effect(() => {
        if (!events.length) return;

        // 先按类别筛选
        let filtered =
            selectedCategory === "all"
                ? events
                : events.filter(
                      (event) =>
                          event.categories &&
                          event.categories.includes(selectedCategory),
                  );

        // 再按搜索关键词筛选
        if (searchQuery.trim()) {
            const query = searchQuery.toLowerCase();
            filtered = filtered.filter(
                (event) =>
                    event.title.toLowerCase().includes(query) ||
                    event.content.toLowerCase().includes(query) ||
                    (event.location_data?.city &&
                        event.location_data.city
                            .toLowerCase()
                            .includes(query)) ||
                    (event.location_data?.country &&
                        event.location_data.country
                            .toLowerCase()
                            .includes(query)),
            );
        }

        // 最后排序
        switch (sortOption) {
            case "newest":
                filtered = [...filtered].sort(
                    (a, b) =>
                        new Date(b.date).getTime() - new Date(a.date).getTime(),
                );
                break;
            case "oldest":
                filtered = [...filtered].sort(
                    (a, b) =>
                        new Date(a.date).getTime() - new Date(b.date).getTime(),
                );
                break;
            case "alphabetical":
                filtered = [...filtered].sort((a, b) =>
                    a.title.localeCompare(b.title),
                );
                break;
        }

        filteredEvents = filtered;
    });

    // 处理搜索输入
    function handleSearchInput(e: any) {
        const target = e.target as HTMLInputElement;
        searchQuery = target.value;
    }

    // 处理类别选择
    function handleCategorySelect(category: string | any) {
        if (typeof category === "string") {
            selectedCategory = category;
        } else {
            const target = category.target as HTMLSelectElement;
            selectedCategory = target.value;
        }
    }

    // 处理排序选择
    function handleSortSelect(option: string | any) {
        if (typeof option === "string") {
            sortOption = option;
        } else {
            const target = option.target as HTMLSelectElement;
            sortOption = target.value;
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

    // 根据事件类型生成颜色
    function getEventColor(event: Event): string {
        if (!event.tags || event.tags.length === 0) {
            return "#6c757d"; // 默认灰色
        }

        // 根据标签返回不同的颜色
        if (event.tags.includes("UFO") || event.tags.includes("天空")) {
            return "#e74c3c"; // 红色
        } else if (event.tags.includes("森林") || event.tags.includes("超自然")) {
            return "#9b59b6"; // 紫色
        } else if (event.tags.includes("海洋") || event.tags.includes("信号")) {
            return "#3498db"; // 蓝色
        } else if (event.tags.includes("沙漠") || event.tags.includes("光点")) {
            return "#f39c12"; // 橙色
        } else if (event.tags.includes("古迹") || event.tags.includes("密室")) {
            return "#27ae60"; // 绿色
        } else if (event.tags.includes("山洞") || event.tags.includes("符文")) {
            return "#f1c40f"; // 黄色
        }

        // 如果没有匹配的标签，根据事件ID生成随机但一致的颜色
        const colors = ["#e74c3c", "#9b59b6", "#3498db", "#f39c12", "#27ae60", "#f1c40f"];
        const index = event.$id.charCodeAt(0) % colors.length;
        return colors[index];
    }

    // 获取事件的首字母缩写
    function getEventInitials(event: Event): string {
        if (event.tags && event.tags.length > 0) {
            // 使用第一个标签的首字母或前两个字母
            const tag = event.tags[0];
            if (tag.length <= 2) {
                return tag.toUpperCase();
            } else {
                // 对于中文标签，取前两个字符
                if (/[\u4e00-\u9fa5]/.test(tag)) {
                    return tag.substring(0, 2);
                }
                // 对于英文标签，取首字母和第一个大写字母或第二个字母
                const firstChar = tag.charAt(0).toUpperCase();
                let secondChar = '';

                // 尝试找第一个大写字母作为第二个字符
                for (let i = 1; i < tag.length; i++) {
                    if (tag.charAt(i) === tag.charAt(i).toUpperCase() && tag.charAt(i) !== tag.charAt(i).toLowerCase()) {
                        secondChar = tag.charAt(i);
                        break;
                    }
                }

                // 如果没找到大写字母，就用第二个字母
                if (!secondChar && tag.length > 1) {
                    secondChar = tag.charAt(1).toUpperCase();
                }

                return firstChar + (secondChar || '');
            }
        } else if (event.location_data?.city) {
            // 使用城市名的首字母或前两个字符
            const city = event.location_data.city;
            if (/[\u4e00-\u9fa5]/.test(city)) {
                return city.substring(0, 2);
            }
            return city.substring(0, 2).toUpperCase();
        } else if (event.title) {
            // 使用标题的首字母或前两个字符
            if (/[\u4e00-\u9fa5]/.test(event.title)) {
                return event.title.substring(0, 2);
            }

            const words = event.title.split(' ');
            if (words.length >= 2) {
                return (words[0].charAt(0) + words[1].charAt(0)).toUpperCase();
            }
            return event.title.substring(0, 2).toUpperCase();
        }

        // 默认返回
        return "MN";
    }

    // 加载数据
    async function loadData() {
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
            // 添加模拟数据以确保显示
            addMockEvents();
        } finally {
            loading = false;
        }
    }

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
                    location_data: {
                        coordinates: { lat: 39.9042, lng: 116.4074 },
                        country: "CN",
                        city: "北京",
                    },
                },
                {
                    $id: "mock2",
                    title: "海底异常信号",
                    content:
                        "深海探测器捕捉到的不明声波信号，可能来自未知生物。",
                    cover: "https://images.unsplash.com/photo-1551244072-5d12893278ab",
                    tags: ["海洋", "信号"],
                    categories: ["all"],
                    date: new Date(Date.now() - 86400000).toISOString(), // 1天前
                    user_id: "user2",
                    creator_name: "海洋学家",
                    creator_avatar:
                        "https://api.dicebear.com/7.x/bottts/svg?seed=ocean",
                    location_data: {
                        coordinates: { lat: 35.6762, lng: 139.6503 },
                        country: "JP",
                        city: "东京",
                    },
                },
                {
                    $id: "mock3",
                    title: "沙漠奇异光点",
                    content: "沙漠中出现的不明光点，夜间移动并改变形状。",
                    cover: "https://images.unsplash.com/photo-1509316785289-025f5b846b35",
                    tags: ["沙漠", "光点"],
                    categories: ["all"],
                    date: new Date(Date.now() - 172800000).toISOString(), // 2天前
                    user_id: "user3",
                    creator_name: "沙漠向导",
                    creator_avatar:
                        "https://api.dicebear.com/7.x/bottts/svg?seed=desert",
                    location_data: {
                        coordinates: { lat: 29.9792, lng: 31.1342 },
                        country: "EG",
                        city: "开罗",
                        name: "金字塔",
                    },
                },
                {
                    $id: "mock4",
                    title: "古城府密室发现",
                    content:
                        "考古队在古城府遗址发现的密室，内有不明文字和图案。",
                    cover: "https://images.unsplash.com/photo-1461988320302-91bde64fc8e4",
                    tags: ["古迹", "密室"],
                    categories: ["all"],
                    date: new Date(Date.now() - 259200000).toISOString(), // 3天前
                    user_id: "user4",
                    creator_name: "考古学家",
                    creator_avatar:
                        "https://api.dicebear.com/7.x/bottts/svg?seed=ancient",
                    location_data: {
                        coordinates: { lat: 40.4319, lng: 116.5704 },
                        country: "CN",
                        city: "北京",
                        name: "长城",
                    },
                },
                {
                    $id: "mock5",
                    title: "天空不明飞行物",
                    content:
                        "多人目击的天空不明飞行物，移动速度超过已知飞行器。",
                    cover: "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a",
                    tags: ["天空", "UFO"],
                    categories: ["all"],
                    date: new Date(Date.now() - 345600000).toISOString(), // 4天前
                    user_id: "user5",
                    creator_name: "天文爱好者",
                    creator_avatar:
                        "https://api.dicebear.com/7.x/bottts/svg?seed=sky",
                    location_data: {
                        coordinates: { lat: 37.7749, lng: -122.4194 },
                        country: "US",
                        city: "旧金山",
                    },
                },
                {
                    $id: "mock6",
                    title: "山洞古老符文",
                    content: "山洞中发现的不明符文，与已知文字系统不符。",
                    cover: "https://images.unsplash.com/photo-1496275068113-fff8c90750d1",
                    tags: ["山洞", "符文"],
                    categories: ["all"],
                    date: new Date(Date.now() - 432000000).toISOString(), // 5天前
                    user_id: "user6",
                    creator_name: "语言学家",
                    creator_avatar:
                        "https://api.dicebear.com/7.x/bottts/svg?seed=cave",
                    location_data: {
                        coordinates: { lat: 51.5074, lng: -0.1278 },
                        country: "GB",
                        city: "伦敦",
                    },
                },
            ];

            events = [...mockEvents];
        }
    }

    // 页面加载时加载数据
    onMount(() => {
        loadData();
        // 初始化用户认证
        auth.init();
    });
</script>

<div class="w-full h-[90vh] px-1 pt-2 flex flex-row">
    
    <div class="w-2/5 h-full flex items-center justify-end p-8 ">
        <div
        class="w-[380px] h-full flex flex-col bg-neutral-900 rounded-xl"
        in:fly={{ x: -300, duration: 800, delay: 200 }}
    >
        <!-- 用户信息和搜索区域 -->
        <div class="p-4 space-y-4">
            <!-- 用户信息 -->
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-lg font-semibold">神秘事件</h2>

        
            </div>

            <!-- 搜索框 -->
            <div class="relative">
                <Input
                    type="text"
                    class="bg-background border-0 rounded-sm pl-12 placeholder:text-xs"
                    value={searchQuery}
                    style=""
                    oninput={handleSearchInput}
                />
                <span
                    class="absolute left-2 top-1/2 text-xs font-semibold
                -translate-y-1/2 h-4 w-12 text-muted-foreground"
                    >搜索事件
                </span>
                <button
                    class="absolute right-2 top-1/2 -translate-y-1/2
                text-muted-foreground hover:text-foreground transition-colors"
                    onclick={() => (searchQuery = "")}
                    aria-label={searchQuery ? "清除搜索" : "搜索"}
                >
                    {#if searchQuery}
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="18"
                            height="18"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                        >
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                    {:else}
                        <Search size={18} />
                    {/if}
                </button>
            </div>

            <!-- 筛选和排序 -->
            <div class="flex justify-between gap-2">
                <!-- 筛选选择器 -->
                <div class="flex-1 relative">
                    <label
                        for="category-select"
                        class="text-[10px] text-muted-foreground block font-semibold mb-1 ml-1"
                        >类别筛选</label
                    >
                    <Select.Root
                        type="single"
                        value={selectedCategory}
                        onValueChange={handleCategorySelect}
                    >
                        <Select.Trigger
                            id="category-select"
                            class="w-full bg-neutral-900 text-xs rounded-sm shadow-lg border backdrop-blur-sm
                        px-3 py-1.5 focus:ring-1 focus:ring-primary"
                        >
                            <span
                                >{categories.find(
                                    (c) => c.$id === selectedCategory,
                                )?.name?.zh || "全部"}</span
                            >
                        </Select.Trigger>
                        <Select.Content
                            class="rounded-xl border border-input shadow-lg"
                        >
                            <Select.Item
                                value="all"
                                class="rounded-lg hover:bg-muted/50"
                                >全部</Select.Item
                            >
                            {#each categories as category}
                                <Select.Item
                                    value={category.$id || ""}
                                    class="rounded-lg hover:bg-muted/50"
                                >
                                    {category.name?.zh || "未分类"}
                                </Select.Item>
                            {/each}
                        </Select.Content>
                    </Select.Root>
                </div>

                <!-- 排序选择器 -->
                <div class="flex-1 relative">
                    <label
                        for="sort-select"
                        class="text-[10px] font-semibold text-muted-foreground block mb-1 ml-1"
                        >排序方式</label
                    >
                    <Select.Root
                        type="single"
                        value={sortOption}
                        onValueChange={handleSortSelect}
                    >
                        <Select.Trigger
                            id="sort-select"
                            class="w-full bg-neutral-900  text-xs rounded-sm border border-input px-3 py-1.5
                         focus:ring-1 focus:ring-primary"
                        >
                            <span>
                                {sortOption === "newest"
                                    ? "最新发布"
                                    : sortOption === "oldest"
                                      ? "最早发布"
                                      : "按字母排序"}
                            </span>
                        </Select.Trigger>
                        <Select.Content
                            class="rounded-xl border border-input shadow-lg"
                        >
                            <Select.Item
                                value="newest"
                                class="rounded-lg hover:bg-muted/50"
                                >最新发布</Select.Item
                            >
                            <Select.Item
                                value="oldest"
                                class="rounded-lg hover:bg-muted/50"
                                >最早发布</Select.Item
                            >
                            <Select.Item
                                value="alphabetical"
                                class="rounded-lg hover:bg-muted/50"
                                >按字母排序</Select.Item
                            >
                        </Select.Content>
                    </Select.Root>
                </div>
            </div>
        </div>

        <!-- 事件列表 -->
        <div class="flex-1 overflow-hidden">
            <ScrollArea class="h-full">
                <div class="divide-y divide-border/30">
                    {#if loading}
                        <!-- 加载状态 -->
                        <div
                            class="flex flex-col items-center justify-center h-40 text-muted-foreground"
                        >
                            <div
                                class="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin mb-2"
                            ></div>
                            <p>加载中...</p>
                        </div>
                    {:else if filteredEvents.length === 0}
                        <!-- 无结果状态 -->
                        <div
                            class="flex flex-col items-center justify-center h-40 text-muted-foreground"
                        >
                            <p>没有找到匹配的事件</p>
                        </div>
                    {:else}
                        <!-- 事件列表 -->
                        {#each filteredEvents as event, index (event.$id)}
                            <Motion
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.3, delay: index * 0.05 }}
                                let:motion
                            >
                                <div
                                    use:motion
                                    role="button"
                                    tabindex="0"
                                    aria-label={`查看事件: ${event.title}`}
                                    class="py-4 px-3 hover:bg-muted/10 transition-all cursor-pointer
                                    flex items-start gap-4 text-foreground relative"
                                    onmouseenter={() => {
                                        // 可以在这里添加悬停效果，例如在地图上显示位置
                                    }}
                                >
                                    <!-- 事件图标/头像 -->
                                    <div class="flex-shrink-0">
                                        <div class="w-14 h-14 rounded-2xl flex items-center backdrop-blur-md 
                                        justify-center bg-neutral-100/20"
                                            >
                                            <!-- 使用首字母作为图标 -->
                                            <span class="text-white text-xl font-medium">
                                                {#if event.tags && event.tags.length > 0}
                                                    {getEventInitials(event)}
                                                {:else if event.location_data?.city}
                                                    {event.location_data.city.substring(0, 2)}
                                                {:else if event.title}
                                                    {event.title.substring(0, 2)}
                                                {:else}
                                                    MN
                                                {/if}
                                            </span>
                                        </div>
                                    </div>

                                    <!-- 事件信息 -->
                                    <div class="flex-1 flex flex-col gap-1 py-1">
                                        <!-- 地区/标题 -->
                                        <!-- <h3 class="font-medium text-base">
                                            {event.location_data?.city || "未知地区"}
                                        </h3> -->

                                        <!-- 事件类型 -->
                                        <p class="text-sm font-medium text-primary">
                                            {event.title}
                                        </p>

                                        <!-- 时间信息 -->
                                        <div class="flex items-center gap-2 text-xs text-muted-foreground mt-1">
                                            <span>今天 {new Date(event.date).toLocaleTimeString('zh-CN', {hour: '2-digit', minute:'2-digit'})}</span>
                                            <span class="text-muted-foreground/50">|</span>
                                            <span class="font-medium">
                                                {Math.floor(Math.random() * 500) + 1} KM
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </Motion>
                        {/each}
                    {/if}
                </div>
            </ScrollArea>
        </div>
    </div>

    </div>
    <div class="w-3/5 h-full flex items-center justify-end p-8">
    
        <MapBase class="rounded-xl border"></MapBase>
    </div>
</div>
