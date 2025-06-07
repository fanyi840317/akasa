<script lang="ts">
  import Upload from "lucide-svelte/icons/upload";
  import ChevronsUpDown from "lucide-svelte/icons/chevrons-up-down";
  import LogOut from "lucide-svelte/icons/log-out";
  import Globe from "lucide-svelte/icons/globe";
  import Palette from "lucide-svelte/icons/palette";

  import * as Avatar from "$lib/components/ui/avatar/index.js";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
  import * as Sidebar from "$lib/components/ui/sidebar/index.js";
  import { useSidebar } from "$lib/components/ui/sidebar/index.js";
  import { auth } from "$lib/stores/auth";
  import { goto } from "$app/navigation";
  import { base } from "$app/paths";
  import { page } from "$app/stores";
  import type { User } from "$lib/types/user";
  import { locale, _ } from 'svelte-i18n';
  import { mode, setMode } from 'mode-watcher';

  /**
   * 用户导航组件
   * 显示当前用户信息和简单的用户菜单
   */
  let { user: user } = $props();
  const sidebar = useSidebar();

  // 语言选项
  const languages = [
    { value: "en", label: "English" },
    { value: "zh", label: "中文" }
  ];

  // 主题选项
  const themes = [
    { value: "light" as const, label: $_('theme.light') },
    { value: "dark" as const, label: $_('theme.dark') }
  ];

  let selectedLanguage = $state($locale);
  let selectedTheme = $state($mode);

  function handleLogout() {
    auth.logout();
    const returnUrl = encodeURIComponent($page.url.pathname);
    goto(`${base}/login?redirect=${returnUrl}`);
  }

  function handleUploadAvatar() {
    // TODO: 实现头像上传功能
    console.log('Upload avatar');
  }

  function handleLanguageChange(value: string) {
    selectedLanguage = value;
    locale.set(value);
  }

  function handleThemeChange(value: "light" | "dark") {
    selectedTheme = value;
    setMode(value);
  }
</script>

<Sidebar.Menu>
  <Sidebar.MenuItem>
    <DropdownMenu.Root>
      <DropdownMenu.Trigger>
        {#snippet child({ props })}
          <Sidebar.MenuButton
            {...props}
            size="lg"
            class="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
          >
            <Avatar.Root class="h-8 w-8 rounded-lg">
              <Avatar.Image src={user.avatar} alt={user.name} />
              <Avatar.Fallback class="rounded-lg">CN</Avatar.Fallback>
            </Avatar.Root>
            <div class="grid flex-1 text-left text-sm leading-tight">
              <span class="truncate font-semibold">{user.name}</span>
              <span class="truncate text-xs">{user.email}</span>
            </div>
            <ChevronsUpDown class="ml-auto size-4" />
          </Sidebar.MenuButton>
        {/snippet}
      </DropdownMenu.Trigger>
      <DropdownMenu.Content
        class="w-[--bits-dropdown-menu-anchor-width] min-w-56 rounded-lg"
        side={sidebar.isMobile ? "bottom" : "right"}
        align="end"
        sideOffset={4}
      >
        <DropdownMenu.Label class="p-0 font-normal">
          <div class="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
            <Avatar.Root class="h-8 w-8 rounded-lg">
              <Avatar.Image src={user.avatar} alt={user.name} />
              <Avatar.Fallback class="rounded-lg">CN</Avatar.Fallback>
            </Avatar.Root>
            <div class="grid flex-1 text-left text-sm leading-tight">
              <span class="truncate font-semibold">{user.name}</span>
              <span class="truncate text-xs">{user.email}</span>
            </div>
          </div>
        </DropdownMenu.Label>
        <DropdownMenu.Separator />
        <DropdownMenu.Group>
          <DropdownMenu.Item onclick={handleUploadAvatar}>
            <Upload class="mr-2 h-4 w-4" />
            {$_('common.uploadAvatar')}
          </DropdownMenu.Item>
        </DropdownMenu.Group>
        <DropdownMenu.Separator />
        <DropdownMenu.Group>
          <DropdownMenu.Sub>
            <DropdownMenu.SubTrigger>
              <Globe class="mr-2 h-4 w-4" />
              {$_('common.changeLanguage')}
            </DropdownMenu.SubTrigger>
            <DropdownMenu.SubContent>
              {#each languages as language}
                <DropdownMenu.Item onclick={() => handleLanguageChange(language.value)}>
                  {language.label}
                  {#if selectedLanguage === language.value}
                    <DropdownMenu.Shortcut>✓</DropdownMenu.Shortcut>
                  {/if}
                </DropdownMenu.Item>
              {/each}
            </DropdownMenu.SubContent>
          </DropdownMenu.Sub>
          <DropdownMenu.Sub>
            <DropdownMenu.SubTrigger>
              <Palette class="mr-2 h-4 w-4" />
              {$_('common.changeTheme')}
            </DropdownMenu.SubTrigger>
            <DropdownMenu.SubContent>
              {#each themes as theme}
                <DropdownMenu.Item onclick={() => handleThemeChange(theme.value)}>
                  {theme.label}
                  {#if selectedTheme === theme.value}
                    <DropdownMenu.Shortcut>✓</DropdownMenu.Shortcut>
                  {/if}
                </DropdownMenu.Item>
              {/each}
            </DropdownMenu.SubContent>
          </DropdownMenu.Sub>
        </DropdownMenu.Group>
        <DropdownMenu.Separator />
        <DropdownMenu.Item onclick={handleLogout}>
          <LogOut class="mr-2 h-4 w-4" />
          {$_('common.logout')}
        </DropdownMenu.Item>
      </DropdownMenu.Content>
    </DropdownMenu.Root>
  </Sidebar.MenuItem>
</Sidebar.Menu>
