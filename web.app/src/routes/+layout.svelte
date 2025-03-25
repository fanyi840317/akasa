<script lang="ts">
  import "../app.css";
  import { ModeWatcher, mode } from "mode-watcher";
  import "../lib/i18n"; // 确保在应用启动时加载 i18n 配置
  import { waitLocale } from "svelte-i18n";
  import Loading from "$lib/components/website/loading.svelte";
  let { children } = $props();
  import Header from "$lib/components/website/header.svelte";
  import Footer from "$lib/components/website/footer.svelte";
  import { Toaster } from "$lib/components/ui/sonner";
  import { onMount, setContext } from "svelte";
  import { base } from "$app/paths";
  import { goto } from "$app/navigation";
  import { fade } from "svelte/transition";
  import { get, writable } from "svelte/store";

  onMount(() => {
    const unsubscribe = mode.subscribe((currentMode) => {
      document.documentElement.dataset.theme = currentMode ?? "light";
    });
    return () => unsubscribe();
  });
</script>

<ModeWatcher />
<Toaster />
{#await waitLocale()}
  <div
    in:fade={{ duration: 200 }}
    class="min-h-screen flex items-center justify-center"
  >
    <Loading size="lg" />
  </div>
{:then}
  <div out:fade={{ duration: 300 }}>
    {@render children()}
  </div>
{/await}
