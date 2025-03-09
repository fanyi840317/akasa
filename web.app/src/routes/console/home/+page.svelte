<script lang="ts">
    import { Shell } from "$lib/components/console";
    import { Button } from "$lib/components/ui/button";
    import { TemplateCard, DatabaseCard, PageCard } from "$lib/components/ui/notion-cards";
    import { 
        LayoutTemplate,
        CalendarClock,
        BookOpen,
        Map,
        Activity,
        Users,
        MoreHorizontal,
        Table,
        FileText,
        Kanban
    } from "lucide-svelte";

    type CardColor = "blue" | "green" | "purple" | "amber";

    // 特色模板
    const templates = [
        {
            title: "事件管理",
            subtitle: "By Akasa",
            description: "管理和追踪神秘事件",
            icon: Activity,
            url: "/console/events/list",
            color: "blue" as CardColor
        },
        {
            title: "会议记录",
            subtitle: "By Akasa",
            description: "团队会议和调查记录",
            icon: CalendarClock,
            url: "/console/meetings",
            color: "purple" as CardColor
        },
        {
            title: "知识库",
            subtitle: "By Akasa",
            description: "事件资料与研究档案",
            icon: BookOpen,
            url: "/console/wiki",
            color: "amber" as CardColor
        }
    ];

    // 数据库
    const databases = [
        {
            title: "事件列表",
            description: "所有神秘事件的追踪记录",
            icon: Table,
            url: "/console/events",
            views: ["表格", "看板", "日历"],
            lastEdited: "2小时前",
            color: "blue" as CardColor
        },
        {
            title: "调查任务",
            description: "实地调查任务分配与进度",
            icon: Kanban,
            url: "/console/tasks",
            views: ["看板", "列表", "时间轴"],
            lastEdited: "1小时前",
            color: "purple" as CardColor
        }
    ];

    // 最近页面
    const recentPages = [
        {
            title: "3月工作计划",
            icon: FileText,
            url: "/console/pages/march-plan",
            lastEdited: "昨天",
            coverImage: "https://images.unsplash.com/photo-1707343843437-caacff5cfa74",
            color: "blue" as CardColor
        },
        {
            title: "调查指南",
            icon: BookOpen,
            emoji: "📚",
            url: "/console/pages/guide",
            lastEdited: "2天前",
            color: "amber" as CardColor
        },
        {
            title: "团队会议记录",
            icon: CalendarClock,
            url: "/console/pages/meeting-notes",
            lastEdited: "3天前",
            color: "purple" as CardColor
        }
    ];
</script>

<style lang="postcss">
    .notion-card {
        @apply relative rounded-lg border bg-card overflow-hidden transition-all duration-200;
        @apply hover:shadow-lg hover:border-primary/50;
    }

    .notion-card-image {
        @apply relative aspect-[1.6] w-full overflow-hidden bg-gradient-to-b from-muted/50 to-muted;
    }

    .notion-card-content {
        @apply p-4 space-y-2;
    }

    .notion-view {
        @apply flex items-center gap-3 p-3 rounded-lg border bg-card/50 hover:bg-card transition-colors;
        @apply hover:border-primary/50;
    }

    .icon-container {
        @apply p-2 rounded-lg shrink-0;
    }

    .icon-container.blue {
        @apply bg-blue-500/10 text-blue-500;
    }

    .icon-container.green {
        @apply bg-green-500/10 text-green-500;
    }

    .icon-container.purple {
        @apply bg-purple-500/10 text-purple-500;
    }

    .icon-container.amber {
        @apply bg-amber-500/10 text-amber-500;
    }
</style>

{#snippet child()}
    <div class="max-w-5xl mx-auto p-6 space-y-12">
        <!-- 欢迎信息 -->
        <div class="space-y-2">
            <h1 class="text-3xl font-bold tracking-tight">晚上好，翼范</h1>
            <p class="text-muted-foreground">开始探索神秘事件</p>
        </div>

        <!-- 特色模板 -->
        <div class="space-y-4">
            <div class="flex items-center justify-between">
                <h2 class="text-sm font-medium text-muted-foreground">特色模板</h2>
                <Button variant="ghost" size="sm">
                    <MoreHorizontal class="h-4 w-4" />
                </Button>
            </div>
            <div class="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
                {#each templates as template}
                    <TemplateCard {...template} />
                {/each}
            </div>
        </div>

        <!-- 数据库 -->
        <div class="space-y-4">
            <div class="flex items-center justify-between">
                <h2 class="text-sm font-medium text-muted-foreground">数据库</h2>
                <Button variant="ghost" size="sm">
                    <MoreHorizontal class="h-4 w-4" />
                </Button>
            </div>
            <div class="grid gap-4 grid-cols-1 lg:grid-cols-2">
                {#each databases as database}
                    <DatabaseCard {...database} />
                {/each}
            </div>
        </div>

        <!-- 最近页面 -->
        <div class="space-y-4">
            <div class="flex items-center justify-between">
                <h2 class="text-sm font-medium text-muted-foreground">最近页面</h2>
                <Button variant="ghost" size="sm">
                    <MoreHorizontal class="h-4 w-4" />
                </Button>
            </div>
            <div class="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
                {#each recentPages as page}
                    <PageCard {...page} />
                {/each}
            </div>
        </div>
    </div>
{/snippet}

<Shell 
    {child}
    titles={[
        { name: "控制台", path: "/console" },
        { name: "首页", path: "/console/home" }
    ]}
    showHeader={false}
/>