<script lang="ts">
	import { cn } from '$lib/utils';
	import { Globe, Search, User, FileText, Heading, Sparkles, Save, ArrowUp, Bot } from '@lucide/svelte';
	import { Card } from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';

	let showAITools = $state(false);
	let rows = $state(2); // 初始行数
	let maxRows = 10; // 最大行数
	let isProcessing = $state(false);

	// 添加属性
	let {
		disabled = false,
		placeholder = 'Ask anything',
		inputValue = $bindable(''),
		class: className,
		onSubmit,
		onSuggestionClick,
		suggestions = [],
		showRemind = $bindable(false),
		models = [],
		selectedModel = $bindable(''),
		onModelChange
	} = $props<{
		class?: string;
		disabled?: boolean;
		placeholder?: string;
		inputValue?: string;
		onSubmit?: (text: string) => void;
		onSuggestionClick?: (suggestion: string) => void;
		suggestions?: string[];
		showRemind?: boolean;
		models?: Array<{id: string, name: string}>;
		selectedModel?: string;
		onModelChange?: (modelId: string) => void;
	}>();

	// 根据内容计算行数
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

	// 监听输入值变化，更新行数
	$effect(() => {
		rows = calculateRows(inputValue);
	});
</script>

<div class={cn('flex-end flex-col', className)}>
	
	<div class="w-full rounded-2xl p-2 bg-card border">
		<form>
			<textarea
				{rows}
				{placeholder}
				class="p-2 w-full h-full resize-none focus:outline-none bg-transparent"
				bind:value={inputValue}
				{disabled}
				oninput={() => (rows = calculateRows(inputValue))}
			>
			</textarea>
		</form>
		<!-- 按钮组 -->
		<div class="flex-between px-2">
			<!-- 左侧按钮组 -->
			<div class="flex-center gap-2">
				<!-- 模型选择下拉菜单 -->
				<DropdownMenu.Root>
					<DropdownMenu.Trigger>
						<Button
							variant="ghost"
							title="选择模型"
							disabled={models.length === 0}
						>
							<Bot class="w-5 h-5" />
						</Button>
					</DropdownMenu.Trigger>
					<DropdownMenu.Content class="w-56 rounded-[16px]" align="start">
						<DropdownMenu.Label>选择模型</DropdownMenu.Label>
						<DropdownMenu.Separator />
						{#each models as model}
							<DropdownMenu.Item
								onclick={() => {
									selectedModel = model.id;
									onModelChange?.(model.id);
								}}
								class={selectedModel === model.id ? 'bg-accent' : ''}
							>
								{model.name}
								{#if selectedModel === model.id}
									<span class="ml-auto">✓</span>
								{/if}
							</DropdownMenu.Item>
						{/each}
						{#if models.length === 0}
							<DropdownMenu.Item disabled>
								暂无可用模型
							</DropdownMenu.Item>
						{/if}
					</DropdownMenu.Content>
				</DropdownMenu.Root>

				<!-- 搜索建议下拉菜单 -->
				<DropdownMenu.Root>
					<DropdownMenu.Trigger>
						<Button
							variant="ghost"
							title="建议"
							disabled={suggestions.length === 0}
						>
							<Globe class="w-5 h-5" />
						</Button>
					</DropdownMenu.Trigger>
					<DropdownMenu.Content class="w-56 rounded-[16px]" align="start">
						<DropdownMenu.Label>建议</DropdownMenu.Label>
						<DropdownMenu.Separator />
						{#each suggestions as suggestion}
							<DropdownMenu.Item
								onclick={() => {
									onSuggestionClick?.(suggestion);
								}}
							>
								{suggestion}
							</DropdownMenu.Item>
						{/each}
						{#if suggestions.length === 0}
							<DropdownMenu.Item disabled>
								暂无建议
							</DropdownMenu.Item>
						{/if}
					</DropdownMenu.Content>
				</DropdownMenu.Root>
			</div>

			<!-- 右侧功能按钮组 -->
			<div class="flex gap-2">
					<!-- AI工具按钮 -->
				<Button
					variant="ghost"
					onclick={() => {
						showAITools = !showAITools;
					}}
					title="AI工具"
					disabled={isProcessing}
				>
					<Sparkles />
				</Button>
				<!-- 生成按钮 -->
				<Button
					variant="secondary"
					size="icon"
					onclick={() => {
						if (onSubmit) {
							onSubmit(inputValue);
						}
					}}
					disabled={disabled || isProcessing}
				>
					{#if isProcessing}
						<Save class="w-5 h-5 animate-spin" />
					{:else}
						<ArrowUp></ArrowUp>
					{/if}
					<!-- {isProcessing ? '处理中...' : 'Generate'} -->
				</Button>
			</div>
		</div>
	</div>

	<!-- AI工具面板 -->

	{#if showRemind}
		<p class="text-xs text-foreground/40 text-center mt-1">Akasa AI. 回答可能不准确或不完整。</p>
	{/if}
</div>
