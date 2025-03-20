<script lang="ts">
    import * as Sidebar from "$lib/components/ui/sidebar";
    import {ScrollArea }from "$lib/components/ui/scroll-area";
    import Nav from "./nav.svelte";
    import NavUser from "./nav-user.svelte";
    import NavPro from "./nav-pro.svelte";
    import Command from "lucide-svelte/icons/command";
    import type { NavItem, User } from "./types";
    import { page } from "$app/stores";
    import * as Card from "$lib/components/ui/card";
    import { Button } from "$lib/components/ui/button";
    
    // Sidebar 配置选项
    let {
        collapsible = 'none',
        collapsed = $bindable(false),
        side = "left" as "left" | "right",
        class: className = '',
        selectedItem = null,
        onNavItemClick = (item: NavItem) => {},
        user = undefined,
    } = $props<{
        collapsible?: 'none' | 'icon' | 'full';
        collapsed?: boolean;
        side?: "left" | "right";
        class?: string;
        selectedItem?: string | null;
        onNavItemClick?: (item: NavItem) => void;
        user?: User;
    }>();
    // 从数据源或存储中获取导航数据
    import { navData } from "$lib/data/navigation-data";
    
    // 如果没有传入用户信息，则使用页面数据中的用户信息
    $effect(() => {
        if (!user && $page.data.user) {
            user = $page.data.user;
        }
    });
    
    // 如果仍然没有用户信息，则使用导航数据中的默认用户信息
    $effect(() => {
        if (!user) {
            user = navData.user;
        }
    });
</script>

<Sidebar.Root {collapsible} {side}>
    <Sidebar.Header>
		<Sidebar.Menu>
			<Sidebar.MenuItem>
				<Sidebar.MenuButton size="lg">
					{#snippet child({ props })}
						<a href="##" {...props}>
							<div
								class="bg-sidebar-primary text-sidebar-primary-foreground flex aspect-square size-8 items-center justify-center rounded-lg"
							>
								<Command class="size-4" />
							</div>
							<div class="grid flex-1 text-left text-sm leading-tight">
								<span class="truncate font-semibold">Acme Inc</span>
								<span class="truncate text-xs">Enterprise</span>
							</div>
						</a>
					{/snippet}
				</Sidebar.MenuButton>
			</Sidebar.MenuItem>
		</Sidebar.Menu>
	</Sidebar.Header>
	
	<Sidebar.Content>
            <Nav items={navData.navMain} label="Platform" {selectedItem} {onNavItemClick} />
            <!-- <Nav items={navData.personalItems} label="个人" {selectedItem} {onNavItemClick} /> -->
           <Sidebar.Separator></Sidebar.Separator>
        <ScrollArea>
            <NavPro />
        </ScrollArea>
       
    </Sidebar.Content>
    
    <Sidebar.Footer>
		<Nav items={navData.navSecondary} {onNavItemClick}></Nav>
        <NavUser {user} />
    </Sidebar.Footer>
    <Sidebar.Rail />
</Sidebar.Root>
