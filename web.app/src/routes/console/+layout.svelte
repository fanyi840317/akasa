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
    let c1 = $state<"none" | "icon" | "offcanvas">("icon");
    let c2 = $state<"none" | "icon" | "offcanvas">("icon");
    let c3 = $state<"none" | "icon" | "offcanvas">("none");

    function c1Click() {
        c2 = "icon";
        // sidebar.toggle();
    }
</script>

{@render children()}


