<script lang="ts">
	import { page } from '$app/stores';
	import { _ } from 'svelte-i18n';

    export const ssr = true;
    export const prerender = true;
    export const trailingSlash = 'never';
    export const layoutConfig = {
        reset: true
    };
</script>
<slot />
<!-- <div class="min-h-screen w-full lg:grid lg:grid-cols-2">
  <div class="flex items-center justify-center py-12">
    <slot />
  </div>
  <div class="bg-muted hidden lg:block">
    <img
      src="/images/placeholder.svg"
      alt={$_('auth.background_image')}
      width="1920"
      height="1080"
      class="h-full w-full object-cover object-center dark:brightness-[0.2] dark:grayscale"
    />
  </div>
</div> -->