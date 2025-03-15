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
    import { _ } from 'svelte-i18n';
    import { Search, Filter, Calendar, MapPin, Users, Star, PlusCircle, Share2 } from "lucide-svelte";
    import * as Card from "$lib/components/ui/card";
    import {
        Avatar,
        AvatarImage,
        AvatarFallback,
    } from "$lib/components/ui/avatar";
    import Map from "$lib/components/map.svelte";
    import * as HoverCard from "$lib/components/ui/hover-card";
    // 导入Svelte动画模块
    import { fade, fly, scale, slide } from "svelte/transition";
    import { flip } from "svelte/animate";
    import { quintOut } from "svelte/easing";
    import {EventList} from "./components';

    let { data }: { data: PageData } = $props();

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
            rating: 4.6
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

    // 为卡片内容元素添加交错动画的延迟函数
    function getStaggerDelay(i: number) {
        return i * 50; // 每个元素延迟50ms
    }


</script>

<div class="w-full h-screen overflow-hidden">


    <div class="absolute top-14 left-14 z-20 w-64 space-y-4">
        <Card.Root class="backdrop-blur-sm border-none shadow-lg bg-gradient-to-r from-transparent via-background/30 to-transparent">
            <Card.Content class="p-4">
                <h1 class="text-xl font-bold">{$_('site.events')}</h1>
                <h2 class="text-sm text-muted-foreground mb-4">{$_('events.subtitle')}</h2>
            </Card.Content>
        </Card.Root>
    </div>

    <!-- 右上角搜索框 -->
    <div class="absolute top-14 right-14 z-20 flex gap-12">
       
        <Search class="h-5 w-5 font-bold" stroke-width="2.5" />
        <Share2 class="h-5 w-5 font-bold" stroke-width="2.5" />

    </div>
    
    <!-- 地图容器 -->
    <div class="absolute inset-0 z-0">
        <Map />
    </div>
    <!-- 黑雾蒙层 -->
    <div class="absolute inset-0 z-10 pointer-events-none" style="background: radial-gradient(circle at center, transparent 30%, rgba(0, 0, 0, 0.2) 50%, rgba(0, 0, 0, 0.9) 100%)"></div>
    
    <!-- 底部事件展示区域 -->
     
    <EventList {events} />
</div>
