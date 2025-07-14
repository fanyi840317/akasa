<script lang="ts">
	import { marked } from 'marked';
	import { cn } from '$lib/utils';

	interface Props {
		class?: string;
		content?: string;
		animated?: boolean;
	}

	let { class: className, content, animated = false }: Props = $props();

	// 解析 Markdown 内容
	const htmlContent = $derived.by(() => {
		if (!content) return '';
		try {
			return marked(content);
		} catch {
			return content;
		}
	});
</script>

<div
	class={cn(
		'text-foreground max-w-none',
		'[&_h1]:text-2xl [&_h1]:font-bold [&_h1]:mb-4 [&_h1]:mt-6',
		'[&_h2]:text-xl [&_h2]:font-semibold [&_h2]:mb-3 [&_h2]:mt-5',
		'[&_h3]:text-lg [&_h3]:font-semibold [&_h3]:mb-2 [&_h3]:mt-4',
		'[&_h4]:text-base [&_h4]:font-medium [&_h4]:mb-2 [&_h4]:mt-3',
		'[&_h5]:text-sm [&_h5]:font-medium [&_h5]:mb-1 [&_h5]:mt-2',
		'[&_h6]:text-sm [&_h6]:font-normal [&_h6]:text-muted-foreground [&_h6]:mb-1 [&_h6]:mt-2',
		'[&_p]:leading-relaxed [&_p]:text-sm [&_p]:mb-3',
		'[&_strong]:font-bold',
		'[&_em]:italic',
		'[&_code]:bg-accent [&_code]:text-accent-foreground [&_code]:px-2 [&_code]:py-1 [&_code]:rounded [&_code]:text-xs [&_code]:font-mono',
		'[&_pre]:bg-accent [&_pre]:text-accent-foreground [&_pre]:border [&_pre]:rounded-lg [&_pre]:p-4 [&_pre]:mb-4',
		'[&_blockquote]:border-l-4 [&_blockquote]:border-l-primary [&_blockquote]:bg-accent/50 [&_blockquote]:pl-4 [&_blockquote]:py-3 [&_blockquote]:italic [&_blockquote]:mb-4',
		'[&_ul]:space-y-1 [&_ol]:space-y-1 [&_ul]:mb-4 [&_ol]:mb-4',
		'[&_li]:text-sm',
		'[&_a]:text-primary [&_a]:font-medium [&_a]:no-underline hover:[&_a]:underline hover:[&_a]:text-primary/80',
		'[&_hr]:border-border [&_hr]:my-6',
		'[&_table]:mb-4',
		'[&_th]:bg-accent [&_th]:font-semibold [&_th]:border [&_th]:border-border [&_th]:p-2',
		'[&_td]:border [&_td]:border-border [&_td]:p-2',
		animated && 'animate-pulse',
		className
	)}
>
	{@html htmlContent}
</div>