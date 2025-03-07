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

<!-- {@render children()} -->

<!-- <Shell child={children} title="" ></Shell> -->
<Sidebar.Provider>
    <Sidebar.Root collapsible={c1} >
        <Sidebar.Header />
        <Sidebar.Content>
            <Sidebar.Group />
            <div>sssssssss</div>
            <Sidebar.Group />
        </Sidebar.Content>
        <Sidebar.Footer />
    </Sidebar.Root>
    <Sidebar.Root collapsible={c2} variant="inset">
        <Sidebar.Header />
        <Sidebar.Content>
            <Sidebar.Group />
            <div>sssssssss</div>
            <Sidebar.Group />
        </Sidebar.Content>
        <Sidebar.Footer />
    </Sidebar.Root>
    <Sidebar.Inset>
        <header
            class="bg-background sticky top-0 flex shrink-0 items-center gap-2 border-b p-4"
        >
            <Sidebar.Trigger class="-ml-1" />
            <Button on:click={c1Click}>open1</Button>
            <Button
                on:click={() => {
                    c2 = "offcanvas";
                }}>open2</Button
            >
            <Button
                on:click={() => {
                    c2 = "none";
                }}>open3</Button
            >
        </header>
        <div class="flex flex-1 flex-col gap-4 p-4">
            {#each Array.from({ length: 24 }) as _, index (index)}
                <div
                    class="bg-muted/50 aspect-video h-12 w-full rounded-lg"
                ></div>
            {/each}
        </div>
    </Sidebar.Inset>
    <Sidebar.Root collapsible={c3}>
        <Sidebar.Header />
        <Sidebar.Content>
            <Sidebar.Group />
            <div class="">sssssssss</div>
            <Sidebar.Group />
        </Sidebar.Content>
        <Sidebar.Footer />
    </Sidebar.Root>
</Sidebar.Provider>
