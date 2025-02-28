<script lang="ts">
	import { Button } from "$lib/components/ui/button";
	import { User } from "lucide-svelte";
	import { _ } from 'svelte-i18n';
	import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "$lib/components/ui/dropdown-menu";
	import { Avatar, AvatarFallback, AvatarImage } from "$lib/components/ui/avatar";
	import { auth } from '$lib/stores/auth';

	function handleLogout() {
		auth.logout();
	}
</script>

{#if $auth.user}
	<DropdownMenu>
		<DropdownMenuTrigger>
			<Avatar class="h-8 w-8 cursor-pointer">
				<AvatarImage src={$auth.user.prefs?.avatar} alt={$auth.user.name} />
				<AvatarFallback><User class="h-4 w-4" /></AvatarFallback>
			</Avatar>
		</DropdownMenuTrigger>
		<DropdownMenuContent align="end">
			<DropdownMenuLabel>{$auth.user.name}</DropdownMenuLabel>
			<DropdownMenuSeparator />
			<a href="/profile"><DropdownMenuItem>{$_('profile.personal_info')}</DropdownMenuItem></a>
			<DropdownMenuItem href="/profile/settings">{$_('profile.settings')}</DropdownMenuItem>
			<DropdownMenuSeparator />
			<DropdownMenuItem onclick={handleLogout}>{$_('site.logout')}</DropdownMenuItem>
		</DropdownMenuContent>
	</DropdownMenu>
{:else}
	<Button variant="ghost" href="/login" class="gap-2 hover:bg-accent/50 transition-colors">
		<User class="h-4 w-4" />
		<span>{$_('site.login')}</span>
	</Button>
{/if}