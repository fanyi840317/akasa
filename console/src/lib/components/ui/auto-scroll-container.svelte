<script lang="ts">
	import { onMount } from 'svelte';
	import { cn } from '$lib/utils';

	interface Props {
		class?: string;
		children?: any;
		// 是否启用自动滚动
		autoScroll?: boolean;
		// 滚动触发器 - 当这些值变化时触发滚动
		scrollTriggers?: any[];
		// 是否在流式响应时持续滚动
		continuousScroll?: boolean;
		// 滚动行为
		scrollBehavior?: 'smooth' | 'instant';
	}

	let { 
		class: className, 
		children,
		autoScroll = true,
		scrollTriggers = [],
		continuousScroll = false,
		scrollBehavior = 'smooth'
	}: Props = $props();

	// 滚动容器引用
	let scrollContainer: HTMLElement;
	let scrollInterval: number | null = null;

	// 滚动到底部的函数
	function scrollToBottom() {
		if (!scrollContainer) return;

		try {
			// 方法1：直接设置 scrollTop
			const scrollHeight = scrollContainer.scrollHeight;
			const clientHeight = scrollContainer.clientHeight;
			scrollContainer.scrollTop = scrollHeight - clientHeight;

			// 方法2：使用 scrollIntoView 作为备用
			const lastChild = scrollContainer.lastElementChild;
			if (lastChild) {
				lastChild.scrollIntoView({ 
					behavior: scrollBehavior, 
					block: 'end' 
				});
			}
		} catch (error) {
			console.warn('Auto scroll failed:', error);
		}
	}

	// 监听滚动触发器变化
	$effect(() => {
		if (autoScroll && scrollTriggers.length > 0) {
			// 使用 requestAnimationFrame 确保 DOM 更新完成后再滚动
			requestAnimationFrame(() => {
				scrollToBottom();
			});
		}
	});

	// 持续滚动模式
	$effect(() => {
		if (continuousScroll && autoScroll) {
			scrollInterval = setInterval(() => {
				scrollToBottom();
			}, 100);

			return () => {
				if (scrollInterval) {
					clearInterval(scrollInterval);
					scrollInterval = null;
				}
			};
		}
	});

	// 暴露滚动方法给父组件
	export function triggerScroll() {
		scrollToBottom();
	}

	// 延迟滚动方法
	export function delayedScroll(delay: number = 300) {
		requestAnimationFrame(() => {
			setTimeout(() => {
				scrollToBottom();
			}, delay);
		});
	}
</script>

<div 
	bind:this={scrollContainer} 
	class={cn('h-full w-full overflow-y-auto', className)}
>
	{@render children?.()}
</div>