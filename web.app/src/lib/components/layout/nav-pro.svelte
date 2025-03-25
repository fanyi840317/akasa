<script lang="ts">
	import * as Collapsible from "$lib/components/ui/collapsible/index.js";
	import * as Sidebar from "$lib/components/ui/sidebar/index.js";
	import * as Dialog from "$lib/components/ui/dialog/index.js";
	import ChevronRight from "@lucide/svelte/icons/chevron-right";
	import File from "@lucide/svelte/icons/file";
	import Folder from "@lucide/svelte/icons/folder";
	import PlusCircle from "@lucide/svelte/icons/plus-circle";
	import { onMount, type ComponentProps } from "svelte";
	import { Button } from "$lib/components/ui/button";
	import { goto } from "$app/navigation";
	import * as Card from "$lib/components/ui/card";
	import EventDetail from "../console/create-event.svelte";
	import { Ellipsis, Forward, Plus, Save, Trash2 } from "lucide-svelte";
	import { auth } from "$lib/stores/auth";
	import { get } from "svelte/store";
	import { toast } from "svelte-sonner";
	import { eventStore } from "$lib/stores/event";
	import { Skeleton } from "$lib/components/ui/skeleton";
	import { caseStore } from "$lib/stores/case";
	import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
	import { useSidebar } from "$lib/components/ui/sidebar/index.js";
	import { appStore } from "$lib/stores/appState";

	let {
		ref = $bindable(null),
		...restProps
	}: ComponentProps<typeof Sidebar.Root> = $props();
	let showDialog = $state(false);
	let folderName = "";

	let userEvents = $state([]);
	let hasEvents = $state(false);
	let isLoading = $state(false);
	/**
	 * 当前选中的事件ID
	 * 统一使用appStore管理状态，避免状态管理混乱
	 */
	let selectedEventId = $state("");

	// 订阅appStore以获取最新的选中状态
	appStore.subscribe((state) => {
		alert(selectedEventId)
		selectedEventId = state.selectedEventId || "";
	});

	// 不再需要手动同步到store，统一由事件处理函数处理
	// 这样避免了双向绑定造成的循环更新问题
	eventStore.subscribe((state) => {
		userEvents = state.events;
		hasEvents = state.events.length > 0;
		isLoading = state.loading;
	});
	onMount(() => {
		// 组件挂载时获取用户事件
		async function loadUserEvents() {
			if (get(auth).user?.$id) {
				try {
					await eventStore.fetchEvents(get(auth).user?.$id);
				} catch (e: any) {
					toast.error("Failed to fetch user events:", e.message);
				}
			}
		}
		console.log("loadUserEvents");
		loadUserEvents();
	});
	// 在组件初始化时获取用户事件
	// $effect(() => {
	// 	alert("appStore.subscribe");
		
	// });
	const sidebar = useSidebar();

	// 处理删除事件
	async function handleDeleteEvent(eventId: string) {
		try {
			await eventStore.deleteEvent(eventId);
			toast.success("事件已成功删除");
		} catch (error) {
			const errorMessage =
				error instanceof Error ? error.message : "删除事件失败";
			toast.error(errorMessage);
		}
	}
</script>

<Sidebar.Group>
	<Sidebar.GroupLabel>私人</Sidebar.GroupLabel>

	{#if isLoading}
		<!-- 加载状态显示 -->
		<div class="flex items-center space-x-4 p-4">
			<!-- <Skeleton class="size-10 rounded-full" /> -->
			<div class="space-y-2 flex-1">
				<Skeleton class="h-4 w-[80%]" />
				<Skeleton class="h-3 w-[60%]" />
				<Skeleton class="h-4 w-[80%]" />
				<Skeleton class="h-3 w-[60%]" />
			</div>
		</div>
	{:else if !hasEvents}
		<Card.Root class="shadow-none my-2 mx-2">
			<form>
				<Card.Header class="p-4 pb-0">
					<Card.Title class="text-sm">分享身边的神秘事件</Card.Title>
					<Card.Description class="text-xs">
						记录和分享你遇到的神秘事件，让更多人了解这个世界的未知面
					</Card.Description>
				</Card.Header>
				<Card.Content class="grid gap-2.5 p-4">
					<Button
						class="bg-sidebar-primary text-sidebar-primary-foreground w-full shadow-none"
						size="sm"
						onclick={() => (showDialog = true)}
					>
						分享事件
					</Button>
				</Card.Content>
			</form>
		</Card.Root>
	{:else}
		<!-- 有事件时显示添加按钮和事件列表 -->
		<Sidebar.GroupAction
			title="Add Project"
			onclick={() => {
				// goto("/console/events/new");
				showDialog = true;
			}}
		>
			<Plus /> <span class="sr-only">Add Project</span>
		</Sidebar.GroupAction>

		<Sidebar.GroupContent>
			<Sidebar.Menu>
				{#each userEvents as event}
					{@render events({ id: event.$id, title: event.title })}
					<!-- <div class="relative group">
						<Sidebar.MenuButton isActive={false}>
							<File />
							{event.title}
						</Sidebar.MenuButton>

					</div> -->
				{/each}
			</Sidebar.Menu>
		</Sidebar.GroupContent>
	{/if}
</Sidebar.Group>

<Dialog.Root bind:open={showDialog}>
	<Dialog.Content class="sm:max-w-[900px] h-[80vh] px-0 py-10 ">
		<EventDetail x_event={undefined}
			on:close={(result) => {
				showDialog = false;
				// 如果事件包含eventId，则设置为选中状态
				if (result?.detail?.$id) {
					// 更新全局状态管理中的选中状态
					appStore.setSelectedEventId(result?.detail?.$id);
					eventStore.setCurrentEvent(result?.detail);
					goto(`/console/events/${selectedEventId}`);
				}
			}}
		/>
	</Dialog.Content>
</Dialog.Root>

{#snippet events({ id, title }: { id: string; title: string })}
	<Sidebar.MenuItem>
		<Sidebar.MenuButton
			isActive={selectedEventId === id}
			onclick={() => {
				// 更新全局状态管理中的选中状态
				appStore.setSelectedEventId(id);
				// 导航到事件详情页面
				goto(`/console/events/${id}`);
			}}
		>
			{#snippet child({ props })}
				<a href="javascript:void(0)" {...props}>
					<File />
					<span>{title}</span>
				</a>
			{/snippet}
		</Sidebar.MenuButton>
		<DropdownMenu.Root>
			<DropdownMenu.Trigger>
				{#snippet child({ props })}
					<Sidebar.MenuAction showOnHover {...props}>
						<Ellipsis />
						<span class="sr-only">More</span>
					</Sidebar.MenuAction>
				{/snippet}
			</DropdownMenu.Trigger>
			<DropdownMenu.Content
				class="w-48 rounded-lg"
				side={sidebar.isMobile ? "bottom" : "right"}
				align={sidebar.isMobile ? "end" : "start"}
			>
				<DropdownMenu.Item
					onclick={() => goto(`/console/events/${id}`)}
				>
					<Folder class="text-muted-foreground" />
					<span>查看事件</span>
				</DropdownMenu.Item>
				<DropdownMenu.Item>
					<Forward class="text-muted-foreground" />
					<span>分享事件</span>
				</DropdownMenu.Item>
				<DropdownMenu.Separator />
				<DropdownMenu.Item onclick={() => handleDeleteEvent(id)}>
					<Trash2 class="text-muted-foreground" />
					<span>删除事件</span>
				</DropdownMenu.Item>
			</DropdownMenu.Content>
		</DropdownMenu.Root>
	</Sidebar.MenuItem>
{/snippet}
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
