<script lang="ts">
  import { page } from "$app/stores";
  import { cn } from "$lib/utils.js";
  import { _ } from 'svelte-i18n';
  import { Button } from "$lib/components/ui/button";
  import { Separator } from "$lib/components/ui/separator";
  import { Settings, User, Users, Bookmark, MessageSquare, History } from "lucide-svelte";

  const navigation = [
    {
      title: $_('profile.personal_info'),
      href: "/profile",
      icon: User
    },
    {
      title: $_('profile.settings'),
      href: "/profile/settings",
      icon: Settings
    },
    {
      title: $_('profile.following'),
      href: "/profile/following",
      icon: Users
    },
    {
      title: $_('profile.bookmarks'),
      href: "/profile/bookmarks",
      icon: Bookmark
    },
    {
      title: $_('profile.messages'),
      href: "/profile/messages",
      icon: MessageSquare
    },
    {
      title: $_('profile.history'),
      href: "/profile/history",
      icon: History
    }
  ];
</script>

<div class="container mx-auto py-8">
  <div class="grid grid-cols-12 gap-8">
    <!-- 左侧导航栏 -->
    <aside class="col-span-3 space-y-6">
      <nav class="flex flex-col space-y-1">
        {#each navigation as item}
          <a
            href={item.href}
            class={cn(
              "flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors",
              $page.url.pathname === item.href
                ? "bg-accent text-accent-foreground"
                : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
            )}
          >
            <svelte:component this={item.icon} class="h-4 w-4" />
            {item.title}
          </a>
        {/each}
      </nav>
    </aside>

    <!-- 右侧内容区 -->
    <main class="col-span-9">
      <div class="rounded-lg border bg-card p-8 text-card-foreground shadow">
        
      </div>
    </main>
  </div>
</div>