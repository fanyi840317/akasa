<script lang="ts">
    import type { PageData } from "./$types";
    import { base } from "$app/paths";

    let { data }: { data: PageData } = $props();
    import { Shell } from "$lib/components/console";
    import * as Sidebar from "$lib/components/ui/sidebar";
    import NavSidebar from "$lib/components/console/navigation/sidebar.svelte";
    import { Button } from "$lib/components/ui/button";
    import { PlusCircle, PanelLeft } from "lucide-svelte";
    import { fly } from "svelte/transition";
    import * as Resizable from "$lib/components/ui/resizable";
    import { Pane, Splitpanes } from "svelte-splitpanes";
    

    // 控制左侧内容区域显示的状态
    let showLeftContent = $state(true);
    let showRightSidebar = $state(true);
    // 切换左侧内容区域的函数
    function toggleLeftContent() {
        showLeftContent = !showLeftContent;
    }
</script>

{#snippet actions()}
    <div class="flex gap-2">
        <Button
            variant="secondary"
            size="sm"
            class="map-control-button"
            on:click={() => {
                showLeftContent = !showLeftContent;
            }}
        >
            <PlusCircle class="h-4 w-4 mr-2" />
            <span>{showLeftContent ? "隐藏" : "显示"}左侧内容</span>
        </Button>

        <Button
            variant="outline"
            data-sidebar="trigger"
            size="sm"
            on:click={() => {
                showRightSidebar = !showRightSidebar;
            }}
        >
            <PanelLeft class="h-4 w-4 mr-2" />
            <span>{showRightSidebar ? "隐藏" : "显示"}右侧内容</span>
        </Button>
    </div>
{/snippet}

{#snippet child()}
    <div class="p-4">
        <h2 class="text-2xl font-bold mb-4">控制台</h2>
        <p>这里是主内容区域</p>
    </div>
{/snippet}

{#snippet leftView()}
    <div class="p-4">
        <h3 class="text-lg font-semibold mb-4">左侧内容</h3>
        <div>这里是左侧视图内容</div>
    </div>
{/snippet}

{#snippet rightView()}
    <div class="p-4 w-[600px]" in:fly={{ x: 200, duration: 500 }}>
        <h3 class="text-lg font-semibold mb-4">右侧内容</h3>
        <div>这里是右侧视图内容</div>
    </div>
{/snippet}

<style>
  :global(.splitpanes__splitter) {
    background-color: transparent !important;
    position: relative;
    margin: 0 -8px;
    width: 16px !important;
    border: none !important;
  }

  :global(.splitpanes__splitter:hover) {
    background-color: hsl(var(--muted)) !important;
  }

  :global(.splitpanes__splitter:active) {
    background-color: hsl(var(--accent)) !important;
  }

  :global(.splitpanes__splitter::before) {
    content: '';
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    height: 32px;
    width: 2px;
    background-color: hsl(var(--muted-foreground) / 0.3);
  }

  :global(.splitpanes__splitter::after) {
    display: none !important;
  }

  :global(.splitpanes--vertical > .splitpanes__splitter) {
    border-left: none !important;
  }

  :global(.splitpanes__splitter:hover::before) {
    background-color: hsl(var(--muted-foreground) / 0.5);
  }
</style>

<Splitpanes class="w-screen h-screen fixed top-0 left-0 z-50 overflow-hidden !bg-transparent">
    <Pane minSize={40} size={100} class="!bg-transparent">
        <iframe 
        src="{base}/console/home" 
        class="w-full h-full border-none"
    />
    </Pane>
    {#if showRightSidebar && rightView}
      <Pane size={0} class="!bg-transparent">
        {@render rightView()}
      </Pane>
    {/if}
</Splitpanes>


<!-- <Sidebar.Provider open={showRightSidebar}>
    <NavSidebar />
    <main>
      <Sidebar.Trigger />
      <div>
        {@render actions()}
      </div>
    </main>
  </Sidebar.Provider> -->
<!--   
  <Shell 
    {actions} 
    {child} 
    {leftView}
    {rightView}
    showLeftView={showLeftContent}
    showRightView={showRightSidebar}
    titles={[{ name: "控制台", path: "/console" }]}
/> -->
