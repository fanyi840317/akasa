<script lang="ts">
	import '../app.css';
	import { ModeWatcher } from "mode-watcher";
	import '../lib/i18n'; // 确保在应用启动时加载 i18n 配置
	import { waitLocale } from 'svelte-i18n';
	let { children } = $props();
</script>
<ModeWatcher />

{#await waitLocale()}
	<div>Loading...</div>
{:then}
{@render children()}
{/await}
