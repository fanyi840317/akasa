<script lang="ts">
	import type { Agent, CreateAgentRequest, UpdateAgentRequest, LLMConfig } from '$lib/types/agent.js';
	import { AgentType, AgentStatus, LLMProvider } from '$lib/types/agent.js';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import * as Sheet from '$lib/components/ui/sheet';
	import { Textarea } from '$lib/components/ui/textarea';
	import { createEventDispatcher } from 'svelte';
	import { Save, X, Bot, Settings, Tag } from '@lucide/svelte';

	interface Props {
		open: boolean;
		agent?: Agent | null;
		loading?: boolean;
	}

	let { open = false, agent = null, loading = false }: Props = $props();

	const dispatch = createEventDispatcher<{
		close: void;
		save: { data: CreateAgentRequest | UpdateAgentRequest };
	}>();

	// Form state
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
	let errors = $state<Record<string, string>>({});

	// Reset form when agent changes
	$effect(() => {
		if (agent) {
			formData = {
				name: agent.name,
				type: agent.type,
				description: agent.description || '',
				prompt: agent.prompt || '',
				tags: agent.tags || [],
				status: agent.status,
				llmConfig: agent.llmConfig || {
					provider: LLMProvider.OPENAI,
					model: 'gpt-4',
					temperature: 0.7,
					maxTokens: 2000,
					topP: 1,
					frequencyPenalty: 0,
					presencePenalty: 0
				}
			};
		} else {
			// Reset to defaults for new agent
			formData = {
				name: '',
				type: AgentType.REPORT_GENERATOR,
				description: '',
				prompt: '',
				tags: [],
				status: AgentStatus.DRAFT,
				llmConfig: {
					provider: LLMProvider.OPENAI,
					model: 'gpt-4',
					temperature: 0.7,
					maxTokens: 2000,
					topP: 1,
					frequencyPenalty: 0,
					presencePenalty: 0
				}
			};
		}
		errors = {};
		tagInput = '';
	});

	const validateForm = () => {
		const newErrors: Record<string, string> = {};

		if (!formData.name.trim()) {
			newErrors.name = 'Name is required';
		}

		if (!formData.prompt.trim()) {
			newErrors.prompt = 'Prompt is required';
		}

		if (formData.llmConfig.temperature !== undefined && (formData.llmConfig.temperature < 0 || formData.llmConfig.temperature > 2)) {
			newErrors.temperature = 'Temperature must be between 0 and 2';
		}

		if (formData.llmConfig.maxTokens && (formData.llmConfig.maxTokens < 1 || formData.llmConfig.maxTokens > 100000)) {
			newErrors.maxTokens = 'Max tokens must be between 1 and 100,000';
		}

		errors = newErrors;
		return Object.keys(newErrors).length === 0;
	};

	const handleSubmit = () => {
		if (!validateForm()) return;

		const data = {
			name: formData.name.trim(),
			type: formData.type,
			description: formData.description.trim() || undefined,
			prompt: formData.prompt.trim(),
			tags: formData.tags.length > 0 ? formData.tags : undefined,
			llmConfig: formData.llmConfig,
			...(agent ? { status: formData.status } : {})
		};

		dispatch('save', { data });
	};

	const handleClose = () => {
		dispatch('close');
	};

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
</script>

