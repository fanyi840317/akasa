<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/stores/auth.svelte.js';
	import { toast } from 'svelte-sonner';

	onMount(async () => {
		// Check if user is authenticated after OAuth callback
		try {
			await authStore.checkAuth();
			if (authStore.isAuthenticated) {
				toast.success('Login successful!');
				goto('/console');
			} else {
				toast.error('Authentication failed');
				goto('/login');
			}
		} catch (error) {
			console.error('OAuth callback error:', error);
			toast.error('Authentication failed');
			goto('/login');
		}
	});
</script>

<svelte:head>
	<title>Authenticating - Akasa Console</title>
</svelte:head>

<div class="flex min-h-screen items-center justify-center bg-background">
	<div class="text-center">
		<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
		<h2 class="text-lg font-semibold mb-2">Authenticating...</h2>
		<p class="text-muted-foreground">Please wait while we complete your login.</p>
	</div>
</div>