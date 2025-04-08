<script lang="ts">
    import * as Sidebar from "$lib/components/ui/sidebar";
    import * as Breadcrumb from "$lib/components/ui/breadcrumb";
    import { Separator } from "$lib/components/ui/separator";
    import { cn } from "$lib/utils.js";
    import type { HTMLAnchorAttributes } from "svelte/elements";
    import type { WithElementRef } from "bits-ui";
    import type { Snippet } from "svelte";

    /**
     * 控制台页面头部组件 - 提供标题、面包屑和页面布局容器
     * @param {any} ref - 组件引用
     * @param {{ name: string; path: string; }[]} titles - 页面标题数组
     * @param {Snippet} actions - 右侧操作区域
     */
    let {
        ref = $bindable(null),
        titles = [] as { name: string; path: string; }[],
        actions = undefined,
        ...restProps
    }: WithElementRef<HTMLAnchorAttributes>&{
        titles?: { name: string; path: string; }[];
        actions?: Snippet;
    } = $props();

    // 定义面包屑项的数组
    let breadcrumbItems = [
        { name: "首页", path: "/" },
        ...titles
    ];
    let hasActions = actions !== undefined;
</script>

<header class="flex h-16 shrink-0 items-center gap-2" class:justify-between={hasActions} class:justify-start={!hasActions}
class:z-10={!hasActions} >
    <div class="flex items-center gap-2 px-4">
        <Sidebar.Trigger class="-ml-1" />
        <Separator orientation="vertical" class="mr-2 h-4" />
        <Breadcrumb.Root>
            <Breadcrumb.List>
                {#each breadcrumbItems as item, index}
                    <Breadcrumb.Item>
                        <a href={item.path}>{item.name}</a>
                    </Breadcrumb.Item>
                    {#if index < breadcrumbItems.length - 1}
                        <Breadcrumb.Separator />
                    {/if}
                {/each}
            </Breadcrumb.List>
        </Breadcrumb.Root>
    </div>
    <div class="pr-4">
        {#if actions}
            {@render actions()}
        {/if}
    </div>
</header>
