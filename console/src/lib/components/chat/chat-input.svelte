<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Badge } from '$lib/components/ui/badge';
	import { Send, Square, Loader2, X } from '@lucide/svelte';
	import type { Resource,Option } from '$lib/types/message';

	// Props
	interface Props {
		value?: string;
		placeholder?: string;
		disabled?: boolean;
		responding?: boolean;
		feedback?: Option;
		autoFocus?: boolean;
		class?: string;
		onSend?: (text: string, options?: { interruptFeedback?: string; resources?: Array<Resource> }) => void;
		onCancel?: () => void;
		onInput?: (text: string) => void;
		onRemoveFeedback?: () => void;
	}

	let {
		value = '',
		placeholder = 'Type your message...',
		disabled = false,
		responding = false,
		feedback = undefined,
		autoFocus = false,
		class: className = '',
		onSend,
		onCancel,
		onInput,
		onRemoveFeedback
	}: Props = $props();

	// 内部状态
	let textareaComponent: any;
	let inputValue = $state(value);
	let maxRows = 10; // 最大行数

	// 监听外部 value 变化
	$effect(() => {
		inputValue = value;
	});

	// 自动聚焦效果
	$effect(() => {
		if (autoFocus && textareaComponent) {
			textareaComponent.focus();
		}
	});
	function calculateRows(text: string): number {
		if (!text) return 2; // 默认至少2行

		// 计算换行符数量
		const newLines = (text.match(/\n/g) || []).length;

		// 估算每行平均字符数（根据实际情况调整）
		const avgCharsPerLine = 50;
		const textLines = Math.ceil(text.length / avgCharsPerLine);

		// 取换行符数量和估算行数的较大值，并确保在2-10行之间
		return Math.max(2, Math.min(maxRows, Math.max(newLines + 1, textLines)));
	}
	// 动态计算行数
	let rows = $derived(calculateRows(inputValue));

	// 处理输入变化
	function handleInput(event: Event) {
		const target = event.target as HTMLTextAreaElement;
		inputValue = target.value;
		onInput?.(inputValue);
	}

	// 处理提交
	function handleSubmit() {
		if (!inputValue.trim() || disabled || responding) return;

		const text = inputValue.trim();
		const options: { interruptFeedback?: string; resources?: Array<Resource> } = {};

		// 如果有反馈数据，添加到选项中
		if (feedback) {
			options.interruptFeedback = feedback.value;
		}

		inputValue = '';
		onSend?.(text, options);
	}

	// 处理取消
	function handleCancel() {
		onCancel?.();
	}

	// 处理移除反馈
	function handleRemoveFeedback() {
		onRemoveFeedback?.();
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
		textareaComponent?.element?.focus();
	}

	// 导出方法给父组件使用
	export { focus };
</script>

<div class="rounded-2xl p-2 bg-card border {className}">
	<!-- 反馈显示区域 -->
	{#if feedback}
		<div class="mb-2 flex items-center justify-between rounded-lg bg-muted p-2">
			<div class="flex items-center gap-2">
				<Badge variant="secondary" class="text-xs">
					{feedback.value === 'accept' ? '✓ Accepted' : '✗ Rejected'}
				</Badge>
				<span class="text-sm text-muted-foreground">
					{feedback.text || 'Feedback provided'}
				</span>
			</div>
			<Button size="sm" variant="ghost" onclick={handleRemoveFeedback} title="Remove feedback">
				<X class="h-3 w-3" />
			</Button>
		</div>
	{/if}

	<div class="relative">
		<!-- 文本输入区域 -->
		<textarea
			bind:this={textareaComponent}
			value={inputValue}
			{placeholder}
			{disabled}
			rows={rows}
			class="w-full min-h-10 resize-none p-2 pr-12 
			focus:outline-none bg-transparent border-none
			{responding ? 'opacity-75' : ''}"
			oninput={handleInput}
			onkeydown={handleKeydown}
		></textarea>

		<!-- 提交/停止按钮 -->
		<div class="absolute bottom-2 right-2">
			{#if responding}
				<Button size="sm" variant="destructive" onclick={handleCancel} title="Cancel generation">
					<Square class="h-4 w-4" />
				</Button>
			{:else}
				<Button
					size="sm"
					disabled={disabled || !inputValue.trim()}
					onclick={handleSubmit}
					title="Send message (Enter)"
				>
					<Send class="h-4 w-4" />
				</Button>
			{/if}
		</div>
	</div>

	<!-- 提示信息 -->
	<div class="text-muted-foreground mt-2 flex items-center justify-between text-xs">
		<div class="flex items-center gap-2">
			{#if responding}
				<Badge variant="secondary" class="text-xs">
					<Loader2 class="mr-1 h-3 w-3 animate-spin" />
					Generating...
				</Badge>
			{/if}
			{#if feedback}
				<Badge variant="outline" class="text-xs">
					With feedback
				</Badge>
			{/if}
		</div>

		<div>
			Press <kbd class="bg-muted rounded px-1 py-0.5 text-xs">Enter</kbd> to send,
			<kbd class="bg-muted rounded px-1 py-0.5 text-xs">Shift+Enter</kbd> for new line
		</div>
	</div>
</div>

