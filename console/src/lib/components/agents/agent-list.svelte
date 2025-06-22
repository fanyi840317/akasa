<script lang="ts">
	import type { Agent, AgentFilters, AgentSortOptions } from '$lib/types/agent.js';
	import { AgentStatus, AgentType } from '$lib/types/agent.js';
	import { agentStore } from '$lib/stores/agent.svelte.js';
	import AgentCard from './agent-card.svelte';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Loading } from '$lib/components/ui/loading';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import {
		Plus,
		Search,
		Filter,
		SortAsc,
		SortDesc,
		RefreshCw,
		Grid3X3,
		List
	} from '@lucide/svelte';
	import { createEventDispatcher, onMount } from 'svelte';
	import { debounce } from '$lib/utils.js';

	interface Props {
		viewMode?: 'grid' | 'list';
	}

	let { viewMode = 'grid' }: Props = $props();

	const dispatch = createEventDispatcher<{
		create: void;
		edit: { agent: Agent };
		delete: { agent: Agent };
		duplicate: { agent: Agent };
		test: { agent: Agent };
		view: { agent: Agent };
	}>();

	let searchQuery = $state('');
	let selectedStatus = $state<AgentStatus | ''>('');
	let selectedType = $state<AgentType | ''>('');
	let currentViewMode = $state(viewMode);

	// Debounced search function
	const debouncedSearch = debounce((query: string) => {
		agentStore.updateFilters({ search: query || undefined });
	}, 300);

	// Watch for search query changes
$effect(() => {
	// 只有当搜索查询实际改变时才触发搜索
	if (searchQuery !== undefined) {
		debouncedSearch(searchQuery);
	}
});

	// Watch for filter changes
$effect(() => {
	// 避免在组件初始化时触发不必要的更新
	if (selectedStatus === '' && selectedType === '') return;
	
	const filters: AgentFilters = {};
	if (selectedStatus) filters.status = selectedStatus;
	if (selectedType) filters.type = selectedType;
	agentStore.updateFilters(filters);
});

	onMount(() => {
		agentStore.loadAgents();
	});

	const handleSort = (field: AgentSortOptions['field']) => {
		const currentSort = agentStore.sort;
		const newOrder = currentSort.field === field && currentSort.order === 'asc' ? 'desc' : 'asc';
		agentStore.updateSort({ field, order: newOrder });
	};

	const handleRefresh = () => {
		agentStore.loadAgents();
	};

	const clearFilters = () => {
		searchQuery = '';
		selectedStatus = '';
		selectedType = '';
		agentStore.updateFilters({});
	};

	const handleAgentAction = (action: string, detail: any) => {
		switch (action) {
			case 'edit':
				dispatch('edit', detail);
				break;
			case 'delete':
				dispatch('delete', detail);
				break;
			case 'duplicate':
				dispatch('duplicate', detail);
				break;
			case 'test':
				dispatch('test', detail);
				break;
			case 'view':
				dispatch('view', detail);
				break;
		}
	};

	const getSortIcon = (field: AgentSortOptions['field']) => {
		const currentSort = agentStore.sort;
		if (currentSort.field !== field) return null;
		return currentSort.order === 'asc' ? SortAsc : SortDesc;
	};

	const hasActiveFilters = $derived(
		searchQuery || selectedStatus || selectedType
	);
</script>

