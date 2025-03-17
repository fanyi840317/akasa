<script lang="ts">
    import { createEventDispatcher, type Snippet } from "svelte";
    import { fade, fly } from "svelte/transition";
    import { Button } from "$lib/components/ui/button";
    import { X, PlusCircle, Minimize, Maximize } from "lucide-svelte";
    import * as Resizable from "$lib/components/ui/resizable/index.js";

    const dispatch = createEventDispatcher();

    // 组件属性
    let {
        open = false,
        title = "",
        icon = PlusCircle,
        iconColor = "bg-blue-500",
        width = 40,
        maxWidth = 80,
        showHeader = true,
        contentView = undefined,
        showFooter = false,
        showBackdrop = true,
        properties = [],
    }: {
        open?: boolean;
        title?: string;
        icon?: any;
        iconColor?: string;
        width?: number;
        maxWidth?: number;
        showHeader?: boolean;
        showFooter?: boolean;
        showBackdrop?: boolean;
        contentView?: Snippet;
        properties?: Array<{
            label: string;
            value: string;
            icon?: any;
            color?: string;
        }>;
    } = $props();
    // 内部状态
    let description = "";
    let isMinimized = false;
    let isMaximized = false;

    // 处理关闭事件
    function handleClose() {
        dispatch("close");
    }

    // 处理最小化事件
    function handleMinimize() {
        isMinimized = !isMinimized;
        dispatch("minimize", { isMinimized });
    }

    // 处理最大化事件
    function handleMaximize() {
        isMaximized = !isMaximized;
        width = isMaximized ? 100 : 40;
        maxWidth = isMaximized ? 100 : 80;
        dispatch("maximize", { isMaximized });
    }

    // 处理保存事件
    function handleSave() {
        dispatch("save", { title, description, properties });
    }
    // 动态组件
    const IconComponent = icon;
</script>

{#if open}
    <!-- 面板 -->
    <div
        class="fixed top-0 right-0 h-full w-full z-50"
        transition:fly={{ x: "100%", duration: 300, opacity: 1 }}
    >
        <Resizable.PaneGroup direction="horizontal" class="h-full w-full ">
            <Resizable.Pane
                defaultSize={100-width}
                class=""
                onclick={handleClose}
            >
                {#if showBackdrop}
                    <div
                        class="w-full h-full bg-background/80 backdrop-blur-sm"
                        transition:fade={{ duration: 200 }}
                    ></div>
                {/if}
            </Resizable.Pane>
            <Resizable.Handle withHandle />
            <Resizable.Pane defaultSize={width} maxSize={maxWidth} minSize={width-10}
                        class="bg-muted shadow-lg" >
                {#if showHeader}
                    <!-- 面板头部 -->
                    <div class="flex items-center justify-between px-4 py-2">
                        <div class="flex items-center gap-2">
                            <Button variant="ghost" size="icon" class="h-4 w-4" onclick={handleMinimize}>
                                <Minimize class="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="icon" class="h-8 w-8" onclick={handleMaximize}>
                                <Maximize class="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="icon" class="h-8 w-8" onclick={handleClose}>
                                <X class="h-4 w-4" />
                            </Button>
                        </div>
                        <div class="flex items-center gap-2">
                      
                        </div>
                    </div>
                {/if}

                <!-- 面板内容 -->
                <div class="flex-1 overflow-y-auto p-4" class:hidden={isMinimized}>
                    {@render contentView?.()}
                </div>

                {#if showFooter}
                    <!-- 面板底部 -->
                    <div
                        class="p-4 border-t flex items-center justify-between sticky bottom-0 bg-card"
                    ></div>
                {/if}
            </Resizable.Pane>
        </Resizable.PaneGroup>
    </div>
{/if}
