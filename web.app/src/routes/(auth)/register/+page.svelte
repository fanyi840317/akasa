<script lang="ts">
	import { Button } from "$lib/components/ui/button";
	import { Input } from "$lib/components/ui/input";
	import { Label } from "$lib/components/ui/label";
	import * as Card from "$lib/components/ui/card";
	import { _ } from 'svelte-i18n';
	import { Github, Mail, Lock, User, Loader2 } from "lucide-svelte";
	import { goto } from '$app/navigation';
	import { toast } from 'svelte-sonner';
	import { base } from '$app/paths';
	import { auth } from '$lib/stores/auth';
	import { page } from '$app/stores';

	let username = '';
	let email = '';
	let password = '';
	let loading = false;

	// 获取returnUrl参数
	const returnUrl = $page.data.returnUrl;

	async function handleSubmit() {
		loading = true;

		try {
			await auth.register(email, password, username, returnUrl);
		} catch (e: any) {
			// 错误已在auth store中处理，这里不需要额外处理
		} finally {
			loading = false;
		}
	}

	async function handleGoogleLogin() {
		try {
			// await account.createOAuth2Session('google', 'http://localhost:5173', 'http://localhost:5173/auth/callback/google');
		} catch (e: any) {
			toast.error(e.message || $_('auth.google_login_failed'));
		}
	}

	async function handleGithubLogin() {
		try {
			// await account.createOAuth2Session('github', 'http://localhost:5173', 'http://localhost:5173/auth/callback/github');
		} catch (e: any) {
			toast.error(e.message || $_('auth.github_login_failed'));
		}
	}
</script>

<div class="h-[100%] flex items-center justify-center bg-background">
	<Card.Root class="w-full max-w-md p-6 space-y-6">
		<form on:submit|preventDefault={handleSubmit} class="space-y-4">
			<div class="text-center space-y-2">
				<h1 class="text-2xl font-semibold tracking-tight">{$_('auth.register')}</h1>
				<p class="text-sm text-muted-foreground">{$_('auth.create_account')}</p>
			</div>
			<div class="space-y-4">
				<div class="space-y-2">
					<Label for="username">{$_('auth.username')}</Label>
					<div class="relative">
						<User class="absolute left-3 top-2.5 h-5 w-5 text-muted-foreground" />
						<Input
							id="username"
							type="text"
							placeholder="tianming"
							bind:value={username}
							required
							class="pl-10"
						/>
					</div>
				</div>
				<div class="space-y-2">
					<Label for="email">{$_('auth.email')}</Label>
					<div class="relative">
						<Mail class="absolute left-3 top-2.5 h-5 w-5 text-muted-foreground" />
						<Input
							id="email"
							type="email"
							placeholder="tianming@akasa.org"
							bind:value={email}
							required
							class="pl-10"
						/>
					</div>
				</div>
				<div class="space-y-2">
					<Label for="password">{$_('auth.password')}</Label>
					<div class="relative">
						<Lock class="absolute left-3 top-2.5 h-5 w-5 text-muted-foreground" />
						<Input
							id="password"
							type="password"
							bind:value={password}
							required
							class="pl-10"
						/>
					</div>
				</div>
			</div>
			<Button type="submit" class="w-full" disabled={loading}>
				{#if loading}
					<Loader2 class="mr-2 h-4 w-4 animate-spin" />
					{$_('common.loading')}
				{:else}
					{$_('auth.register')}
				{/if}
			</Button>
			<div class="relative">
				<div class="absolute inset-0 flex items-center">
					<span class="w-full border-t" />
				</div>
				<div class="relative flex justify-center text-xs uppercase">
					<span class="bg-background px-2 text-muted-foreground">
						{$_('auth.or_continue_with')}
					</span>
				</div>
			</div>
			<div class="grid grid-cols-2 gap-4">
				<Button variant="outline" type="button" class="gap-2" onclick={handleGoogleLogin}>
					<img src="{base}/icons/google.svg" alt="Google" class="h-4 w-4" />
					Google
				</Button>
				<Button variant="outline" type="button" class="gap-2" onclick={handleGithubLogin}>
					<Github class="h-4 w-4" />
					GitHub
				</Button>
			</div>
		</form>
		<div class="text-center text-sm">
			<span class="text-muted-foreground">{$_('auth.have_account')}</span>
			<a href="{base}/login" class="text-primary hover:underline ml-1">
				{$_('auth.login')}
			</a>
		</div>
	</Card.Root>
</div>