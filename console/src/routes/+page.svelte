<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/stores/auth.svelte.js';
	import { browser } from '$app/environment';

	onMount(async () => {
		if (browser) {
			// Wait for auth check to complete
			while (authStore.loading) {
				await new Promise(resolve => setTimeout(resolve, 100));
			}
			
			// Redirect based on authentication status
			if (authStore.isAuthenticated) {
				goto('/console');
			} else {
				goto('/auth/login');
			}
		}
	});
</script>

<svelte:head>
	<title>Akasa Console</title>
</svelte:head>

<div class="flex min-h-screen items-center justify-center bg-background">
	<div class="text-center">
		<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
		<h2 class="text-lg font-semibold mb-2">Loading...</h2>
		<p class="text-muted-foreground">Checking authentication status...</p>
	</div>
</div>