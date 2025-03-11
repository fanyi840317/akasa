<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
  import { Label } from '$lib/components/ui/label';
  import { Card } from '$lib/components/ui/card';
  import { _ } from 'svelte-i18n';
  import { Github, Mail, Lock, Loader2 } from 'lucide-svelte';
  import { auth } from '$lib/stores/auth';
  import { base } from '$app/paths';
  import { toast } from 'svelte-sonner';
  import { page } from '$app/stores';

  let email = '';
  let password = '';
  let loading = false;
  
  // 获取returnUrl参数
  const returnUrl = $page.data.returnUrl;

  async function handleSubmit() {
    loading = true;

    try {
      await auth.login(email, password, returnUrl);
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
  <Card class="w-full max-w-md p-6 space-y-6">
    <div class="text-center space-y-2">
      <h1 class="text-2xl font-semibold tracking-tight">{$_('auth.login')}</h1>
      <p class="text-sm text-muted-foreground">{$_('auth.enter_credentials')}</p>
    </div>

    <form on:submit|preventDefault={handleSubmit} class="space-y-4">
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

      <Button type="submit" class="w-full" disabled={loading}>
        {#if loading}
          <Loader2 class="mr-2 h-4 w-4 animate-spin" />
          {$_('common.loading')}
        {:else}
          {$_('auth.login')}
        {/if}
      </Button>
    </form>

    <div class="text-center text-sm">
      <a href="/forgot-password" class="text-primary hover:underline">
        {$_('auth.forgot_password')}
      </a>
    </div>

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

    <div class="text-center text-sm">
      <span class="text-muted-foreground">{$_('auth.no_account')}</span>
      <a href="{base}/register" class="text-primary hover:underline ml-1">
        {$_('auth.register')}  
      </a>
    </div>
  </Card>
</div>
