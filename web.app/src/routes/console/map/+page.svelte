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
    <div class="absolute top-14 right-14 z-20 w-80 flex gap-2">
        <Button variant="ghost" class="hover:bg-background/40">
            <Search class="h-4 w-4" />
        </Button>
        <Button variant="ghost" class="hover:bg-background/40">
            <Share2 class="h-4 w-4" />
        </Button>
    </div>
    
    <!-- 地图容器 -->
    <div class="absolute inset-0 z-0">
        <Map />
    </div>
    <!-- 黑雾蒙层 -->
    <div class="absolute inset-0 z-10 pointer-events-none" style="background: radial-gradient(circle at center, transparent 30%, rgba(0, 0, 0, 0.2) 50%, rgba(0, 0, 0, 0.9) 100%)"></div>
    
    <!-- 底部事件展示区域 -->
    <div class="absolute bottom-0 left-0 right-0 z-20 p-4 overflow-x-auto">
        <div class="flex space-x-4" in:fade={{ duration: 300, delay: 200 }}>
            {#each events as event, i (event.id)}
                <div animate:flip={{ duration: 300 }} in:fade={{ duration: 300, delay: 100 + i * 50 }}>
                    <HoverCard.Root>
                        <HoverCard.Trigger>
                            <div class="flex-shrink-0 w-72 relative">
                                <div class="bg-gradient-to-r from-card/20 via-card/30 to-card/20 overflow-hidden flex items-center p-4 gap-6 transition-all duration-300 hover:bg-card/40 hover:scale-105 hover:shadow-lg">
                                    <!-- 左侧圆形图片容器 -->
                                    <div class="relative w-16 h-16 flex-shrink-0 transition-all duration-300 group-hover:w-20 group-hover:h-20">
                                        <img src={event.image} alt={event.title} class="w-full h-full object-cover rounded-full ring-2 ring-offset-2 ring-primary ring-offset-background" />
                                        <!-- 叠加在图片右下角的头像 -->
                                        <div class="absolute -bottom-2 -right-2">
                                            <Avatar class="h-8 w-8 border-2 border-background group-hover:h-10 group-hover:w-10 transition-all duration-300">
                                                <AvatarImage src="/images/avatar.png" />
                                                <AvatarFallback>U{event.id}</AvatarFallback>
                                            </Avatar>
                                        </div>
                                    </div>
                                    <!-- 右侧内容 -->
                                    <div class="flex-1 flex flex-col justify-between">
                                        <!-- 上方标题和信息 -->
                                        <div>
                                            <h3 class="text-md font-semibold text-white/70 truncate group-hover:text-white transition-colors duration-300">{event.title}</h3>
                                            <div class="flex items-center mt-0.5 text-xs text-gray-300/40 group-hover:text-gray-300/60">
                                                <!-- <MapPin class="h-3 w-3 mr-1" /> -->
                                                <span>{event.location}</span>
                                            </div>
                                            <div class="flex items-center mt-0.5 text-xs text-gray-300/40 group-hover:text-gray-300/60">
                                                <!-- <Calendar class="h-3 w-3 mr-1" /> -->
                                                <span>{formatDate(event.date)}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </HoverCard.Trigger>
                        <HoverCard.Content sideOffset={-100} class="w-[400px] p-0">
                            <div 
                                in:scale={{ duration: 200, delay: 50, opacity: 0, start: 0.95, easing: quintOut }}
                                out:fade={{ duration: 100 }}
                                class="bg-card/90 backdrop-blur-sm rounded-lg overflow-hidden p-6 shadow-2xl">
                                <div class="flex flex-col space-y-4">
                                    <div 
                                        in:fly={{ y: 20, duration: 200, delay: getStaggerDelay(0) }}
                                        class="flex items-start space-x-4">
                                        <img src={event.image} alt={event.title} class="w-20 h-20 object-cover rounded-lg ring-2 ring-offset-2 ring-primary ring-offset-background" />
                                        <div class="flex-1">
                                            <h3 class="text-xl font-bold text-white mb-2">{event.title}</h3>
                                            <div class="flex flex-wrap gap-2 mb-2">
                                                {#each event.tags as tag}
                                                    <Badge variant="secondary" class="text-xs">{tag}</Badge>
                                                {/each}
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="space-y-2">
                                        <div 
                                            in:fly={{ y: 20, duration: 200, delay: getStaggerDelay(1) }}
                                            class="flex items-center text-sm text-gray-300/80">
                                            <MapPin class="h-4 w-4 mr-2" />
                                            <span>{event.location}</span>
                                        </div>
                                        <div 
                                            in:fly={{ y: 20, duration: 200, delay: getStaggerDelay(2) }}
                                            class="flex items-center text-sm text-gray-300/80">
                                            <Calendar class="h-4 w-4 mr-2" />
                                            <span>{formatDate(event.date)}</span>
                                        </div>
                                        <div 
                                            in:fly={{ y: 20, duration: 200, delay: getStaggerDelay(3) }}
                                            class="flex items-center text-sm text-gray-300/80">
                                            <Users class="h-4 w-4 mr-2" />
                                            <span>{event.attendees} 人参与</span>
                                        </div>
                                        <div 
                                            in:fly={{ y: 20, duration: 200, delay: getStaggerDelay(4) }}
                                            class="flex items-center text-sm text-gray-300/80">
                                            <Star class="h-4 w-4 mr-2 text-yellow-400" />
                                            <span>{event.rating} 分</span>
                                        </div>
                                        <div 
                                            in:fly={{ y: 20, duration: 200, delay: getStaggerDelay(5) }}
                                            class="flex items-center text-sm text-gray-300/80">
                                            <span>☎ (800) 367 5437</span>
                                        </div>
                                    </div>
                                    
                                    <div 
                                        in:fly={{ y: 20, duration: 200, delay: getStaggerDelay(6) }}
                                        class="pt-4 border-t border-gray-700">
                                        <Button 
                                            variant="secondary" 
                                            size="lg" 
                                            class="w-full">获取更多信息</Button>
                                    </div>
                                </div>
                            </div>
                        </HoverCard.Content>
                    </HoverCard.Root>
                </div>
            {/each}
        </div>
    </div>
</div>
