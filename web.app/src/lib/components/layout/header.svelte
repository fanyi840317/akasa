<script lang="ts">
    import * as Sidebar from "$lib/components/ui/sidebar";
    import * as Breadcrumb from "$lib/components/ui/breadcrumb";
    import { Separator } from "$lib/components/ui/separator";
    import { cn } from "$lib/utils.js";

    /**
     * 控制台页面头部组件 - 提供标题、面包屑和页面布局容器
     * @param {any} ref - 组件引用
     * @param {{ name: string; path: string; }[]} titles - 页面标题数组
     */
    let {
        ref = $bindable(null),
        titles = [] as { name: string; path: string; }[],
        ...restProps
    } = $props<{
        ref?: any;
        titles?: { name: string; path: string; }[];
    }>();

    // 定义面包屑项的数组
    let breadcrumbItems = [
        { name: "首页", path: "/" },
        ...titles
    ];
</script>

<header class="flex h-16 shrink-0 items-center gap-2 justify-between">
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
        <slot name="actions" />
    </div>
</header>
