import type { MCPServerMetadata } from '$lib/types/mcp';
import { chatStream } from '$lib/services/chat';
import { browser } from '$app/environment';
import type { Message, Resource } from '$lib/types/message';
import { mergeMessage } from './merge-message';

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
	messageIds = $state<string[]>([]);
	messages = $state<Map<string, Message>>(new Map());
	currentThreadId = $state<string | null>(null);
	isStreaming = $state(false);
	error = $state<string | null>(null);
	input = $state('');
	config = $state<ChatConfig>(DEFAULT_CONFIG);
	abortController = $state<AbortController | null>(null);
	// 研究相关状态
	researchIds = $state<string[]>([]);
	researchPlanIds = $state<Map<string, string>>(new Map());
	researchReportIds = $state<Map<string, string>>(new Map());
	researchActivityIds = $state<Map<string, string[]>>(new Map());
	ongoingResearchId = $state<string | null>(null);
	openResearchId = $state<string | null>(null);

	// 生成存储键名
	private getStorageKey(threadId: string): string {
		return `akasa_chat_${threadId}`;
	}

	// 保存聊天记录到本地存储
	private saveChatToStorage() {
		if (!browser || !this.currentThreadId) return;

		try {
			const chatData = {
				messageIds: this.messageIds,
				messages: Array.from(this.messages.entries()),
				timestamp: Date.now()
			};
			localStorage.setItem(this.getStorageKey(this.currentThreadId), JSON.stringify(chatData));
		} catch (error) {
			console.error('Failed to save chat to storage:', error);
		}
	}

	// 从本地存储加载聊天记录
	private loadChatFromStorage(threadId: string): {
		messageIds: string[];
		messages: Map<string, Message>;
	} {
		if (!browser) return { messageIds: [], messages: new Map() };

		try {
			const stored = localStorage.getItem(this.getStorageKey(threadId));
			// console.log(this.getStorageKey(threadId),stored);
			if (stored) {
				const chatData = JSON.parse(stored);
				const messageIds = chatData.messageIds || [];
				const messagesArray = chatData.messages || [];
				const messages = new Map(messagesArray as [string, Message][]);
				return { messageIds, messages };
			}
		} catch (error) {
			console.error('Failed to load chat from storage:', error);
		}
		return { messageIds: [], messages: new Map() };
	}

	// 研究相关辅助方法
	private appendResearch(researchId: string) {
		// 查找最近的 planner 消息
		let planMessage: Message | undefined;
		const reversedMessageIds = [...this.messageIds].reverse();
		for (const messageId of reversedMessageIds) {
			const message = this.getMessage(messageId);
			if (message?.agent === 'planner') {
				planMessage = message;
				break;
			}
		}

		const messageIds = [researchId];
		if (planMessage) {
			messageIds.unshift(planMessage.id);
			this.researchPlanIds.set(researchId, planMessage.id);
		}

		this.researchIds = [...this.researchIds, researchId];
		this.researchActivityIds.set(researchId, messageIds);
		this.ongoingResearchId = researchId;
	}

	private appendResearchActivity(message: Message) {
		const researchId = this.ongoingResearchId;
		if (researchId) {
			const current = this.researchActivityIds.get(researchId) || [];
			if (!current.includes(message.id)) {
				this.researchActivityIds.set(researchId, [...current, message.id]);
			}
			if (message.agent === 'reporter') {
				this.researchReportIds.set(researchId, message.id);
			}
		}
	}

	private openResearch(messageId: string) {
		this.openResearchId = messageId;
	}

	private closeResearch() {
		this.openResearchId = null;
	}

	// 查找消息的辅助方法
	private existsMessage(messageId: string): boolean {
		return this.messages.has(messageId);
	}

	public getMessage(messageId: string): Message | undefined {
		return this.messages.get(messageId);
	}

	private findMessageByToolCallId(toolCallId: string): Message | undefined {
		for (const message of this.messages.values()) {
			if (message.toolCalls?.some((tc) => tc.id === toolCallId)) {
				return message;
			}
		}
		return undefined;
	}

	// 初始化聊天
	initializeChat(threadId: string) {
		this.currentThreadId = threadId;
		const { messageIds, messages } = this.loadChatFromStorage(threadId);
		this.messageIds = messageIds;
		this.messages = messages;
		this.error = null;
	}

	// 添加消息
	addMessage(message: Omit<Message, 'id'> & { id?: string }) {
		const id = message.id || crypto.randomUUID();
		const newMessage: Message = {
			id,
			...message
		};

		// 处理研究相关消息
		if (
			newMessage.agent === 'coder' ||
			newMessage.agent === 'reporter' ||
			newMessage.agent === 'researcher'
		) {
			if (!this.ongoingResearchId) {
				this.appendResearch(id);
				this.openResearch(id);
			}
			this.appendResearchActivity(newMessage);
		}

		// 只有当消息不存在时才添加到 messageIds
		if (!this.messageIds.includes(id)) {
			this.messageIds = [...this.messageIds, id];
		}
		this.messages.set(id, newMessage);
		this.saveChatToStorage();
		return newMessage;
	}

	// 更新消息
	updateMessage(messageId: string, updates: Partial<Message>) {
		const message = this.messages.get(messageId);
		if (message) {
			const updatedMessage = { ...message, ...updates };

			// 处理研究完成状态
			if (
				this.ongoingResearchId &&
				updatedMessage.agent === 'reporter' &&
				!updatedMessage.isStreaming
			) {
				this.ongoingResearchId = null;
			}

			this.messages.set(messageId, updatedMessage);
			this.saveChatToStorage();
		}
	}

	// 发送消息
	async sendMessage(
		content: string,
		{
			interruptFeedback,
			resources
		}: {
			interruptFeedback?: string;
			resources?: Array<Resource>;
		} = {}
	) {
		if (!this.currentThreadId || this.isStreaming) return;

		// 添加用户消息
		this.addMessage({
			threadId: this.currentThreadId,
			role: 'user',
			content,
			contentChunks: [content],
			resources
		});

		this.isStreaming = true;
		this.error = null;
		this.abortController = new AbortController();

		let messageId: string | undefined;

		try {
			const stream = chatStream(
				content,
				{
					thread_id: this.currentThreadId,
      				interrupt_feedback: interruptFeedback,
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
				const { type, data } = event;
				messageId = data.id;
				let message: Message | undefined;

				if (type === 'tool_call_result') {
					message = this.findMessageByToolCallId(data.tool_call_id);
				} else if (!this.existsMessage(messageId)) {
					// 基于事件 ID 创建新消息
					message = {
						id: messageId,
						threadId: data.thread_id,
						agent: data.agent,
						role: data.role,
						content: '',
						contentChunks: [],
						reasoningContent: '',
						reasoningContentChunks: [],
						isStreaming: true
					};
					this.addMessage(message);
				}

				message ??= this.getMessage(messageId);
				if (message) {
					const mergedMessage = mergeMessage(message, event);
					this.messages.set(message.id, mergedMessage);
				}
			}
		} catch (error: unknown) {
			if ((error as Error).name !== 'AbortError') {
				console.error('Chat error:', error);
				this.error = (error as Error).message || 'An error occurred';
			}
			// 更新消息状态
			if (messageId != null) {
				const message = this.getMessage(messageId);
				if (message?.isStreaming) {
					message.isStreaming = false;
					this.messages.set(messageId, message);
				}
			}
			this.ongoingResearchId = null;
		} finally {
			this.isStreaming = false;
			this.abortController = null;
			this.saveChatToStorage();
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
		const messageIndex = this.messageIds.findIndex((id) => id === messageId);
		if (messageIndex === -1) return;

		// 移除该消息及其后的所有消息
		const messageIdsToKeep = this.messageIds.slice(0, messageIndex);
		const messageIdsToRemove = this.messageIds.slice(messageIndex);

		// 从 Map 中删除被移除的消息
		messageIdsToRemove.forEach((id) => this.messages.delete(id));

		this.messageIds = messageIdsToKeep;

		// 找到最后一条用户消息
		const lastUserMessage = messageIdsToKeep
			.slice()
			.reverse()
			.map((id) => this.messages.get(id))
			.find((m) => m && m.role === 'user');

		if (lastUserMessage) {
			await this.sendMessage(lastUserMessage.content);
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
		this.messageIds = [];
		this.messages = new Map();
		this.researchIds = [];
		this.researchPlanIds = new Map();
		this.researchReportIds = new Map();
		this.researchActivityIds = new Map();
		this.ongoingResearchId = null;
		this.openResearchId = null;
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
		return this.messageIds.map((id) => this.messages.get(id)).filter(Boolean) as Message[];
	}

	// 获取消息 ID 列表
	getMessageIds(): string[] {
		return this.messageIds;
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

	// 获取研究 ID 列表
	getResearchIds(): string[] {
		return this.researchIds;
	}

	// 切换研究报告显示状态
	toggleResearchReport(researchId: string) {
		if (this.openResearchId === researchId) {
			this.closeResearch();
		} else {
			this.openResearch(researchId);
		}
	}

	// 获取研究报告状态
	getResearchReport(researchId: string) {
		return {
			isOpen: this.openResearchId === researchId,
			isGenerating: this.ongoingResearchId === researchId
		};
	}

	// 获取研究活动消息 IDs
	getResearchActivityIds(researchId: string): string[] {
		return this.researchActivityIds.get(researchId) || [];
	}

	// 获取研究计划消息 ID
	getResearchPlanId(researchId: string): string | undefined {
		return this.researchPlanIds.get(researchId);
	}

	// 获取研究报告消息 ID
	getResearchReportId(researchId: string): string | undefined {
		return this.researchReportIds.get(researchId);
	}

	// 检查是否有报告
	hasResearchReport(researchId: string): boolean {
		return this.researchReportIds.has(researchId);
	}

	// 获取正在进行的研究 ID
	getOngoingResearchId(): string | null {
		return this.ongoingResearchId;
	}

	// 获取当前打开的研究 ID
	getOpenResearchId(): string | null {
		return this.openResearchId;
	}

	// 获取最后一个等待反馈的消息 ID
	getLastFeedbackMessageId(): string | null {
		// 从最新的消息开始查找，找到第一个有 options 的消息
		for (let i = this.messageIds.length - 1; i >= 0; i--) {
			const messageId = this.messageIds[i];
			const message = this.messages.get(messageId);
			if (message && message.options && message.options.length > 0) {
				return messageId;
			}
		}
		return null;
	}

	getLastInterruptMessage(): Message | null {
		// 从最新的消息开始查找，找到第一个有 interruptFeedback 的消息
		for (let i = this.messageIds.length - 1; i >= 0; i--) {
			const messageId = this.messageIds[i];
			const message = this.messages.get(messageId);
			if (message && message.interruptFeedback) {
				return message;
			}
		}
		return null;
	}
}

// 创建全局实例
export const chatStore = new ChatStore();
