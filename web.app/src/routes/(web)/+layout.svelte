<script lang="ts">
    import type { Snippet } from "svelte";
    import Header from "$lib/components/header.svelte";
    import Footer from "$lib/components/footer.svelte";
</script>

<div class="layout">
    <Header />
    <main class="flex-1 main">
        <slot></slot>
    </main>
    <Footer />
</div>
<style>
	.layout {
		display: flex;
		flex-direction: column;
		height: 100vh;
	}

	:global(body) {
		margin: 0;
		padding: 0;
	}
</style>