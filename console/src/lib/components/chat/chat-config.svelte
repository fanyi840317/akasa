<script lang="ts">
	import type { ChatConfig } from '$lib/stores/chat.svelte';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Label } from '$lib/components/ui/label';
	import { Switch } from '$lib/components/ui/switch';
	import { Slider } from '$lib/components/ui/slider';
	import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '$lib/components/ui/select';
	import { Settings, RotateCcw } from '@lucide/svelte';

	// Props
	interface Props {
		config: ChatConfig;
		onConfigChange?: (config: ChatConfig) => void;
		onReset?: () => void;
	}

	let {
		config,
		onConfigChange,
		onReset
	}: Props = $props();

	// 内部状态
	let localConfig = $state({ ...config });

	// 监听外部配置变化
	$effect(() => {
		localConfig = { ...config };
	});

	// 更新配置
	function updateConfig(updates: Partial<ChatConfig>) {
		localConfig = { ...localConfig, ...updates };
		onConfigChange?.(localConfig);
	}

	// 重置配置
	function handleReset() {
		onReset?.();
	}

	// 处理开关变化
	function handleSwitchChange(key: keyof ChatConfig, value: boolean) {
		updateConfig({ [key]: value });
	}

	// 处理滑块变化
	function handleSliderChange(key: keyof ChatConfig, values: number[]) {
		updateConfig({ [key]: values[0] });
	}

	// 处理选择变化
	function handleSelectChange(key: keyof ChatConfig, value: string) {
		updateConfig({ [key]: value });
	}
</script>

<Card class="chat-config">
	<CardHeader class="pb-3">
		<div class="flex items-center justify-between">
			<CardTitle class="flex items-center gap-2 text-base">
				<Settings class="w-4 h-4" />
				Chat Configuration
			</CardTitle>
			<Button
				variant="ghost"
				size="sm"
				onclick={handleReset}
				title="Reset to defaults"
			>
				<RotateCcw class="w-4 h-4" />
			</Button>
		</div>
	</CardHeader>
	
	<CardContent class="space-y-6">
		<!-- Deep Thinking -->
		<div class="space-y-2">
			<div class="flex items-center justify-between">
				<Label for="deep-thinking" class="text-sm font-medium">
					Deep Thinking
				</Label>
				<Switch
					id="deep-thinking"
					checked={localConfig.deepThinking}
					onCheckedChange={(checked) => handleSwitchChange('deepThinking', checked)}
				/>
			</div>
			<p class="text-xs text-muted-foreground">
				Enable detailed reasoning process for complex queries
			</p>
		</div>

		<!-- Background Investigation -->
		<div class="space-y-2">
			<div class="flex items-center justify-between">
				<Label for="background-investigation" class="text-sm font-medium">
					Background Investigation
				</Label>
				<Switch
					id="background-investigation"
					checked={localConfig.backgroundInvestigation}
					onCheckedChange={(checked) => handleSwitchChange('backgroundInvestigation', checked)}
				/>
			</div>
			<p class="text-xs text-muted-foreground">
				Perform background research before responding
			</p>
		</div>

		<!-- Plan Iterations -->
		<div class="space-y-3">
			<Label class="text-sm font-medium">Plan Iterations</Label>
			<div class="space-y-2">
				<Slider
					value={[localConfig.planIterations]}
					min={1}
					max={10}
					step={1}
					onValueChange={(values) => handleSliderChange('planIterations', values)}
					class="w-full"
				/>
				<div class="flex justify-between text-xs text-muted-foreground">
					<span>1</span>
					<span class="font-medium">{localConfig.planIterations}</span>
					<span>10</span>
				</div>
			</div>
			<p class="text-xs text-muted-foreground">
				Number of planning iterations for complex tasks
			</p>
		</div>

		<!-- Temperature -->
		<div class="space-y-3">
			<Label class="text-sm font-medium">Temperature</Label>
			<div class="space-y-2">
				<Slider
					value={[localConfig.temperature]}
					min={0}
					max={2}
					step={0.1}
					onValueChange={(values) => handleSliderChange('temperature', values)}
					class="w-full"
				/>
				<div class="flex justify-between text-xs text-muted-foreground">
					<span>0.0</span>
					<span class="font-medium">{localConfig.temperature.toFixed(1)}</span>
					<span>2.0</span>
				</div>
			</div>
			<p class="text-xs text-muted-foreground">
				Controls randomness in responses (0 = deterministic, 2 = very creative)
			</p>
		</div>

		<!-- Max Tokens -->
		<div class="space-y-3">
			<Label class="text-sm font-medium">Max Tokens</Label>
			<div class="space-y-2">
				<Slider
					value={[localConfig.maxTokens]}
					min={100}
					max={4000}
					step={100}
					onValueChange={(values) => handleSliderChange('maxTokens', values)}
					class="w-full"
				/>
				<div class="flex justify-between text-xs text-muted-foreground">
					<span>100</span>
					<span class="font-medium">{localConfig.maxTokens}</span>
					<span>4000</span>
				</div>
			</div>
			<p class="text-xs text-muted-foreground">
				Maximum number of tokens in the response
			</p>
		</div>

		<!-- Model Selection -->
		<div class="space-y-2">
			<Label class="text-sm font-medium">Model</Label>
			<Select
				value={localConfig.model}
				onValueChange={(value) => handleSelectChange('model', value)}
			>
				<SelectTrigger>
					<SelectValue placeholder="Select a model" />
				</SelectTrigger>
				<SelectContent>
					<SelectItem value="gpt-4-turbo">GPT-4 Turbo</SelectItem>
					<SelectItem value="gpt-4">GPT-4</SelectItem>
					<SelectItem value="gpt-3.5-turbo">GPT-3.5 Turbo</SelectItem>
					<SelectItem value="claude-3-opus">Claude 3 Opus</SelectItem>
					<SelectItem value="claude-3-sonnet">Claude 3 Sonnet</SelectItem>
					<SelectItem value="claude-3-haiku">Claude 3 Haiku</SelectItem>
				</SelectContent>
			</Select>
			<p class="text-xs text-muted-foreground">
				Choose the AI model for chat responses
			</p>
		</div>

		<!-- Stream Response -->
		<div class="space-y-2">
			<div class="flex items-center justify-between">
				<Label for="stream-response" class="text-sm font-medium">
					Stream Response
				</Label>
				<Switch
					id="stream-response"
					checked={localConfig.streamResponse}
					onCheckedChange={(checked) => handleSwitchChange('streamResponse', checked)}
				/>
			</div>
			<p class="text-xs text-muted-foreground">
				Show responses as they are generated in real-time
			</p>
		</div>
	</CardContent>
</Card>

<style>
	.chat-config :global(.slider-track) {
		@apply bg-muted;
	}
	
	.chat-config :global(.slider-range) {
		@apply bg-primary;
	}
	
	.chat-config :global(.slider-thumb) {
		@apply bg-primary border-primary;
	}
</style>