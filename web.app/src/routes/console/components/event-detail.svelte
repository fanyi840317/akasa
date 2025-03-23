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
    import type { AppState } from "$lib/components/editor/affine-editor";
    import { eventStore } from "$lib/stores/event";
    import { auth } from "$lib/stores/auth";
    import {
        User,
        MapPin,
        Clock,
        Calendar as CalendarIcon,
        ChevronsUpDown,
        Save,
        Send,
    } from "lucide-svelte";
    import { Button } from "$lib/components/ui/button";
    import * as Popover from "$lib/components/ui/popover";
    import * as Collapsible from "$lib/components/ui/collapsible";
    import { cn } from "$lib/utils";
    import {
        DateFormatter,
        type DateValue,
        getLocalTimeZone,
    } from "@internationalized/date";
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
    let dateValue: DateValue | undefined = undefined;

    // 日期格式化器
    const df = new DateFormatter("zh-CN", {
        dateStyle: "long",
    });

    onMount(async () => {
        // 自动聚焦到标题输入框
     

        // 延迟一点时间后让编辑器获得焦点
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
            eventDate = jsDate.toISOString().split("T")[0]; // 转换为YYYY-MM-DD格式
        } else {
            eventDate = "";
        }
    }

    // 发布事件到Appwrite
    let isPublishing = false;
    let editorContent = "";
    
    // 获取编辑器内容的函数
    function getEditorContent() {
        // 这里应该实现从AffineEditor获取内容的逻辑
        // 由于当前实现可能不支持直接获取，我们先使用空字符串
        return editorContent;
    }
    
    async function publishToAppwrite() {
        if (!eventTitle) {
            alert("请先填写事件标题");
            return;
        }

        isPublishing = true;
        try {
            // 获取当前用户信息
            const user = $auth.user;
            if (!user) {
                throw new Error("用户未登录");
            }
            
            // 准备事件数据
            const eventData = {
                title: eventTitle,
                location: eventLocation,
                date: eventDate,
                status: eventStatus || "未开始",
                content: getEditorContent(),
                user_id: user.$id,
                creator_name: creator.name || user.name,
                creator_avatar: creator.avatar || ""
            };
            
            // 使用eventStore创建事件
            const result = await eventStore.createEvent(eventData);
            
            alert("事件已成功发布！");
        } catch (error) {
            console.error("发布事件失败:", error);
            alert("发布失败，请稍后重试: " + (error instanceof Error ? error.message : String(error)));
        } finally {
            isPublishing = false;
        }
    }
</script>

<div class="flex flex-col h-full w-full relative">
    <ScrollArea class="flex flex-1 w-full py-10">
        <div class="px-24 space-y-4">
            <!-- 标题区域 -->
            <div>
                <Button
                    variant="outline"
                    class={cn(
                        " text-left  font-normal h-7 px-2 py-1",
                        !eventLocation && "text-muted-foreground/70",
                    )}
                    size="sm"
                >
                    <MapPin class="h-3 w-3" />
                    {eventLocation || "添加位置"}
                </Button>
                <Popover.Root>
                    <Popover.Trigger>
                        <Button
                            variant="outline"
                            class={cn(
                                " justify-start text-left  font-normal h-7 px-2 py-1",
                                !dateValue && "text-muted-foreground/70",
                            )}
                            size="sm"
                        >
                            <CalendarIcon class="h-3 w-3" />
                            {dateValue
                                ? df.format(dateValue.toDate(getLocalTimeZone()))
                                : "选择发生日期"}
                        </Button>
                    </Popover.Trigger>
                    <Popover.Content class="w-auto p-0" align="start">
                        <RangeCalendar
                            type="single"
                            bind:value={dateValue}
                            on:valueChange={(e) => handleDateChange(e.detail)}
                        />
                    </Popover.Content>
                </Popover.Root>

                <Button
                    variant="outline"
                    class={cn(
                        " text-left  font-normal h-7 px-2 py-1",
                        !eventLocation && "text-muted-foreground/70",
                    )}
                    size="sm"
                >
                    <MapPin class="h-3 w-3" />
                    {eventLocation || "添加位置"}
                </Button>
            </div>

            <div class="space-y-2">
                <input
                    type="text"
                    placeholder="无标题"
                    class="text-4xl font-bold bg-transparent border-none outline-none w-full placeholder:text-muted-foreground/50"
                    bind:value={eventTitle}
                />
            </div>
        </div>
        <!-- 描述区域 -->
        <div class="flex-1 flex flex-col">
            <AffineEditor docId="event-doc" class="flex-1" />
        </div>
    </ScrollArea>
    
    <!-- 底部按钮区域 -->
    <div class="absolute bottom-0 left-0 w-full bg-background/80 backdrop-blur-smp-4">
        <div class="flex justify-between items-center px-24">
            <div>
                <Button 
                    onclick={publishToAppwrite} 
                    disabled={isPublishing} 
                    variant="outline" 
                    class="gap-2"
                >
                    <Send class="h-4 w-4" />
                    {isPublishing ? '发布中...' : '发布'}
                </Button>
            </div>
            <div>
                <!-- 右侧可以添加其他按钮 -->
            </div>
        </div>
    </div>
</div>

