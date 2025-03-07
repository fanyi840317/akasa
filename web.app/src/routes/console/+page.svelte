<script lang="ts">
    import type { PageData } from './$types';

    let { data }: { data: PageData } = $props();
    import {Shell} from "$lib/components/console";
    import * as Sidebar from "$lib/components/ui/sidebar";
    import NavSidebar from "$lib/components/console/navigation/sidebar.svelte";
    import { Button } from '$lib/components/ui/button';
    import { PlusCircle, PanelLeft } from 'lucide-svelte';
    
    // 控制左侧内容区域显示的状态
    let showLeftContent = true;
    
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
    >
        <PlusCircle class="h-4 w-4 mr-2" />
        <span>创建事件</span>
    </Button>
    
    <Button 
        variant="outline"
        size="sm"
        on:click={toggleLeftContent}
    >
        <PanelLeft class="h-4 w-4 mr-2" />
        <span>{showLeftContent ? '隐藏' : '显示'}左侧内容</span>
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
    <div class="p-4">
        <h3 class="text-lg font-semibold mb-4">右侧内容</h3>
        <div>这里是右侧视图内容</div>
    </div>
{/snippet}

<Shell 
    {actions} 
    {child} 
    {leftView}
    {rightView}
    showLeftContent={showLeftContent}
    showRightSidebar={true}
    leftContentMode="none"
    rightSidebarMode="offcanvas"
    titles={[{ name: "控制台", path: "/console" }]}
/>
