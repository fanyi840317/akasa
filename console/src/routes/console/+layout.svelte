<script lang="ts">
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import AppSidebar from '$lib/components/layout/app-sidebar.svelte';
	import { DamIcon } from '@lucide/svelte';
	import UserAvatar from '$lib/components/user';
	import UserMenu from '$lib/components/user/user-menu.svelte';
	import { page } from '$app/state';
	import { eventStore } from '$lib/stores/event.svelte';
	import { authStore } from '$lib/stores/auth.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	import Loading from '$lib/components/ui/loading';

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

			// 加载用户事件
			try {
				if (authStore.user?.email) {
					userEvents = await eventStore.getEvents(authStore.user.$id);
				}
			} catch (error) {
				console.error('Failed to load user events:', error);
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

	const handleCreateEvent = () => {
		console.log('Creating new event');
		// 这里可以添加创建事件的逻辑，比如打开创建事件的模态框或跳转到创建页面
		goto('/console/events/new');
	};

	const handleFileClick = (fileName: string) => {
		console.log('File clicked:', fileName);

		// 检查是否是事件文件
		const event = userEvents.find((e) => e.name === fileName);
		if (event) {
			// 跳转到事件详情页面
			goto(`/console/events/my-${event.$id}`);
		}
	};

	const handleEventView = (eventId: string) => {
		console.log('Viewing event:', eventId);
		// 跳转到事件详情页面
		goto(`/console/events/${eventId}`);
	};

	const handleEventDelete = async (eventId: string) => {
		console.log('Deleting event:', eventId);
		try {
			// 调用eventStore删除事件
			await eventStore.deleteEvent(eventId);
			// 重新加载事件列表
			if (authStore.user?.email) {
				userEvents = await eventStore.getEvents(authStore.user.email);
			}
		} catch (error) {
			console.error('Failed to delete event:', error);
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
			onCreateEvent={handleCreateEvent}
			onFileClick={handleFileClick}
			onEventView={handleEventView}
			onEventDelete={handleEventDelete}
		/>
		<Sidebar.Inset class="">
			<header class="w-full h-14 flex-between px-2 -mt-2">
				<Sidebar.Trigger class="-ml-1" />
				<UserMenu {user} onMenuAction={handleUserMenuAction} onLogout={handleLogout}>
					<UserAvatar {user} size="size-8" />
				</UserMenu>
			</header>
			<div class=" w-full bg-base-200 rounded-3xl h-full">
				{@render children()}
			</div>
		</Sidebar.Inset>
	</Sidebar.Provider>
{/if}
