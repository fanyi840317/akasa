<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Badge } from '$lib/components/ui/badge';
	import { Send, Square, Loader2 } from '@lucide/svelte';

	// Props
	interface Props {
		value?: string;
		placeholder?: string;
		disabled?: boolean;
		isStreaming?: boolean;
		onSubmit?: (text: string) => void;
		onStop?: () => void;
		onInput?: (text: string) => void;
	}

	let {
		value = '',
		placeholder = 'Type your message...',
		disabled = false,
		isStreaming = false,
		onSubmit,
		onStop,
		onInput
	}: Props = $props();

	// 内部状态
	let textareaElement: HTMLTextAreaElement;
	let inputValue = $state(value);

	// 监听外部 value 变化
	$effect(() => {
		inputValue = value;
	});

	// 动态计算行数
	const rows = $derived(() => {
		if (!inputValue) return 1;
		const lines = inputValue.split('\n').length;
		return Math.min(Math.max(lines, 1), 10);
	});

	// 处理输入变化
	function handleInput(event: Event) {
		const target = event.target as HTMLTextAreaElement;
		inputValue = target.value;
		onInput?.(inputValue);
	}

	// 处理提交
	function handleSubmit() {
		if (!inputValue.trim() || disabled || isStreaming) return;
		
		const text = inputValue.trim();
		inputValue = '';
		onSubmit?.(text);
	}

	// 处理停止
	function handleStop() {
		onStop?.();
	}

	// 处理键盘事件
	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			handleSubmit();
		}
	}

	// 聚焦到输入框
	function focus() {
		textareaElement?.focus();
	}

	// 导出方法
	const api = {
		focus
	};
</script>

<div class="chat-input">
	<div class="relative">
		<!-- 文本输入区域 -->
		<Textarea
			bind:this={textareaElement}
			value={inputValue}
			placeholder={placeholder}
			disabled={disabled}
			rows={rows}
			class="min-h-[44px] max-h-[240px] resize-none pr-12 {isStreaming ? 'opacity-75' : ''}"
			oninput={handleInput}
			onkeydown={handleKeydown}
		/>

		<!-- 提交/停止按钮 -->
		<div class="absolute bottom-2 right-2">
			{#if isStreaming}
				<Button
					size="sm"
					variant="destructive"
					onclick={handleStop}
					title="Stop generation"
				>
					<Square class="w-4 h-4" />
				</Button>
			{:else}
				<Button
					size="sm"
					disabled={disabled || !inputValue.trim()}
					onclick={handleSubmit}
					title="Send message (Enter)"
				>
					<Send class="w-4 h-4" />
				</Button>
			{/if}
		</div>
	</div>

	<!-- 提示信息 -->
	<div class="flex items-center justify-between mt-2 text-xs text-muted-foreground">
		<div class="flex items-center gap-2">
			{#if isStreaming}
				<Badge variant="secondary" class="text-xs">
					<Loader2 class="w-3 h-3 animate-spin mr-1" />
					Generating...
				</Badge>
			{/if}
		</div>
		
		<div>
			Press <kbd class="px-1 py-0.5 bg-muted rounded text-xs">Enter</kbd> to send, 
			<kbd class="px-1 py-0.5 bg-muted rounded text-xs">Shift+Enter</kbd> for new line
		</div>
	</div>
</div>

<style>
	.chat-input :global(textarea) {
		@apply transition-all duration-200;
	}
	
	.chat-input :global(textarea:focus) {
		@apply ring-2 ring-primary/20;
	}
	
	kbd {
		@apply font-mono;
	}
</style>