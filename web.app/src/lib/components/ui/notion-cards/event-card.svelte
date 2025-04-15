<script lang="ts">
    import { Star } from "lucide-svelte";
    import { Badge } from "$lib/components/ui/badge";
    import {
        Avatar,
        AvatarImage,
        AvatarFallback,
    } from "$lib/components/ui/avatar";
    import { Skeleton } from "$lib/components/ui/skeleton";

    let {
        title,
        image = "",
        tags = [],
        rating = 0,
        url = "#",
        avatarSrc = "",
        avatarFallback = title ? title.slice(0, 2) : "",
        loading = false,
    } = $props<{
        title: string;
        image?: string;
        tags?: string[];
        rating?: number;
        url?: string;
        avatarSrc?: string;
        avatarFallback?: string;
        loading?: boolean;
    }>();

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

    let coverUrl = $state(image || getRandomDefaultCover());
    let categoryText = $state("神秘事件");

    $effect(() => {
        if (!image) {
            coverUrl = getRandomDefaultCover();
        } else {
            // 处理 ImgBB URL，确保图片正确显示
            try {
                // 检查是否是有效的 URL
                if (image.startsWith("http")) {
                    coverUrl = image;
                } else {
                    // 尝试解析 JSON 格式的封面数据
                    const coverData = JSON.parse(image);
                    coverUrl = coverData.url || getRandomDefaultCover();
                }
            } catch (e) {
                console.error("解析封面数据失败:", e);
                coverUrl = getRandomDefaultCover();
            }
        }

        // 设置分类文本
        if (
            tags &&
            tags.length > 0 &&
            tags.some((tag: string) => tag && tag.trim() !== "")
        ) {
            categoryText = tags[0];
        } else {
            categoryText = "未知分类";
        }
    });

    function handleImageError() {
        coverUrl = getRandomDefaultCover();
    }

    // 添加鼠标跟随效果
    let card: HTMLElement;

    function handleMouseMove(e: MouseEvent) {
        if (!card) return;
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty("--mouse-x", `${x}px`);
        card.style.setProperty("--mouse-y", `${y}px`);
    }
</script>

