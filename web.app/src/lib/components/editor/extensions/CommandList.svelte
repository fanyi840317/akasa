<script lang="ts">
	import { getPrevText } from '$lib/components/editor/editor.js';
	import type { CommandItemProps } from './slash-command.js';
	import { anyify } from '$lib/utils.js';
	import { toast } from 'svelte-sonner';
	import Loading from '$lib/components/Loading.svelte';
	import { Popover } from '$lib/components/ui/popover';
	import { cn } from '$lib/utils.js';
	import { onMount, afterUpdate } from 'svelte';

	export let items: CommandItemProps[] = [];
	export let editor: any;
	export let range: any;
	export let navigationKey: string = '';

	let selectedIndex = 0;
	let isLoading = false;
	let container: HTMLElement;

	// Handle navigation keys coming from parent
	$: if (navigationKey) {
		handleNavigationKey(navigationKey);
		navigationKey = ''; // Reset after handling
	}

	function handleNavigationKey(key: string) {
		if (key === 'ArrowUp') {
			selectedIndex = (selectedIndex + items.length - 1) % items.length;
			scrollSelectedItemIntoView();
		} else if (key === 'ArrowDown') {
			selectedIndex = (selectedIndex + 1) % items.length;
			scrollSelectedItemIntoView();
		}
	}

	function scrollSelectedItemIntoView() {
		if (!container) return;
		
		const item = container.querySelector(`[data-index="${selectedIndex}"]`) as HTMLElement;
		if (item) {
			item.scrollIntoView({
				block: 'nearest'
			});
		}
	}

	const selectItem = (index: number) => {
		const item = items[index];
		if (item) {
			if (item.title === 'Continue writing') {
				if (isLoading) return;
				const prevText = getPrevText(editor, {
					chars: 5000,
					offset: 1
				});
				// TODO: Implement AI completion logic here
			} else if (item.command) {
				item.command({ editor, range });
			}
		}
	};

	function handleSelectCurrentItem() {
		selectItem(selectedIndex);
	}

	onMount(() => {
		if (items.length > 0 && container) {
			const firstItem = container.querySelector('[data-index="0"]') as HTMLElement;
			if (firstItem) {
				firstItem.scrollIntoView({ block: 'nearest' });
			}
		}

		// Add event listener for select-current-item custom event
		const handleCustomEvent = () => handleSelectCurrentItem();
		container.addEventListener('select-current-item', handleCustomEvent);

		return () => {
			container.removeEventListener('select-current-item', handleCustomEvent);
		};
	});

	afterUpdate(() => {
		scrollSelectedItemIntoView();
	});
</script>

{#if items.length > 0}
	<div
		id="slash-command"
		class="z-50 h-auto max-h-[330px] w-72 overflow-y-auto rounded-md border border-stone-200 bg-white px-1 py-2 shadow-md transition-all"
		bind:this={container}
	>
		{#each items as item, index (index)}
			<button
				class="flex w-full items-center space-x-2 rounded-md px-2 py-1 text-left text-sm text-stone-900 hover:bg-stone-100 scroll-my-2
				{index === selectedIndex ? 'bg-stone-100 text-stone-900' : ''}"
				on:click={() => selectItem(index)}
				data-index={index}
				type="button"
			>
				<div
					class="flex h-10 w-10 items-center justify-center rounded-md border border-stone-200 bg-white"
				>
					{#if item.title === 'Continue writing' && isLoading}
						<Loading size="sm" />
					{:else}
						<svelte:component this={anyify(item.icon)} size="18" />
					{/if}
				</div>
				<div>
					<p class="font-medium">{item.title}</p>
					<p class="text-xs text-stone-500">{item.description}</p>
				</div>
			</button>
		{/each}
	</div>
{/if}
