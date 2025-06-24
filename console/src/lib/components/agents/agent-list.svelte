<script lang="ts">
	import type { Agent } from '$lib/types/agent.js';
	import { agentStore } from '$lib/stores/agent.svelte.js';
	import { Button } from '$lib/components/ui/button';
	import ErrorDisplay from '$lib/components/ui/error-display.svelte';
	import { Loading } from '$lib/components/ui/loading';
	import { Plus } from '@lucide/svelte';
	import { onMount } from 'svelte';
	import AgentCard from './agent-card.svelte';

	interface Props {
		oncreate?: () => void;
		onedit?: (agent: Agent) => void;
		ondelete?: (agent: Agent) => void;
		onduplicate?: (agent: Agent) => void;
		ontest?: (agent: Agent) => void;
		onview?: (agent: Agent) => void;
	}

	let { oncreate, onedit, ondelete, onduplicate, ontest, onview }: Props = $props();
	$effect(() => {
		if(agentStore.agents){
			console.log("create",agentStore.agents);
		}
	})
	onMount(() => {
		agentStore.loadAgents();
	});

	const handleAgentAction = (action: string, agent: Agent) => {
		switch (action) {
			case 'edit':
				onedit?.(agent);
				break;
			case 'delete':
				ondelete?.(agent);
				break;
			case 'duplicate':
				onduplicate?.(agent);
				break;
			case 'test':
				ontest?.(agent);
				break;
			case 'view':
				onview?.(agent);
				break;
		}
	};

	const handleRefresh = () => {
		agentStore.loadAgents();
	};
</script>

<div class="space-y-6">



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
				<Button onclick={() => oncreate?.()} >
					创建您的第一个代理
				</Button>
			</div>
		</div>
	{:else}
		<!-- Agent Grid -->
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
			{#each agentStore.agents || [] as agent (agent.name)}
				<AgentCard 
					{agent} 
					onedit={(agent) => handleAgentAction('edit', agent)}
					ondelete={(agent) => handleAgentAction('delete', agent)}
					onduplicate={(agent) => handleAgentAction('duplicate', agent)}
					ontest={(agent) => handleAgentAction('test', agent)}
					onview={(agent) => handleAgentAction('view', agent)}
				/>
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