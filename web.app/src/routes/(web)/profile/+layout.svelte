<script lang="ts">
  import { page } from '$app/stores';
  import { _ } from 'svelte-i18n';
  import { Button } from "$lib/components/ui/button";
  import { User, Settings, Bell, Monitor, Heart } from "lucide-svelte";

  const navItems = [
    { href: '/profile/personal', icon: User, label: 'profile.personal_info' },
    { href: '/profile/settings', icon: Settings, label: 'profile.settings' },
    { href: '/profile/notifications', icon: Bell, label: 'profile.notifications' },
    { href: '/profile/appearance', icon: Monitor, label: 'profile.appearance' },
    { href: '/profile/favorites', icon: Heart, label: 'profile.favorites' }
  ];
</script>

<div class="container py-8 max-w-6xl">
  <div class="flex gap-8">
    <!-- 左侧导航栏 -->
    <aside class="w-64 shrink-0">
      <nav class="space-y-1">
        {#each navItems as item}
          <Button
            variant={$page.url.pathname === item.href ? 'secondary' : 'ghost'}
            class="w-full justify-start"
            href={item.href}
          >
            <svelte:component this={item.icon} class="mr-2 h-4 w-4" />
            {$_(item.label)}
          </Button>
        {/each}
      </nav>
    </aside>

    <!-- 右侧内容区域 -->
    <main class="flex-1">
      <slot />
    </main>
  </div>
</div>