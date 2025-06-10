<script lang="ts">
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import AppSidebar from '$lib/components/layout/app-sidebar.svelte';
	import { DamIcon } from '@lucide/svelte';
	import UserAvatar from '$lib/components/user';
	import { page } from '$app/state';

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
	let user = {
		name: 'John Doe'
	};
	let files = [
		'button.svelte',
		'lib',
		['components', ['ui', ['sidebar', ['index.js', 'root.svelte']]]]
	];
	let open = $state(true);
</script>

<Sidebar.Provider
	style="--sidebar-width:224px"
	onOpenChange={(state) => {
		open = state;
	}}
>
	<AppSidebar {actions} {files} bind:isOpen={open}/>
	<Sidebar.Inset class="">
		<header class="w-full h-14 flex-between px-2 -mt-2">
			<Sidebar.Trigger class="-ml-1" />
			<UserAvatar {user} size="size-8" />
		</header>
		<div class=" w-full bg-base-200 rounded-3xl h-full">
			{@render children()}
		</div>
	</Sidebar.Inset>
</Sidebar.Provider>
