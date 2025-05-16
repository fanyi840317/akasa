<script lang="ts">
  import BlockSuiteEditor from "$lib/components/editor/BlockSuiteEditor.svelte";
  import { appStore } from "$lib/stores/app-state";
  import { onDestroy, onMount } from "svelte";

  // Ensure BlockSuite effects are initialized. 
  // This might be better handled globally or within the BlockSuiteEditor component itself
  // if it's the sole entry point for BlockSuite usage.
  import { effects as blocksEffects } from "@blocksuite/blocks/effects";
  import { effects as presetsEffects } from "@blocksuite/presets/effects";
  blocksEffects();
  presetsEffects();

  onMount(() => {
    appStore.setShowHeader(false);
  });

  onDestroy(() => {
    appStore.setShowHeader(true);
  });
</script>

<div class="w-full h-screen">
  <BlockSuiteEditor />
</div>
