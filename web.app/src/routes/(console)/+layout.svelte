<script lang="ts">
    import { fade, fly, slide } from "svelte/transition";
    import type { LayoutData } from "./$types";
    import * as Sidebar from "$lib/components/ui/sidebar";
    import { Separator } from "$lib/components/ui/separator";
    import * as Breadcrumb from "$lib/components/ui/breadcrumb";
    import LeftSidebar from "$lib/components/console/left-sidebar.svelte";
    import NotionSidePanel from "$lib/components/NotionSidePanel.svelte";
    import * as Resizable from "$lib/components/ui/resizable";
    import { Button } from "$lib/components/ui/button";
    import { PaneGroup, Pane, PaneResizer, type PaneAPI } from "paneforge";
    import {
        Share2,
        X as CloseIcon,
        ChevronRight,
        ChevronLeft,
    } from "lucide-svelte";
    import { onMount } from "svelte";
    import Card from "$lib/components/ui/card/card.svelte";
    import { auth } from '$lib/stores/auth';

    let { data } = $props();
    let user = $derived(data.user);

    // 如果需要响应式地获取最新的用户状态，可以使用：
    // $: user = $auth.user;

    // 控制右侧面板状态
    let showRightPanel = $state(false);
    let leftPaneAPI: PaneAPI;
    // let collapsed = false;

    // 切换右侧面板显示状态
    function toggleRightPanel() {
        showRightPanel = !showRightPanel;
        if(showRightPanel){
            leftPaneAPI.expand();
        }else{
            leftPaneAPI.collapse();
        }
    }

    // 关闭右侧面板
    function closeRightPanel() {
        showRightPanel = false;
    }
</script>

<!-- 添加外层包装div来控制溢出 -->
<div class="fixed inset-0 overflow-hidden">
    <!-- 使用PaneGroup组件在最外层，以实现动态调整大小 -->
    <PaneGroup direction="horizontal">
        <!-- 主内容区域，包含Sidebar.Provider -->
        <Pane defaultSize={100} order={1} collapsedSize={40} collapsible={true} bind:pane={leftPaneAPI} >
            <Sidebar.Provider>
                <LeftSidebar collapsible="icon" side="left" />
                <Sidebar.Inset>
                    <header
                        class="flex h-16 shrink-0 items-center gap-2 justify-between"
                    >
                        <div class="flex items-center gap-2 px-4">
                            <Sidebar.Trigger class="-ml-1" />
                            <Separator
                                orientation="vertical"
                                class="mr-2 h-4"
                            />
                            <Breadcrumb.Root>
                                <Breadcrumb.List>
                                    <Breadcrumb.Item class="hidden md:block">
                                        <Breadcrumb.Link href="#"
                                            >Building Your Application</Breadcrumb.Link
                                        >
                                    </Breadcrumb.Item>
                                    <Breadcrumb.Separator
                                        class="hidden md:block"
                                    />
                                    <Breadcrumb.Item>
                                        <Breadcrumb.Page
                                            >Data Fetching</Breadcrumb.Page
                                        >
                                    </Breadcrumb.Item>
                                </Breadcrumb.List>
                            </Breadcrumb.Root>
                        </div>
                        <div class="pr-4">
                            <Button
                                variant="ghost"
                                size="icon"
                                onclick={toggleRightPanel}
                            >
                                <Share2 class="h-5 w-5" />
                            </Button>
                        </div>
                    </header>
                    <div class="flex flex-1 p-4">
                        <slot></slot>
                    </div>
                </Sidebar.Inset>
            </Sidebar.Provider>
        </Pane>
        {#if showRightPanel}
            <Resizable.Handle withHandle />
            <!-- 右侧面板 -->
            <Pane
                class="bg-card h-full relative"
                defaultSize={0}
                minSize={60}
                order={2}
            >
                <!-- 分享面板内容 -->
                <div class="h-full w-full bg-card" transition:fly={{ duration: 300, x: 300, easing: (t) => t * (2 - t) }}>
                    <slot name="leftPane"></slot>
                </div>
            </Pane>
        {/if}
    </PaneGroup>
</div>

<div class="min-h-screen flex flex-col">
    <header class="border-b">
        <div class="container mx-auto p-4">
            <div class="flex justify-between items-center">
                <div>Console</div>
                <div>
                    {#if user}
                        <span class="mr-2">{user.name}</span>
                    {/if}
                </div>
            </div>
        </div>
    </header>

    <main class="flex-1 container mx-auto p-4">
        <slot />
    </main>
</div>
