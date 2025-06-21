<script lang="ts">
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import AppSidebar from '$lib/components/layout/app-sidebar.svelte';
	import { LayoutDashboard, Bot, Calendar, Settings } from '@lucide/svelte';
	import UserAvatar from '$lib/components/user';
	import UserMenu from '$lib/components/user/user-menu.svelte';
	import { page } from '$app/state';
	import { authStore } from '$lib/stores/auth.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	import Loading from '$lib/components/ui/loading';
	import { ScrollArea } from '$lib/components/ui/scroll-area';

	let { children } = $props();
	let activeMenu = $state('');
	const currentPath = $derived(page.url.pathname);
	$effect(() => {
		if (currentPath.startsWith('/console/events')) {
			activeMenu = 'events';
		} else if (currentPath.startsWith('/console/agents')) {
			activeMenu = 'agents';
		} else if (currentPath.startsWith('/console/config')) {
			activeMenu = 'config';
		}
	});
	let actions = $derived([
		{
			title: 'Dashboard',
			url: '/dashboard',
			icon: LayoutDashboard,
			isActive: false
		},
		{
			title: 'Agents',
			url: '/console/agents',
			icon: Bot,
			isActive: activeMenu === 'agents'
		},
		{
			title: 'Events',
			url: '/console/events',
			icon: Calendar,
			isActive: activeMenu === 'events'
		},
		{
			title: 'Config',
			url: '/console/config',
			icon: Settings,
			isActive: activeMenu === 'config'
		}
	]);
	// 使用真实的认证用户信息
	let user = $derived(
		authStore.user
			? {
					name: authStore.user.name,
					email: authStore.user.email
				}
			: null
	);
	// 使用 eventStore 获取用户创建的事件
	let userEvents = $state<any[]>([]);
	let files = $derived([
		...userEvents.map((event) => ({ name: `${event.name}`, id: event.$id, type: 'event' }))
	]);

	// 在组件挂载时检查认证状态并加载用户事件
	onMount(async () => {
		if (browser) {
			// 等待认证检查完成
			while (authStore.loading) {
				await new Promise((resolve) => setTimeout(resolve, 100));
			}

			// 如果用户未认证，重定向到登录页面
			if (!authStore.isAuthenticated) {
				goto('/login');
				return;
			}
		}
	});
	let open = $state(true);
	const handleUserMenuAction = (action: string) => {
		console.log('Menu action:', action);
		// 这里可以添加具体的路由跳转或功能处理
	};

	const handleLogout = async () => {
		console.log('User logout');
		const result = await authStore.logout();
		if (result.success) {
			goto('/login');
		}
	};
</script>

{#if authStore.loading}
	<Loading />
{:else if user}
	<Sidebar.Provider
		style="--sidebar-width:224px"
		onOpenChange={(state) => {
			open = state;
		}}
	>
		<AppSidebar {actions} {files} bind:isOpen={open} />
		<main class="size-full px-2">
			<header class=" flex h-14 w-full items-center justify-between pr-2">
				<Sidebar.Trigger class="" />
				<UserMenu {user} onMenuAction={handleUserMenuAction} onLogout={handleLogout}>
					<UserAvatar {user} size="size-8" />
				</UserMenu>
			</header>
			<ScrollArea orientation="vertical" class=" rounded-input bg-base-200 h-[calc(100vh-64px)]  ">
				{@render children()}
			</ScrollArea>
		</main>
	</Sidebar.Provider>
{/if}