<div class="event-card group" bind:this={card} on:mousemove={handleMouseMove}>
    <div class="glass-effect"></div>
    {#if loading}
        <div class="p-4 space-y-4">
            <Skeleton class="h-48 w-full rounded-lg" />
            <div class="space-y-3">
                <div class="flex items-center gap-3">
                    <Skeleton class="h-8 w-8 rounded-full" />
                    <div class="space-y-2">
                        <Skeleton class="h-4 w-[200px]" />
                        <Skeleton class="h-3 w-[100px]" />
                    </div>
                </div>
                <div class="flex gap-2">
                    <Skeleton class="h-5 w-16 rounded-full" />
                    <Skeleton class="h-5 w-16 rounded-full" />
                </div>
            </div>
        </div>
    {:else}
        <div class="event-card-image">
            <img
                src={coverUrl}
                alt={title}
                on:error={handleImageError}
                class="transition-opacity duration-300"
                style="opacity: {coverUrl ? 1 : 0}"
            />
            {#if !coverUrl}
                <div class="absolute inset-0 flex items-center justify-center">
                    <div class="text-muted-foreground text-sm">暂无图片</div>
                </div>
            {/if}
        </div>
        <div class="event-card-content">
            <div class="event-card-title">
                <div class="event-card-avatar">
                    <Avatar
                        class="h-8 w-8 ring-1 ring-black/[0.03] dark:ring-white/[0.03]"
                    >
                        {#if avatarSrc}
                            <AvatarImage src={avatarSrc} alt={title} />
                            <AvatarFallback
                                class="bg-black/[0.02] dark:bg-white/[0.02]"
                                >{avatarFallback}</AvatarFallback
                            >
                        {:else}
                            <AvatarFallback class="bg-primary/10 text-primary"
                                >{avatarFallback}</AvatarFallback
                            >
                        {/if}
                    </Avatar>
                </div>
                <div class="space-y-1">
                    <h3
                        class="font-medium leading-none group-hover:text-foreground/90 transition-colors truncate"
                    >
                        {title}
                    </h3>
                    <p class="text-xs text-muted-foreground">{categoryText}</p>
                </div>
            </div>
            {#if tags && tags.length > 0 && tags.some((tag: string) => tag && tag.trim() !== "")}
                <div class="event-card-tags">
                    {#each tags.filter((tag: string) => tag && tag.trim() !== "") as tag}
                        <Badge variant="outline" class="event-card-badge"
                            >{tag}</Badge
                        >
                    {/each}
                </div>
            {/if}
        </div>
    {/if}
    {#if rating > 0}
        <div class="event-card-rating">
            <Star class="h-3 w-3" />
            <span>{rating}</span>
        </div>
    {/if}
</div>

<style lang="postcss">
    .event-card {
        @apply relative overflow-hidden rounded-xl bg-card/50 transition-all duration-500;
        @apply hover:shadow-[0_8px_30px_rgb(0,0,0,0.12)] dark:hover:shadow-[0_8px_30px_rgb(255,255,255,0.07)];
        @apply border border-black/[0.02] dark:border-white/[0.02];
        @apply backdrop-blur-xl;
        transform: translateZ(0);
        will-change: transform, box-shadow;
    }

    .event-card::before {
        content: "";
        @apply absolute inset-0 bg-gradient-to-br;
        @apply from-white/[0.02] via-transparent to-black/[0.02];
        @apply dark:from-white/[0.01] dark:to-white/[0.02];
        @apply opacity-0 transition-opacity duration-500;
    }

    .event-card:hover::before {
        @apply opacity-100;
    }

    .event-card::after {
        content: "";
        @apply absolute inset-0 opacity-[0.02] dark:opacity-[0.03];
        @apply transition-opacity duration-500;
        background-size: 20px 20px;
        background-image: linear-gradient(
                to right,
                currentColor 1px,
                transparent 1px
            ),
            linear-gradient(to bottom, currentColor 1px, transparent 1px);
    }

    .event-card:hover::after {
        @apply opacity-[0.03] dark:opacity-[0.04];
    }

    .event-card:hover {
        transform: translateY(-2px) translateZ(0);
    }

    .event-card-image {
        @apply relative h-48 overflow-hidden;
        @apply bg-black/[0.02] dark:bg-white/[0.02];
    }

    .event-card-image img {
        @apply w-full h-full object-cover;
        @apply transition-all duration-700 ease-out;
        @apply saturate-[0.9] contrast-[0.95];
        @apply hover:saturate-100 hover:contrast-100;
        object-position: center;
    }

    .event-card-image::after {
        content: "";
        @apply absolute inset-0;
        @apply bg-gradient-to-t from-background/90 via-background/20 to-transparent;
    }

    .event-card-content {
        @apply relative z-10 p-4 space-y-3;
        @apply bg-gradient-to-b from-background/95 to-background;
    }

    .event-card-title {
        @apply flex items-center gap-3;
    }

    .event-card-avatar {
        @apply relative;
    }

    .event-card-avatar::after {
        content: "";
        @apply absolute inset-0 rounded-full;
        @apply border border-black/5 dark:border-white/5;
    }

    .event-card-tags {
        @apply flex flex-wrap gap-2;
    }

    .event-card-rating {
        @apply absolute top-3 right-3 flex items-center gap-1;
        @apply px-2 py-1 rounded-full text-xs;
        @apply bg-black/5 dark:bg-white/5;
        @apply backdrop-blur-sm;
    }

    :global(.event-card-badge) {
        @apply bg-black/[0.02] dark:bg-white/[0.02];
        @apply text-foreground/70;
        @apply border-black/5 dark:border-white/5;
        @apply transition-all duration-300;
    }

    :global(.event-card:hover .event-card-badge) {
        @apply bg-black/[0.03] dark:bg-white/[0.03];
        @apply text-foreground/80;
        @apply border-black/10 dark:border-white/10;
    }

    .glass-effect {
        @apply absolute inset-0 opacity-0;
        @apply transition-opacity duration-500;
        background: radial-gradient(
            800px circle at var(--mouse-x) var(--mouse-y),
            rgba(255, 255, 255, 0.06),
            transparent 40%
        );
    }

    .event-card:hover .glass-effect {
        @apply opacity-100;
    }
</style>
