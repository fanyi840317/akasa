<script lang="ts" module>
	// This is sample data.
	const data = {
		changes: [
			{
				file: "README.md",
				state: "M",
			},
			{
				file: "routes/+page.svelte",
				state: "U",
			},
			{
				file: "routes/+layout.svelte",
				state: "M",
			},
		],
		tree: [
			["lib", ["components", "button.svelte", "card.svelte"], "utils.ts"],
			[
				"routes",
				["hello", "+page.svelte", "+page.ts"],
				"+page.svelte",
				"+page.server.ts",
				"+layout.svelte",
			],
			["static", "favicon.ico", "svelte.svg"],
			"eslint.config.js",
			".gitignore",
			"svelte.config.js",
			"tailwind.config.js",
			"package.json",
			"README.md",
		],
	};
</script>

<script lang="ts">
	import * as Collapsible from "$lib/components/ui/collapsible/index.js";
	import * as Sidebar from "$lib/components/ui/sidebar/index.js";
	import * as Dialog from "$lib/components/ui/dialog/index.js";
	import ChevronRight from "@lucide/svelte/icons/chevron-right";
	import File from "@lucide/svelte/icons/file";
	import Folder from "@lucide/svelte/icons/folder";
	import PlusCircle from "@lucide/svelte/icons/plus-circle";
	import type { ComponentProps } from "svelte";
	import { Button } from "$lib/components/ui/button";
	import { goto } from "$app/navigation";
    import * as Card from "$lib/components/ui/card";
    import EventDetail from "./event-detail.svelte";

	let {
		ref = $bindable(null),
		...restProps
	}: ComponentProps<typeof Sidebar.Root> = $props();
	let showDialog = $state(false);
	let folderName = "";

	function handleCreateFolder() {
		// TODO: 实现创建文件夹的逻辑
		showDialog = false;
		folderName = "";
	}
</script>

<Dialog.Root bind:open={showDialog}>
	<Dialog.Content class="sm:max-w-[800px] h-[80vh]">
		<EventDetail
			eventTitle="新建事件"
			eventLocation=""
			eventDate=""
			eventStatus="未开始"
			creator={{
				name: "范一",
				avatar: "https://github.com/shadcn.png"
			}}
		/>
	</Dialog.Content>
</Dialog.Root>

<Sidebar.Group>
	<Sidebar.GroupLabel>私人</Sidebar.GroupLabel>
	<Sidebar.GroupAction
		title="Add Project"
		onclick={() => {
			// goto("/console/events/new");
			showDialog = true;
		}}
	>
		<PlusCircle /> <span class="sr-only">Add Project</span>
	</Sidebar.GroupAction>

	<Card.Root class="shadow-none my-2 mx-2">
		<form>
			<Card.Header class="p-4 pb-0">
				<Card.Title class="text-sm">分享身边的神秘事件</Card.Title>
				<Card.Description>
					记录和分享你遇到的神秘事件，让更多人了解这个世界的未知面
				</Card.Description>
			</Card.Header>
			<Card.Content class="grid gap-2.5 p-4">
				<Button
					class="bg-sidebar-primary text-sidebar-primary-foreground w-full shadow-none"
					size="sm" onclick={() => showDialog = true}
				>
					分享事件
				</Button>
			</Card.Content>
		</form>
	</Card.Root>
	<Sidebar.GroupContent>
		<!-- <Sidebar.Menu>
			<Sidebar.MenuItem>
				<Collapsible.Root
					class="group/collapsible [&[data-state=open]>button>svg:first-child]:rotate-90"
					open={name === "lib" || name === "components"}
				>
					<Collapsible.Trigger>
						{#snippet child({ props })}
							<Sidebar.MenuButton {...props}>
								<ChevronRight className="transition-transform" />
								<Folder />
								{name}
							</Sidebar.MenuButton>
						{/snippet}
					</Collapsible.Trigger>
					<Collapsible.Content>
						<Sidebar.MenuSub>
							{#each items as subItem, index (index)}
								{@render Tree({ item: subItem })}
							{/each}
						</Sidebar.MenuSub>
					</Collapsible.Content>
				</Collapsible.Root>
			</Sidebar.MenuItem>
		</Sidebar.Menu> -->
		<Sidebar.Menu>
			{#each data.tree as item, index (index)}
				{@render Tree({ item })}
			{/each}
		</Sidebar.Menu> 
		
		
	</Sidebar.GroupContent>
	
</Sidebar.Group>

<!-- eslint-disable-next-line @typescript-eslint/no-explicit-any -->
{#snippet Tree({ item }: { item: string | any[] })}
	{@const [name, ...items] = Array.isArray(item) ? item : [item]}
	{#if !items.length}
		<Sidebar.MenuButton
			isActive={name === "button.svelte"}
			class="data-[active=true]:bg-transparent"
		>
			<File />
			{name}
		</Sidebar.MenuButton>
	{:else}
		<Sidebar.MenuItem>
			<Collapsible.Root
				class="group/collapsible [&[data-state=open]>button>svg:first-child]:rotate-90"
				open={name === "lib" || name === "components"}
			>
				<Collapsible.Trigger>
					{#snippet child({ props })}
						<Sidebar.MenuButton {...props}>
							<ChevronRight className="transition-transform" />
							<Folder />
							{name}
						</Sidebar.MenuButton>
					{/snippet}
				</Collapsible.Trigger>
				<Collapsible.Content>
					<Sidebar.MenuSub>
						{#each items as subItem, index (index)}
							{@render Tree({ item: subItem })}
						{/each}
					</Sidebar.MenuSub>
				</Collapsible.Content>
			</Collapsible.Root>
		</Sidebar.MenuItem>
	{/if}
{/snippet}
