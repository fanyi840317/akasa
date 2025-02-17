<script lang="ts">
	import ModeToggle from "./mode-toggle.svelte";
	import { siteConfig } from "$lib/config/site.js";
	import { page } from "$app/stores";
	import { cn } from "$lib/utils.js";
	import LanguageToggle from "./language-toggle.svelte";
	import SettingsControls from "./settings-controls.svelte";
	import { _ } from 'svelte-i18n';
</script>


<header
	class="border-border/40 bg-background/95 supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50 w-full border-b backdrop-blur"
>
	<div class="container flex h-14 max-w-screen-2xl items-center">
		
<div class="mr-4 hidden md:flex">
	<a href="/" class="mr-6 flex items-center space-x-2">
		<!-- <Icons.logo class="h-6 w-6" /> -->
		<span class="hidden font-bold xl:inline-block">
			{$_('site.name')}
		</span>
	</a>
	<nav class="flex items-center gap-6 text-sm">
		<a
			href="/events"
			class={cn(
				"hover:text-foreground/80 transition-colors",
				$page.url.pathname === "/events" ? "text-foreground" : "text-foreground/60"
			)}
		>
			{$_('site.events')}
		</a>
		<a
			href="/cultivation"
			class={cn(
				"hover:text-foreground/80 transition-colors",
				$page.url.pathname.startsWith("/cultivation")
					? "text-foreground"
					: "text-foreground/60"
			)}
		>
			{$_('site.cultivation')}
		</a>
		<a
			href="/legacy"
			class={cn(
				"hover:text-foreground/80 transition-colors",
				$page.url.pathname.startsWith("/legacy") ? "text-foreground" : "text-foreground/60"
			)}
		>
			{$_('site.legacy')}
		</a>
		<!-- <a
			href="/examples"
			class={cn(
				"hover:text-foreground/80 transition-colors",
				$page.url.pathname.startsWith("/examples")
					? "text-foreground"
					: "text-foreground/60"
			)}
		>
			{$_('site.examples')}
		</a>

		<a
			href="/blocks"
			class={cn(
				"hover:text-foreground/80 transition-colors",
				$page.url.pathname.startsWith("/blocks") ? "text-foreground" : "text-foreground/60"
			)}
		>
			{$_('site.blocks')}
		</a>
		<a
			href="/colors"
			class={cn(
				"hover:text-foreground/80 transition-colors",
				$page.url.pathname.startsWith("/colors") ? "text-foreground" : "text-foreground/60"
			)}
		>
			{$_('site.colors')}
		</a> -->
	</nav>
</div>
		<div class="flex flex-1 items-center justify-between space-x-2 md:justify-end">
			<!-- <div class="w-full flex-1 md:w-auto md:flex-none">
				<CommandMenu />
			</div> -->
			
			<SettingsControls />
		</div>
	</div>

</header>

<style>
	.active {
		@apply text-foreground;
	}
	a:not(.active) {
		@apply text-foreground/60;
	}
</style>