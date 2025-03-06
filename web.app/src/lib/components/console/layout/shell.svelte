<script lang="ts">
  import { onMount } from "svelte";
  import type { Snippet } from "svelte";
  import * as Sidebar from "$lib/components/ui/sidebar";
  import NavSidebar from "$lib/components/console/navigation/sidebar.svelte";

  /**
   * 控制台主外壳组件 - 提供整体布局骨架
   * @param {Snippet} child - 子内容片段
   * @param {string} title - 页面标题
   */
  let { 
    child, 
    title 
  } = $props();

  onMount(() => {
    // 组件挂载完成后的初始化逻辑
  });
</script>

<Sidebar.Provider>
  <NavSidebar collapsible="icon" side="left" />
  <Sidebar.Inset>
    {@render child()}
  </Sidebar.Inset>
</Sidebar.Provider>
