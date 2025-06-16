<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/stores/auth.svelte.js';

	// If user is already authenticated, redirect to console
	onMount(() => {
		if (authStore.isAuthenticated) {
			goto('/console');
		}
	});
</script>

<main class="min-h-screen bg-background">
	<slot />
</main>