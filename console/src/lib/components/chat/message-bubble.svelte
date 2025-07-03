<script lang="ts">
	import type { Message } from '$lib/types/message';
	import { cn } from '$lib/utils';

	interface Props {
		class?: string;
		message: Message;
		children?: any;
	}

	let { class: className, message, children }: Props = $props();
</script>

<div
	class={cn(
		'group flex w-fit  flex-col rounded-2xl px-4 py-3 shadow-sm',
		message.role === 'user' && 'max-w-[85%] bg-primary text-primary-foreground rounded-ee-none',
		message.role === 'assistant' && 'w-full ',
		className
	)}
>
	{@render children?.()}
</div>