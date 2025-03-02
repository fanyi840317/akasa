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
</script>
<ModeWatcher />
<Toaster />
{#await waitLocale()}
	<div class="min-h-screen flex items-center justify-center">
		<Loading size="lg" />
	</div>
{:then}

{@render children()}
{/await}
