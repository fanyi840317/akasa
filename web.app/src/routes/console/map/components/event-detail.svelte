<script lang="ts">
    import { Separator } from "$lib/components/ui/separator";
    import ShadEditor from "$lib/components/shad-editor/shad-editor.svelte";
    import type { Content } from '@tiptap/core';
    import type { Editor } from '@tiptap/core';

    // 组件属性
    export let eventTitle = "";
    export let eventDescription: Content = {
        type: 'doc',
        content: [
            {
                type: 'paragraph',
                content: []
            }
        ]
    };
    export let eventLocation = "";
    export let eventDate = "";
    export let eventStatus = "未开始";

    let editor: Editor;
</script>

<div class="space-y-6">
    <!-- 标题区域 -->
    <div class="px-6 pt-6 space-y-2">
        <input
            type="text"
            placeholder="无标题"
            class="text-2xl font-bold bg-transparent border-none outline-none w-full placeholder:text-muted-foreground/50 focus:ring-0"
            bind:value={eventTitle}
        />
        <Separator class="my-4" />
    </div>

    <!-- 属性区域 -->
    <div class="px-6 space-y-4">
        <div class="flex gap-2">
            <!-- 状态选择器 -->
            <div class="flex items-center group hover:bg-gray-100 dark:hover:bg-gray-800 rounded p-1.5 cursor-pointer">
                <div class="flex items-center gap-2">
                    <span class="text-sm text-muted-foreground">状态</span>
                    <div class="px-2 py-1 rounded bg-gray-100 dark:bg-gray-800 text-xs flex items-center gap-1.5">
                        <span class="w-2 h-2 rounded-full bg-gray-400"></span>
                        <span>{eventStatus}</span>
                    </div>
                </div>
            </div>

            <!-- 位置输入 -->
            <div class="flex items-center group hover:bg-gray-100 dark:hover:bg-gray-800 rounded p-1.5 cursor-pointer">
                <div class="flex items-center gap-2">
                    <span class="text-sm text-muted-foreground">位置</span>
                    <input
                        type="text"
                        placeholder="添加位置"
                        class="text-sm bg-transparent border-none outline-none placeholder:text-muted-foreground/50 focus:ring-0 w-24"
                        bind:value={eventLocation}
                    />
                </div>
            </div>

            <!-- 日期选择器 -->
            <div class="flex items-center group hover:bg-gray-100 dark:hover:bg-gray-800 rounded p-1.5 cursor-pointer">
                <div class="flex items-center gap-2">
                    <span class="text-sm text-muted-foreground">日期</span>
                    <input
                        type="date"
                        class="text-sm bg-transparent border-none outline-none focus:ring-0"
                        bind:value={eventDate}
                    />
                </div>
            </div>
        </div>
    </div>

    <!-- 描述区域 -->
    <div>
        <ShadEditor
            bind:content={eventDescription}
            bind:editor={editor}
            class="min-h-24 border-none "
            showToolbar={false}
            showAllMenus={true}
            editable={true}
        />
    </div>
    <!-- 按钮区域 -->
</div>