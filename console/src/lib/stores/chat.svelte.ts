import type { Message, Resource } from '$lib/types/message';
import type { MCPServerMetadata } from '$lib/types/mcp';
import { chatStream } from '$lib/services/chat';
import { browser } from '$app/environment';

// 聊天配置接口
export interface ChatConfig {
	deepThinking: boolean;
	backgroundInvestigation: boolean;
	planIterations: number;
	temperature: number;
	maxTokens: number;
	model: string;
	streamResponse: boolean;
	// 保留原有配置以兼容后端
	auto_accepted_plan?: boolean;
	max_plan_iterations?: number;
	max_step_num?: number;
	max_search_results?: number;
	enable_deep_thinking?: boolean;
	enable_background_investigation?: boolean;
	report_style?: 'academic' | 'popular_science' | 'news' | 'social_media';
	mcp_settings?: {
		servers: Record<
			string,
			MCPServerMetadata & {
				enabled_tools: string[];
				add_to_agents: string[];
			}
		>;
	};
}

// 默认配置
const DEFAULT_CONFIG: ChatConfig = {
	deepThinking: true,
	backgroundInvestigation: false,
	planIterations: 3,
	temperature: 0.7,
	maxTokens: 2000,
	model: 'gpt-4-turbo',
	streamResponse: true,
	// 兼容后端的配置
	auto_accepted_plan: true,
	max_plan_iterations: 3,
	max_step_num: 10,
	max_search_results: 5,
	enable_deep_thinking: true,
	enable_background_investigation: false
};

// 聊天状态管理类
class ChatStore {
	// 响应式状态
	messages = $state<Message[]>([]);
	currentThreadId = $state<string | null>(null);
	isStreaming = $state(false);
	error = $state<string | null>(null);
	input = $state('');
	config = $state<ChatConfig>(DEFAULT_CONFIG);
	abortController = $state<AbortController | null>(null);

	// 生成存储键名
	private getStorageKey(threadId: string): string {
		return `akasa_chat_${threadId}`;
	}

	// 保存聊天记录到本地存储
	private saveChatToStorage() {
		if (!browser || !this.currentThreadId) return;

		try {
			const chatData = {
				messages: this.messages,
				timestamp: Date.now()
			};
			localStorage.setItem(this.getStorageKey(this.currentThreadId), JSON.stringify(chatData));
		} catch (error) {
			console.error('Failed to save chat to storage:', error);
		}
	}

	// 从本地存储加载聊天记录
	private loadChatFromStorage(threadId: string): Message[] {
		if (!browser) return [];

		try {
			const stored = localStorage.getItem(this.getStorageKey(threadId));
			if (stored) {
				const chatData = JSON.parse(stored);
				return chatData.messages || [];
			}
		} catch (error) {
			console.error('Failed to load chat from storage:', error);
		}
		return [];
	}

	// 初始化聊天
	initializeChat(threadId: string) {
		this.currentThreadId = threadId;
		this.messages = this.loadChatFromStorage(threadId);
		this.error = null;
	}

	// 添加消息
	addMessage(message: Omit<Message, 'id'>) {
		const newMessage: Message = {
			id: crypto.randomUUID(),
			...message
		};
		this.messages = [...this.messages, newMessage];
		this.saveChatToStorage();
		return newMessage;
	}

	// 更新消息
	updateMessage(messageId: string, updates: Partial<Message>) {
		const index = this.messages.findIndex((m) => m.id === messageId);
		if (index !== -1) {
			this.messages[index] = { ...this.messages[index], ...updates };
			this.messages = [...this.messages]; // 触发响应式更新
			this.saveChatToStorage();
		}
	}

