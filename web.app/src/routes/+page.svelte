<script lang="ts">
  import Header from '$lib/components/Header.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import Map from '$lib/components/Map.svelte';
</script>

<div class="layout">
  <Header />
  <main class="main">
    <Map />
  </main>
  <Footer />
</div>

<style>
  .layout {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }

  .main {
    flex: 1;
    position: relative;
  }

  :global(body) {
    margin: 0;
    padding: 0;
  }
</style>