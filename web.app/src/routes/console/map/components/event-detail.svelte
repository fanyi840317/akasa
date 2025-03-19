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
    import { onMount, onDestroy, setContext } from "svelte";
    import { browser } from "$app/environment";
    import { writable } from "svelte/store";
    import AffineEditor from "$lib/components/editor/affine-editor.svelte";
    import { initEditor } from "$lib/components/editor/affine-editor";
    import type { AppState } from "$lib/components/editor/affine-editor";
    import { User, MapPin, Clock, Calendar as CalendarIcon } from "lucide-svelte";
    import { Button } from "$lib/components/ui/button";
    import * as Popover from "$lib/components/ui/popover";
    import { cn } from "$lib/utils";
    import { DateFormatter, type DateValue, getLocalTimeZone } from "@internationalized/date";
    import { RangeCalendar } from "$lib/components/ui/range-calendar";

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
    let editorContainer: HTMLElement;
    let dateValue: DateValue | undefined = undefined;

    // 日期格式化器
    const df = new DateFormatter("zh-CN", {
        dateStyle: "long"
    });

    onMount(async () => {
        // 自动聚焦到标题输入框
        if (titleInput && !eventTitle) {
            titleInput.focus();
            titleInput.setSelectionRange(
                titleInput.value.length,
                titleInput.value.length,
            );
        }
        
        // 延迟一点时间后让编辑器获得焦点
        setTimeout(() => {
            if (editorContainer) {
                const editor = editorContainer.querySelector('[contenteditable="true"]');
                if (editor) {
                    (editor as HTMLElement).focus();
                }
            }
        }, 500);
    });

    // 自动聚焦函数
    const autofocus = (node: HTMLInputElement) => {
        titleInput = node;
        return {
            destroy: () => {},
        };
    };
    
    // 处理日期变化
    function handleDateChange(date: DateValue) {
        dateValue = date;
        if (date) {
            const jsDate = date.toDate(getLocalTimeZone());
            eventDate = jsDate.toISOString().split('T')[0]; // 转换为YYYY-MM-DD格式
        } else {
            eventDate = "";
        }
    }
</script>

<ScrollArea class="h-[calc(100vh-4rem)] py-4">
    <div class="space-y-6 flex flex-col h-full">

        <div class="px-6 space-y-4">
            
        <!-- 标题区域 -->
            <div class=" pt-6 space-y-2">
                <input
                    type="text"
                    placeholder="无标题"
                    class="text-4xl font-bold bg-transparent border-none outline-none w-full placeholder:text-muted-foreground/50 "
                    bind:value={eventTitle}
                />
                <Separator class="my-4" />
            </div>
           
        <!-- 属性区域 -->
            <div class="flex flex-col gap-2 w-full">
                <!-- 创作者 -->
                <div class="flex items-center group w-full">
                    <div class="flex items-center gap-2 w-24">
                        <User class="h-4 w-4 text-muted-foreground" />
                        <span class="text-sm text-muted-foreground">创作者</span>
                    </div>
                    <div class="flex items-center gap-2 flex-1">
                        <Avatar class="h-6 w-6">
                            <AvatarImage src={creator.avatar} alt={creator.name} />
                            <AvatarFallback>{creator.name[0]}</AvatarFallback>
                        </Avatar>
                        <span class="text-sm">{creator.name}</span>
                    </div>
                </div>
                
                <!-- 位置输入 -->
                <div class="flex items-center group w-full">
                    <div class="flex items-center gap-2 w-24">
                        <MapPin class="h-4 w-4 text-muted-foreground" />
                        <span class="text-sm text-muted-foreground">位置</span>
                    </div>
                    <div class="flex-1">
                        <Button
                            variant="outline"
                            class="w-full justify-start text-left font-normal h-9 px-3 py-1"
                            size="sm"
                        >
                            <MapPin class="h-4 w-4 mr-2" />
                            {eventLocation || "添加位置"}
                        </Button>
                    </div>
                </div>

                <!-- 日期选择器 -->
                <div class="flex items-center group w-full">
                    <div class="flex items-center gap-2 w-24">
                        <Clock class="h-4 w-4 text-muted-foreground" />
                        <span class="text-sm text-muted-foreground">日期</span>
                    </div>
                    <div class="flex-1">
                        <Popover.Root>
                            <Popover.Trigger>
                                <Button
                                    variant="outline"
                                    class={cn(
                                        "w-full justify-start text-left font-normal h-9 px-3 py-1",
                                        !dateValue && "text-muted-foreground"
                                    )}
                                    size="sm"
                                >
                                    <CalendarIcon class="h-4 w-4 mr-2" />
                                    {dateValue ? df.format(dateValue.toDate(getLocalTimeZone())) : "选择日期"}
                                </Button>
                            </Popover.Trigger>
                            <Popover.Content class="w-auto p-0" align="start">
                                <RangeCalendar type="single" bind:value={dateValue} on:valueChange={(e) => handleDateChange(e.detail)} />
                            </Popover.Content>
                        </Popover.Root>
                    </div>
                </div>
            </div>
        </div>

        <!-- 描述区域 -->
        <div class="flex-1 flex flex-col">
            <div bind:this={editorContainer} class="flex-1">
                <AffineEditor docId="event-doc" class="flex-1" />
            </div>
        </div>
    </div>
</ScrollArea>
