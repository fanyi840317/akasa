<script lang="ts">
  import Header from "$lib/components/layout/header.svelte";
  import "../app.css";
  import { onMount } from "svelte";
  import { auth } from "$lib/stores/auth";
  import { goto } from "$app/navigation";
  import { ModeWatcher, mode, setMode } from "mode-watcher";
  import { waitLocale } from "svelte-i18n";
  import { appStore } from "$lib/stores/app-state";

  let { children } = $props();
  let isMounted = $state(false);
  let user = $state<any>(null);
  let showHeader = $state(false);
 

  onMount(() => {
    // setMode("dark");
    isMounted = true;    
    // Initialize auth store
    const unsubscribe = appStore.subscribe((state) => {
      showHeader = state.showHeader;
    });
    return () => {
      unsubscribe();
    };
  });

  // Handle login, logout and profile navigation
  function handleLogin() {
    goto("/login");
  }

  function handleLogout() {
    auth.logout();
  }

  function handleProfile() {

    
    goto("/profile");
  }
</script>

<mode-watcher></mode-watcher>
{#await waitLocale()}
  <div class="min-h-screen flex items-center justify-center">
    <div class="loading loading-infinity loading-xl"></div>
  </div>
{:then}
  <Header
    {user}
    onLogin={handleLogin}
    onLogout={handleLogout}
    onProfile={handleProfile}
    isShow={showHeader}
  />
  {#if isMounted}
    {@render children()}
  {/if}
{/await}
