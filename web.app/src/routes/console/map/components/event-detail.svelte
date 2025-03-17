<script lang="ts">
    import { Separator } from "$lib/components/ui/separator";
    import {
        Avatar,
        AvatarFallback,
        AvatarImage,
    } from "$lib/components/ui/avatar";
    import { Badge } from "$lib/components/ui/badge";
    import { ScrollArea } from "$lib/components/ui/scroll-area";
    import { Input } from "$lib/components/ui/input";
    import { onMount, onDestroy } from "svelte";
    import { browser } from "$app/environment";
    import { writable } from "svelte/store";
    import AffineEditor from "$lib/components/editor/affine-editor.svelte";

    // 组件属性类型定义
    interface Props {
        eventTitle?: string;
        eventLocation?: string;
        eventDate?: string;
        eventStatus?: string;
        creator?: {
            name: string;
            avatar: string;
        };
    }

    // 组件属性
    let {
        eventTitle = "",
        eventLocation = "",
        eventDate = "",
        eventStatus = "未开始",
        creator = {
            name: "范一",
            avatar: "https://github.com/shadcn.png",
        },
    }: Props = $props();

    let titleInput: HTMLInputElement;

    onMount(() => {
        // 自动聚焦到标题输入框
        if (titleInput && !eventTitle) {
            titleInput.focus();
            titleInput.setSelectionRange(
                titleInput.value.length,
                titleInput.value.length,
            );
        }
    });

    // 自动聚焦函数
    const autofocus = (node: HTMLInputElement) => {
        titleInput = node;
        return {
            destroy: () => {},
        };
    };
</script>

<ScrollArea class="h-[calc(100vh-4rem)]">
    <div class="space-y-6">
        <!-- 标题区域 -->
        

        <!-- 属性区域 -->
        <div class="px-6 space-y-4">
            <div class="px-6 pt-6 space-y-2">
                <Input
                    type="text"
                    placeholder="无标题"
                    class="text-4xl font-bold bg-transparent border-none outline-none w-full placeholder:text-muted-foreground/50 focus:ring-0"
                    bind:value={eventTitle}
                />
                <Separator class="my-4" />
            </div>
            <div class="flex gap-2">
                <span class="text-sm text-muted-foreground">创作者</span>
                <Avatar class="h-6 w-6">
                    <AvatarImage src={creator.avatar} alt={creator.name} />
                    <AvatarFallback>{creator.name[0]}</AvatarFallback>
                </Avatar>
                <span class="text-sm text-muted-foreground">{creator.name}</span
                >
            </div>
            <div class="flex gap-4">
                <!-- 状态标签 -->
                <div
                    class="flex flex-col group hover:bg-gray-100 dark:hover:bg-gray-800 rounded p-1.5 cursor-pointer"
                >
                    <span class="text-sm text-muted-foreground mb-1">状态</span>
                    <Badge variant="outline" class="text-xs">
                        <span class="mr-1.5 size-2 rounded-full bg-gray-400"
                        ></span>
                        {eventStatus}
                    </Badge>
                </div>

                <!-- 位置输入 -->
                <div
                    class="flex flex-col group hover:bg-gray-100 dark:hover:bg-gray-800 rounded p-1.5 cursor-pointer"
                >
                    <span class="text-sm text-muted-foreground mb-1">位置</span>
                    <Input
                        type="text"
                        placeholder="添加位置"
                        class="text-sm bg-transparent border-none outline-none placeholder:text-muted-foreground/50 focus:ring-0 w-24"
                        bind:value={eventLocation}
                    />
                </div>

                <!-- 日期选择器 -->
                <div
                    class="flex flex-col group hover:bg-gray-100 dark:hover:bg-gray-800 rounded p-1.5 cursor-pointer"
                >
                    <span class="text-sm text-muted-foreground mb-1">日期</span>
                    <Input
                        type="date"
                        class="text-sm bg-transparent border-none outline-none focus:ring-0"
                        bind:value={eventDate}
                    />
                </div>
            </div>
        </div>

        <!-- 描述区域 -->
        <div class="px-6">
            <AffineEditor docId="event-doc" />
        </div>
    </div>
</ScrollArea>
