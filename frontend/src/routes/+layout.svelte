<script lang="ts">
  import Header from "$lib/components/layout/header.svelte";
  import "../app.css";
  import { onMount } from "svelte";
  import { auth } from "$lib/stores/auth";
  import { goto } from "$app/navigation";
  import { ModeWatcher, mode, setMode } from "mode-watcher";
  import { waitLocale } from "svelte-i18n";
  import { appStore } from "$lib/stores/app-state";
  import { Toaster } from "$lib/components/ui/sonner";

  let { children } = $props();
  let isMounted = $state(false);

  onMount(() => {
    // setMode("dark");
    isMounted = true;
    // goto("/web");
    // Initialize auth store
    // const unsubscribe = appStore.subscribe((state) => {
    //     showHeader = state.showHeader;
    //   });
    //   return () => {
    //     unsubscribe();
    //   };
  });
</script>

<Toaster ></Toaster>
<mode-watcher></mode-watcher>
{#await waitLocale()}
  <div class="min-h-screen flex items-center justify-center">
    <div class="loading loading-infinity loading-xl"></div>
  </div>
{:then}
  {#if isMounted}
    {@render children()}
  {/if}
{/await}
