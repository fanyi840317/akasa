<script lang="ts">
  import {
    ChevronDown,
    PlusCircle,
    PlusIcon,
    SparklesIcon,
    LogOut,
    Settings,
    MapIcon,
    User as UserIcon,
  } from "lucide-svelte";
  import { UserAvatar, Tooltip } from "../ui";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
  import type { User } from "$lib/types/user";
  import { cn } from "$lib/utils";
  import { goto } from "$app/navigation";
  import { page } from "$app/state";

  let {
    title,
    subtitle,
    handleCreate,
    handleUseAI,
    user,
    class: className,
  } = $props<{
    title?: string;
    subtitle?: string;
    handleCreate?: () => void;
    handleUseAI?: () => void;
    class?: string;
    src?: string;
    fallback?: string;
    user?: User;
  }>();

  function handleLogout() {
    // 处理登出逻辑
    console.log("用户登出");
  }

  function handleSettings() {
    // 处理设置逻辑
    console.log("打开设置");
  }

  function handleProfile() {
    // 处理个人资料逻辑
    console.log("查看个人资料");
  }
  let currentPath = $derived(page.url.pathname);
</script>

<div class={cn("flex justify-between items-center", className)}>
  <div class="items-start">
    <h1
      class="text-xl font-bold text-center bg-clip-text
      text-base-content
      tracking-tight"
    >
      Akasa
    </h1>
    <!-- <p class="text-[10px] text-base-content/40">
      प्रत्यभिज्ञानं आरम्भः  
    </p> -->
  </div>
  <div class="flex flex-col items-center gap-0 -mb-1">
    <div role="tablist" class="tabs tabs-border">
      <a role="tab" class="tab"
      onclick={() => {
        goto("/console/events");
      }}
      class:tab-active={currentPath.startsWith("/console/events")}
      >Events</a>
      <a
        role="tab"
        class="tab gap-1"
        class:tab-active={currentPath.startsWith("/console/map")}
      >
        <MapIcon class="w-3 h-3" />
        Map
      </a>
      <!-- svelte-ignore a11y_interactive_supports_focus -->
      <a
        class="tab gap-1 "
        onclick={() => {
          goto("/console/my/events");
        }}
        class:tab-active={currentPath.startsWith("/console/my/events")}
      >
        My

        <ChevronDown class="w-3 h-3" />
      </a>
      <!-- <a role="tab" class="tab"></a> -->
    </div>
    <!-- {#if title}
      <button class="btn btn-ghost btn-sm">
        <h1 class="text-lg font-semibold">{title}</h1>
        <ChevronDown class="w-5 h-5" />
      </button>
    {/if}
    {#if subtitle}
      <span class="px-1 text-xs text-base-content/70">{subtitle}</span>
    {/if} -->
  </div>
  <div class="flex items-center gap-4">
    <!-- <span class="text-sm text-base-content/70">42182 events</span> -->
    <div class="flex items-center gap-4">
   
      <DropdownMenu.Root>
        <DropdownMenu.Trigger>
          <UserAvatar
            class="cursor-pointer size-6"
            src={user?.src}
            fallback={user?.name?.charAt(0)}
          />
        </DropdownMenu.Trigger>
        <DropdownMenu.Content class="w-56" sideOffset={5} align="end">
          <div class="flex items-center justify-start gap-2 p-2">
            <div class="flex h-10 w-10 items-center justify-center space-y-0">
              <UserAvatar src={user?.src} fallback={user?.name?.charAt(0)} />
            </div>
            <div class="space-y-1">
              <p class="text-sm font-medium leading-none">
                {user?.name || "用户"}
              </p>
              <p class="text-xs leading-none text-muted">{user?.email || ""}</p>
            </div>
          </div>
          <DropdownMenu.Separator />
          <DropdownMenu.Item onclick={handleProfile}>
            <UserIcon class="mr-2 h-4 w-4" />
            <span>个人资料</span>
          </DropdownMenu.Item>
          <DropdownMenu.Item onclick={handleSettings}>
            <Settings class="mr-2 h-4 w-4" />
            <span>设置</span>
          </DropdownMenu.Item>
          <DropdownMenu.Separator />
          <DropdownMenu.Item onclick={handleLogout}>
            <LogOut class="mr-2 h-4 w-4" />
            <span>退出登录</span>
          </DropdownMenu.Item>
        </DropdownMenu.Content>
      </DropdownMenu.Root>
    </div>
  </div>
</div>
