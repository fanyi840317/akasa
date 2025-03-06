<script lang="ts">
    import * as Sidebar from "$lib/components/ui/sidebar";
    import NavMain from "./nav-main.svelte";
    import NavProjects from "./nav-projects.svelte";
    import NavUser from "./nav-user.svelte";
    import NavSecondary from "./nav-secondary.svelte";
	import Command from "lucide-svelte/icons/command";
    
    // Sidebar 配置选项
    let {
        collapsible = "icon" as "icon" | "none" | "offcanvas",
        side = "left" as "left" | "right"
    } = $props();
    
    // 从数据源或存储中获取导航数据
    import { navData } from "$lib/data/navigation-data";
    import { Footer } from "$lib/components/ui/sheet";
</script>

<Sidebar.Root {collapsible} {side}  variant="inset" >
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
		<NavMain items={navData.navMain} />
		<NavProjects projects={navData.projects} />
	</Sidebar.Content>
	
    <Sidebar.Footer>
		<NavSecondary items={navData.navSecondary} />
        <NavUser user={navData.user} />
    </Sidebar.Footer>
</Sidebar.Root>
