<script lang="ts">
    import type { LayoutData } from "./$types";
    import type { Snippet } from "svelte";
    import { Shell as ConsoleShell } from "$lib/components/console";

    /**
     * 控制台布局组件
     * 提供整个控制台应用的基础布局结构
     */
    let {
        data,
        children,
    }: { data: LayoutData; children: Snippet; } = $props();
</script>

{#snippet child()}
   {@render children()}
{/snippet}

<ConsoleShell {child} title="Console"></ConsoleShell>
