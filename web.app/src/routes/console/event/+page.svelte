<script lang="ts">
    /**
     * 事件页面组件
     * 展示地图和事件信息，支持移动端适配
     */
    import { onMount } from 'svelte';
    import { _ } from 'svelte-i18n';
    import { goto } from '$app/navigation';
    import { base } from "$app/paths";
    import { fade, fly } from "svelte/transition";
    import { spring } from "svelte/motion";
    
    // 控制台组件
    import { 
        Header as HeaderPage, 
        MapView, 
        SearchBox,
        NotionCard 
    } from '$lib/components/console';
    
    // UI 组件
    import { Button } from '$lib/components/ui/button';
    import { Card } from '$lib/components/ui/card';
    import EventList from '$lib/components/event-list.svelte';
    import { Splitpanes, Pane } from 'svelte-splitpanes';
    
    // 创建事件相关
    import NotionEventCreator from './(create-event)/notion-event-creator.svelte';
    
    // 图标
    import { PlusCircle, MapPin, X as CloseIcon } from 'lucide-svelte';
    
    // 存储
    import { auth } from "$lib/stores/auth";
    
    // 类型导入
    import type { PageData } from './$types';

    // 页面属性和状态
    let { data }: { data: PageData } = $props();
    let searchQuery = "";
    let map: any;
    
    // 使用$state进行响应式状态管理
    let isMobileView = $state(false);
    let showCreateEvent = $state(false);
    let isAnimating = $state(false);
    
    // 使用spring动画值来实现平滑的尺寸过渡
    const size = spring({ width: 0, height: 0 }, {
        stiffness: 0.1,
        damping: 0.6
    });
    
    /**
     * 更新容器宽度以检测移动视图
     */
    function handleResize(event: CustomEvent) {
        const { detail } = event;
        if (!isAnimating || showCreateEvent) {
            const width = detail[0].size;
            isMobileView = width < 600;
            size.set({ width, height: detail[0].size });
        }
    }
    
    // 事件分类数据
    const categories = [
        { name: $_("events.categories.urban"), icon: "/icons/urban.svg", type: "urban" },
        { name: $_("events.categories.paranormal"), icon: "/icons/paranormal.svg", type: "paranormal" },
        { name: $_("events.categories.supernatural"), icon: "/icons/supernatural.svg", type: "supernatural" },
        { name: $_("events.categories.mysterious"), icon: "/icons/mysterious.svg", type: "mysterious" },
        { name: $_("events.categories.unexplained"), icon: "/icons/unexplained.svg", type: "unexplained" },
        { name: $_("events.categories.phenomena"), icon: "/icons/phenomena.svg", type: "phenomena" }
    ];
    
    /**
     * 处理创建新事件
     * 如果用户未登录，跳转到登录页
     */
    function handleShare() {
        if (!$auth.user) {
            goto(`${base}/login`);
            return;
        }
        isAnimating = true;
        showCreateEvent = !showCreateEvent;
        setTimeout(() => {
            isAnimating = false;
        }, 300);
    }
    
    /**
     * 更新地图位置
     * @param location 位置搜索字符串
     */
    async function updateMapLocation(location: string) {
        if (!location.trim()) return;
        
        try {
            const response = await fetch(
                `https://api.example.com/geocode?address=${encodeURIComponent(location)}`
            );
            
            if (!response.ok) {
                throw new Error(`API响应状态: ${response.status}`);
            }
            
            const data = await response.json();
            if (data?.results?.[0]?.geometry?.location) {
                const { lat, lng } = data.results[0].geometry.location;
                map.setCenter([lng, lat]);
            }
        } catch (error) {
            console.error("位置更新失败:", error);
            // 这里可以添加用户友好的错误提示UI
        }
    }
    
    // 简化的位置搜索处理函数
    const searchLocation = () => updateMapLocation(searchQuery);
</script>

<Splitpanes theme="my-theme" class="h-[calc(100vh-4rem)] w-full overflow-hidden" on:resize={handleResize}>
    <Pane class="flex-1 w-full overflow-hidden">
        <HeaderPage title="event">
            {#snippet actions()}
                <Button variant="secondary" size="sm" class="map-control-button" on:click={handleShare}>
                    <PlusCircle class="h-4 w-4 mr-2" />
                    {$_('events.share')}
                </Button>
            {/snippet}
            {#snippet children()}
                <MapView locationData={data.location}>
                    <!-- 最新事件卡片 -->
                    {#if !isMobileView}
                        <div 
                            class="absolute top-4 right-4 w-80 z-10"
                            transition:fly={{ x: 20, duration: 250, easing: t => {
                                return 1 - Math.pow(1 - t, 3);
                            }}}
                        >
                            <NotionCard title={$_("events.latest")}>
                                <EventList />
                            </NotionCard>
                        </div>
                    {/if}
                    
                    <!-- 搜索框 -->
                    <div class="absolute top-4 left-4 w-80 z-10"
                        style="transform: translate3d(0,0,0);"
                        in:fly={{ y: -10, duration: 200, delay: 100 }}
                    >
                        <SearchBox 
                            placeholder={$_("events.search_placeholder")}
                            bind:value={searchQuery}
                            on:search={searchLocation}
                            on:locationSearch={searchLocation}
                        />
                    </div>
                    
                    <!-- 调试信息: 显示容器尺寸 -->
                    <div class="absolute bottom-4 left-4 text-xs text-white bg-black/50 px-2 py-1 rounded-md pointer-events-none">
                        宽度: {$size.width.toFixed(0)}px / 高度: {$size.height.toFixed(0)}px
                        {isMobileView ? '(移动视图)' : '(桌面视图)'}
                    </div>
                </MapView>
            {/snippet}
        </HeaderPage>
    </Pane>
    
    <!-- 创建事件面板 -->
    {#if showCreateEvent}
        <Pane size={70}>
            <div class="flex h-full flex-col bg-card overflow-hidden" 
                in:fly={{ x: 30, duration: 250, easing: t => 1 - Math.pow(1 - t, 3) }}
                out:fly={{ x: 30, duration: 250, easing: t => 1 - Math.pow(1 - t, 3) }}
            >
                <div class="flex items-center justify-between px-4 py-2 border-b flex-shrink-0">
                    <Button variant="ghost" class="p-2 hover:bg-muted/50 transition-colors duration-150" on:click={() => (showCreateEvent = false)}>
                        <CloseIcon class="h-4 w-4" />
                        <span class="sr-only">返回</span>
                    </Button>
                    <h2 class="text-lg font-medium text-foreground">{$_("events.create.title")}</h2>
                    <div class="w-8" /><!-- 空间占位，保持标题居中 -->
                </div>
                <div class="flex-1 overflow-auto p-4">
                    <NotionEventCreator />
                </div>
            </div>
        </Pane>
    {/if}
</Splitpanes>

<style>
    /* 确保使用Inter字体，符合Notion设计风格 */
    :global(.font-inter) {
        font-family: 'Inter', sans-serif;
    }
    
    /* Notion风格的微妙过渡效果 */
    :global(.map-control-button) {
        transition: all 150ms ease-in-out;
    }
    
    :global(.map-control-button:hover) {
        background-color: rgba(55, 53, 47, 0.08);
    }
    
    /* 添加页面元素的响应式动画 */
    :global(.splitpanes__pane) {
        transition: flex-basis 300ms cubic-bezier(0.34, 1.56, 0.64, 1);
    }
</style>
