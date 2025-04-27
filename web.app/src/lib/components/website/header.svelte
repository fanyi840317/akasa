<script lang="ts">
	import ModeToggle from "./mode-toggle.svelte";
	import { page } from "$app/stores";
	import { cn } from "$lib/utils.js";
	import LanguageToggle from "./language-toggle.svelte";
	import SettingsControls from "./settings-controls.svelte";
	import { _ } from "svelte-i18n";
	import { Button } from "$lib/components/ui/button";
	import { User } from "lucide-svelte";
	import { goto } from "$app/navigation";
	import UserAvatar from "./user-avatar.svelte";
	import { base } from "$app/paths";
</script>

<header
	class="border-border/40 bg-card/95 supports-[backdrop-filter]:bg-card/60 sticky top-0 z-50 w-full border-b backdrop-blur"
>
	<div class="container flex h-14 max-w-screen-2xl items-center">
		<div class="mr-4 hidden md:flex">
			<a href="{base}/" class="mr-6 flex items-center space-x-2">
				<svg
				  xmlns="http://www.w3.org/2000/svg"
				  viewBox="0 0 64 32"
				  class="h-6 w-6 fill-current"
				  aria-label={$_("site.name")}
				>
				  <!-- X -->
				  <polygon points="0,0 8,0 20,16 8,32 0,32 12,16" />
				  <polygon points="12,0 20,0 32,16 20,32 12,32 24,16" />
				  <!-- 2 -->
				  <path d="M38,0 h18 a6,6 0 0 1 6,6 v6 a6,6 0 0 1 -6,6 h-10 l12,14 h-18 l-12,-14 v-6 a6,6 0 0 1 6,-6 z" />
				</svg>
				<span class="hidden font-bold xl:inline-block">
					{$_("site.name")}
				</span>
			</a>
			<nav class="flex items-center gap-6 text-sm">
				<a
					href="{base}/events"
					class={cn(
						"transition-colors py-1 hover:text-foreground",
						$page.url.pathname.startsWith("/events")
							? "text-foreground"
							: "text-foreground/60",
					)}
				>
					{$_("site.events")}
				</a>
				<a
					href="{base}/cultivation"
					class={cn(
						"transition-colors py-1 hover:text-foreground",
						$page.url.pathname.startsWith("/cultivation")
							? "text-foreground"
							: "text-foreground/60",
					)}
				>
					{$_("site.cultivation")}
				</a>
				<a
					href="{base}/legacy"
					class={cn(
						"transition-colors py-1 hover:text-foreground",
						$page.url.pathname.startsWith("/legacy")
							? "text-foreground"
							: "text-foreground/60",
					)}
				>
					{$_("site.legacy")}
				</a>
			</nav>
		</div>
		<div
			class="flex flex-1 items-center justify-between space-x-2 md:justify-end"
		>
			<div class="flex items-center gap-2">
				<SettingsControls />

				<UserAvatar />
			</div>
		</div>
	</div>
</header>

<style>
	.active {
		@apply text-foreground;
	}
	/* 移除未使用的样式 */
</style>
