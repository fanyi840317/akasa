<script lang="ts">
    import * as Card from "$lib/components/ui/card";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Search, Filter, Plus, Heart, UserPlus } from "lucide-svelte";
    import { fly } from "svelte/transition";
    import { getContext } from 'svelte';
    import { ScrollArea } from "$lib/components/ui/scroll-area";
    import { Avatar, AvatarImage, AvatarFallback } from "$lib/components/ui/avatar";
    import type { Snippet } from "svelte";

    type ShellContext = {
        showRightView: boolean;
        setShowRightView: (value: boolean) => void;
        setTemplate: (template: any) => void;
    }

    const { setShowRightView, setTemplate } = getContext<ShellContext>('shell');

    // 关注的人相关状态
    let searchQuery = $state("");
    let showFilters = $state(false);
    let selectedPerson = $state<string | null>(null);

    // 模拟关注的人数据
    let followingList = $state([
        {
            id: 1,
            name: "张三",
            avatar: "/images/avatars/avatar-1.png",
            role: "调查员",
            location: "北京",
            lastActive: "刚刚"
        },
        {
            id: 2,
            name: "李四",
            avatar: "/images/avatars/avatar-2.png",
            role: "研究员",
            location: "上海",
            lastActive: "10分钟前"
        },
        {
            id: 3,
            name: "王五",
            avatar: "/images/avatars/avatar-3.png",
            role: "分析师",
            location: "广州",
            lastActive: "1小时前"
        },
        {
            id: 4,
            name: "赵六",
            avatar: "/images/avatars/avatar-4.png",
            role: "顾问",
            location: "深圳",
            lastActive: "昨天"
        }
    ]);

    // 处理搜索
    function handleSearch() {
        // 实现搜索逻辑
        console.log("搜索:", searchQuery);
    }

    // 处理选择关注的人
    function selectPerson(person: typeof followingList[0]) {
        selectedPerson = person.id.toString();
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
                    placeholder="搜索关注的人..." 
                    class="pl-8" 
                    bind:value={searchQuery}
                    on:keydown={(e) => e.key === 'Enter' && handleSearch()}
                />
            </div>
            <Button variant="outline" size="icon" on:click={() => showFilters = !showFilters}>
                <Filter class="h-4 w-4" />
            </Button>
            <Button>
                <UserPlus class="mr-2 h-4 w-4" />
                关注新用户
            </Button>
        </div>

        {#if showFilters}
            <div class="mt-2 flex flex-wrap gap-2" transition:fly|local={{ y: -20 }}>
                <Button variant="outline" size="sm">调查员</Button>
                <Button variant="outline" size="sm">研究员</Button>
                <Button variant="outline" size="sm">分析师</Button>
                <Button variant="outline" size="sm">顾问</Button>
                <Button variant="outline" size="sm" class="ml-auto">
                    清除筛选
                </Button>
            </div>
        {/if}
    </div>

    <!-- 主要内容区域 -->
    <div class="flex-1 p-4">
        <ScrollArea class="h-[calc(100vh-10rem)]">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {#each followingList as person}
                    <Card.Root class="cursor-pointer hover:bg-muted" on:click={() => selectPerson(person)}>
                        <Card.Content class="p-4">
                            <div class="flex items-start gap-3">
                                <Avatar class="h-12 w-12">
                                    <AvatarImage src={person.avatar} alt={person.name} />
                                    <AvatarFallback>{person.name.substring(0, 2)}</AvatarFallback>
                                </Avatar>
                                <div class="flex-1">
                                    <h4 class="font-medium">{person.name}</h4>
                                    <p class="text-sm text-muted-foreground">{person.role}</p>
                                    <div class="flex items-center gap-2 mt-1">
                                        <span class="text-xs">{person.location}</span>
                                        <span class="text-xs text-muted-foreground">· 活跃于 {person.lastActive}</span>
                                    </div>
                                </div>
                                <Button variant="ghost" size="icon" class="h-8 w-8">
                                    <Heart class="h-4 w-4 text-primary" fill="currentColor" />
                                </Button>
                            </div>
                        </Card.Content>
                    </Card.Root>
                {/each}
            </div>
        </ScrollArea>
    </div>
</div>