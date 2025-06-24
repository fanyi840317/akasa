<script lang="ts">
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { toast } from 'svelte-sonner';
	import type { Agent, UpdateAgentRequest, LLMConfig } from '$lib/types/agent.js';
	import { AgentType, AgentStatus, LLMProvider } from '$lib/types/agent.js';
	import { agentStore } from '$lib/stores/agent.svelte.js';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import * as Select from '$lib/components/ui/select';
	import { Badge } from '$lib/components/ui/badge';
	import { Separator } from '$lib/components/ui/separator';
	import { ArrowLeft, Save, Settings, Bot, Tag, X } from '@lucide/svelte';

	// Get agent ID from URL
	const agentId = $page.params.id;

	// State
	let agent = $state<Agent | null>(null);
	let loading = $state(true);
	let saving = $state(false);
	let errors = $state<Record<string, string>>({});

	// Form data
	let formData = $state({
		name: '',
		type: AgentType.REPORT_GENERATOR,
		description: '',
		prompt: '',
		tags: [] as string[],
		status: AgentStatus.DRAFT,
		llmConfig: {
			provider: LLMProvider.OPENAI,
			model: 'gpt-4',
			temperature: 0.7,
			maxTokens: 2000,
			topP: 1,
			frequencyPenalty: 0,
			presencePenalty: 0
		} as LLMConfig
	});

	let tagInput = $state('');

	// Load agent data
	onMount(async () => {
		try {
			const loadedAgent = await agentStore.loadAgent(agentId);
			// if (loadedAgent) {
			// 	agent = loadedAgent;
			// 	formData = {
			// 		name: loadedAgent.name,
			// 		type: loadedAgent.type,
			// 		description: loadedAgent.description || '',
			// 		prompt: loadedAgent.prompt || '',
			// 		tags: loadedAgent.tags || [],
			// 		status: loadedAgent.status,
			// 		llmConfig: loadedAgent.llmConfig || {
			// 			provider: LLMProvider.OPENAI,
			// 			model: 'gpt-4',
			// 			temperature: 0.7,
			// 			maxTokens: 2000,
			// 			topP: 1,
			// 			frequencyPenalty: 0,
			// 			presencePenalty: 0
			// 		}
			// 	};
			// } else {
			// 	toast.error('Agent not found');
			// 	goto('/console/agents');
			// }
		} catch (error) {
			toast.error('Failed to load agent');
			goto('/console/agents');
		} finally {
			loading = false;
		}
	});

	// Validation
	const validateForm = () => {
		const newErrors: Record<string, string> = {};

		if (!formData.name.trim()) {
			newErrors.name = '名称是必填项';
		}

		if (!formData.prompt.trim()) {
			newErrors.prompt = '指令是必填项';
		}

		if (formData.llmConfig.temperature !== undefined && 
			(formData.llmConfig.temperature < 0 || formData.llmConfig.temperature > 2)) {
			newErrors.temperature = '温度值必须在 0 到 2 之间';
		}

		if (formData.llmConfig.maxTokens && 
			(formData.llmConfig.maxTokens < 1 || formData.llmConfig.maxTokens > 100000)) {
			newErrors.maxTokens = '最大令牌数必须在 1 到 100,000 之间';
		}

		errors = newErrors;
		return Object.keys(newErrors).length === 0;
	};

	// Save agent
	const handleSave = async () => {
		if (!validateForm()) return;

		saving = true;
		try {
			const updateData: UpdateAgentRequest = {
				name: formData.name.trim(),
				type: formData.type,
				description: formData.description.trim() || undefined,
				prompt: formData.prompt.trim(),
				tags: formData.tags.length > 0 ? formData.tags : undefined,
				status: formData.status,
				llmConfig: formData.llmConfig
			};

			await agentStore.updateAgent(agentId, updateData);
			toast.success('Agent 已保存');
		} catch (error) {
			toast.error('保存失败: ' + (error instanceof Error ? error.message : '未知错误'));
		} finally {
			saving = false;
		}
	};

	// Tag management
	const addTag = () => {
		const tag = tagInput.trim();
		if (tag && !formData.tags.includes(tag)) {
			formData.tags = [...formData.tags, tag];
			tagInput = '';
		}
	};

	const removeTag = (index: number) => {
		formData.tags = formData.tags.filter((_, i) => i !== index);
	};

	const handleTagKeydown = (event: KeyboardEvent) => {
		if (event.key === 'Enter') {
			event.preventDefault();
			addTag();
		}
	};

	// Get model options based on provider
	const getModelOptions = (provider: LLMProvider) => {
		switch (provider) {
			case LLMProvider.OPENAI:
				return ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo', 'gpt-4o', 'gpt-4o-mini'];
			case LLMProvider.ANTHROPIC:
				return ['claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku', 'claude-3-5-sonnet'];
			case LLMProvider.GOOGLE:
				return ['gemini-pro', 'gemini-pro-vision', 'gemini-1.5-pro', 'gemini-1.5-flash'];
			case LLMProvider.OLLAMA:
				return ['llama2', 'llama3', 'mistral', 'codellama', 'phi3'];
			default:
				return [];
		}
	};

	// Update model when provider changes
	$effect(() => {
		const models = getModelOptions(formData.llmConfig.provider);
		if (models.length > 0 && !models.includes(formData.llmConfig.model)) {
			formData.llmConfig.model = models[0];
		}
	});

	// Agent type options
	const agentTypeOptions = [
		{ value: AgentType.MYSTERY_RESEARCHER, label: '神秘研究员' },
		{ value: AgentType.ACADEMIC_RESEARCHER, label: '学术研究员' },
		{ value: AgentType.CORRELATION_ANALYZER, label: '关联分析师' },
		{ value: AgentType.REPORT_GENERATOR, label: '报告生成器' },
		{ value: AgentType.DATA_ANALYST, label: '数据分析师' },
		{ value: AgentType.CONTENT_CREATOR, label: '内容创作者' },
		{ value: AgentType.STRATEGY_ADVISOR, label: '策略顾问' }
	];

	// Status options
	const statusOptions = [
		{ value: AgentStatus.DRAFT, label: '草稿' },
		{ value: AgentStatus.ACTIVE, label: '活跃' },
		{ value: AgentStatus.INACTIVE, label: '非活跃' },
		{ value: AgentStatus.ARCHIVED, label: '已归档' }
	];

	// Provider options
	const providerOptions = [
		{ value: LLMProvider.OPENAI, label: 'OpenAI' },
		{ value: LLMProvider.ANTHROPIC, label: 'Anthropic' },
		{ value: LLMProvider.GOOGLE, label: 'Google' },
		{ value: LLMProvider.OLLAMA, label: 'Ollama' }
	];
