<script lang="ts">
	interface Props {
		text?: string;
		size?: 'sm' | 'md' | 'lg';
		class?: string;
	}

	let { text = '加载中...', size = 'md', class: className = '' }: Props = $props();

	const sizeClasses = {
		sm: 'h-4 w-4',
		md: 'h-8 w-8',
		lg: 'h-12 w-12'
	};
</script>

<div class="flex-center size-full {className}">
	<div class="text-center">
		<div class="animate-spin rounded-full {sizeClasses[size]} border-b-2 border-primary mx-auto mb-2"></div>
		<p class="text-sm text-muted-foreground">{text}</p>
	</div>
</div>