	// 发送消息
	async sendMessage(content: string, resources?: Resource[]) {
		if (!this.currentThreadId || this.isStreaming) return;

		// 添加用户消息
		this.addMessage({
			threadId: this.currentThreadId,
			role: 'user',
			content,
			contentChunks: [content],
			resources
		});

		// 创建助手消息占位符
		const assistantMessage = this.addMessage({
			threadId: this.currentThreadId,
			role: 'assistant',
			content: '',
			contentChunks: [],
			isStreaming: true
		});

		this.isStreaming = true;
		this.error = null;
		this.abortController = new AbortController();

		try {
			const stream = chatStream(
				content,
				{
					thread_id: this.currentThreadId,
					resources,
					auto_accepted_plan: this.config.auto_accepted_plan ?? false,
					max_plan_iterations: this.config.max_plan_iterations ?? 3,
					max_step_num: this.config.max_step_num ?? 10,
					max_search_results: this.config.max_search_results,
					enable_deep_thinking: this.config.enable_deep_thinking,
					enable_background_investigation: this.config.enable_background_investigation ?? false,
					report_style: this.config.report_style,
					mcp_settings: this.config.mcp_settings
				},
				{
					abortSignal: this.abortController.signal
				}
			);

			for await (const event of stream) {
				switch (event.type) {
					case 'message_chunk': {
						const { content: chunkContent, reasoning_content } = event.data;

						// 更新助手消息内容
						if (chunkContent) {
							this.updateMessage(assistantMessage.id, {
								content: assistantMessage.content + chunkContent,
								contentChunks: [...assistantMessage.contentChunks, chunkContent]
							});
						}

						if (reasoning_content) {
							this.updateMessage(assistantMessage.id, {
								reasoningContent: (assistantMessage.reasoningContent || '') + reasoning_content,
								reasoningContentChunks: [
									...(assistantMessage.reasoningContentChunks || []),
									reasoning_content
								]
							});
						}

						// 检查是否完成
						if (event.data.finish_reason) {
							this.updateMessage(assistantMessage.id, {
								isStreaming: false,
								finishReason: event.data.finish_reason
							});
						}
						break;
					}

					case 'tool_calls':
						// 处理工具调用
						this.updateMessage(assistantMessage.id, {
							toolCalls: event.data.tool_calls.map((tc) => ({
								id: tc.id,
								name: tc.name,
								args: tc.args
							}))
						});
						break;

					case 'tool_call_result': {
						// 处理工具调用结果
						const toolCalls = assistantMessage.toolCalls || [];
						const toolCallIndex = toolCalls.findIndex((tc) => tc.id === event.data.tool_call_id);
						if (toolCallIndex !== -1) {
							toolCalls[toolCallIndex].result = event.data.content;
							this.updateMessage(assistantMessage.id, { toolCalls: [...toolCalls] });
						}
						break;
					}

					case 'interrupt':
						// 处理中断事件
						this.updateMessage(assistantMessage.id, {
							options: event.data.options
						});
						break;
				}
			}
		} catch (error: unknown) {
			if ((error as Error).name !== 'AbortError') {
				console.error('Chat error:', error);
				this.error = (error as Error).message || 'An error occurred';
				this.updateMessage(assistantMessage.id, {
					content: 'Sorry, an error occurred while processing your request.',
					isStreaming: false
				});
			}
		} finally {
			this.isStreaming = false;
			this.abortController = null;
		}
	}

	// 停止流式传输
	stopStreaming() {
		if (this.abortController) {
			this.abortController.abort();
			this.abortController = null;
			this.isStreaming = false;
		}
	}

	// 重新生成消息
	async regenerateMessage(messageId: string) {
		const messageIndex = this.messages.findIndex((m) => m.id === messageId);
		if (messageIndex > 0) {
			const userMessage = this.messages[messageIndex - 1];
			if (userMessage.role === 'user') {
				// 删除助手消息
				this.messages = this.messages.slice(0, messageIndex);
				// 重新发送用户消息
				await this.sendMessage(userMessage.content, userMessage.resources);
			}
		}
	}

	// 处理选项点击（用于中断反馈）
	async handleOptionClick(option: { text: string; value: string }) {
		if (option.value) {
			await this.sendMessage(option.value);
		}
	}

	// 清空聊天
	clearChat() {
		this.messages = [];
		this.error = null;
		this.saveChatToStorage();
	}

	// 清除特定线程的聊天记录
	clearThreadChat(threadId: string) {
		if (!browser) return;

		try {
			localStorage.removeItem(this.getStorageKey(threadId));
			// 如果是当前线程，也清空内存中的聊天
			if (this.currentThreadId === threadId) {
				this.clearChat();
			}
		} catch (error) {
			console.error('Failed to clear thread chat:', error);
		}
	}

	// 切换到不同的线程
	switchToThread(threadId: string) {
		// 如果是同一个线程，不需要重新初始化
		if (this.currentThreadId === threadId) {
			return;
		}

		// 重新初始化聊天并加载对应的聊天记录
		this.initializeChat(threadId);
	}

	// 设置输入值
	setInput(value: string) {
		this.input = value;
	}

	// 更新配置
	updateConfig(newConfig: Partial<ChatConfig>) {
		this.config = { ...this.config, ...newConfig };
	}

	// 获取消息
	getMessages(): Message[] {
		return this.messages;
	}

	// 获取流式状态
	getIsStreaming(): boolean {
		return this.isStreaming;
	}

	// 获取错误
	getError(): string | null {
		return this.error;
	}

	// 获取输入值
	getInput(): string {
		return this.input;
	}

	// 获取配置
	getConfig(): ChatConfig {
		return this.config;
	}

	// 清除错误
	clearError() {
		this.error = null;
	}
}

// 创建全局实例
export const chatStore = new ChatStore();
