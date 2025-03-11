<script lang="ts">
    import * as Card from "$lib/components/ui/card";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Search, Filter, Plus, MessageSquare, Users, UserPlus } from "lucide-svelte";
    import { fly } from "svelte/transition";
    import { getContext } from 'svelte';
    import { ScrollArea } from "$lib/components/ui/scroll-area";
    import { Avatar, AvatarImage, AvatarFallback } from "$lib/components/ui/avatar";
    import { Badge } from "$lib/components/ui/badge";
    import type { Snippet } from "svelte";

    type ShellContext = {
        showRightView: boolean;
        setShowRightView: (value: boolean) => void;
        setTemplate: (template: any) => void;
    }

    const { setShowRightView, setTemplate } = getContext<ShellContext>('shell');

    // 调查组相关状态
    let searchQuery = $state("");
    let showFilters = $state(false);
    let selectedTeam = $state<string | null>(null);

    // 模拟调查组数据
    let teams = $state([
        {
            id: 1,
            name: "异常现象研究小组",
            description: "专注于研究和记录各类超自然现象",
            members: 8,
            activeCase: 3,
            lastActive: "今天",
            type: "研究"
        },
        {
            id: 2,
            name: "时空异常调查团",
            description: "调查与时空异常相关的事件和现象",
            members: 5,
            activeCase: 2,
            lastActive: "昨天",
            type: "调查"
        },
        {
            id: 3,
            name: "能量波动分析组",
            description: "分析不明能量波动及其影响",
            members: 6,
            activeCase: 1,
            lastActive: "3天前",
            type: "分析"
        },
        {
            id: 4,
            name: "神秘事件记录小组",
            description: "记录和整理各类神秘事件的档案",
            members: 4,
            activeCase: 0,
            lastActive: "1周前",
            type: "记录"
        }
    ]);

    // 处理搜索
    function handleSearch() {
        // 实现搜索逻辑
        console.log("搜索:", searchQuery);
    }

    // 处理选择调查组
    function selectTeam(team: typeof teams[0]) {
        selectedTeam = team.id.toString();
    }
</script>

<div class="flex h-full flex-col">
    <!-- 搜索和过滤区域 -->
    <div class="border-b p-4">
        <div class="flex items-center gap-2">
            <div class="relative flex-1">
                <Search class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input 
                    type="search" 
                    placeholder="搜索调查组..." 
                    class="pl-8" 
                    bind:value={searchQuery}
                    on:keydown={(e) => e.key === 'Enter' && handleSearch()}
                />
            </div>
            <Button variant="outline" size="icon" on:click={() => showFilters = !showFilters}>
                <Filter class="h-4 w-4" />
            </Button>
            <Button>
                <Plus class="mr-2 h-4 w-4" />
                创建调查组
            </Button>
        </div>

        {#if showFilters}
            <div class="mt-2 flex flex-wrap gap-2" transition:fly|local={{ y: -20 }}>
                <Button variant="outline" size="sm">研究</Button>
                <Button variant="outline" size="sm">调查</Button>
                <Button variant="outline" size="sm">分析</Button>
                <Button variant="outline" size="sm">记录</Button>
                <Button variant="outline" size="sm" class="ml-auto">
                    清除筛选
                </Button>
            </div>
        {/if}
    </div>

    <!-- 主要内容区域 -->
    <div class="flex-1 p-4">
        <ScrollArea class="h-[calc(100vh-10rem)]">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {#each teams as team}
                    <Card.Root class="cursor-pointer hover:bg-muted" on:click={() => selectTeam(team)}>
                        <Card.Content class="p-4">
                            <div class="flex flex-col gap-3">
                                <div class="flex items-start justify-between">
                                    <div class="flex items-center gap-2">
                                        <div class="bg-primary/10 p-2 rounded-full">
                                            <MessageSquare class="h-5 w-5 text-primary" />
                                        </div>
                                        <div>
                                            <h4 class="font-medium">{team.name}</h4>
                                            <p class="text-sm text-muted-foreground">{team.description}</p>
                                        </div>
                                    </div>
                                    <Badge variant="outline">{team.type}</Badge>
                                </div>
                                
                                <div class="flex items-center justify-between mt-2">
                                    <div class="flex items-center gap-4">
                                        <div class="flex items-center gap-1">
                                            <Users class="h-4 w-4 text-muted-foreground" />
                                            <span class="text-sm">{team.members} 成员</span>
                                        </div>
                                        <div class="flex items-center gap-1">
                                            <MessageSquare class="h-4 w-4 text-muted-foreground" />
                                            <span class="text-sm">{team.activeCase} 活跃案例</span>
                                        </div>
                                    </div>
                                    <span class="text-xs text-muted-foreground">活跃于 {team.lastActive}</span>
                                </div>
                                
                                <div class="flex -space-x-2 mt-2">
                                    {#each Array(Math.min(4, team.members)) as _, i}
                                        <Avatar class="h-8 w-8 border-2 border-background">
                                            <AvatarFallback class="bg-primary/10 text-primary text-xs">用户{i+1}</AvatarFallback>
                                        </Avatar>
                                    {/each}
                                    {#if team.members > 4}
                                        <div class="flex items-center justify-center h-8 w-8 rounded-full bg-muted text-xs font-medium">
                                            +{team.members - 4}
                                        </div>
                                    {/if}
                                </div>
                            </div>
                        </Card.Content>
                    </Card.Root>
                {/each}
            </div>
        </ScrollArea>
    </div>
</div>