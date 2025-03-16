<script lang="ts">
    import { createEventDispatcher, type Snippet } from "svelte";
    import { fade, fly } from "svelte/transition";
    import { Button } from "$lib/components/ui/button";
    import { Separator } from "$lib/components/ui/separator";
    import {
        Avatar,
        AvatarFallback,
        AvatarImage,
    } from "$lib/components/ui/avatar";
    import { Textarea } from "$lib/components/ui/textarea";
    import { X, Share2, Check, PlusCircle } from "lucide-svelte";
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
    // 处理关闭事件
    function handleClose() {
        dispatch("close");
        // 移除直接修改open的代码，让父组件负责更新状态
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
                        class="bg-muted shadow-xl border-l" >
                {#if showHeader}
                    <!-- 面板头部 -->
                {/if}

                <!-- 面板内容 -->
                <div class="flex-1 overflow-y-auto p-4">
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
