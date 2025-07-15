<script lang="ts">
	import { cn } from '$lib/utils';

	interface Props {
		class?: string;
		url: string;
		title?: string;
	}

	let { class: className, url, title }: Props = $props();

	let imgSrc = $state(new URL(url).origin + '/favicon.ico');

	function handleError() {
		imgSrc = 'https://perishablepress.com/wp/wp-content/images/2021/favicon-standard.png';
	}
</script>

<img
	class={cn('bg-accent h-4 w-4 rounded-sm shadow-sm', className)}
	width={16}
	height={16}
	src={imgSrc}
	alt={title}
	onerror={handleError}
/>