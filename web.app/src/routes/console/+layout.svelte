<script lang="ts">
    import type { LayoutData } from "./$types";
    import type { Snippet } from "svelte";
    import { Shell } from "$lib/components/console";
    import * as Sidebar from "$lib/components/ui/sidebar";
    import NavSidebar from "$lib/components/console/navigation/sidebar.svelte";
    import { Button } from "$lib/components/ui/button";
    import { useSidebar } from "$lib/components/ui/sidebar";

    const sidebar = useSidebar();

    /**
     * 控制台布局组件
     * 提供整个控制台应用的基础布局结构
     */
    let { data, children }: { data: LayoutData; children: Snippet } = $props();

</script>

{@render children()}


