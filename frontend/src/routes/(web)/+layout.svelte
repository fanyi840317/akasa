<script lang="ts">
  import Header from "$lib/components/layout/header.svelte";
  import { onMount } from "svelte";
  import { auth } from "$lib/stores/auth";
  import { goto } from "$app/navigation";
  import { ModeWatcher, mode, setMode } from "mode-watcher";
  import { waitLocale } from "svelte-i18n";
  import { appStore } from "$lib/stores/app-state";

  let { children } = $props();
  let isMounted = $state(false);
  let user = $state<any>(null);
  let showHeader = $state(true);

  onMount(() => {
    // setMode("dark");
    isMounted = true;
    // Initialize auth store
    const unsubscribe = appStore.subscribe((state) => {
      showHeader = state.showHeader;
    });
    const unsubscribeAuth = auth.subscribe((state) => {
      user = state.user;
    });
    return () => {
      unsubscribe();
      unsubscribeAuth();
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

  // Handle login, logout and profile navigation
</script>

<Header
  {user}
  onLogin={handleLogin}
  onLogout={handleLogout}
  onProfile={handleProfile}
  isShow={showHeader}
/>
{@render children()}
