<script lang="ts">
	import type { Agent } from '$lib/types/agent.js';
	import { AgentStatus, AgentType } from '$lib/types/agent.js';
	import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { Badge } from '$lib/components/ui/badge';
	import {
		MoreVertical,
		Play,
		Edit,
		Copy,
		Trash2,
		Bot,
		Clock,
		Activity
	} from '@lucide/svelte';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import { formatDistanceToNow } from 'date-fns';
	import CardFooter from '../ui/card/card-footer.svelte';

	interface Props {
		agent: Agent;
		onedit?: (agent: Agent) => void;
		ondelete?: (agent: Agent) => void;
		onduplicate?: (agent: Agent) => void;
		ontest?: (agent: Agent) => void;
		onview?: (agent: Agent) => void;
	}

	let { agent, onedit, ondelete, onduplicate, ontest, onview }: Props = $props();

	const getStatusColor = (status: AgentStatus) => {
		switch (status) {
			case AgentStatus.ACTIVE:
				return 'bg-green-100 text-green-800 border-green-200';
			case AgentStatus.INACTIVE:
				return 'bg-gray-100 text-gray-800 border-gray-200';
			case AgentStatus.DRAFT:
				return 'bg-yellow-100 text-yellow-800 border-yellow-200';
			case AgentStatus.ARCHIVED:
				return 'bg-red-100 text-red-800 border-red-200';
			default:
				return 'bg-gray-100 text-gray-800 border-gray-200';
		}
	};

	const getTypeColor = (type: AgentType) => {
		switch (type) {
		case AgentType.MYSTERY_RESEARCHER:
			return 'bg-purple-100 text-purple-800 border-purple-200';
		case AgentType.ACADEMIC_RESEARCHER:
			return 'bg-blue-100 text-blue-800 border-blue-200';
		case AgentType.CORRELATION_ANALYZER:
			return 'bg-indigo-100 text-indigo-800 border-indigo-200';
		case AgentType.REPORT_GENERATOR:
			return 'bg-pink-100 text-pink-800 border-pink-200';
		case AgentType.DATA_ANALYST:
			return 'bg-green-100 text-green-800 border-green-200';
		case AgentType.CONTENT_CREATOR:
			return 'bg-orange-100 text-orange-800 border-orange-200';
		case AgentType.STRATEGY_ADVISOR:
			return 'bg-teal-100 text-teal-800 border-teal-200';
		default:
			return 'bg-gray-100 text-gray-800 border-gray-200';
	}
	};

	const handleEdit = () => onedit?.(agent);
	const handleDelete = () => ondelete?.(agent);
	const handleDuplicate = () => onduplicate?.(agent);
	const handleTest = () => ontest?.(agent);
	const handleView = () => onview?.(agent);
</script>

<Card class="group h-[300px] hover:shadow-md transition-shadow cursor-pointer" onclick={handleView}>
	<CardHeader class="pb-3">
		<CardTitle>{agent.name}</CardTitle>
		<CardDescription>{agent.description}</CardDescription>
	
		<!-- <div class="flex items-center gap-2 mt-2">
			<span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border {getStatusColor(agent.status)}">
				{agent.status}
			</span>
			<span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border {getTypeColor(agent.type)}">
				{agent.type}
			</span>
		</div> -->
	</CardHeader>
	<CardContent class="flex-1 ">
		
	</CardContent>
	<!-- <CardContent class="pt-0">
		{#if agent.description}
			<p class="text-sm text-muted-foreground mb-3 line-clamp-2">
				{agent.description}
			</p>
		{/if}
		
		{#if agent.tags && agent.tags.length > 0}
			<div class="flex flex-wrap gap-1 mb-3">
				{#each agent.tags.slice(0, 3) as tag}
					<span class="inline-flex items-center px-2 py-1 rounded-md text-xs bg-secondary text-secondary-foreground">
						{tag}
					</span>
				{/each}
				{#if agent.tags.length > 3}
					<span class="inline-flex items-center px-2 py-1 rounded-md text-xs bg-secondary text-secondary-foreground">
						+{agent.tags.length - 3}
					</span>
				{/if}
			</div>
		{/if}

		<div class="flex items-center justify-between text-xs text-muted-foreground">
			<div class="flex items-center gap-4">
				{#if agent.lastUsed}
					<div class="flex items-center gap-1">
						<Clock class="h-3 w-3" />
						<span>Used {formatDistanceToNow(agent.lastUsed)} ago</span>
					</div>
				{/if}
				{#if agent.usageCount !== undefined}
					<div class="flex items-center gap-1">
						<Activity class="h-3 w-3" />
						<span>{agent.usageCount} uses</span>
					</div>
				{/if}
			</div>
			{#if agent.updatedAt}
				<span>Updated {formatDistanceToNow(agent.updatedAt)} ago</span>
			{/if}
		</div>
	</CardContent> -->
	<CardFooter>
		<div class="flex w-full items-center justify-between">
			<Bot class="size-4"></Bot>
			<DropdownMenu.Root>
				<DropdownMenu.Trigger>
					<Button
						variant="ghost"
						size="sm"
						class="h-8 w-8 p-0 opacity-0 group-hover:opacity-100 transition-opacity"
						onclick={(e) => e.stopPropagation()}
					>
						<MoreVertical class="h-4 w-4" />
					</Button>
				</DropdownMenu.Trigger>
				<DropdownMenu.Content align="start" class="rounded-[16px]">
					<DropdownMenu.Item onclick={handleTest}>
						<Play class="mr-2 h-4 w-4" />
						Test Agent
					</DropdownMenu.Item>
					<DropdownMenu.Item onclick={handleEdit}>
						<Edit class="mr-2 h-4 w-4" />
						Edit
					</DropdownMenu.Item>
					<DropdownMenu.Item onclick={handleDuplicate}>
						<Copy class="mr-2 h-4 w-4" />
						Duplicate
					</DropdownMenu.Item>
					<DropdownMenu.Separator />
					<DropdownMenu.Item onclick={handleDelete} class="text-destructive">
						<Trash2 class="mr-2 h-4 w-4" />
						Delete
					</DropdownMenu.Item>
				</DropdownMenu.Content>
			</DropdownMenu.Root>
		</div>
	</CardFooter>
</Card>

<style>
	.line-clamp-2 {
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}
</style>