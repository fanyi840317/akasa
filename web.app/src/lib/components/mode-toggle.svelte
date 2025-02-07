<script lang="ts">
	import Moon from "svelte-radix/Moon.svelte";
	import Sun from "svelte-radix/Sun.svelte";
	import { resetMode, setMode } from "mode-watcher";
	import { Button,buttonVariants } from "$lib/components/ui/button";
	import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
	import { _ } from 'svelte-i18n';
</script>

<DropdownMenu.Root>
	<DropdownMenu.Trigger
	  class={buttonVariants({ variant: "ghost", class: "h-8 w-8 px-0" })}
	>


	  <Sun
		class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
	  />
	  <Moon
		class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
	  />
	  <span class="sr-only">{$_('common.changeTheme')}</span>
	</DropdownMenu.Trigger>
	<DropdownMenu.Content align="end">
	  <DropdownMenu.Item onclick={() => setMode("light")}>
		{$_('theme.light')}
	  </DropdownMenu.Item>
	  <DropdownMenu.Item onclick={() => setMode("dark")}>
		{$_('theme.dark')}
	  </DropdownMenu.Item>
	  <DropdownMenu.Item onclick={() => resetMode()}>
		{$_('theme.system')}
	  </DropdownMenu.Item>
	</DropdownMenu.Content>
  </DropdownMenu.Root>
