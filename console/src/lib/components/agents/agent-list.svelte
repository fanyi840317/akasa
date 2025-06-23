<script lang="ts">
	import type { Agent } from '$lib/types/agent.js';
	import { agentStore } from '$lib/stores/agent.svelte.js';
	import { Button } from '$lib/components/ui/button';
	import ErrorDisplay from '$lib/components/ui/error-display.svelte';
	import { Loading } from '$lib/components/ui/loading';
	import { Plus } from '@lucide/svelte';
	import { createEventDispatcher, onMount } from 'svelte';

	const dispatch = createEventDispatcher<{
		create: void;
		edit: { agent: Agent };
		delete: { agent: Agent };
		duplicate: { agent: Agent };
		test: { agent: Agent };
		view: { agent: Agent };
	}>();

	onMount(() => {
		agentStore.loadAgents();
	});

	const handleAgentAction = (action: string, agent: Agent) => {
		switch (action) {
			case 'edit':
				dispatch('edit', { agent });
				break;
			case 'delete':
				dispatch('delete', { agent });
				break;
			case 'duplicate':
				dispatch('duplicate', { agent });
				break;
			case 'test':
				dispatch('test', { agent });
				break;
			case 'view':
				dispatch('view', { agent });
				break;
		}
	};

	const handleRefresh = () => {
		agentStore.loadAgents();
	};

	// Helper functions for agent display
	const getAgentColor = (type: string) => {
		const colors: Record<string, string> = {
			'mystery_researcher': '#8B5CF6',
			'academic_researcher': '#3B82F6', 
			'correlation_analyzer': '#6366F1',
			'report_generator': '#EC4899',
			'data_analyst': '#10B981',
			'content_creator': '#F59E0B',
			'strategy_advisor': '#14B8A6',
			'customer_support': '#EF4444',
			'hr': '#22C55E',
			'marketing': '#8B5CF6',
			'legal': '#6B7280',
			'product': '#3B82F6',
			'new-agent-1': '#22C55E',
			'new-agent-2': '#6B7280',
			'new-agent-3': '#6B7280',
			'flagsupport': '#22C55E'
		};
		return colors[type] || '#6B7280';
	};

	const getAgentIcon = (type: string) => {
		const icons: Record<string, string> = {
			'mystery_researcher': '📊',
			'academic_researcher': '🎓',
			'correlation_analyzer': '🔗',
			'report_generator': '📝',
			'data_analyst': '📈',
			'content_creator': '✍️',
			'strategy_advisor': '🎯',
			'customer_support': '🎧',
			'hr': '👥',
			'marketing': '📢',
			'legal': '⚖️',
			'product': '🔍',
			'new-agent-1': '🤖',
			'new-agent-2': '🧪',
			'new-agent-3': '📋',
			'flagsupport': '🏳️'
		};
		return icons[type] || '🤖';
	};

	const getAgentTypeDisplay = (type: string) => {
		const displays: Record<string, string> = {
			'mystery_researcher': 'mystery_researcher',
			'academic_researcher': 'academic_researcher',
			'correlation_analyzer': 'correlation_analyzer',
			'report_generator': 'report_generator',
			'data_analyst': 'data_analyst',
			'content_creator': 'content_creator',
			'strategy_advisor': 'strategy_advisor',
			'customer_support': 'customersupport',
			'hr': 'hr',
			'marketing': 'marketing',
			'legal': 'legal',
			'product': 'product',
			'new-agent-1': 'new-agent-1',
			'new-agent-2': 'new-agent-2',
			'new-agent-3': 'new-agent-3',
			'flagsupport': 'flagsupport'
		};
		return displays[type] || type;
	};

	const getStatusColor = (status: string) => {
		const colors: Record<string, string> = {
			'active': '#DCFCE7',
			'inactive': '#F3F4F6',
			'draft': '#FEF3C7',
			'archived': '#FEE2E2'
		};
		return colors[status] || '#F3F4F6';
	};

	const getStatusTextColor = (status: string) => {
		const colors: Record<string, string> = {
			'active': '#166534',
			'inactive': '#374151',
			'draft': '#92400E',
			'archived': '#991B1B'
		};
		return colors[status] || '#374151';
	};

	const getStatusDisplay = (status: string) => {
		const displays: Record<string, string> = {
			'active': '活跃',
			'inactive': '非活跃',
			'draft': '草稿',
			'archived': '已归档'
		};
		return displays[status] || status;
	};
</script>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold tracking-tight">浏览代理</h1>
			<p class="text-muted-foreground mt-2">
				发现并创建适合您的代理，将概念、统计和知识的任何任务组合在一起。
			</p>
		</div>
		<Button onclick={() => dispatch('create')} class="bg-orange-500 hover:bg-orange-600 text-white">
			<Plus class="mr-2 h-4 w-4" />
			创建
		</Button>
	</div>

	<!-- Section Title -->
	<div>
		<h2 class="text-xl font-semibold mb-4">由我创建</h2>
	</div>



	<!-- Content -->
	{#if agentStore.loading}
		<div class="flex items-center justify-center py-12">
			<Loading />
		</div>
	{:else if agentStore.error}
		<ErrorDisplay
			title="加载代理时出错"
			message={agentStore.error}
			showRetry={true}
			onRetry={handleRefresh}
		/>
	{:else if agentStore.agents?.length === 0}
		<div class="flex items-center justify-center py-12">
			<div class="text-center">
				<p class="text-muted-foreground mb-4">暂无代理</p>
				<Button onclick={() => dispatch('create')} class="bg-orange-500 hover:bg-orange-600 text-white">
					创建您的第一个代理
				</Button>
			</div>
		</div>
	{:else}
		<!-- Agent Grid -->
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
			{#each agentStore.agents || [] as agent (agent.$id)}
				<div 
					class="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-lg transition-all duration-200 cursor-pointer group"
					onclick={() => handleAgentAction('view', agent)}
				>
					<!-- Agent Icon -->
					<div class="w-12 h-12 rounded-lg mb-4 flex items-center justify-center text-2xl"
						 style="background-color: {getAgentColor(agent.type)}">
						{getAgentIcon(agent.type)}
					</div>
					
					<!-- Agent Name -->
					<h3 class="font-semibold text-lg mb-2 text-gray-900 group-hover:text-gray-700">
						{agent.name}
					</h3>
					
					<!-- Agent Type -->
					<p class="text-sm text-gray-500 mb-3">
						@{getAgentTypeDisplay(agent.type)}
					</p>
					
					<!-- Agent Description -->
					{#if agent.description}
						<p class="text-sm text-gray-600 mb-4 line-clamp-2">
							{agent.description}
						</p>
					{/if}
					
					<!-- Status and Usage -->
					<div class="flex items-center justify-between">
						<span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
							style="background-color: {getStatusColor(agent.status)}; color: {getStatusTextColor(agent.status)}">
							{getStatusDisplay(agent.status)}
						</span>
						{#if agent.usageCount !== undefined}
							<span class="text-xs text-gray-500">
								{agent.usageCount}
							</span>
						{/if}
					</div>
				</div>
		{/each}
	</div>
{/if}
</div>

<style>
	.line-clamp-2 {
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}
</style>