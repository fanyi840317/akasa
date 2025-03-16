<script lang="ts">
    import { createEventDispatcher } from "svelte";
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

    const dispatch = createEventDispatcher();

    // 组件属性
    export let open = false;
    export let title = "";
    export let icon = PlusCircle;
    export let iconColor = "bg-blue-500";
    export let width = "50%";
    export let maxWidth = "max-w-3xl";
    export let showHeader = true;
    export let showFooter = true;
    export let properties: Array<{
        label: string;
        value: string;
        icon?: any;
        color?: string;
    }> = [];

    // 内部状态
    let description = "";

    // 处理关闭事件
    function handleClose() {
        dispatch("close");
    }

    // 处理保存事件
    function handleSave() {
        dispatch("save", { title, description, properties });
    }

    // 动态组件
    const IconComponent = icon;
</script>

{#if open}
    <!-- 背景遮罩 -->
    <div
        class="fixed inset-0 bg-background/80 backdrop-blur-sm z-50"
        on:click={handleClose}
        transition:fade={{ duration: 200 }}
    ></div>

    <!-- 面板 -->
    <div
        class="fixed top-0 right-0 h-full {width} {maxWidth} bg-card border-l shadow-lg z-50 flex flex-col"
        transition:fly={{ x: 300, duration: 300, opacity: 1 }}
    >
        {#if showHeader}{/if}

        {#if showFooter}{/if}
    </div>
{/if}
