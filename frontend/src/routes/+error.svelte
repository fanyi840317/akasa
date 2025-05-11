<script lang="ts">
  import { page } from '$app/stores';
  // import { Button } from '$lib/components/ui/button';
  import { _ } from 'svelte-i18n';
</script>

<div class="h-[80vh] flex items-center justify-center bg-background">
  <div class="text-center space-y-6 p-4">
    <h1 class="text-6xl font-bold text-primary mb-4">{$page.status}</h1>
    <p class="text-xl text-muted-foreground mb-6">
      {#if $page.status === 404}
        {$_('error.not_found')}
      {:else}
        {$_('error.something_wrong')}
      {/if}
    </p>
    <div class="flex justify-center gap-4">
      <button class="btn gap-2">
        {$_('common.back_home')}
      </button>
      {#if $page.status !== 404}
        <button class="btn gap-2">
          {$_('common.contact_support')}
        </button>
      {/if}
    </div>
  </div>
</div>