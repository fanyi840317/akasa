<script lang="ts">
	import { cn } from '$lib/utils';

	interface Props {
		class?: string;
		animated?: boolean;
		children?: any;
	}

	let { class: className, animated = false, children }: Props = $props();
</script>

<span
	class={cn(
		animated && 'rainbow-text-animated',
		className
	)}
>
	{@render children?.()}
</span>

<style>
	.rainbow-text-animated {
		color: hsl(var(--foreground));
		opacity: 0.8;
		animation: textPulse 2s ease-in-out infinite alternate;
	}

	@keyframes textPulse {
		0% {
			opacity: 0.6;
		}
		100% {
			opacity: 1;
		}
	}
</style>