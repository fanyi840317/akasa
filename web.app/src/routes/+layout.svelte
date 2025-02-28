<script lang="ts">
	import '../app.css';
	import { ModeWatcher } from "mode-watcher";
	import '../lib/i18n'; // 确保在应用启动时加载 i18n 配置
	import { waitLocale } from 'svelte-i18n';
	import Loading from '$lib/components/Loading.svelte';
	let { children } = $props();
	import Header from '$lib/components/Header.svelte';
	import Footer from '$lib/components/Footer.svelte';
	import { Toaster } from "$lib/components/ui/sonner";
	import { auth } from '$lib/stores/auth';
	import { onMount } from 'svelte';
</script>
<ModeWatcher />
<Toaster />
{#await waitLocale()}
	<div class="min-h-screen flex items-center justify-center">
		<Loading size="lg" />
	</div>
{:then}
<div class="layout">
	<Header />
	<main class="flex-1 main">
	   
	{@render children()}
	</main>
	<Footer />
  </div>
{/await}

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