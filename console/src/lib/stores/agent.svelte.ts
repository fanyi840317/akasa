import { agentService } from '$lib/services/agent';
import type {
	Agent,
	CreateAgentRequest,
	UpdateAgentRequest,
	AgentFilters,
	AgentSortOptions
} from '$lib/types/agent.js';

class AgentStore {
	agents = $state<Agent[]>([]);
	currentAgent = $state<Agent | null>(null);
	loading = $state(false);
	error = $state<string | null>(null);
	total = $state(0);
	currentPage = $state(1);
	limit = $state(20);
	filters = $state<AgentFilters>({});
	sort = $state<AgentSortOptions>({ field: 'updatedAt', order: 'desc' });

	async loadAgents() {
		this.loading = true;
		this.error = null;

		try {
			const response = await agentService.getAgents(
				this.filters,
				this.sort,
				this.currentPage,
				this.limit
			);
			this.agents = response.agents;
			this.total = response.total;
		} catch (err) {
			this.error = err instanceof Error ? err.message : 'Failed to load agents';
			this.agents = [];
			this.total = 0;
			console.error('Failed to load agents:', err);
		} finally {
			this.loading = false;
		}
	}

	async loadAgent(id: string) {
		this.loading = true;
		this.error = null;

		try {
			this.currentAgent = await agentService.getAgent(id);
		} catch (err) {
			this.error = err instanceof Error ? err.message : 'Failed to load agent';
			console.error('Failed to load agent:', err);
		} finally {
			this.loading = false;
		}
	}

	async createAgent(data: CreateAgentRequest) {
		this.loading = true;
		this.error = null;

		try {
			const newAgent = await agentService.createAgent(data);
			this.agents = [newAgent, ...this.agents];
			this.total += 1;
			return newAgent;
		} catch (err) {
			this.error = err instanceof Error ? err.message : 'Failed to create agent';
			console.error('Failed to create agent:', err);
			throw err;
		} finally {
			this.loading = false;
		}
	}

	async updateAgent(id: string, data: UpdateAgentRequest) {
		this.loading = true;
		this.error = null;

		try {
			const updatedAgent = await agentService.updateAgent(id, data);
			const index = this.agents.findIndex((agent) => agent.$id === id);
			if (index !== -1) {
				this.agents[index] = updatedAgent;
			}
			if (this.currentAgent?.$id === id) {
				this.currentAgent = updatedAgent;
			}
			return updatedAgent;
		} catch (err) {
			this.error = err instanceof Error ? err.message : 'Failed to update agent';
			console.error('Failed to update agent:', err);
			throw err;
		} finally {
			this.loading = false;
		}
	}

	async deleteAgent(id: string) {
		this.loading = true;
		this.error = null;

		try {
			await agentService.deleteAgent(id);
			this.agents = this.agents.filter((agent) => agent.$id !== id);
			this.total -= 1;
			if (this.currentAgent?.$id === id) {
				this.currentAgent = null;
			}
		} catch (err) {
			this.error = err instanceof Error ? err.message : 'Failed to delete agent';
			console.error('Failed to delete agent:', err);
			throw err;
		} finally {
			this.loading = false;
		}
	}

	async duplicateAgent(id: string, name?: string) {
		this.loading = true;
		this.error = null;

		try {
			const duplicatedAgent = await agentService.duplicateAgent(id, name);
			this.agents = [duplicatedAgent, ...this.agents];
			this.total += 1;
			return duplicatedAgent;
		} catch (err) {
			this.error = err instanceof Error ? err.message : 'Failed to duplicate agent';
			console.error('Failed to duplicate agent:', err);
			throw err;
		} finally {
			this.loading = false;
		}
	}

	updateFilters(newFilters: Partial<AgentFilters>) {
		// 检查过滤器是否实际发生变化
		const currentFiltersStr = JSON.stringify(this.filters);
		const newFiltersObj = { ...this.filters, ...newFilters };
		const newFiltersStr = JSON.stringify(newFiltersObj);
		
		if (currentFiltersStr === newFiltersStr) {
			return; // 如果过滤器没有变化，不执行任何操作
		}
		
		this.filters = newFiltersObj;
		this.currentPage = 1; // Reset to first page when filters change
		this.loadAgents();
	}

	updateSort(newSort: AgentSortOptions) {
		this.sort = newSort;
		this.currentPage = 1; // Reset to first page when sort changes
		this.loadAgents();
	}

	setPage(page: number) {
		this.currentPage = page;
		this.loadAgents();
	}

	clearError() {
		this.error = null;
	}

	clearCurrentAgent() {
		this.currentAgent = null;
	}

	get totalPages() {
		return Math.ceil(this.total / this.limit);
	}

	get hasNextPage() {
		return this.currentPage < this.totalPages;
	}

	get hasPrevPage() {
		return this.currentPage > 1;
	}
}

export const agentStore = new AgentStore();