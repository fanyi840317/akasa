<script lang="ts">
    import type { PageData } from "./$types";
    import { Button } from "$lib/components/ui/button";
    import {
        Pagination,
        PaginationContent,
        PaginationItem,
        PaginationLink,
    } from "$lib/components/ui/pagination";
    import { Input } from "$lib/components/ui/input";
    import { Badge } from "$lib/components/ui/badge";
    import { _ } from "svelte-i18n";
    import {
        Search,
        Filter,
        Calendar,
        MapPin,
        Users,
        Star,
        PlusCircle,
        Share2,
    } from "lucide-svelte";
    import * as Card from "$lib/components/ui/card";
    import {
        Avatar,
        AvatarImage,
        AvatarFallback,
    } from "$lib/components/ui/avatar";
    import Map from "$lib/components/map.svelte";
    import * as HoverCard from "$lib/components/ui/hover-card";
    import { fade, fly, scale, slide } from "svelte/transition";
    import { flip } from "svelte/animate";
    import { quintOut } from "svelte/easing";
    import { EventList } from "../components/index.js";

    let { data }: { data: PageData } = $props();

    // 地点分类数据
    const placeCategories = [
        { id: "atm", name: "ATMs", count: 12 },
        { id: "bus", name: "Bus Stops", count: 24 },
        { id: "cafe", name: "Cafés", count: 3 },
        { id: "emergency", name: "Emergencies", count: 5 },
        { id: "museum", name: "Museums", count: 8 },
        { id: "parking", name: "Parkings", count: 15 },
        { id: "restaurant", name: "Restaurants", count: 32 },
        { id: "sport", name: "Sport Centers", count: 6 },
    ];

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
            rating: 4.5,
        },
        {
            id: 2,
            title: "户外徒步活动",
            location: "杭州市",
            date: "2023-12-20",
            image: "/images/31.04_banner-373x373.jpg",
            tags: ["户外", "徒步"],
            attendees: 36,
            rating: 4.8,
        },
        {
            id: 3,
            title: "创意绘画课程",
            location: "北京市",
            date: "2023-12-25",
            image: "/images/31.05_banner-373x373.jpg",
            tags: ["艺术", "绘画"],
            attendees: 18,
            rating: 4.2,
        },
        {
            id: 4,
            title: "音乐节",
            location: "成都市",
            date: "2023-12-30",
            image: "/images/33.04_banner-373x373.jpg",
            tags: ["音乐", "演出"],
            attendees: 120,
            rating: 4.7,
        },
        {
            id: 5,
            title: "科技展览",
            location: "深圳市",
            date: "2024-01-05",
            image: "/images/33.05_banner-373x373.jpg",
            tags: ["科技", "展览"],
            attendees: 85,
            rating: 4.4,
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

    let selectedCategory = "cafe";
    let searchQuery = "";
    let currentPage = 1;
    const itemsPerPage = 6;
    const totalPages = Math.ceil(events.length / itemsPerPage);

    function handleCategoryClick(categoryId: string) {
        selectedCategory = categoryId;
        currentPage = 1;
    }

    function formatDate(dateString: string) {
        const date = new Date(dateString);
        return date.toLocaleDateString("zh-CN", {
            year: "numeric",
            month: "long",
            day: "numeric",
        });
    }

    function getStaggerDelay(i: number) {
        return i * 50;
    }

    function getCategoryTransform(index: number, total: number) {
        const verticalSpacing = 60; // 每个项目之间的垂直间距
        return `translate(0, ${index * verticalSpacing}px)`;
    }
</script>

<div class="w-full h-screen overflow-hidden">
    <!-- 左侧分类列表 -->
    <div class="absolute left-14 top-[64px] z-20">
        {#each placeCategories as category, i}
            <a
                class="block px-4 py-1 mb-2 flex items-center justify-between gap-4 transition-all transform hover:scale-105 origin-left {selectedCategory === category.id ? 'bg-background/10' : 'hover:bg-background/20'}"
              
                on:click={() => handleCategoryClick(category.id)}
                in:fly={{ y: 20, delay: i * 50, duration: 400 }}
            >
                <h4
                    class="font-medium whitespace-nowrap transition-all {selectedCategory === category.id ? 'text-primary text-4xl font-bold' : 'text-muted-foreground text-xs hover:text-primary'}"
                >
                    {category.name}
                </h4>
                <span class="text-xs opacity-80">({category.count})</span>
            </a>
        {/each}
    </div>

    <div class="absolute top-14 left-14 z-20">
        <h1 class="text-3xl font-bold mb-2">{$_("site.events")}</h1>
        <h2 class="text-sm text-muted-foreground">{$_("events.subtitle")}</h2>
    </div>

    <!-- 右上角搜索框 -->
    <div class="absolute top-14 right-14 z-20 flex items-center gap-4">
        <Button variant="ghost" size="icon" class="hover:bg-background/20">
            <Search class="h-5 w-5" />
        </Button>
        <Button variant="ghost" size="icon" class="hover:bg-background/20">
            <Share2 class="h-5 w-5" />
        </Button>
    </div>

    <!-- 地图容器 -->
    <div class="absolute inset-0 z-0">
        <Map />
    </div>
    <!-- 黑雾蒙层 -->
    <div
        class="absolute inset-0 z-10 pointer-events-none"
        style="background: radial-gradient(circle at center, transparent 30%, rgba(0, 0, 0, 0.2) 50%, rgba(0, 0, 0, 0.9) 100%)"
    ></div>

    <!-- 底部事件展示区域 -->
    <div class=" absolute bottom-4 left-0 right-0 z-20 mx-10 px-14">
        <EventList class="" {events} />
    </div>
</div>
