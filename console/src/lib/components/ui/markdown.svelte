<script lang="ts">
	import { marked } from 'marked';
	import { cn } from '$lib/utils';

	interface Props {
		class?: string;
		children?: string;
		animated?: boolean;
	}

	let { class: className, children, animated = false }: Props = $props();

	// 解析 Markdown 内容
	const htmlContent = $derived(() => {
		if (!children) return '';
		try {
			return marked(children);
		} catch {
			return children;
		}
	});
</script>

<div
	class={cn(
		'prose dark:prose-invert max-w-none',
		animated && 'animate-pulse',
		className
	)}
>
	{@html htmlContent}
</div>