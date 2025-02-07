<script lang="ts">
	import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
	import Globe from "svelte-radix/Globe.svelte";
	import { buttonVariants } from "$lib/components/ui/button";
	import { locale, _ } from 'svelte-i18n';

	// 定义支持的语言
	const languages = [
		{ code: 'en', label: 'English' },
		{ code: 'zh', label: '中文' },
		{ code: 'ja', label: '日本語' }
	];

	function setLanguage(lang: string) {
		locale.set(lang);
	}
</script>

<DropdownMenu.Root>
	<DropdownMenu.Trigger
		class={buttonVariants({ variant: "ghost", class: "h-8 w-8 px-0" })}
	>
		<Globe class="h-[1.2rem] w-[1.2rem]" />
		<span class="sr-only">{$_('common.changeLanguage')}</span>
	</DropdownMenu.Trigger>
	<DropdownMenu.Content align="end">
		{#each languages as {code, label}}
			<DropdownMenu.Item onclick={() => setLanguage(code)}>
				{label}
			</DropdownMenu.Item>
		{/each}
	</DropdownMenu.Content>
</DropdownMenu.Root> 