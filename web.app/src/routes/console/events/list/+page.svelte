<script lang="ts">
    import { Shell } from "$lib/components/console";
    import * as Card from "$lib/components/ui/card";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Search, Filter, Plus } from "lucide-svelte";
    import { fly } from "svelte/transition";

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
</script>

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

{#snippet child()}
    <div class="p-6">
        <Card.Root>
            <Card.Header>
                <Card.Title>事件列表</Card.Title>
                <Card.Description>
                    查看和管理所有神秘事件
                </Card.Description>
            </Card.Header>
            <Card.Content>
                <div class="rounded-md border">
                    <table class="w-full">
                        <thead>
                            <tr class="border-b bg-muted/50">
                                <th class="p-3 text-left">事件名称</th>
                                <th class="p-3 text-left">地点</th>
                                <th class="p-3 text-left">日期</th>
                                <th class="p-3 text-left">状态</th>
                                <th class="p-3 text-left">浏览量</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each events as event}
                                <tr class="border-b">
                                    <td class="p-3">
                                        <a href="/console/events/{event.id}" class="hover:underline">
                                            {event.title}
                                        </a>
                                    </td>
                                    <td class="p-3">{event.location}</td>
                                    <td class="p-3">{event.date}</td>
                                    <td class="p-3">
                                        <span class="inline-flex items-center rounded-full px-2 py-1 text-xs" 
                                            class:bg-yellow-100={event.status === "调查中"}
                                            class:text-yellow-800={event.status === "调查中"}
                                            class:bg-green-100={event.status === "已结案"}
                                            class:text-green-800={event.status === "已结案"}
                                            class:bg-gray-100={event.status === "待处理"}
                                            class:text-gray-800={event.status === "待处理"}>
                                            {event.status}
                                        </span>
                                    </td>
                                    <td class="p-3">{event.views}</td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            </Card.Content>
        </Card.Root>
    </div>
{/snippet}

{#snippet rightView()}
    {#if showFilters}
        <div class="p-4 w-[300px]" in:fly={{ x: 200, duration: 300 }}>
            <h3 class="text-lg font-semibold mb-4">筛选条件</h3>
            <div class="space-y-4">
                <div class="grid gap-2">
                    <label class="text-sm font-medium">状态</label>
                    <select class="w-full rounded-md border p-2">
                        <option value="">全部</option>
                        <option value="调查中">调查中</option>
                        <option value="已结案">已结案</option>
                        <option value="待处理">待处理</option>
                    </select>
                </div>
                <div class="grid gap-2">
                    <label class="text-sm font-medium">日期范围</label>
                    <Input type="date" class="w-full" />
                    <Input type="date" class="w-full" />
                </div>
                <Button class="w-full">应用筛选</Button>
            </div>
        </div>
    {/if}
{/snippet}

<Shell 
    {child}
    {actions}
    {rightView}
    showRightView={showFilters}
    titles={[
        { name: "控制台", path: "/console" },
        { name: "事件管理", path: "/console/events" },
        { name: "事件列表", path: "/console/events/list" }
    ]}
/> 