<script lang="ts">
    import * as Sidebar from "$lib/components/ui/sidebar";
    import * as Breadcrumb from "$lib/components/ui/breadcrumb";
    import { Separator } from "$lib/components/ui/separator";
    import { cn } from "$lib/utils.js";
    import type { Snippet } from "svelte";

    /**
     * 控制台页面头部组件 - 提供标题、面包屑和页面布局容器
     * @param {any} ref - 组件引用
     * @param {string} title - 页面标题
     */
    let {
        ref = $bindable(null),
        title,
        children = undefined,
        actions = undefined,
        ...restProps
    } = $props<{
        ref?: any;
        title: string;
        children?: Snippet;
        actions?: Snippet;
    }>();
</script>

<header class="flex h-16 shrink-0 items-center gap-2 justify-between">
    <div class="flex items-center gap-2 px-4">
        <Sidebar.Trigger class="-ml-1" />
        <Separator orientation="vertical" class="mr-2 h-4" />
        <Breadcrumb.Root>
            <Breadcrumb.List>
                <Breadcrumb.Item>
                    <Breadcrumb.Page>{title}</Breadcrumb.Page>
                </Breadcrumb.Item>
            </Breadcrumb.List>
        </Breadcrumb.Root>
    </div>
    <div class="pr-4">
        <!-- 可扩展的右侧工具栏区域 -->
        {@render actions?.()}
    </div>
</header>
<div class="flex flex-1 w-full h-full p-0">
    {@render children?.()}
</div>
