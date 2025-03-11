<script lang="ts">
    import * as Card from "$lib/components/ui/card";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Search, Filter, Plus, Map } from "lucide-svelte";
    import { fly } from "svelte/transition";
    import { getContext } from 'svelte';
    import { ScrollArea } from "$lib/components/ui/scroll-area";
    import type { Snippet } from "svelte";

    type ShellContext = {
        showRightView: boolean;
        setShowRightView: (value: boolean) => void;
        setTemplate: (template: any) => void;
    }

    const { setShowRightView, setTemplate } = getContext<ShellContext>('shell');

    // 地图相关状态
    let searchQuery = $state("");
    let showFilters = $state(false);
    let selectedLocation = $state<string | null>(null);

    // 模拟地图位置数据
    let locations = $state([
        {
            id: 1,
            name: "北京异常区域",
            coordinates: "39.9042° N, 116.4074° E",
            type: "异常能量",
            level: "高",
            lastUpdated: "2024-03-15"
        },
        {
            id: 2,
            name: "上海观测点",
            coordinates: "31.2304° N, 121.4737° E",
            type: "时空异常",
            level: "中",
            lastUpdated: "2024-03-14"
        },
        {
            id: 3,
            name: "广州监测站",
            coordinates: "23.1291° N, 113.2644° E",
            type: "能量波动",
            level: "低",
            lastUpdated: "2024-03-13"
        }
    ]);

    // 处理搜索
    function handleSearch() {
        // 实现搜索逻辑
        console.log("搜索:", searchQuery);
    }

    // 处理位置选择
    function selectLocation(location: typeof locations[0]) {
        selectedLocation = location.id.toString();
        // 在实际应用中，这里可能会触发地图上的标记选中效果
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
                    placeholder="搜索地图位置..." 
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
                添加位置
            </Button>
        </div>

        {#if showFilters}
            <div class="mt-2 flex flex-wrap gap-2" transition:fly|local={{ y: -20 }}>
                <Button variant="outline" size="sm">异常能量</Button>
                <Button variant="outline" size="sm">时空异常</Button>
                <Button variant="outline" size="sm">能量波动</Button>
                <Button variant="outline" size="sm">高风险区域</Button>
                <Button variant="outline" size="sm" class="ml-auto">
                    <X class="mr-1 h-3 w-3" /> 清除筛选
                </Button>
            </div>
        {/if}
    </div>

    <!-- 主要内容区域 -->
    <div class="grid flex-1 grid-cols-1 md:grid-cols-3 gap-0">
        <!-- 左侧位置列表 -->
        <div class="border-r md:col-span-1">
            <ScrollArea class="h-[calc(100vh-10rem)]">
                <div class="p-4 space-y-2">
                    <h3 class="font-medium mb-2">位置列表</h3>
                    {#each locations as location}
                        <Card.Root class="cursor-pointer hover:bg-muted" on:click={() => selectLocation(location)}>
                            <Card.Content class="p-3">
                                <div class="flex justify-between items-start">
                                    <div>
                                        <h4 class="font-medium">{location.name}</h4>
                                        <p class="text-sm text-muted-foreground">{location.coordinates}</p>
                                        <div class="flex items-center gap-2 mt-1">
                                            <span class="text-xs bg-primary/10 text-primary px-2 py-0.5 rounded">{location.type}</span>
                                            <span class="text-xs">风险等级: {location.level}</span>
                                        </div>
                                    </div>
                                    <Map class="h-5 w-5 text-muted-foreground" />
                                </div>
                            </Card.Content>
                        </Card.Root>
                    {/each}
                </div>
            </ScrollArea>
        </div>

        <!-- 右侧地图区域 -->
        <div class="md:col-span-2 bg-muted/30 flex items-center justify-center">
            <div class="text-center">
                <Map class="h-16 w-16 mx-auto text-muted-foreground mb-4" />
                <h3 class="text-xl font-medium">地图组件将在此处显示</h3>
                <p class="text-muted-foreground mt-2">这里将集成地图组件，显示所有标记的位置和异常区域</p>
            </div>
        </div>
    </div>
</div>