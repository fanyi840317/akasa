<script lang="ts">
	import LogoIcon from './logo-icon.svelte';
	import UserMenu from '../user/user-menu.svelte';
	import UserAvatar from '../user/user-avatar.svelte';
	import SettingDialog from '../settings/setting-dalog.svelte';
	import type { Snippet } from 'svelte';

	let {
		open = true,
		user,
		leftActions,
		onMenuAction,
		onLogout
	}: {
		open?: boolean;
		user?: any;
		leftActions?: Snippet;
		onMenuAction?: (action: string) => void;
		onLogout?: () => void;
	} = $props();
</script>

<header class="flex h-12 w-full items-center justify-between pr-2">
	{#if !open}
		<div class="flex items-center justify-center gap-2">
			<LogoIcon isOpen={true} />
		</div>
	{:else}
		<div></div>
	{/if}
	<div class="flex items-center gap-2">
		
		<SettingDialog />
		<UserMenu {user} {onMenuAction} {onLogout}>
			<UserAvatar {user} size="size-8" fallbackClass="text-sm" />
		</UserMenu>
	</div>
</header>
