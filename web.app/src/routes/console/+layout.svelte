<script lang="ts">
    import type { LayoutData } from "./$types";
    import type { Snippet } from "svelte";
    import { NotionPanel, Shell } from "./components/index.js";
    import { setContext } from 'svelte';
    import { page } from "$app/stores";
    import { ScrollArea } from "$lib/components/ui/scroll-area";
    import { Button } from "$lib/components/ui/button";
    import { SettingDialog } from "./settings/index.js";

    import { Settings } from "lucide-svelte";
    import { effects as blocksEffects } from "@blocksuite/blocks/effects";
    import { effects as presetsEffects } from "@blocksuite/presets/effects";
    
    blocksEffects();
    presetsEffects();
 
    
    let {
        data,
        children,
    } = $props<{
        data: LayoutData;
        children: Snippet;
    }>();

    let showLeftView = $state(false);
    let showRightPanel = $state(false);
    let showRightView = $state(false);
    let selectedTemplate = $state<any>(null);

    // 根据 page.data.rightView 控制右侧视图
    $effect(() => {
        if ($page.data.rightView) {
            showRightView = true;
        } else if (selectedTemplate) {
            showRightView = true;
        } else {
            showRightView = false;
        }
    });

    setContext('shell', {
        showRightView:Boolean,
        setShowRightView: (value: boolean) => showRightView = value,
        setTemplate: (template: any) => {
            selectedTemplate = template;
            showRightView = true;
        }
    });
</script>

{#snippet leftView()}

{/snippet}

{#snippet rightView()}

{/snippet}

{#snippet headerActions()}

{/snippet}

{#snippet child()}
    {@render children()}
{/snippet}
<!-- {#if showDialog}
  <Dialog.Root bind:open={showDialog} on:openChange={(e) => appStore.setShowDialog(e.detail)}>
    {@render dialogView()}
  </Dialog.Root>
{/if} -->
<Shell 
    showLeftView={showLeftView}
    showRightView={showRightView}
    child={child}
    actions={headerActions}
    showHeader={$page.data.showHeader}
    titles={[{ name: $page.data.title , path:$page.data?.path }]}
    user={$page.data.user}
/>


<!-- 事件详情面板 -->
<!-- <NotionPanel 
    open={showRightPanel} 
    title={event.title}
    width={40}
    maxWidth={60}
    showHeader={true}
    showFooter={false}
    contentView={panelContent}
    properties={[
        { label: "位置", value: selectedEvent?.location },
        { label: "日期", value: selectedEvent?.date ? formatDate(selectedEvent.date) : '未设置' }
    ]}
    on:close={handleClosePanel}
/> -->
