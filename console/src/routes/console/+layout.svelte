<script lang="ts">
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import AppSidebar from '$lib/components/layout/app-sidebar.svelte';
	import { DamIcon } from '@lucide/svelte';
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
		}
	});
	let actions = $derived([
		{
			title: 'Dashboard',
			url: '/dashboard',
			icon: DamIcon,
			isActive: false
		},
		{
			title: 'Events',
			url: '/console/events',
			icon: DamIcon,
			isActive: activeMenu === 'events'
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
		<AppSidebar
			{actions}
			{files}
			bind:isOpen={open}
		
		/>
		<Sidebar.Inset class="overflow-hidden">
			<header class="w-full h-14 flex justify-between items-center px-2 -mt-2">
				<Sidebar.Trigger class="-ml-1" />
				<UserMenu {user} onMenuAction={handleUserMenuAction} onLogout={handleLogout}>
					<UserAvatar {user} size="size-8" />
				</UserMenu>
			</header>
			<ScrollArea orientation="vertical" class=" h-[calc(100vh-64px)] rounded-input border bg-base-200">
				{@render children()}
			</ScrollArea>
		</Sidebar.Inset>
	</Sidebar.Provider>
{/if}
