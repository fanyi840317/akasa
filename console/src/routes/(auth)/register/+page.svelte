<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { authStore } from '$lib/stores/auth.svelte.js';
	import { toast } from 'svelte-sonner';

	let name = $state('');
	let email = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let isLoading = $state(false);

	onMount(() => {
		// If already authenticated, redirect to console
		if (authStore.isAuthenticated) {
			goto('/console');
		}
	});

	async function handleRegister(e: Event) {
		e.preventDefault();
		
		if (!name || !email || !password || !confirmPassword) {
			toast.error('Please fill in all fields');
			return;
		}

		if (password !== confirmPassword) {
			toast.error('Passwords do not match');
			return;
		}

		if (password.length < 8) {
			toast.error('Password must be at least 8 characters long');
			return;
		}

		isLoading = true;
		const result = await authStore.register(email, password, name);
		isLoading = false;

		if (result.success) {
			toast.success('Registration successful!');
			goto('/console');
		} else {
			toast.error(result.error || 'Registration failed');
		}
	}

	async function handleGoogleLogin() {
		await authStore.loginWithGoogle();
	}

	async function handleAppleLogin() {
		await authStore.loginWithApple();
	}
</script>

<svelte:head>
	<title>Register - Akasa Console</title>
</svelte:head>

<div class="flex min-h-screen items-center justify-center bg-background p-4">
	<div class="w-full max-w-md">
		<Card.Root>
			<Card.Header class="text-center">
				<Card.Title class="text-xl">Create an account</Card.Title>
				<Card.Description>Sign up with your Apple or Google account</Card.Description>
			</Card.Header>
			<Card.Content>
				<form onsubmit={handleRegister}>
					<div class="grid gap-6">
						<div class="flex flex-col gap-4">
							<Button 
								variant="outline" 
								class="w-full" 
								type="button"
								onclick={handleAppleLogin}
							>
								<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="mr-2 h-4 w-4">
									<path
										d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"
										fill="currentColor"
									/>
								</svg>
								Sign up with Apple
							</Button>
							<Button 
								variant="outline" 
								class="w-full" 
								type="button"
								onclick={handleGoogleLogin}
							>
								<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="mr-2 h-4 w-4">
									<path
										d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"
										fill="currentColor"
									/>
								</svg>
								Sign up with Google
							</Button>
						</div>
						<div
							class="after:border-border relative text-center text-sm after:absolute after:inset-0 after:top-1/2 after:z-0 after:flex after:items-center after:border-t"
						>
							<span class="bg-card text-muted-foreground relative z-10 px-2">
								Or continue with
							</span>
						</div>
						<div class="grid gap-6">
							<div class="grid gap-3">
								<Label for="name">Full Name</Label>
								<Input
									id="name"
									type="text"
									placeholder="John Doe"
									bind:value={name}
									required
								/>
							</div>
							<div class="grid gap-3">
								<Label for="email">Email</Label>
								<Input
									id="email"
									type="email"
									placeholder="m@example.com"
									bind:value={email}
									required
								/>
							</div>
							<div class="grid gap-3">
								<Label for="password">Password</Label>
								<Input 
									id="password" 
									type="password" 
									placeholder="At least 8 characters"
									bind:value={password}
									required 
								/>
							</div>
							<div class="grid gap-3">
								<Label for="confirmPassword">Confirm Password</Label>
								<Input 
									id="confirmPassword" 
									type="password" 
									placeholder="Confirm your password"
									bind:value={confirmPassword}
									required 
								/>
							</div>
							<Button 
								type="submit" 
								class="w-full" 
								disabled={isLoading}
							>
								{isLoading ? 'Creating account...' : 'Create account'}
							</Button>
						</div>
						<div class="text-center text-sm">
							Already have an account?
							<a href="/login" class="underline underline-offset-4"> Sign in </a>
						</div>
					</div>
				</form>
			</Card.Content>
		</Card.Root>
		<div
			class="text-muted-foreground *:[a]:hover:text-primary *:[a]:underline *:[a]:underline-offset-4 text-balance text-center text-xs mt-4"
		>
			By clicking continue, you agree to our <a href="/terms">Terms of Service</a>
			and <a href="/privacy">Privacy Policy</a>.
		</div>
	</div>
</div>