<script lang="ts">
    import * as Card from "$lib/components/ui/card";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Search, Filter, Plus, Bookmark, Folder, FileText, Link } from "lucide-svelte";
    import { fly } from "svelte/transition";
    import { getContext } from 'svelte';
    import { ScrollArea } from "$lib/components/ui/scroll-area";
    import { Tabs, TabsContent, TabsList, TabsTrigger } from "$lib/components/ui/tabs";
    import type { Snippet } from "svelte";

    type ShellContext = {
        showRightView: boolean;
        setShowRightView: (value: boolean) => void;
        setTemplate: (template: any) => void;
    }

    const { setShowRightView, setTemplate } = getContext<ShellContext>('shell');

    // 收藏相关状态
    let searchQuery = $state("");
    let showFilters = $state(false);
    let selectedBookmark = $state<string | null>(null);

    // 模拟收藏数据
    let bookmarks = $state([
        {
            id: 1,
            title: "异常现象研究报告",
            type: "document",
            category: "研究",
            addedDate: "2024-03-15",
            url: "/documents/research-report-1"
        },
        {
            id: 2,
            title: "时空异常调查指南",
            type: "document",
            category: "指南",
            addedDate: "2024-03-14",
            url: "/documents/investigation-guide"
        },
        {
            id: 3,
            title: "神秘事件数据库",
            type: "link",
            category: "数据",
            addedDate: "2024-03-13",
            url: "https://example.com/mysterious-events"
        },
        {
            id: 4,
            title: "能量波动分析工具",
            type: "link",
            category: "工具",
            addedDate: "2024-03-12",
            url: "https://example.com/energy-analysis"
        }
    ]);

    // 处理搜索
    function handleSearch() {
        // 实现搜索逻辑
        console.log("搜索:", searchQuery);
    }

    // 处理选择收藏
    function selectBookmark(bookmark: typeof bookmarks[0]) {
        selectedBookmark = bookmark.id.toString();
    }

    // 获取图标
    function getBookmarkIcon(type: string) {
        switch(type) {
            case 'document':
                return FileText;
            case 'link':
                return Link;
            default:
                return Bookmark;
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
                    placeholder="搜索收藏..." 
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
                添加收藏
            </Button>
        </div>

        {#if showFilters}
            <div class="mt-2 flex flex-wrap gap-2" transition:fly|local={{ y: -20 }}>
                <Button variant="outline" size="sm">文档</Button>
                <Button variant="outline" size="sm">链接</Button>
                <Button variant="outline" size="sm">研究</Button>
                <Button variant="outline" size="sm">指南</Button>
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
                    <TabsTrigger value="all">全部</TabsTrigger>
                    <TabsTrigger value="documents">文档</TabsTrigger>
                    <TabsTrigger value="links">链接</TabsTrigger>
                    <TabsTrigger value="recent">最近</TabsTrigger>
                </TabsList>
            </div>
            
            <TabsContent value="all" class="p-0 border-none">
                <ScrollArea class="h-[calc(100vh-12rem)]">
                    <div class="p-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {#each bookmarks as bookmark}
                            <Card.Root class="cursor-pointer hover:bg-muted" on:click={() => selectBookmark(bookmark)}>
                                <Card.Content class="p-4">
                                    <div class="flex items-start gap-3">
                                        <div class="bg-primary/10 p-2 rounded-md">
                                            <svelte:component this={getBookmarkIcon(bookmark.type)} class="h-5 w-5 text-primary" />
                                        </div>
                                        <div class="flex-1">
                                            <h4 class="font-medium">{bookmark.title}</h4>
                                            <p class="text-sm text-muted-foreground">{bookmark.url}</p>
                                            <div class="flex items-center gap-2 mt-1">
                                                <span class="text-xs bg-secondary/20 px-2 py-0.5 rounded">{bookmark.category}</span>
                                                <span class="text-xs text-muted-foreground">添加于 {bookmark.addedDate}</span>
                                            </div>
                                        </div>
                                        <Button variant="ghost" size="icon" class="h-8 w-8">
                                            <Bookmark class="h-4 w-4" />
                                        </Button>
                                    </div>
                                </Card.Content>
                            </Card.Root>
                        {/each}
                    </div>
                </ScrollArea>
            </TabsContent>
            
            <TabsContent value="documents" class="p-4">
                <div class="text-center py-8">
                    <FileText class="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                    <h3 class="text-xl font-medium">文档收藏</h3>
                    <p class="text-muted-foreground mt-2">这里将显示所有收藏的文档</p>
                </div>
            </TabsContent>
            
            <TabsContent value="links" class="p-4">
                <div class="text-center py-8">
                    <Link class="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                    <h3 class="text-xl font-medium">链接收藏</h3>
                    <p class="text-muted-foreground mt-2">这里将显示所有收藏的外部链接</p>
                </div>
            </TabsContent>
            
            <TabsContent value="recent" class="p-4">
                <div class="text-center py-8">
                    <Folder class="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                    <h3 class="text-xl font-medium">最近收藏</h3>
                    <p class="text-muted-foreground mt-2">这里将显示最近添加的收藏项目</p>
                </div>
            </TabsContent>
        </Tabs>
    </div>
</div>