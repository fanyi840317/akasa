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
		background: linear-gradient(
			to right,
			hsl(var(--foreground) / 0.3) 15%,
			hsl(var(--foreground) / 0.75) 35%,
			hsl(var(--foreground) / 0.75) 65%,
			hsl(var(--foreground) / 0.3) 85%
		);
		-webkit-background-clip: text;
		background-clip: text;
		-webkit-text-fill-color: transparent;
		text-fill-color: transparent;
		background-size: 500% auto;
		animation: textShine 2s ease-in-out infinite alternate;
	}

	@keyframes textShine {
		0% {
			background-position: 0% 50%;
		}
		100% {
			background-position: 100% 50%;
		}
	}
</style>