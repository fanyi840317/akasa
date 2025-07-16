<script lang="ts">
	import { Menu } from '@lucide/svelte';
	import { Button } from '$lib/components/ui/button';
	import { appStore } from '$lib/stores/app-state';
	import { cn } from '$lib/utils';

	interface Props {
		title: string;
		description?: string;
		class?: string;
		rightContent?: import('svelte').Snippet;
	}

	let { title, description, class: className = '', rightContent }: Props = $props();

	function toggleSidebar() {
		appStore.toggleSidebar();
	}
</script>

<header class={cn("flex items-center gap-4 border-b px-6 py-4 ",className)}>
	<Button variant="ghost" size="icon" onclick={toggleSidebar}>
		<Menu class="h-5 w-5" />
	</Button>
	<div class="flex flex-col flex-1">
		<h1 class="text-xl font-semibold">{title}</h1>
		{#if description}
			<p class="text-sm text-muted-foreground">{description}</p>
		{/if}
	</div>
	{#if rightContent}
		<div class="flex items-center">
			{@render rightContent()}
		</div>
	{/if}
</header>