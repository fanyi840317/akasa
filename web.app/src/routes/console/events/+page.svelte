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
    import EventCard from "$lib/components/notion-cards/event-card.svelte";
    import TagNav from "$lib/components/nav/tag-nav.svelte";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";
    import ShareButton from "$lib/components/share/share-button.svelte";
    import SharePanel from "$lib/components/share/share-panel.svelte";

    let { data }: { data: PageData } = $props();
    let showSharePanel = $state(false);

    // 模拟事件数据
    const events = [
        {
            id: 1,
            title: "摄影工作坊",
            location: "上海市",
            date: "2023-12-15",
            image: "/images/31.03_banner-373x373.jpg",
            tags: ["摄影", "工作坊"],
            attendees: 24,
            rating: 4.5
        },
        {
            id: 2,
            title: "户外徒步活动",
            location: "杭州市",
            date: "2023-12-20",
            image: "/images/31.04_banner-373x373.jpg",
            tags: ["户外", "徒步"],
            attendees: 36,
            rating: 4.8
        },
        {
            id: 3,
            title: "创意绘画课程",
            location: "北京市",
            date: "2023-12-25",
            image: "/images/31.05_banner-373x373.jpg",
            tags: ["艺术", "绘画"],
            attendees: 18,
            rating: 4.2
        },
        {
            id: 4,
            title: "音乐节",
            location: "成都市",
            date: "2023-12-30",
            image: "/images/33.04_banner-373x373.jpg",
            tags: ["音乐", "演出"],
            attendees: 120,
            rating: 4.7
        },
        {
            id: 5,
            title: "科技展览",
            location: "深圳市",
            date: "2024-01-05",
            image: "/images/33.05_banner-373x373.jpg",
            tags: ["科技", "展览"],
            attendees: 85,
            rating: 4.4
        },
        {
            id: 6,
            title: "美食节",
            location: "广州市",
            date: "2024-01-10",
            image: "/images/31.03_banner-373x373.jpg",
            tags: ["美食", "文化"],
            attendees: 150,
            rating: 4.6,
        },
    ];

    // 分类标签
    const categories = [
        { id: "all", name: "全部" },
        { id: "photography", name: "摄影" },
        { id: "outdoor", name: "户外" },
        { id: "art", name: "艺术" },
        { id: "music", name: "音乐" },
        { id: "tech", name: "科技" },
        { id: "food", name: "美食" },
    ];

    let selectedCategory = "all";
    let searchQuery = "";
    let currentPage = 1;
    const itemsPerPage = 6;
    const totalPages = Math.ceil(events.length / itemsPerPage);

    function formatDate(dateString: string) {
        const date = new Date(dateString);
        return date.toLocaleDateString("zh-CN", {
            year: "numeric",
            month: "long",
            day: "numeric",
        });
    }
</script>

<ScrollArea class="h-[calc(100vh-1rem)]">
<div class="container mx-auto p-16 space-y-10">
    <!-- 页面标题和搜索栏 -->
    <div
        class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4"
    >
        <div>
                <h1 class="text-3xl font-bold mb-2">活动与事件</h1>
                <p class="text-sm text-muted-foreground">发现并参与各种精彩活动</p>
        </div>
        <div class="flex items-center gap-2 w-full md:w-auto">
            <div class="relative w-full md:w-[300px]">
                <Search
                    class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
                />
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
        <TagNav bind:selectedId={selectedCategory} items={categories} />

        <div class="space-y-4">
            <!-- 精选模板区域 -->
            <div class="flex items-center gap-2 px-2 text-muted-foreground">
                <Star class="h-3 w-3 " />
                <span class="text-xs">精选模板</span>
    </div>

    <!-- 事件卡片网格 -->
    <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-3 gap-6">
        {#each events as event}
            <EventCard
                title={event.title}
                image={event.image}
                tags={event.tags}
                rating={event.rating}
            />
        {/each}
            </div>
    </div>

    <!-- 分页控件 -->
        <div class="flex justify-center mt-8"></div>
    </div>
    <div class="fixed bottom-20 right-4">
        <ShareButton on:click={() => (showSharePanel = true)} />
</div>
</ScrollArea>
