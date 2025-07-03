<script lang="ts">
	import { cn } from '$lib/utils';

	interface Props {
		class?: string;
		size?: 'normal' | 'sm';
	}

	let { class: className, size = 'normal' }: Props = $props();
</script>

<div
	class={cn(
		'flex',
		className
	)}
>
	<div
		class={cn(
			'rounded-full bg-muted-foreground/60 opacity-100 animate-bounce',
			size === 'sm' ? 'w-1.5 h-1.5 mx-0.5' : 'w-2 h-2 mx-1'
		)}
		style="animation-delay: 0s;"
	></div>
	<div
		class={cn(
			'rounded-full bg-muted-foreground/60 opacity-100 animate-bounce',
			size === 'sm' ? 'w-1.5 h-1.5 mx-0.5' : 'w-2 h-2 mx-1'
		)}
		style="animation-delay: 0.2s;"
	></div>
	<div
		class={cn(
			'rounded-full bg-muted-foreground/60 opacity-100 animate-bounce',
			size === 'sm' ? 'w-1.5 h-1.5 mx-0.5' : 'w-2 h-2 mx-1'
		)}
		style="animation-delay: 0.4s;"
	></div>
</div>

<style>
	@keyframes bounce {
		0%, 80%, 100% {
			transform: scale(0);
			opacity: 0.5;
		}
		40% {
			transform: scale(1);
			opacity: 1;
		}
	}

	.animate-bounce {
		animation: bounce 1.4s infinite ease-in-out;
	}
</style>