<script lang="ts">
    import type { Event } from "$lib/types/event";
    import { MapPin, Clock, Share2, Heart } from "lucide-svelte";
    import { onMount } from "svelte";
    import { fly } from "svelte/transition";
    import { MapBase } from "$lib/components/map";
    import type { Location } from "$lib/types/map";

    let { event } = $props<{ event: Event | null }>();

    let mapLocation = $state<Location | null>(null);
    let coverImageUrl = $state("");

    // 初始化状态
    $effect(() => {
        if (event && event.cover) {
            try {
                // 尝试解析封面数据
                if (typeof event.cover === 'string') {
                    if (event.cover.startsWith('http')) {
                        coverImageUrl = event.cover;
                    } else {
                        try {
                            const coverData = JSON.parse(event.cover);
                            if (coverData.url) {
                                coverImageUrl = coverData.url;
                            }
                        } catch (e) {
                            coverImageUrl = event.cover;
                        }
                    }
                }
            } catch (e) {
                console.error("Failed to parse cover data:", e);
            }
        }
    });

    onMount(() => {
        if (event && event.location_data) {
            try {
                // 检查 location_data 是否已经是对象
                if (typeof event.location_data === 'object') {
                    mapLocation = event.location_data;
                } else {
                    // 尝试解析 JSON 字符串
                    mapLocation = JSON.parse(event.location_data as unknown as string);
                }
            } catch (e) {
                console.error("Failed to parse location data:", e);
            }
        }
    });

    // 格式化日期
    function formatDate(dateString: string | undefined) {
        if (!dateString || dateString === "未知") return "时间未知";
        const date = new Date(dateString);
        return date.toLocaleDateString("zh-CN", {
            year: "numeric",
            month: "long",
            day: "numeric",
        });
    }
</script>

{#if event}
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
        ></div>

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
                        {#if event.location_data}
                            <div class="flex items-center gap-1">
                                <MapPin class="h-4 w-4" />
                                <span>
                                    {#if typeof event.location_data === 'object' && event.location_data.city}
                                        {event.location_data.city}
                                    {:else}
                                        未知位置
                                    {/if}
                                </span>
                            </div>
                        {/if}
                    </div>
                </div>
                <div class="flex items-center gap-2">
                    <button class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors bg-secondary text-secondary-foreground hover:bg-secondary/80 shadow-sm h-8 rounded-md px-3 text-xs">
                        <Heart class="h-4 w-4" />
                        <span>收藏</span>
                    </button>
                    <button class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors bg-secondary text-secondary-foreground hover:bg-secondary/80 shadow-sm h-8 rounded-md px-3 text-xs">
                        <Share2 class="h-4 w-4" />
                        <span>分享</span>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- 内容区域 -->
    <div class="flex-1 bg-card overflow-auto">
        <div class="p-6 space-y-6 bg-background/10">
            <!-- 创建者信息 -->
            <div class="flex items-center gap-3">
                <div class="relative w-8 h-8">
                    <div class="w-8 h-8 rounded-full overflow-hidden">
                        {#if event.creator_avatar}
                            <img
                                src={event.creator_avatar}
                                alt={event.creator_name || "创建者"}
                                class="w-full h-full object-cover"
                            />
                        {:else}
                            <div class="bg-primary/10 text-primary flex items-center justify-center w-full h-full">
                                {event.creator_name?.[0] || "?"}
                            </div>
                        {/if}
                    </div>
                </div>
                <div>
                    <div class="font-medium">
                        {event.creator_name || "未知创建者"}
                    </div>
                    <div class="text-sm text-muted-foreground">
                        创建于 {formatDate(event.$createdAt)}
                    </div>
                </div>
            </div>

            <hr class="border-t border-gray-200 dark:border-gray-700 my-4" />

            <!-- 事件内容 -->
            <div class="prose dark:prose-invert max-w-none">
                {#if event.content}
                    <p>{event.content}</p>
                {:else}
                    <p class="text-muted-foreground">暂无详细描述</p>
                {/if}
            </div>

            <!-- 地图信息 -->
            {#if mapLocation}
                <div class="rounded-lg border bg-card text-card-foreground shadow-sm overflow-hidden">
                    <div class="relative h-[240px]">
                        <MapBase
                            locationData={mapLocation}
                            zoom={15}
                            class="w-full h-full"
                        />
                    </div>
                </div>
            {/if}

            <!-- 事件标签 -->
            {#if event.tags && event.tags.length > 0}
                <div class="flex items-center gap-2 pt-4">
                    {#each event.tags as tag}
                        <span class="inline-flex select-none items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 text-foreground">{tag}</span>
                    {/each}
                </div>
            {/if}
        </div>
    </div>
</div>
{:else}
<div class="flex items-center justify-center h-full">
    <p class="text-muted-foreground">未选择事件</p>
</div>
{/if}
