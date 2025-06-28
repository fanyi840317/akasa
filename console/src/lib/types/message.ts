export type MessageRole = 'user' | 'assistant' | 'tool';

export interface Message {
	id: string;
	threadId: string;
	agent?: 'coordinator' | 'planner' | 'researcher' | 'coder' | 'reporter' | 'podcast';
	role: MessageRole;
	isStreaming?: boolean;
	content: string;
	contentChunks: string[];
	reasoningContent?: string;
	reasoningContentChunks?: string[];
	toolCalls?: ToolCallRuntime[];
	options?: Option[];
	finishReason?: 'stop' | 'interrupt' | 'tool_calls';
	interruptFeedback?: string;
	resources?: Array<Resource>;
}

export interface Option {
	text: string;
	value: string;
}

export interface ToolCallRuntime {
	id: string;
	name: string;
	args: Record<string, unknown>;
	argsChunks?: string[];
	result?: string;
}

export interface Resource {
	uri: string;
	title: string;
}
// Tool Calls

export interface ToolCall {
	type: 'tool_call';
	id: string;
	name: string;
	args: Record<string, unknown>;
}

export interface ToolCallChunk {
	type: 'tool_call_chunk';
	index: number;
	id: string;
	name: string;
	args: string;
}

// Events

interface GenericEvent<T extends string, D extends object> {
	type: T;
	data: {
		id: string;
		thread_id: string;
		agent: 'coordinator' | 'planner' | 'researcher' | 'coder' | 'reporter';
		role: 'user' | 'assistant' | 'tool';
		finish_reason?: 'stop' | 'tool_calls' | 'interrupt';
	} & D;
}

export type MessageChunkEvent = GenericEvent<
	'message_chunk',
	{
		content?: string;
		reasoning_content?: string;
	}
>;

export type ToolCallsEvent = GenericEvent<
	'tool_calls',
	{
		tool_calls: ToolCall[];
		tool_call_chunks: ToolCallChunk[];
	}
>;

export type ToolCallChunksEvent = GenericEvent<
	'tool_call_chunks',
	{
		tool_call_chunks: ToolCallChunk[];
	}
>;

export type ToolCallResultEvent = GenericEvent<
	'tool_call_result',
	{
		tool_call_id: string;
		content?: string;
	}
>;

export type InterruptEvent = GenericEvent<
	'interrupt',
	{
		options: Option[];
	}
>;

export type ChatEvent =
	| MessageChunkEvent
	| ToolCallsEvent
	| ToolCallChunksEvent
	| ToolCallResultEvent
	| InterruptEvent;