</script>

<svelte:head>
	<title>编辑 Agent - {formData.name || 'Loading...'}</title>
</svelte:head>

{#if loading}
	<div class="flex items-center justify-center min-h-[400px]">
		<div class="text-center">
			<Bot class="h-8 w-8 animate-spin mx-auto mb-2" />
			<p class="text-muted-foreground">加载 Agent 信息中...</p>
		</div>
	</div>
{:else}
	<div class="container mx-auto p-6 max-w-4xl">
		<!-- Header -->
		<div class="flex items-center gap-4 mb-6">
			<Button variant="ghost" size="sm" onclick={() => goto('/console/agents')}>
				<ArrowLeft class="h-4 w-4" />
				返回
			</Button>
			<div class="flex-1">
				<h1 class="text-2xl font-bold flex items-center gap-2">
					<Bot class="h-6 w-6" />
					编辑 Agent
				</h1>
				<p class="text-muted-foreground">修改 Agent 的配置和行为</p>
			</div>
			<Button onclick={handleSave} disabled={saving}>
				<Save class="h-4 w-4 mr-2" />
				{saving ? '保存中...' : '保存'}
			</Button>
		</div>

		<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
			<!-- Main Content -->
			<div class="lg:col-span-2 space-y-6">
				<!-- Basic Information -->
				<Card>
					<CardHeader>
						<CardTitle class="flex items-center gap-2">
							<Bot class="h-5 w-5" />
							基本信息
						</CardTitle>
					</CardHeader>
					<CardContent class="space-y-4">
						<!-- Name -->
						<div class="space-y-2">
							<Label for="name">名称 *</Label>
							<Input
								id="name"
								bind:value={formData.name}
								placeholder="给你的 agent 一个名称"
								class={errors.name ? 'border-destructive' : ''}
							/>
							{#if errors.name}
								<p class="text-sm text-destructive">{errors.name}</p>
							{/if}
						</div>

						<!-- Type -->
						<div class="space-y-2">
							<Label for="type">处理</Label>
							<Select.Root
								selected={{ value: formData.type, label: agentTypeOptions.find(opt => opt.value === formData.type)?.label || '' }}
								onSelectedChange={(v) => v && (formData.type = v.value as AgentType)}
							>
								<Select.Trigger>
									<Select.Value placeholder="选择 Agent 类型" />
								</Select.Trigger>
								<Select.Content>
									{#each agentTypeOptions as option}
										<Select.Item value={option.value}>{option.label}</Select.Item>
									{/each}
								</Select.Content>
							</Select.Root>
						</div>

						<!-- Description -->
						<div class="space-y-2">
							<Label for="description">描述</Label>
							<Textarea
								id="description"
								bind:value={formData.description}
								placeholder="描述这个 agent 将帮助你的团队做什么"
								rows={3}
							/>
						</div>
					</CardContent>
				</Card>

				<!-- Instructions -->
				<Card>
					<CardHeader>
						<CardTitle>指令</CardTitle>
						<p class="text-sm text-muted-foreground">
							通过添加自定义指令来控制你的 agent 行为
						</p>
					</CardHeader>
					<CardContent>
						<div class="space-y-2">
							<Textarea
								bind:value={formData.prompt}
								placeholder='例如："回答所有西班牙语问题" 或 "始终遵循我们特定的语音指南"'
								rows={8}
								class={errors.prompt ? 'border-destructive' : ''}
							/>
							{#if errors.prompt}
								<p class="text-sm text-destructive">{errors.prompt}</p>
							{/if}
						</div>
					</CardContent>
				</Card>
			</div>

			<!-- Sidebar -->
			<div class="space-y-6">
				<!-- Status -->
				<Card>
					<CardHeader>
						<CardTitle class="text-lg">状态</CardTitle>
					</CardHeader>
					<CardContent>
						<Select.Root
							selected={{ value: formData.status, label: statusOptions.find(opt => opt.value === formData.status)?.label || '' }}
							onSelectedChange={(v) => v && (formData.status = v.value as AgentStatus)}
						>
							<Select.Trigger>
								<Select.Value placeholder="选择状态" />
							</Select.Trigger>
							<Select.Content>
								{#each statusOptions as option}
									<Select.Item value={option.value}>{option.label}</Select.Item>
								{/each}
							</Select.Content>
						</Select.Root>
					</CardContent>
				</Card>

				<!-- Tags -->
				<Card>
					<CardHeader>
						<CardTitle class="flex items-center gap-2 text-lg">
							<Tag class="h-4 w-4" />
							标签
						</CardTitle>
					</CardHeader>
					<CardContent class="space-y-3">
						<!-- Tag Input -->
						<div class="flex gap-2">
							<Input
								bind:value={tagInput}
								placeholder="添加标签"
								onkeydown={handleTagKeydown}
								class="flex-1"
							/>
							<Button size="sm" onclick={addTag} disabled={!tagInput.trim()}>
								添加
							</Button>
						</div>

						<!-- Tag List -->
						{#if formData.tags.length > 0}
							<div class="flex flex-wrap gap-2">
								{#each formData.tags as tag, index}
									<Badge variant="secondary" class="flex items-center gap-1">
										{tag}
										<button
											type="button"
											onclick={() => removeTag(index)}
											class="ml-1 hover:bg-destructive/20 rounded-full p-0.5"
										>
											<X class="h-3 w-3" />
										</button>
									</Badge>
								{/each}
							</div>
						{/if}
					</CardContent>
				</Card>

				<!-- LLM Configuration -->
				<Card>
					<CardHeader>
						<CardTitle class="flex items-center gap-2 text-lg">
							<Settings class="h-4 w-4" />
							LLM 配置
						</CardTitle>
					</CardHeader>
					<CardContent class="space-y-4">
						<!-- Provider -->
						<div class="space-y-2">
							<Label>提供商</Label>
							<Select.Root
								selected={{ value: formData.llmConfig.provider, label: providerOptions.find(opt => opt.value === formData.llmConfig.provider)?.label || '' }}
								onSelectedChange={(v) => v && (formData.llmConfig.provider = v.value as LLMProvider)}
							>
								<Select.Trigger>
									<Select.Value placeholder="选择提供商" />
								</Select.Trigger>
								<Select.Content>
									{#each providerOptions as option}
										<Select.Item value={option.value}>{option.label}</Select.Item>
									{/each}
								</Select.Content>
							</Select.Root>
						</div>

						<!-- Model -->
						<div class="space-y-2">
							<Label>模型</Label>
							<Select.Root
								selected={{ value: formData.llmConfig.model, label: formData.llmConfig.model }}
								onSelectedChange={(v) => v && (formData.llmConfig.model = v.value)}
							>
								<Select.Trigger>
									<Select.Value placeholder="选择模型" />
								</Select.Trigger>
								<Select.Content>
									{#each getModelOptions(formData.llmConfig.provider) as model}
										<Select.Item value={model}>{model}</Select.Item>
									{/each}
								</Select.Content>
							</Select.Root>
						</div>

						<Separator />

						<!-- Temperature -->
						<div class="space-y-2">
							<Label for="temperature">温度</Label>
							<Input
								id="temperature"
								type="number"
								min="0"
								max="2"
								step="0.1"
								bind:value={formData.llmConfig.temperature}
								class={errors.temperature ? 'border-destructive' : ''}
							/>
							{#if errors.temperature}
								<p class="text-sm text-destructive">{errors.temperature}</p>
							{/if}
						</div>

						<!-- Max Tokens -->
						<div class="space-y-2">
							<Label for="maxTokens">最大令牌数</Label>
							<Input
								id="maxTokens"
								type="number"
								min="1"
								max="100000"
								bind:value={formData.llmConfig.maxTokens}
								class={errors.maxTokens ? 'border-destructive' : ''}
							/>
							{#if errors.maxTokens}
								<p class="text-sm text-destructive">{errors.maxTokens}</p>
							{/if}
						</div>

						<!-- Top P -->
						<div class="space-y-2">
							<Label for="topP">Top P</Label>
							<Input
								id="topP"
								type="number"
								min="0"
								max="1"
								step="0.1"
								bind:value={formData.llmConfig.topP}
							/>
						</div>

						<!-- Frequency Penalty -->
						<div class="space-y-2">
							<Label for="frequencyPenalty">频率惩罚</Label>
							<Input
								id="frequencyPenalty"
								type="number"
								min="-2"
								max="2"
								step="0.1"
								bind:value={formData.llmConfig.frequencyPenalty}
							/>
						</div>

						<!-- Presence Penalty -->
						<div class="space-y-2">
							<Label for="presencePenalty">存在惩罚</Label>
							<Input
								id="presencePenalty"
								type="number"
								min="-2"
								max="2"
								step="0.1"
								bind:value={formData.llmConfig.presencePenalty}
							/>
						</div>
					</CardContent>
				</Card>
			</div>
		</div>
	</div>
{/if}