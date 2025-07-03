<script lang="ts">
	import { cn } from '$lib/utils';
	import { fly } from 'svelte/transition';

	interface Props {
		class?: string;
		children?: any;
	}

	let { class: className, children }: Props = $props();
</script>

<span
	class={cn(
		'relative flex h-[2em] items-center overflow-hidden',
		className
	)}
>
	{#key children}
		<div
			class="absolute w-fit"
			in:fly={{ y: 20, duration: 300 }}
			out:fly={{ y: -20, duration: 300 }}
		>
			{@render children?.()}
		</div>
	{/key}
</span>