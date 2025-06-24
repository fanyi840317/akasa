import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/svelte';
import { page } from '$app/stores';
import { goto } from '$app/navigation';
import { toast } from 'svelte-sonner';
import AgentEditPage from './+page.svelte';
import { agentStore } from '$lib/stores/agent.svelte.js';
import { AgentType, AgentStatus, LLMProvider } from '$lib/types/agent.js';

// Mock dependencies
vi.mock('$app/stores', () => ({
	page: {
		params: { id: 'test-agent-id' }
	}
}));

vi.mock('$app/navigation', () => ({
	goto: vi.fn()
}));

vi.mock('svelte-sonner', () => ({
	toast: {
		error: vi.fn(),
		success: vi.fn()
	}
}));

vi.mock('$lib/stores/agent.svelte.js', () => ({
	agentStore: {
		getAgent: vi.fn(),
		updateAgent: vi.fn()
	}
}));

const mockAgent = {
	id: 'test-agent-id',
	name: 'Test Agent',
	type: AgentType.REPORT_GENERATOR,
	description: 'Test description',
	prompt: 'Test prompt',
	tags: ['test', 'agent'],
	status: AgentStatus.ACTIVE,
	llmConfig: {
		provider: LLMProvider.OPENAI,
		model: 'gpt-4',
		temperature: 0.7,
		maxTokens: 2000,
		topP: 1,
		frequencyPenalty: 0,
		presencePenalty: 0
	},
	createdAt: new Date(),
	updatedAt: new Date()
};

describe('Agent Edit Page', () => {
	beforeEach(() => {
		vi.clearAllMocks();
		vi.mocked(agentStore.getAgent).mockResolvedValue(mockAgent);
	});

	it('renders loading state initially', () => {
		render(AgentEditPage);
		expect(screen.getByText('加载 Agent 信息中...')).toBeInTheDocument();
	});

	it('renders edit form after loading', async () => {
		render(AgentEditPage);
		
		// Wait for loading to complete
		await vi.waitFor(() => {
			expect(screen.getByText('编辑 Agent')).toBeInTheDocument();
		});
		
		expect(screen.getByDisplayValue('Test Agent')).toBeInTheDocument();
		expect(screen.getByDisplayValue('Test description')).toBeInTheDocument();
		expect(screen.getByDisplayValue('Test prompt')).toBeInTheDocument();
	});

	it('renders back button', async () => {
		render(AgentEditPage);
		
		await vi.waitFor(() => {
			expect(screen.getByText('返回')).toBeInTheDocument();
		});
	});

	it('renders save button', async () => {
		render(AgentEditPage);
		
		await vi.waitFor(() => {
			expect(screen.getByText('保存')).toBeInTheDocument();
		});
	});
});