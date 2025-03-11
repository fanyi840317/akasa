<script lang="ts">
    import { Shell } from "$lib/components/console";
    import * as Card from "$lib/components/ui/card";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Search, Filter, Plus, X } from "lucide-svelte";
    import { fly } from "svelte/transition";
    import { getContext } from 'svelte';
    import { ScrollArea } from "$lib/components/ui/scroll-area";
    import type { Snippet } from "svelte";
    import type { PersonalItem } from "$lib/components/console/types";
    import { Activity } from "lucide-svelte";

    type ShellContext = {
        showRightView: boolean;
        setShowRightView: (value: boolean) => void;
        setTemplate: (template: any) => void;
        setLeftViewItem: (item: PersonalItem | null) => void;
    }

    const { setShowRightView, setTemplate } = getContext<ShellContext>('shell');

    // 模拟事件数据
    let events = $state([
        {
            id: 1,
            title: "神秘光球事件",
            location: "北京海淀区",
            date: "2024-03-15",
            status: "调查中",
            views: 1200
        },
        {
            id: 2,
            title: "不明声音现象",
            location: "上海浦东新区",
            date: "2024-03-14",
            status: "已结案",
            views: 890
        },
        {
            id: 3,
            title: "异常天气记录",
            location: "广州天河区",
            date: "2024-03-13",
            status: "待处理",
            views: 650
        }
    ]);

    let searchQuery = $state("");
    let showFilters = $state(false);

    // 事件详情数据
    const eventDetail = {
        title: "外星人目击事件",
        subtitle: "调查中",
        description: "在新墨西哥州发现疑似外星人痕迹，目前正在进行实地调查...",
        color: "blue" as const,
        // icon: Activity
    };

    function handleEventClick(event: typeof eventDetail) {
        setTemplate(event);
        setShowRightView(true);
    }
</script>

<!-- 默认内容 -->
<div>
    <ScrollArea class="h-[calc(100vh-1rem)]">
        <div class="max-w-5xl mx-auto px-8 py-10 space-y-8">
            <div class="flex items-center justify-between">
                <h1 class="text-2xl font-semibold">事件列表</h1>
                <Button>新建事件</Button>
            </div>
            
            <!-- 事件列表 -->
            <div class="space-y-4">
                <button 
                    class="w-full p-4 rounded-lg border bg-card hover:bg-muted/50 transition-colors text-left"
                    on:click={() => handleEventClick(eventDetail)}
                >
                    <div class="flex items-center justify-between">
                        <div class="space-y-1">
                            <h3 class="font-medium">{eventDetail.title}</h3>
                            <p class="text-sm text-muted-foreground">{eventDetail.description}</p>
                        </div>
                        <div class="text-xs text-muted-foreground">2小时前更新</div>
                    </div>
                </button>
            </div>
        </div>
    </ScrollArea>
</div>

<!-- 提供 actions snippet -->
{#snippet actions()}
    <div class="flex items-center gap-2">
        <div class="relative">
            <Search class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
                type="search"
                placeholder="搜索事件..."
                class="w-[200px] pl-8"
                bind:value={searchQuery}
            />
        </div>
        <Button variant="outline" size="sm" on:click={() => showFilters = !showFilters}>
            <Filter class="h-4 w-4 mr-2" />
            <span>筛选</span>
        </Button>
        <Button size="sm">
            <Plus class="h-4 w-4 mr-2" />
            <span>新建事件</span>
        </Button>
    </div>
{/snippet}

<!-- 提供 rightView snippet -->
{#snippet rightView()}
    {#if selectedTemplate}
        <!-- 右侧面板内容 -->
    {/if}
{/snippet}