<Sheet.Root {open} onOpenChange={(isOpen) => !isOpen && handleClose()}>
	<Sheet.Content class="w-full sm:max-w-2xl overflow-y-auto">
		<Sheet.Header>
			<Sheet.Title class="flex items-center gap-2">
				<Bot class="h-5 w-5" />
				{agent ? 'Edit Agent' : 'Create Agent'}
			</Sheet.Title>
			<Sheet.Description>
				{agent ? 'Update your agent configuration' : 'Create a new AI agent with custom settings'}
			</Sheet.Description>
		</Sheet.Header>

		<div class="space-y-6 py-6">
			<!-- Basic Information -->
			<Card>
				<CardHeader>
					<CardTitle class="text-lg">Basic Information</CardTitle>
				</CardHeader>
				<CardContent class="space-y-4">
					<div class="space-y-2">
						<Label for="name">Name *</Label>
						<Input
							id="name"
							bind:value={formData.name}
							placeholder="Enter agent name"
							class={errors.name ? 'border-destructive' : ''}
						/>
						{#if errors.name}
							<p class="text-sm text-destructive">{errors.name}</p>
						{/if}
					</div>

					<div class="grid grid-cols-2 gap-4">
						<div class="space-y-2">
							<Label for="type">Type</Label>
							<select
								id="type"
								bind:value={formData.type}
								class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
							>
								{#each Object.values(AgentType) as type}
									<option value={type}>{type}</option>
								{/each}
							</select>
						</div>

						{#if agent}
							<div class="space-y-2">
								<Label for="status">Status</Label>
								<select
									id="status"
									bind:value={formData.status}
									class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
								>
									{#each Object.values(AgentStatus) as status}
										<option value={status}>{status}</option>
									{/each}
								</select>
							</div>
						{/if}
					</div>

					<div class="space-y-2">
						<Label for="description">Description</Label>
						<Textarea
							id="description"
							bind:value={formData.description}
							placeholder="Describe what this agent does"
							rows={3}
						/>
					</div>

					<div class="space-y-2">
						<Label for="prompt">System Prompt *</Label>
						<Textarea
							id="prompt"
							bind:value={formData.prompt}
							placeholder="Enter the system prompt for this agent"
							rows={6}
							class={errors.prompt ? 'border-destructive' : ''}
						/>
						{#if errors.prompt}
							<p class="text-sm text-destructive">{errors.prompt}</p>
						{/if}
					</div>

					<!-- Tags -->
					<div class="space-y-2">
						<Label class="flex items-center gap-2">
							<Tag class="h-4 w-4" />
							Tags
						</Label>
						<div class="flex gap-2">
							<Input
								bind:value={tagInput}
								placeholder="Add a tag"
								onkeydown={handleTagKeydown}
								class="flex-1"
							/>
							<Button type="button" variant="outline" onclick={addTag}>
								Add
							</Button>
						</div>
						{#if formData.tags.length > 0}
							<div class="flex flex-wrap gap-2 mt-2">
								{#each formData.tags as tag, index}
									<span class="inline-flex items-center gap-1 px-2 py-1 rounded-md text-xs bg-secondary text-secondary-foreground">
										{tag}
										<button
											type="button"
											onclick={() => removeTag(index)}
											class="hover:text-destructive"
										>
											<X class="h-3 w-3" />
										</button>
									</span>
								{/each}
							</div>
						{/if}
					</div>
				</CardContent>
			</Card>

			<!-- LLM Configuration -->
			<Card>
				<CardHeader>
					<CardTitle class="text-lg flex items-center gap-2">
						<Settings class="h-5 w-5" />
						LLM Configuration
					</CardTitle>
				</CardHeader>
				<CardContent class="space-y-4">
					<div class="grid grid-cols-2 gap-4">
						<div class="space-y-2">
							<Label for="provider">Provider</Label>
							<select
								id="provider"
								bind:value={formData.llmConfig.provider}
								class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
							>
								{#each Object.values(LLMProvider) as provider}
									<option value={provider}>{provider}</option>
								{/each}
							</select>
						</div>

						<div class="space-y-2">
							<Label for="model">Model</Label>
							<select
								id="model"
								bind:value={formData.llmConfig.model}
								class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
							>
								{#each getModelOptions(formData.llmConfig.provider) as model}
									<option value={model}>{model}</option>
								{/each}
							</select>
						</div>
					</div>

					<div class="grid grid-cols-2 gap-4">
						<div class="space-y-2">
							<Label for="temperature">Temperature</Label>
							<Input
								id="temperature"
								type="number"
								bind:value={formData.llmConfig.temperature}
								min="0"
								max="2"
								step="0.1"
								class={errors.temperature ? 'border-destructive' : ''}
							/>
							{#if errors.temperature}
								<p class="text-sm text-destructive">{errors.temperature}</p>
							{/if}
						</div>

						<div class="space-y-2">
							<Label for="maxTokens">Max Tokens</Label>
							<Input
								id="maxTokens"
								type="number"
								bind:value={formData.llmConfig.maxTokens}
								min="1"
								max="100000"
								class={errors.maxTokens ? 'border-destructive' : ''}
							/>
							{#if errors.maxTokens}
								<p class="text-sm text-destructive">{errors.maxTokens}</p>
							{/if}
						</div>
					</div>

					<div class="grid grid-cols-3 gap-4">
						<div class="space-y-2">
							<Label for="topP">Top P</Label>
							<Input
								id="topP"
								type="number"
								bind:value={formData.llmConfig.topP}
								min="0"
								max="1"
								step="0.1"
							/>
						</div>

						<div class="space-y-2">
							<Label for="frequencyPenalty">Frequency Penalty</Label>
							<Input
								id="frequencyPenalty"
								type="number"
								bind:value={formData.llmConfig.frequencyPenalty}
								min="-2"
								max="2"
								step="0.1"
							/>
						</div>

						<div class="space-y-2">
							<Label for="presencePenalty">Presence Penalty</Label>
							<Input
								id="presencePenalty"
								type="number"
								bind:value={formData.llmConfig.presencePenalty}
								min="-2"
								max="2"
								step="0.1"
							/>
						</div>
					</div>
				</CardContent>
			</Card>
		</div>

		<Sheet.Footer class="flex justify-end gap-2">
			<Button variant="outline" onclick={handleClose} disabled={loading}>
				Cancel
			</Button>
			<Button onclick={handleSubmit} disabled={loading}>
				{#if loading}
					<div class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent"></div>
				{:else}
					<Save class="mr-2 h-4 w-4" />
				{/if}
				{agent ? 'Update' : 'Create'} Agent
			</Button>
		</Sheet.Footer>
	</Sheet.Content>
</Sheet.Root>