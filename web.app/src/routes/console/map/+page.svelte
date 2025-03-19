<script lang="ts">
    import type { PageData } from "./$types";
    import { Button } from "$lib/components/ui/button";
    import type { ShellContext } from "../components/types";
    import { EventDetail } from "./components/index.js";
    
    import { _ } from "svelte-i18n";
    import {
        Search,
        MapPin,
        PlusCircle,
    } from "lucide-svelte";
    import Map from "$lib/components/map.svelte";
    import { EventList, NotionPanel } from "../components/index.js";
    import CategoryList from "../components/category-list.svelte";
    import { getContext, setContext } from "svelte";
    import { writable } from "svelte/store";
    import { initEditor } from "$lib/components/editor/affine-editor";
    import type { AppState } from "$lib/components/editor/affine-editor";
    import { goto } from "$app/navigation";

    let { data }: { data: PageData } = $props();
    
    // 初始化编辑器状态并设置为context
    // const appState = writable<AppState>(initEditor());
    // setContext("appState", appState);

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
            id: "1",
            title: "摄影工作坊",
            location: "上海市",
            date: "2023-12-15",
            image: "/images/31.03_banner-373x373.jpg",
            tags: ["摄影", "工作坊"],
            attendees: 24,
            rating: 4.5,
        },
        {
            id: "2",
            title: "户外徒步活动",
            location: "杭州市",
            date: "2023-12-20",
            image: "/images/31.04_banner-373x373.jpg",
            tags: ["户外", "徒步"],
            attendees: 36,
            rating: 4.8,
        },
        {
            id: "3",
            title: "创意绘画课程",
            location: "北京市",
            date: "2023-12-25",
            image: "/images/31.05_banner-373x373.jpg",
            tags: ["艺术", "绘画"],
            attendees: 18,
            rating: 4.2,
        },
        {
            id: "4",
            title: "音乐节",
            location: "成都市",
            date: "2023-12-30",
            image: "/images/33.04_banner-373x373.jpg",
            tags: ["音乐", "演出"],
            attendees: 120,
            rating: 4.7,
        },
        {
            id: "5",
            title: "科技展览",
            location: "深圳市",
            date: "2024-01-05",
            image: "/images/33.05_banner-373x373.jpg",
            tags: ["科技", "展览"],
            attendees: 85,
            rating: 4.4,
        },
        {
            id: "6",
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

    // 创建事件相关状态
    let showCreatePanel = $state(false);
    let eventTitle = $state("");
    let eventDescription = $state("");
    let eventLocation = $state("");
    let eventDate = $state("");
    let eventStatus = $state("未开始");

    // 事件属性
    let eventProperties = [
        { label: "状态", value: "未开始", icon: true, color: "bg-gray-400" },
        { label: "负责人", value: "空白", icon: true, color: "bg-gray-200" },
        { label: "优先级", value: "空白", icon: true, color: "bg-gray-400" },
        { label: "截止日期", value: eventDate || "未设置", icon: false },
    ];

    const { setShowRightView, setTemplate } = getContext<ShellContext>("shell");
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

    function handleCreateEvent() {
        // 处理创建事件的逻辑
        // console.log(event.detail);
        // showCreatePanel = false;
        // 重置表单
        eventTitle = "";
        eventDescription = "";
        eventLocation = "";
        eventDate = "";
        setShowRightView(true);
    }

    function handleClosePanel() {
        showCreatePanel = false;
    }
</script>

<div class="w-full h-screen overflow-hidden">
    <!-- 左侧分类列表 -->
    <div class="absolute left-16 top-[180px] z-20">
        <CategoryList
            categories={placeCategories}
            {selectedCategory}
            onCategoryClick={handleCategoryClick}
        />
    </div>

    <div class="absolute top-14 left-14 z-20 p-4">
        <h1 class="text-3xl font-bold mb-2">{$_("site.events")}</h1>
        <h2 class="text-sm text-muted-foreground">{$_("events.subtitle")}</h2>
    </div>

    <!-- 右上角搜索框 -->
    <div class="absolute top-16 right-14 z-20 flex items-center gap-4">
        <Button variant="ghost" size="icon">
            <Search class="h-5 w-5" />
        </Button>
        <Button variant="ghost" size="icon">
            <MapPin class="h-5 w-5" />
        </Button>
        <Button
            variant="secondary"
            size="icon"
            onclick={() => (goto("/console/events/new"))}
        >
            <PlusCircle class="h-5 w-5 hover:bg-background/20" />
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
    <div
        class="absolute bottom-6 left-0 right-0 z-20 mx-auto max-w-[1200px] px-14"
    >
        <EventList class="" {events} />
    </div>
</div>
{#snippet contentView()}
    <EventDetail />
{/snippet}
<!-- 底部分页栏 -->
<NotionPanel
    open={showCreatePanel}
    showBackdrop={false}
    {contentView}
    width={40}
    maxWidth={60}
    on:close={handleClosePanel}
></NotionPanel>
