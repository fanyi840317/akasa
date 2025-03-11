<script lang="ts">
    import * as Card from "$lib/components/ui/card";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Search, Filter, Plus, Activity, Calendar, MapPin } from "lucide-svelte";
    import { fly } from "svelte/transition";
    import { getContext } from 'svelte';
    import { ScrollArea } from "$lib/components/ui/scroll-area";
    import { Badge } from "$lib/components/ui/badge";
    import { Tabs, TabsContent, TabsList, TabsTrigger } from "$lib/components/ui/tabs";
    import type { Snippet } from "svelte";

    type ShellContext = {
        showRightView: boolean;
        setShowRightView: (value: boolean) => void;
        setTemplate: (template: any) => void;
    }

    const { setShowRightView, setTemplate } = getContext<ShellContext>('shell');

    // 事件相关状态
    let searchQuery = $state("");
    let showFilters = $state(false);
    let selectedEvent = $state<string | null>(null);

    // 模拟事件数据
    let events = $state([
        {
            id: 1,
            title: "神秘光球事件",
            location: "北京海淀区",
            date: "2024-03-15",
            status: "调查中",
            type: "目击事件",
            description: "多名目击者报告在夜空中看到不明光球，呈现出不规则移动轨迹",
            views: 1200
        },
        {
            id: 2,
            title: "不明声音现象",
            location: "上海浦东新区",
            date: "2024-03-14",
            status: "已结案",
            type: "声音异常",
            description: "区域内多次记录到无法解释的低频声波，持续时间约3分钟",
            views: 890
        },
        {
            id: 3,
            title: "异常天气记录",
            location: "广州天河区",
            date: "2024-03-13",
            status: "待处理",
            type: "自然异常",
            description: "局部区域出现与周围环境温度相差显著的气候异常，形成明显边界",
            views: 650
        },
        {
            id: 4,
            title: "时间异常报告",
            location: "深圳南山区",
            date: "2024-03-12",
            status: "调查中",
            type: "时空异常",
            description: "多人报告在特定区域内经历时间流速异常，手表和电子设备均有记录",
            views: 1050
        }
    ]);

    // 处理搜索
    function handleSearch() {
        // 实现搜索逻辑
        console.log("搜索:", searchQuery);
    }

    // 处理选择事件
    function selectEvent(event: typeof events[0]) {
        selectedEvent = event.id.toString();
        // 在实际应用中，这里可能会触发详情页面的显示
    }

    // 获取状态徽章颜色
    function getStatusColor(status: string) {
        switch(status) {
            case '调查中':
                return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
            case '已结案':
                return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
            case '待处理':
                return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
            default:
                return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
        }
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
                    placeholder="搜索神秘事件..." 
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
                记录新事件
            </Button>
        </div>

        {#if showFilters}
            <div class="mt-2 flex flex-wrap gap-2" transition:fly|local={{ y: -20 }}>
                <Button variant="outline" size="sm">目击事件</Button>
                <Button variant="outline" size="sm">声音异常</Button>
                <Button variant="outline" size="sm">自然异常</Button>
                <Button variant="outline" size="sm">时空异常</Button>
                <Button variant="outline" size="sm" class="ml-auto">
                    清除筛选
                </Button>
            </div>
        {/if}
    </div>

    <!-- 主要内容区域 -->
    <div class="flex-1">
        <Tabs defaultValue="all" class="w-full">
            <div class="border-b px-4">
                <TabsList>
                    <TabsTrigger value="all">全部事件</TabsTrigger>
                    <TabsTrigger value="investigating">调查中</TabsTrigger>
                    <TabsTrigger value="pending">待处理</TabsTrigger>
                    <TabsTrigger value="closed">已结案</TabsTrigger>
                </TabsList>
            </div>
            
            <TabsContent value="all" class="p-0 border-none">
                <ScrollArea class="h-[calc(100vh-12rem)]">
                    <div class="p-4 space-y-3">
                        {#each events as event}
                            <Card.Root class="cursor-pointer hover:bg-muted" on:click={() => selectEvent(event)}>
                                <Card.Content class="p-4">
                                    <div class="flex flex-col gap-2">
                                        <div class="flex items-start justify-between">
                                            <div>
                                                <h4 class="font-medium text-lg">{event.title}</h4>
                                                <p class="text-sm text-muted-foreground">{event.description}</p>
                                            </div>
                                            <Badge class={getStatusColor(event.status)}>{event.status}</Badge>
                                        </div>
                                        
                                        <div class="flex items-center gap-4 mt-2">
                                            <div class="flex items-center gap-1">
                                                <MapPin class="h-4 w-4 text-muted-foreground" />
                                                <span class="text-sm">{event.location}</span>
                                            </div>
                                            <div class="flex items-center gap-1">
                                                <Calendar class="h-4 w-4 text-muted-foreground" />
                                                <span class="text-sm">{event.date}</span>
                                            </div>
                                            <div class="flex items-center gap-1">
                                                <Activity class="h-4 w-4 text-muted-foreground" />
                                                <span class="text-sm">{event.views} 浏览</span>
                                            </div>
                                            <span class="text-xs bg-secondary/20 px-2 py-0.5 rounded ml-auto">{event.type}</span>
                                        </div>
                                    </div>
                                </Card.Content>
                            </Card.Root>
                        {/each}
                    </div>
                </ScrollArea>
            </TabsContent>
            
            <TabsContent value="investigating" class="p-0 border-none">
                <ScrollArea class="h-[calc(100vh-12rem)]">
                    <div class="p-4 space-y-3">
                        {#each events.filter(e => e.status === '调查中') as event}
                            <Card.Root class="cursor-pointer hover:bg-muted" on:click={() => selectEvent(event)}>
                                <Card.Content class="p-4">
                                    <div class="flex flex-col gap-2">
                                        <div class="flex items-start justify-between">
                                            <div>
                                                <h4 class="font-medium text-lg">{event.title}</h4>
                                                <p class="text-sm text-muted-foreground">{event.description}</p>
                                            </div>
                                            <Badge class={getStatusColor(event.status)}>{event.status}</Badge>
                                        </div>
                                        
                                        <div class="flex items-center gap-4 mt-2">
                                            <div class="flex items-center gap-1">
                                                <MapPin class="h-4 w-4 text-muted-foreground" />
                                                <span class="text-sm">{event.location}</span>
                                            </div>
                                            <div class="flex items-center gap-1">
                                                <Calendar class="h-4 w-4 text-muted-foreground" />
                                                <span class="text-sm">{event.date}</span>
                                            </div>
                                            <span class="text-xs bg-secondary/20 px-2 py-0.5 rounded ml-auto">{event.type}</span>
                                        </div>
                                    </div>
                                </Card.Content>
                            </Card.Root>
                        {/each}
                    </div>
                </ScrollArea>
            </TabsContent>
            
            <TabsContent value="pending" class="p-0 border-none">
                <ScrollArea class="h-[calc(100vh-12rem)]">
                    <div class="p-4 space-y-3">
                        {#each events.filter(e => e.status === '待处理') as event}
                            <Card.Root class="cursor-pointer hover:bg-muted" on:click={() => selectEvent(event)}>
                                <Card.Content class="p-4">
                                    <!-- 内容与其他选项卡相同 -->
                                    <div class="flex flex-col gap-2">
                                        <div class="flex items-start justify-between">
                                            <div>
                                                <h4 class="font-medium text-lg">{event.title}</h4>
                                                <p class="text-sm text-muted-foreground">{event.description}</p>
                                            </div>
                                            <Badge class={getStatusColor(event.status)}>{event.status}</Badge>
                                        </div>
                                        
                                        <div class="flex items-center gap-4 mt-2">
                                            <div class="flex items-center gap-1">
                                                <MapPin class="h-4 w-4 text-muted-foreground" />
                                                <span class="text-sm">{event.location}</span>
                                            </div>
                                            <div class="flex items-center gap-1">
                                                <Calendar class="h-4 w-4 text-muted-foreground" />
                                                <span class="text-sm">{event.date}</span>
                                            </div>
                                            <span class="text-xs bg-secondary/20 px-2 py-0.5 rounded ml-auto">{event.type}</span>
                                        </div>
                                    </div>
                                </Card.Content>
                            </Card.Root>
                        {/each}
                    </div>
                </ScrollArea>
            </TabsContent>
            
            <TabsContent value="closed" class="p-0 border-none">
                <ScrollArea class="h-[calc(100vh-12rem)]">
                    <div class="p-4 space-y-3">
                        {#each events.filter(e => e.status === '已结案') as event}
                            <Card.Root class="cursor-pointer hover:bg-muted" on:click={() => selectEvent(event)}>
                                <Card.Content class="p-4">
                                    <!-- 内容与其他选项卡相同 -->
                                    <div class="flex flex-col gap-2">
                                        <div class="flex items-start justify-between">
                                            <div>
                                                <h4 class="font-medium text-lg">{event.title}</h4>
                                                <p class="text-sm text-muted-foreground">{event.description}</p>
                                            </div>
                                            <Badge class={getStatusColor(event.status)}>{event.status}</Badge>
                                        </div>
                                        
                                        <div class="flex items-center gap-4 mt-2">
                                            <div class="flex items-center gap-1">
                                                <MapPin class="h-4 w-4 text-muted-foreground" />
                                                <span class="text-sm">{event.location}</span>
                                            </div>
                                            <div class="flex items-center gap-1">
                                                <Calendar class="h-4 w-4 text-muted-foreground" />
                                                <span class="text-sm">{event.date}</span>
                                            </div>
                                            <span class="text-xs bg-secondary/20 px-2 py-0.5 rounded ml-auto">{event.type}</span>
                                        </div>
                                    </div>
                                </Card.Content>
                            </Card.Root>
                        {/each}
                    </div>
                </ScrollArea>
            </TabsContent>
        </Tabs>
    </div>
</div>