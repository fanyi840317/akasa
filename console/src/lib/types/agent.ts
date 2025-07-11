import type { Entity } from './entity.js';

export interface Agent extends Entity {
	type: AgentType;
	description?: string;
	prompt?: string;
	llmConfig?: LLMConfig;
	status: AgentStatus;
	tags?: string[];
	version?: string;
	lastUsed?: Date;
	usageCount?: number;
}

export enum AgentType {
	MYSTERY_RESEARCHER = 'mystery_researcher',
	ACADEMIC_RESEARCHER = 'academic_researcher',
	CORRELATION_ANALYZER = 'correlation_analyzer',
	REPORT_GENERATOR = 'report_generator',
	DATA_ANALYST = 'data_analyst',
	CONTENT_CREATOR = 'content_creator',
	STRATEGY_ADVISOR = 'strategy_advisor'
}

export enum AgentStatus {
	ACTIVE = 'active',
	INACTIVE = 'inactive',
	DRAFT = 'draft',
	ARCHIVED = 'archived'
}

export enum LLMProvider {
	OPENAI = 'openai',
	ANTHROPIC = 'anthropic',
	GOOGLE = 'google',
	OLLAMA = 'ollama'
}

export interface LLMConfig {
	provider: LLMProvider;
	model: string;
	temperature?: number;
	maxTokens?: number;
	topP?: number;
	frequencyPenalty?: number;
	presencePenalty?: number;
}

export interface LLMUsage {
	promptTokens?: number;
	completionTokens?: number;
	totalTokens?: number;
	cost?: number;
}

export interface CreateAgentRequest {
	name: string;
	type: AgentType;
	description?: string;
	prompt?: string;
	llmConfig?: LLMConfig;
	tags?: string[];
}

export interface UpdateAgentRequest extends Partial<CreateAgentRequest> {
	status?: AgentStatus;
}

export interface AgentListResponse {
	agents: Agent[];
	total: number;
	page: number;
	limit: number;
}

export interface AgentFilters {
	type?: AgentType;
	status?: AgentStatus;
	tags?: string[];
	search?: string;
}

export interface AgentSortOptions {
	field: 'name' | 'createdAt' | 'updatedAt' | 'lastUsed' | 'usageCount';
	order: 'asc' | 'desc';
}