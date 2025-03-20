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
	import { Input } from "$lib/components/ui/input";
	import { Button } from "$lib/components/ui/button";
	import { goto } from "$app/navigation";
    import * as Card from "$lib/components/ui/card";

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
	<Dialog.Content>
		<Dialog.Header>
			<Dialog.Title>新建文件夹</Dialog.Title>
			<Dialog.Description>请输入新文件夹的名称</Dialog.Description>
		</Dialog.Header>
		<div class="grid gap-4 py-4">
			<div class="grid grid-cols-4 items-center gap-4">
				<Input
					id="name"
					bind:value={folderName}
					placeholder="文件夹名称"
					class="col-span-4"
				/>
			</div>
		</div>
		<Dialog.Footer>
			<Button type="submit" size="sm" onclick={handleCreateFolder}
				>button</Button
			>
		</Dialog.Footer>
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
