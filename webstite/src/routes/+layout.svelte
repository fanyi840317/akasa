<script lang="ts">
	import Header from "$lib/components/layout/header.svelte";
	import "../app.css";
	import { onMount } from "svelte";
	import { auth } from "$lib/stores/auth";
	import { goto } from "$app/navigation";
	import { ModeWatcher, mode } from "mode-watcher";
	import { waitLocale } from "svelte-i18n";

	let { children } = $props();
	let isMounted = $state(false);
	let user = $state<any>(null);

	// Initialize auth store
	onMount(() => {
		isMounted = true;
		auth.init();

		// Subscribe to auth store
		const unsubscribe = auth.subscribe((state) => {
			user = state.user;
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

<Header
	class="z-50 header-main"
	{user}
	onLogin={handleLogin}
	onLogout={handleLogout}
	onProfile={handleProfile}
/>
{#await waitLocale()}
	<div class="min-h-screen flex items-center justify-center">
		<div class="loading loading-infinity loading-xl"></div>
	</div>
{:then}
	{#if isMounted}
		{@render children()}
	{/if}
{/await}

<style>
	:global(:root) {
		--header-height: 64px;
	}

	:global(.header-main) {
		height: var(--header-height);
		position: relative;
	}
</style>
