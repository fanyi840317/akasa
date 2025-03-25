<script lang="ts">
  import type { LayoutData } from "./$types";
  import type { Snippet } from "svelte";
  import { Shell, NotionPanel } from "$lib/components/layout";
  import { setContext } from "svelte";
  import { page } from "$app/stores";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import { Button } from "$lib/components/ui/button";
  import { SettingDialog } from "./settings/index.js";

  import { Settings } from "lucide-svelte";
  import { effects as blocksEffects } from "@blocksuite/blocks/effects";
  import { effects as presetsEffects } from "@blocksuite/presets/effects";

  blocksEffects();
  presetsEffects();

//   customElements.define('affine-paragraph', ParagraphBlockComponent);
  let { data, children } = $props<{
    data: LayoutData;
    children: Snippet;
  }>();
</script>

<Shell
  child={children}
  showHeader={$page.data.showHeader}
  titles={[{ name: $page.data.title, path: $page.data?.path }]}
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
