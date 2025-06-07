<script lang="ts">
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import type { NavItem } from "$lib/types/types";
  import * as Sidebar from "$lib/components/ui/sidebar/index.js";
  import { Badge } from "$lib/components/ui/badge";
  import ChevronRight from "lucide-svelte/icons/chevron-right";
  import type { ComponentProps } from "svelte";

  // 组件属性
  let {
    items = [],
    label = "",
    onNavItemClick = (item: NavItem) => {},
    ref = $bindable(null),
    ...restProps
  } = $props<
    {
      items: NavItem[];
      label?: string;
      onNavItemClick?: (item: NavItem) => void;
      ref?: any;
    } & ComponentProps<typeof Sidebar.Group>
  >();

  // 打开的子菜单状态
  let openItem = $state<string | null>(null);

  // 判断项目是否激活
  function isActive(item: NavItem): boolean {
    // 如果设置了clickOnly属性或状态为disabled，则不进行激活状态显示
    if (item.clickOnly || item.state === "disabled") {
      return false;
    }

    // 如果item有isActive属性且为true，直接返回true
    if (item.isActive === true) {
      return true;
    }

    if (item.url) {
      const pathname = $page.url.pathname;
      const itemPath = item.url;

      // 精确匹配：完全相同的路径
      if (pathname === itemPath) {
        return true;
      }

      // 特殊处理根路径 /console，只有完全匹配才返回true
      if (itemPath === "/console") {
        return pathname === "/console";
      }

      // 检查是否为子项目的激活状态
      if (item.items?.length) {
        return item.items.some((subItem) => isActive(subItem));
      }
    }

    return false;
  }

  // 处理导航项点击
  function handleItemClick(item: NavItem) {
    // 如果项目状态为disabled，不执行任何操作
    if (item.state === "disabled") {
      return;
    }

    if (item.clickOnly) {
      // 统一使用onNavItemClick处理所有交互，包括leftView和modal
      onNavItemClick(item);
      return;
    }

    if (item.url) {
      // 如果有URL，进行导航
      goto(item.url);
    }
    
    if (item.items?.length) {
      // 如果有子项，切换展开状态
      openItem = openItem === item.title ? null : item.title;
    }
  }
</script>

<Sidebar.Group bind:ref {...restProps}>
  {#if label}
    <Sidebar.GroupLabel class="group-data-[collapsible=icon]:hidden">
      {label}
    </Sidebar.GroupLabel>
  {/if}

  <Sidebar.Menu>
    {#each items as item (item.title)}
      <Sidebar.MenuItem>
        <Sidebar.MenuButton
          data-state={openItem === item.title ? "open" : "closed"}
          onclick={() => handleItemClick(item)}
          size={item.size || "md"}
          class="group-data-[collapsible=icon]:justify-center {isActive(item)
            ? 'bg-sidebar-accent text-sidebar-accent-foreground'
            : ''} {item.state === 'disabled'
            ? 'opacity-50 cursor-not-allowed'
            : ''}"
        >
          <div class="flex items-center justify-between w-full group-data-[collapsible=icon]:justify-center">
            <div class="flex items-center gap-2 group-data-[collapsible=icon]:gap-0">
              <item.icon class="h-4 w-4 shrink-0" />
              <span class="group-data-[collapsible=icon]:hidden">{item.title}</span>
            </div>
            {#if item.items?.length}
              <ChevronRight
                class="h-4 w-4 transition-transform group-data-[collapsible=icon]:hidden {openItem === item.title
                  ? 'rotate-90'
                  : ''}"
              />
            {:else if item.badge && !item.clickOnly}
              <Badge variant="secondary" class="ml-auto group-data-[collapsible=icon]:hidden">
                {item.badge}
              </Badge>
            {:else if item.unread}
              <Badge variant="outline" class="ml-auto group-data-[collapsible=icon]:hidden">
                {item.unread}
              </Badge>
            {/if}
          </div>
        </Sidebar.MenuButton>

        {#if item.items?.length}
          <Sidebar.MenuSub
            data-state={openItem === item.title ? "open" : "closed"}
            class="group-data-[collapsible=icon]:hidden"
          >
            {#each item.items as subItem}
              <Sidebar.MenuSubItem>
                <Sidebar.MenuSubButton
                  href={subItem.url}
                  class={isActive(subItem)
                    ? "bg-sidebar-accent text-sidebar-accent-foreground"
                    : ""}
                >
                  <span>{subItem.title}</span>
                  {#if subItem.unread}
                    <Badge variant="secondary" class="ml-auto">
                      {subItem.unread}
                    </Badge>
                  {/if}
                </Sidebar.MenuSubButton>
              </Sidebar.MenuSubItem>
            {/each}
          </Sidebar.MenuSub>
        {:else if item.url}
          <a href={item.url} class="sr-only">{item.title}</a>
        {/if}
      </Sidebar.MenuItem>
    {/each}
  </Sidebar.Menu>
</Sidebar.Group>
