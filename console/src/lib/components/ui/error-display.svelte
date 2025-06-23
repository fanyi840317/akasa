<script lang="ts">
	import { Button } from '$lib/components/ui/button';

	interface Props {
		title?: string;
		message: string;
		showRetry?: boolean;
		retryText?: string;
		onRetry?: () => void;
	}

	let {
		title = 'Error',
		message,
		showRetry = false,
		retryText = 'Try Again',
		onRetry
	}: Props = $props();
</script>

<div class="flex items-center justify-center py-12">
	<div class="text-center">
		<p class="text-destructive mb-2">{title}</p>
		<p class="text-sm text-muted-foreground mb-4">{message}</p>
		{#if showRetry && onRetry}
			<Button onclick={onRetry}>{retryText}</Button>
		{/if}
	</div>
</div>