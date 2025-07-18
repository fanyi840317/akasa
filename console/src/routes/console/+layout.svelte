<script lang="ts">
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import AppSidebar from '$lib/components/layout/app-sidebar.svelte';
	import { LayoutDashboard, Bot, Calendar, Settings, MessageSquare, MapPin, Search } from '@lucide/svelte';
	import UserAvatar from '$lib/components/user';
	// import UserMenu from '$lib/components/user/user-menu.svelte';
	import { page } from '$app/state';
	import { authStore } from '$lib/stores/auth.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	import Loading from '$lib/components/ui/loading';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import LogoIcon from '$lib/components/layout/logo-icon.svelte';
	import ConsoleHeader from '$lib/components/layout/console-header.svelte';
	import { appStore } from '$lib/stores/app-state';
	import { chatStore } from '$lib/stores/chat.svelte';

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
			title: 'Map',
			url: '/console/map',
			icon: MapPin,
			isActive: currentPath.startsWith('/console/map')
		},
		{
			title: 'Research',
			url: '/console/research',
			icon: Search,
			isActive: currentPath.startsWith('/console/research')
		},
		{
			title: 'Config',
			url: '/console/config',
			icon: Settings,
			isActive: currentPath.startsWith('/console/config')
		}
		//{...actions}
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
	// let userEvents = $state<Array<{ name: string; $id: string }>>([]);
	// 获取本地聊天数据
	let chatSessions = $state<Array<{ name: string; id: string; timestamp: number }>>([]);

	// 加载本地聊天会话
	function loadLocalChats() {
		chatSessions = chatStore.getAllChatSessions();
	}
	// 获取当前选中的聊天ID
	let selectedChatId = $derived.by(() => {
		if (currentPath.startsWith('/console/chat/')) {
			return currentPath.split('/console/chat/')[1];
		}
		return undefined;
	});
	let files = $derived([
		// ...userEvents.map((event) => ({ name: `${event.name}`, id: event.$id, type: 'event' })),
		...chatSessions.map((chat) => ({
			name: chat.name,
			id: chat.id,
			isActive: typeof selectedChatId === 'string' && selectedChatId === chat.id
		}))
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
		// 加载本地聊天数据
		loadLocalChats();
	});
	appStore.setSidebarCollapsed(true);
	let open = $derived(!$appStore.sidebarCollapsed);
	const handleUserMenuAction = (action: string) => {
		console.log('Menu action:', action);
		// 这里可以添加具体的路由跳转或功能处理
	};

	// 处理聊天点击
	const handleChatClick = (chatId: string) => {
		// 导航到聊天页面
		goto(`/console/chat/${chatId}`);
	};

	// 处理聊天删除
	const handleChatDelete = (chatId: string) => {
		if (chatStore.deleteChatSession(chatId)) {
			// 重新加载聊天列表
			loadLocalChats();
			// 如果删除的是当前选中的聊天，导航到聊天首页
			if (selectedChatId === chatId) {
				goto('/console/chat');
			}
		}
	};

	// 处理聊天重命名
	const handleChatRename = (chatId: string, newName: string) => {
		if (chatStore.renameChatSession(chatId, newName)) {
			// 重新加载聊天列表
			loadLocalChats();
		}
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
		{open}
		style="--sidebar-width:200px"
		onOpenChange={(state: boolean) => {
			appStore.setSidebarCollapsed(state);
		}}
	>
		<AppSidebar
			{actions}
			{files}
			{selectedChatId}
			onChatClick={handleChatClick}
			onChatDelete={handleChatDelete}
			onChatRename={handleChatRename}
		/>
		<main class="size-full px-2">
			<ConsoleHeader {open} {user} onMenuAction={handleUserMenuAction} onLogout={handleLogout} />

			{@render children()}
		</main>
	</Sidebar.Provider>
{/if}
