<script lang="ts">
  import BlockSuiteEditor from "$lib/components/editor/BlockSuiteEditor.svelte";
  import { page } from "$app/stores";
  import { appStore } from "$lib/stores/app-state";
  import { onDestroy, onMount } from "svelte";

  // Ensure BlockSuite effects are initialized.
  // This might be better handled globally or within the BlockSuiteEditor component itself
  // if it's the sole entry point for BlockSuite usage.
  import { effects as blocksEffects } from "@blocksuite/blocks/effects";
  import { effects as presetsEffects } from "@blocksuite/presets/effects";
  blocksEffects();
  presetsEffects();

  let eventId: string | undefined;
  let eventData: any = null; // Placeholder for loaded event data
  let loading = true;

  // Get event ID from route params
  $: eventId = $page.params.id;

  async function loadEventData(id: string) {
    loading = true;
    console.log(`Loading event data for ID: ${id}`);
    // Placeholder for actual data fetching logic using Context7 or other services
    // For now, simulate a delay and set some mock data
    await new Promise(resolve => setTimeout(resolve, 500)); 
    eventData = {
      id: id,
      title: `Event ${id}`,
      // Assuming BlockSuite document data/ID would be part of this object
      // For BlockSuiteEditor, you might pass a specific docId or the whole eventData
      docId: `event-doc-${id}` // Example: derive a docId for BlockSuite
    };
    loading = false;
  }

  $: {
    if (eventId) {
      loadEventData(eventId);
    }
  }

  onMount(() => {
    appStore.setShowHeader(false);
  });

  onDestroy(() => {
    appStore.setShowHeader(true);
  });
</script>

<div class="w-full h-screen">
  {#if loading}
    <div class="flex justify-center items-center h-full">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
  {:else if eventData}
    <!-- Pass the relevant document ID or data to BlockSuiteEditor -->
    <BlockSuiteEditor docId={eventData.docId} />
    <!-- Or you might pass the whole eventData if BlockSuiteEditor is designed to handle it -->
    <!-- <BlockSuiteEditor event={eventData} /> -->
  {:else}
    <div class="flex justify-center items-center h-full">
      <p>Event not found or failed to load.</p>
    </div>
  {/if}
</div>