<div class="space-y-4">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-2xl font-bold tracking-tight">Agents</h1>
			<p class="text-muted-foreground">
				Manage your AI agents and their configurations
			</p>
		</div>
		<Button onclick={() => dispatch('create')}>
			<Plus class="mr-2 h-4 w-4" />
			Create Agent
		</Button>
	</div>

	<!-- Filters and Controls -->
	<div class="flex items-center gap-4 flex-wrap">
		<!-- Search -->
		<div class="relative flex-1 min-w-64">
			<Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
			<Input
				bind:value={searchQuery}
				placeholder="Search agents..."
				class="pl-10"
			/>
		</div>

		<!-- Status Filter -->
		<DropdownMenu.Root>
			<DropdownMenu.Trigger>
			{#snippet child({ props })}
				<Button {...props} variant="outline" size="sm">
					<Filter class="mr-2 h-4 w-4" />
					Status
					{#if selectedStatus}
						: {selectedStatus}
					{/if}
				</Button>
			{/snippet}
		</DropdownMenu.Trigger>
			<DropdownMenu.Content>
				<DropdownMenu.Item onclick={() => selectedStatus = ''}>
					All Statuses
				</DropdownMenu.Item>
				<DropdownMenu.Separator />
				{#each Object.values(AgentStatus) as status}
					<DropdownMenu.Item onclick={() => selectedStatus = status}>
						{status}
					</DropdownMenu.Item>
				{/each}
			</DropdownMenu.Content>
		</DropdownMenu.Root>

		<!-- Type Filter -->
		<DropdownMenu.Root>
			<DropdownMenu.Trigger>
			{#snippet child({ props })}
				<Button {...props} variant="outline" size="sm">
					<Filter class="mr-2 h-4 w-4" />
					Type
					{#if selectedType}
						: {selectedType}
					{/if}
				</Button>
			{/snippet}
		</DropdownMenu.Trigger>
			<DropdownMenu.Content>
				<DropdownMenu.Item onclick={() => selectedType = ''}>
					All Types
				</DropdownMenu.Item>
				<DropdownMenu.Separator />
				{#each Object.values(AgentType) as type}
					<DropdownMenu.Item onclick={() => selectedType = type}>
						{type}
					</DropdownMenu.Item>
				{/each}
			</DropdownMenu.Content>
		</DropdownMenu.Root>

		<!-- Sort -->
		<DropdownMenu.Root>
			<DropdownMenu.Trigger>
			{#snippet child({ props })}
				<Button {...props} variant="outline" size="sm">
					{@const SortIcon = getSortIcon(agentStore.sort.field)}
					{#if SortIcon}
						<SortIcon class="mr-2 h-4 w-4" />
					{:else}
						<SortAsc class="mr-2 h-4 w-4" />
					{/if}
						Sort
					</Button>
				{/snippet}
			</DropdownMenu.Trigger>
			<DropdownMenu.Content>
				<DropdownMenu.Item onclick={() => handleSort('name')}>
					Name
				</DropdownMenu.Item>
				<DropdownMenu.Item onclick={() => handleSort('createdAt')}>
					Created Date
				</DropdownMenu.Item>
				<DropdownMenu.Item onclick={() => handleSort('updatedAt')}>
					Updated Date
				</DropdownMenu.Item>
				<DropdownMenu.Item onclick={() => handleSort('lastUsed')}>
					Last Used
				</DropdownMenu.Item>
				<DropdownMenu.Item onclick={() => handleSort('usageCount')}>
					Usage Count
				</DropdownMenu.Item>
			</DropdownMenu.Content>
		</DropdownMenu.Root>

		<!-- View Mode Toggle -->
		<div class="flex items-center border rounded-md">
			<Button
				variant={currentViewMode === 'grid' ? 'default' : 'ghost'}
				size="sm"
				class="rounded-r-none"
				onclick={() => currentViewMode = 'grid'}
			>
				<Grid3X3 class="h-4 w-4" />
			</Button>
			<Button
				variant={currentViewMode === 'list' ? 'default' : 'ghost'}
				size="sm"
				class="rounded-l-none"
				onclick={() => currentViewMode = 'list'}
			>
				<List class="h-4 w-4" />
			</Button>
		</div>

		<!-- Refresh -->
		<Button variant="outline" size="sm" onclick={handleRefresh} disabled={agentStore.loading}>
			<RefreshCw class="h-4 w-4 {agentStore.loading ? 'animate-spin' : ''}" />
		</Button>

		<!-- Clear Filters -->
		{#if hasActiveFilters}
			<Button variant="ghost" size="sm" onclick={clearFilters}>
				Clear Filters
			</Button>
		{/if}
	</div>

	<!-- Results Info -->
	<div class="flex items-center justify-between text-sm text-muted-foreground">
		<div>
			Showing {agentStore.agents?.length || 0} of {agentStore.total} agents
		</div>
		{#if agentStore.totalPages > 1}
			<div class="flex items-center gap-2">
				<Button
					variant="outline"
					size="sm"
					disabled={!agentStore.hasPrevPage || agentStore.loading}
					onclick={() => agentStore.setPage(agentStore.currentPage - 1)}
				>
					Previous
				</Button>
				<span>
					Page {agentStore.currentPage} of {agentStore.totalPages}
				</span>
				<Button
					variant="outline"
					size="sm"
					disabled={!agentStore.hasNextPage || agentStore.loading}
					onclick={() => agentStore.setPage(agentStore.currentPage + 1)}
				>
					Next
				</Button>
			</div>
		{/if}
	</div>

	<!-- Content -->
	{#if agentStore.loading}
		<div class="flex items-center justify-center py-12">
			<Loading />
		</div>
	{:else if agentStore.error}
		<div class="flex items-center justify-center py-12">
			<div class="text-center">
				<p class="text-destructive mb-2">Error loading agents</p>
				<p class="text-sm text-muted-foreground mb-4">{agentStore.error}</p>
				<Button onclick={handleRefresh}>Try Again</Button>
			</div>
		</div>
	{:else if agentStore.agents?.length === 0}
		<div class="flex items-center justify-center py-12">
			<div class="text-center">
				<p class="text-muted-foreground mb-4">
					{hasActiveFilters ? 'No agents match your filters' : 'No agents found'}
				</p>
				{#if hasActiveFilters}
					<Button variant="outline" onclick={clearFilters}>Clear Filters</Button>
				{:else}
					<Button onclick={() => dispatch('create')}>Create Your First Agent</Button>
				{/if}
			</div>
		</div>
	{:else}
		<!-- Agent Grid/List -->
		<div class="{currentViewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4' : 'space-y-4'}">
			{#each agentStore.agents || [] as agent (agent.$id)}
				<AgentCard
					{agent}
					on:edit={(e: CustomEvent<{ agent: Agent }>) => handleAgentAction('edit', e.detail.agent)}
					on:delete={(e: CustomEvent<{ agent: Agent }>) => handleAgentAction('delete', e.detail.agent)}
					on:duplicate={(e: CustomEvent<{ agent: Agent }>) => handleAgentAction('duplicate', e.detail.agent)}
					on:test={(e: CustomEvent<{ agent: Agent }>) => handleAgentAction('test', e.detail.agent)}
					on:view={(e: CustomEvent<{ agent: Agent }>) => handleAgentAction('view', e.detail.agent)}
				/>
			{/each}
		</div>
	{/if}
</div>