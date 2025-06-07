<script lang="ts">
  import type { LayoutData } from "./$types";
  import type { Snippet } from "svelte";
  import { Shell } from "$lib/components/layout";
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import { Button } from "$lib/components/ui/button";
  import { SettingDialog } from "./settings/index.js";

  import { Settings } from "lucide-svelte";
  import { effects as blocksEffects } from "@blocksuite/blocks/effects";
  import { effects as presetsEffects } from "@blocksuite/presets/effects";

  // 使用一个标志来追踪是否已经初始化
  let isEffectsInitialized = false;

  onMount(() => {
    if (!isEffectsInitialized) {
      try {
        blocksEffects();
        presetsEffects();
        isEffectsInitialized = true;
      } catch (error) {
        console.warn('Effects already initialized:', error);
      }
    }
  });

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
