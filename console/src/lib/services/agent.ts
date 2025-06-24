import type {
	Agent,
	CreateAgentRequest,
	UpdateAgentRequest,
	AgentListResponse,
	AgentFilters,
	AgentSortOptions,
	LLMUsage
} from '$lib/types/agent.js';

const API_BASE = 'http://localhost:8000/api';

class AgentService {
	async getAgents(
		filters?: AgentFilters,
		sort?: AgentSortOptions,
		page = 1,
		limit = 20
	): Promise<AgentListResponse> {
		const params = new URLSearchParams({
			page: page.toString(),
			limit: limit.toString()
		});

		if (filters) {
			if (filters.type) params.append('type', filters.type);
			if (filters.status) params.append('status', filters.status);
			if (filters.search) params.append('search', filters.search);
			if (filters.tags?.length) {
				filters.tags.forEach((tag) => params.append('tags', tag));
			}
		}

		if (sort) {
			params.append('sortField', sort.field);
			params.append('sortOrder', sort.order);
		}
		// ?${params}
		const response = await fetch(`${API_BASE}/agents`);
		if (!response.ok) {
			throw new Error(`Failed to fetch agents: ${response.statusText}`);
		}

		const data = await response.json().then((data) => data.data);
		console.log(data);
		return data;
	}

	async getAgent(id: string): Promise<Agent> {
		const response = await fetch(`${API_BASE}/agents/${id}`);
		if (!response.ok) {
			throw new Error(`Failed to fetch agent: ${response.statusText}`);
		}

		return response.json();
	}

	async createAgent(data: CreateAgentRequest): Promise<Agent> {
		const response = await fetch(`${API_BASE}/agents`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		});

		if (!response.ok) {
			throw new Error(`Failed to create agent: ${response.statusText}`);
		}

		return response.json();
	}

	async updateAgent(id: string, data: UpdateAgentRequest): Promise<Agent> {
		const response = await fetch(`${API_BASE}/agents/${id}`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		});

		if (!response.ok) {
			throw new Error(`Failed to update agent: ${response.statusText}`);
		}

		return response.json();
	}

	async deleteAgent(id: string): Promise<void> {
		const response = await fetch(`${API_BASE}/agents/${id}`, {
			method: 'DELETE'
		});

		if (!response.ok) {
			throw new Error(`Failed to delete agent: ${response.statusText}`);
		}
	}

	async duplicateAgent(id: string, name?: string): Promise<Agent> {
		const response = await fetch(`${API_BASE}/agents/${id}/duplicate`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ name })
		});

		if (!response.ok) {
			throw new Error(`Failed to duplicate agent: ${response.statusText}`);
		}

		return response.json();
	}

	async testAgent(id: string, input: string): Promise<{ output: string; usage?: LLMUsage }> {
		const response = await fetch(`${API_BASE}/agents/${id}/test`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ input })
		});

		if (!response.ok) {
			throw new Error(`Failed to test agent: ${response.statusText}`);
		}

		return response.json();
	}
}

export const agentService = new AgentService();