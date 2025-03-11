<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { TemplateCard, DatabaseCard, PageCard } from "$lib/components/ui/notion-cards";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";
    // import type { PersonalItem } from "./components/types";
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
        Kanban,
        X
    } from "lucide-svelte";
    import { getContext } from 'svelte';
    import type { Snippet } from "svelte";

    type CardColor = "blue" | "green" | "purple" | "amber";

    type ShellContext = {
        showRightView: boolean;
        setShowRightView: (value: boolean) => void;
        setTemplate: (template: any) => void;
        // setLeftViewItem: (item: PersonalItem | null) => void;
    }

    const { setShowRightView, setTemplate } = getContext<ShellContext>('shell');
    
    let showRightView = $state(false);
    let showLeftView = $state(false);
    let selectedTemplate = $state<typeof templates[0] | null>(null);
    // let leftViewItem = $state<PersonalItem | null>(null);

    function handleTemplateClick(template: typeof templates[0]) {
        setTemplate(template);
        setShowRightView(true);
    }

    function handleCloseRightView() {
        showRightView = false;
        selectedTemplate = null;
    }

    // function handleLeftViewChange(item: PersonalItem | null) {
    //     console.log('Page: Left view item changed:', item);
    //     leftViewItem = item;
    //     showLeftView = !!item;
    // }

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


<ScrollArea class="h-[calc(100vh-1rem)]">
    <div class="max-w-5xl mx-auto px-8 py-10 space-y-16">
        <!-- 欢迎信息 -->
        <div class="space-y-1">
            <h1 class="text-4xl font-medium tracking-tight">早上好呀，翼范</h1>
            <p class="text-base text-muted-foreground">开始探索神秘事件</p>
        </div>

        <!-- 特色模板 -->
        <div class="space-y-5">
            <div class="flex items-center justify-between">
                <h2 class="text-sm font-medium text-muted-foreground/80">特色模板</h2>
                <Button variant="ghost" size="sm">
                    <MoreHorizontal class="h-4 w-4" />
                </Button>
            </div>
            <div class="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
                {#each templates as template}
                    <button class="text-left" on:click={() => handleTemplateClick(template)}>
                        <TemplateCard {...template} />
                    </button>
                {/each}
            </div>
        </div>

        <!-- 数据库 -->
        <div class="space-y-5">
            <div class="flex items-center justify-between">
                <h2 class="text-sm font-medium text-muted-foreground/80">数据库</h2>
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
        <div class="space-y-5">
            <div class="flex items-center justify-between">
                <h2 class="text-sm font-medium text-muted-foreground/80">最近页面</h2>
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
</ScrollArea>
