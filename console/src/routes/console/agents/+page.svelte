<script lang="ts">
	import type { Agent, CreateAgentRequest, UpdateAgentRequest } from '$lib/types/agent.js';
	import { agentStore } from '$lib/stores/agent.svelte.js';
	import AgentList from '$lib/components/agents/agent-list.svelte';
	import AgentForm from '$lib/components/agents/agent-form.svelte';
	import { toast } from 'svelte-sonner';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { Button } from '$lib/components/ui/button';
	import { Plus } from '@lucide/svelte';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import PageHeader from '$lib/components/ui/page-header.svelte';

	// State for form modal
	let showForm = $state(false);
	let editingAgent = $state<Agent | null>(null);
	let formLoading = $state(false);

	// Handle agent actions
	const handleCreate = () => {
		editingAgent = null;
		showForm = true;
	};

	const handleEdit = (event: CustomEvent<{ agent: Agent }>) => {
		editingAgent = event.detail.agent;
		showForm = true;
	};

	const handleView = (agent: Agent) => {
		// Navigate to agent detail page (to be implemented)
		goto(`/console/agents/${agent.$id}`);
	};

	const handleDelete = async (event: CustomEvent<{ agent: Agent }>) => {
		const agent = event.detail.agent;

		if (
			!confirm(`Are you sure you want to delete "${agent.name}"? This action cannot be undone.`)
		) {
			return;
		}

		try {
			await agentStore.deleteAgent(agent.$id);
			toast.success(`Agent "${agent.name}" deleted successfully`);
		} catch (error) {
			toast.error(
				`Failed to delete agent: ${error instanceof Error ? error.message : 'Unknown error'}`
			);
		}
	};

	const handleDuplicate = async (event: CustomEvent<{ agent: Agent }>) => {
		const agent = event.detail.agent;
		const newName = prompt(`Enter name for duplicated agent:`, `${agent.name} (Copy)`);

		if (!newName) return;

		try {
			await agentStore.duplicateAgent(agent.$id, newName);
			toast.success(`Agent duplicated as "${newName}"`);
		} catch (error) {
			toast.error(
				`Failed to duplicate agent: ${error instanceof Error ? error.message : 'Unknown error'}`
			);
		}
	};

	const handleTest = (event: CustomEvent<{ agent: Agent }>) => {
		const agent = event.detail.agent;
		// Navigate to test page or open test modal (to be implemented)
		toast.info(`Test functionality for "${agent.name}" coming soon`);
	};

	// Handle form submission
	const handleFormSave = async (
		event: CustomEvent<{ data: CreateAgentRequest | UpdateAgentRequest }>
	) => {
		formLoading = true;

		try {
			if (editingAgent) {
				// Update existing agent
				await agentStore.updateAgent(editingAgent.$id, event.detail.data as UpdateAgentRequest);
				toast.success(`Agent "${event.detail.data.name}" updated successfully`);
			} else {
				// Create new agent
				await agentStore.createAgent(event.detail.data as CreateAgentRequest);
				toast.success(`Agent "${event.detail.data.name}" created successfully`);
			}

			showForm = false;
			editingAgent = null;
		} catch (error) {
			toast.error(
				`Failed to ${editingAgent ? 'update' : 'create'} agent: ${error instanceof Error ? error.message : 'Unknown error'}`
			);
		} finally {
			formLoading = false;
		}
	};

	const handleFormClose = () => {
		showForm = false;
		editingAgent = null;
		formLoading = false;
	};

	// Clear any errors when component mounts
	onMount(() => {
		agentStore.clearError();
	});
</script>

<svelte:head>
	<title>Agents - Akasa Console</title>
	<meta name="description" content="Manage your AI agents and their configurations" />
</svelte:head>
<div class="h-content bg-base-200 flex flex-col rounded-2xl border">
	<PageHeader
		title="浏览代理"
		description="发现并创建适合您的代理，将概念、统计和知识的任何任务组合在一起。"
	>
		{#snippet rightContent()}
			<Button>
				<Plus class="mr-2 h-4 w-4" />
				创建
			</Button>
		{/snippet}
	</PageHeader>

	<ScrollArea class="flex-center h-full flex-col gap-10 p-10">
		<AgentList oncreate={handleCreate} onview={handleView} />
	</ScrollArea>
</div>
<!-- Agent Form Modal -->
<AgentForm
	open={showForm}
	agent={editingAgent}
	loading={formLoading}
	on:save={handleFormSave}
	on:close={handleFormClose}
/>
