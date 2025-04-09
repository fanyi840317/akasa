<script lang="ts">
    import type { Event } from "$lib/types/event";
    import { Button } from "$lib/components/ui/button";
    import { ScrollArea } from "$lib/components/ui/scroll-area";
    import {
        Calendar,
        MapPin,
        Users,
        Clock,
        Share2,
        Heart,
        Navigation,
    } from "lucide-svelte";
    import { Badge } from "$lib/components/ui/badge";
    import { Separator } from "$lib/components/ui/separator";
    import {
        Avatar,
        AvatarImage,
        AvatarFallback,
    } from "$lib/components/ui/avatar";
    import { Card } from "$lib/components/ui/card";
    import { fly } from "svelte/transition";
    import { onMount } from "svelte";
    import { Client, Storage } from "appwrite";
    import { ImageGravity, ImageFormat } from "appwrite";
    import AffineEditor from "$lib/components/editor/affine-editor.svelte";
    import { createEmptyDoc } from "@blocksuite/presets";
    import type { Doc } from "@blocksuite/store";
    import { createDocByJson } from "../editor/affine-editor";
    import EventEditorArea from "./event-editor-area.svelte";

    let { event } = $props<{ event: Event }>();

    let mapLocation: { lat: number; lng: number } | null = null;

    let title = "";
    let content = "";
    let location = "";
    let selectedCategories: string[] = [];
    let date: Date | undefined;
    let coverImageUrl = $state("");
    let locationData: any = null;
    let doc = $state<Doc | null>(null);

    // 初始化 Appwrite 客户端
    const client = new Client();
    const storage = new Storage(client);

    client
        .setEndpoint("https://cloud.appwrite.io/v1")
        .setProject("67f13e1d003e1c7ea764");

    $effect(() => {
        console.log("Event:", event);
        if (event) {
            title = event.title;
            content = event.content;
            location = event.location;
            selectedCategories = event.categories || [];
            date = event.date ? new Date(event.date) : undefined;
            console.log("Event cover data:", event.cover);

            if (event.cover) {
                try {
                    const coverData = JSON.parse(event.cover);
                    console.log("Parsed cover data:", coverData);

                    // 直接使用 coverData.url 作为图片 URL
                    if (coverData.url) {
                        coverImageUrl = coverData.url;
                        console.log("Cover image URL set to:", coverImageUrl);
                    } else {
                        console.error("No URL found in cover data");
                    }
                } catch (e) {
                    console.error("Failed to parse cover data:", e);
                    console.error("Raw cover data:", event.cover);
                }
            }
            locationData = event.location_data
                ? JSON.parse(event.location_data)
                : null;

            // 初始化编辑器文档
            if (content) {
                try {
                    // 创建新文档
                    createDocByJson(content).then((newdoc) => {
                        if (newdoc) {
                            doc = newdoc;
                            doc.awarenessStore.setReadonly(
                                doc.blockCollection,
                                true,
                            );
                        }
                    });
                    // 这里应该设置文档内容，但需要根据 AffineEditor 的 API 来实现
                    // 可能需要使用 importDoc 或其他方法
                } catch (e) {
                    console.error("Failed to initialize editor document:", e);
                }
            }
        }
    });

    onMount(() => {
        if (event.location_data) {
            try {
                mapLocation = JSON.parse(event.location_data);
            } catch (e) {
                console.error("Failed to parse location data:", e);
            }
        }
    });

    // 格式化日期
    function formatDate(dateString: string) {
        if (!dateString || dateString === "未知") return "时间未知";
        const date = new Date(dateString);
        return date.toLocaleDateString("zh-CN", {
            year: "numeric",
            month: "long",
            day: "numeric",
        });
    }

    function handleNavigate() {
        if (mapLocation) {
            window.open(
                `https://uri.amap.com/navigation?to=${mapLocation.lng},${mapLocation.lat},${encodeURIComponent(event.title)}&mode=car&coordinate=gaode`,
                "_blank",
            );
        }
    }
</script>

