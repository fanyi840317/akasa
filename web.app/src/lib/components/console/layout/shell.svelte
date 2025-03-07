<script lang="ts">
  import { onMount } from "svelte";
  import type { Snippet } from "svelte";
  import * as Sidebar from "$lib/components/ui/sidebar";
  import NavSidebar from "$lib/components/console/navigation/sidebar.svelte";
  import Header from "$lib/components/console/layout/header.svelte";
  import { Splitpanes, Pane } from 'svelte-splitpanes';

  /**
   * 控制台主外壳组件 - 提供整体布局骨架
   * @param {Snippet} child - 子内容片段
   * @param {Snippet} actions - 右侧操作区域
   * @param {{ name: string; path: string; }[]} titles - 页面标题数组
   */
  let { 
    child, 
    titles = [] as { name: string; path: string; }[],
    actions = undefined,
  } = $props<{
    child: Snippet;
    titles?: { name: string; path: string; }[];
    actions?: Snippet;
  }>();

  onMount(() => {
    // 组件挂载完成后的初始化逻辑
  });
</script>

<Sidebar.Provider>
  <NavSidebar collapsible="icon" side="left" />
  <Sidebar.Inset>
    <!-- <Header {titles} {actions} /> -->
    {@render child()}
  </Sidebar.Inset>
</Sidebar.Provider>
