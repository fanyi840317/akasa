<script lang="ts">
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import AppSidebar from '$lib/components/layout/app-sidebar.svelte';
	import { LayoutDashboard, Bot, Calendar, Settings ,MessageSquare } from '@lucide/svelte';
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
	const currentPath = $derived(page.url.pathname);
	let actions = $derived([
		{
			title: 'Chat',
			url: '/console/chat',
			icon: MessageSquare,
			isActive: currentPath.startsWith('/console/chat')
		},
		{
			title: 'Agents',
			url: '/console/agents',
			icon: Bot,
			isActive: currentPath.startsWith('/console/agents')
		},
		{
			title: 'Events',
			url: '/console/events',
			icon: Calendar,
			isActive: currentPath.startsWith('/console/events')
		},
		{
			title: 'Config',
			url: '/console/config',
			icon: Settings,
			isActive: currentPath.startsWith('/console/config')
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
	let userEvents = $state<Array<{ name: string; $id: string }>>([]);
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
		style="--sidebar-width:220px"
		onOpenChange={(state) => {
			open = state;
		}}
	>
		<AppSidebar {actions} {files} bind:isOpen={open} />
		<main class="size-full px-1">
			<header class=" flex h-12 w-full items-center justify-between pr-1">
				<div></div>
				<!-- <Sidebar.Trigger class="" /> -->
				<UserMenu {user} onMenuAction={handleUserMenuAction} onLogout={handleLogout}>
					<UserAvatar {user} size="size-6" fallbackClass="text-xs"/>
				</UserMenu>
			</header>
			{@render children()}
		</main>
	</Sidebar.Provider>
{/if}