<div class="flex flex-col h-full">
    <!-- 封面区域 -->
    <div class="relative h-[240px] bg-muted" in:fly={{ y: 20, duration: 300 }}>
        {#if coverImageUrl}
            <img
                src={coverImageUrl}
                alt={event.title}
                class="w-full h-full object-cover"
            />
        {/if}
        <div
            class="absolute inset-0 bg-gradient-to-t from-background via-background/20 to-transparent"
        />

        <!-- 标题和操作按钮 -->
        <div class="absolute bottom-0 left-0 right-0 p-6">
            <div class="flex items-start justify-between">
                <div class="flex-1">
                    <h1 class="text-2xl font-semibold mb-2">{event.title}</h1>
                    <div
                        class="flex items-center gap-4 text-sm text-muted-foreground"
                    >
                        <div class="flex items-center gap-1">
                            <Clock class="h-4 w-4" />
                            <span>{formatDate(event.date)}</span>
                        </div>
                        {#if event.location}
                            <div class="flex items-center gap-1">
                                <MapPin class="h-4 w-4" />
                                <span>{event.location}</span>
                            </div>
                        {/if}
                    </div>
                </div>
                <div class="flex items-center gap-2">
                    <Button variant="secondary" size="sm" class="gap-1">
                        <Heart class="h-4 w-4" />
                        <span>收藏</span>
                    </Button>
                    <Button variant="secondary" size="sm" class="gap-1">
                        <Share2 class="h-4 w-4" />
                        <span>分享</span>
                    </Button>
                </div>
            </div>
        </div>
    </div>

    <!-- 内容区域 -->
    <ScrollArea class="flex-1">
        <div class="p-6 space-y-6">
            <!-- 创建者信息 -->
            <div class="flex items-center gap-3">
                <Avatar class="h-8 w-8">
                    {#if event.creator_avatar}
                        <AvatarImage
                            src={event.creator_avatar}
                            alt={event.creator_name || "创建者"}
                        />
                        <AvatarFallback
                            >{event.creator_name?.[0] || "?"}</AvatarFallback
                        >
                    {:else}
                        <AvatarFallback class="bg-primary/10 text-primary"
                            >{event.creator_name?.[0] || "?"}</AvatarFallback
                        >
                    {/if}
                </Avatar>
                <div>
                    <div class="font-medium">
                        {event.creator_name || "未知创建者"}
                    </div>
                    <div class="text-sm text-muted-foreground">
                        创建于 {formatDate(event.$createdAt)}
                    </div>
                </div>
            </div>

            <Separator />

            <!-- 事件内容 - 使用 AffineEditor 只读模式 -->
            <div class="prose dark:prose-invert max-w-none">
                {#if doc}
                    <div class="h-[500px] border rounded-md overflow-hidden">
                        <AffineEditor bind:doc />
                        <!-- <EventEditorArea {title} {doc} showAICard={false} /> -->
                    </div>
                {:else if event.content}
                    <p class="text-muted-foreground">正在加载内容...</p>
                {:else}
                    <p class="text-muted-foreground">暂无详细描述</p>
                {/if}
            </div>

            <!-- 地图信息 -->
            {#if mapLocation}
                <Card class="overflow-hidden">
                    <div class="relative h-[240px]">
                        <!-- 地图组件暂时注释掉，因为存在类型错误 -->
                        <!-- <Map 
                            center={mapLocation}
                            zoom={15}
                            markers={[{
                                position: mapLocation,
                                title: event.title
                            }]}
                            class="w-full h-full"
                        /> -->
                        <div
                            class="w-full h-full bg-muted flex items-center justify-center"
                        >
                            <p class="text-muted-foreground">地图加载中...</p>
                        </div>
                        <Button
                            variant="secondary"
                            size="sm"
                            class="absolute bottom-4 right-4 gap-2"
                            onclick={handleNavigate}
                        >
                            <Navigation class="h-4 w-4" />
                            <span>导航</span>
                        </Button>
                    </div>
                </Card>
            {/if}

            <!-- 事件标签 -->
            {#if event.category}
                <div class="flex items-center gap-2 pt-4">
                    <Badge variant="outline">{event.category}</Badge>
                </div>
            {/if}
        </div>
    </ScrollArea>
</div>

<style>
    :global(.readonly-editor) {
        pointer-events: none;
        user-select: none;
    }
</style>
