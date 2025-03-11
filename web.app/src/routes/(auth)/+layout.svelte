<script lang="ts">
	import { _ } from 'svelte-i18n';
	import { base } from '$app/paths';
</script>
<div class="min-h-screen flex flex-col">
  <div class="flex justify-center items-center p-16">
    <a href="{base}/" class="flex items-center space-x-2">
      <img src="{base}/images/logo.png" alt={$_('site.name')} class="h-6 w-6" />
      <span class="font-bold text-foreground">{$_('site.name')}</span>
    </a>
  </div>
  <slot />
</div>

<!-- <div class="min-h-screen w-full lg:grid lg:grid-cols-2">
  <div class="relative">
    <div class="absolute top-4 left-4 z-10">
      <a href="{base}/" class="flex items-center space-x-2">
        <img src="{base}/images/logo.png" alt={$_('site.name')} class="h-6 w-6" />
        <span class="font-bold text-foreground">{$_('site.name')}</span>
      </a>
    </div>
    <slot />
  </div>
  <div class="bg-muted hidden lg:block">
    <img
      src="{base}/images/login_bg_01.webp"
      alt={$_('auth.background_image')}
      width="1920"
      height="1080"
      class="h-full w-full object-cover object-center dark:brightness-[0.8] dark:grayscale"
    />
  </div>
</div> -->