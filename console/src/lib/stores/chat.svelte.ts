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

	// 统一的状态更新方法
	private updateMapState<K, V>(map: Map<K, V>, key: K, value: V): Map<K, V> {
		return new Map(map.set(key, value));
	}

	private deleteFromMapState<K, V>(map: Map<K, V>, key: K): Map<K, V> {
		const newMap = new Map(map);
		newMap.delete(key);
		return newMap;
	}

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
				researchIds: this.researchIds,
				messages: Array.from(this.messages.entries()),
				researchPlanIds: Array.from(this.researchPlanIds.entries()),
				researchReportIds: Array.from(this.researchReportIds.entries()),
				researchActivityIds: Array.from(this.researchActivityIds.entries()),
				ongoingResearchId: this.ongoingResearchId,
				openResearchId: this.openResearchId,
				config: this.config,
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
		researchIds: string[];
		messages: Map<string, Message>;
		researchPlanIds?: Map<string, string>;
		researchReportIds?: Map<string, string>;
		researchActivityIds?: Map<string, string[]>;
		ongoingResearchId?: string | null;
		openResearchId?: string | null;
		config?: ChatConfig;
	} {
		const defaultResult = {
			messageIds: [],
			researchIds: [],
			messages: new Map<string, Message>(),
			researchPlanIds: new Map<string, string>(),
			researchReportIds: new Map<string, string>(),
			researchActivityIds: new Map<string, string[]>(),
			ongoingResearchId: null,
			openResearchId: null,
			config: { ...DEFAULT_CONFIG }
		};

		if (!browser) return defaultResult;

		try {
			const stored = localStorage.getItem(this.getStorageKey(threadId));
			if (!stored) return defaultResult;

			const {
				messageIds = [],
				researchIds = [],
				messages: messagesArray = [],
				researchPlanIds: researchPlanIdsArray = [],
				researchReportIds: researchReportIdsArray = [],
				researchActivityIds: researchActivityIdsArray = [],
				ongoingResearchId = null,
				openResearchId = null,
				config = DEFAULT_CONFIG
			} = JSON.parse(stored);

			return {
				messageIds,
				researchIds,
				messages: new Map(messagesArray as [string, Message][]),
				researchPlanIds: new Map(researchPlanIdsArray as [string, string][]),
				researchReportIds: new Map(researchReportIdsArray as [string, string][]),
				researchActivityIds: new Map(researchActivityIdsArray as [string, string[]][]),
				ongoingResearchId,
				openResearchId,
				config
			};
		} catch (error) {
			console.error('Failed to load chat from storage:', error);
			return defaultResult;
		}
	}

	// 研究相关辅助方法
	private appendResearch(researchId: string) {
		// 查找最近的 planner 消息
		const planMessage = this.findLatestPlannerMessage();
		const messageIds = [researchId];

		if (planMessage) {
			messageIds.unshift(planMessage.id);
			this.researchPlanIds = this.updateMapState(this.researchPlanIds, researchId, planMessage.id);
		}

		this.researchIds = [...this.researchIds, researchId];
		this.researchActivityIds = this.updateMapState(
			this.researchActivityIds,
			researchId,
			messageIds
		);
		this.ongoingResearchId = researchId;
	}

	private appendResearchActivity(message: Message) {
		const researchId = this.ongoingResearchId;
		if (!researchId) return;

		const current = this.researchActivityIds.get(researchId) || [];
		if (!current.includes(message.id)) {
			this.researchActivityIds = this.updateMapState(this.researchActivityIds, researchId, [
				...current,
				message.id
			]);
		}
		if (message.agent === 'reporter') {
			this.researchReportIds = this.updateMapState(this.researchReportIds, researchId, message.id);
		}
	}

	private findLatestPlannerMessage(): Message | undefined {
		const reversedMessageIds = [...this.messageIds].reverse();
		for (const messageId of reversedMessageIds) {
			const message = this.getMessage(messageId);
			if (message?.agent === 'planner') {
				return message;
			}
		}
		return undefined;
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
		// for (const message of this.messages.values()) {
		// 	if (message.toolCalls?.some((tc) => tc.id === toolCallId)) {
		// 		return message;
		// 	}
		// }
		// return undefined;
		return Array.from(this.messages.values())
			.reverse()
			.find((message) => {
				if (message.toolCalls) {
					return message.toolCalls.some((toolCall) => toolCall.id === toolCallId);
				}
				return undefined;
			});
	}

	// 初始化聊天
	initializeChat(threadId: string) {
		// 避免重复初始化同一个线程
		if (this.currentThreadId === threadId) {
			return;
		}

		this.currentThreadId = threadId;
		const {
			messageIds,
			researchIds,
			messages,
			researchPlanIds,
			researchReportIds,
			researchActivityIds,
			ongoingResearchId,
			openResearchId,
			config
		} = this.loadChatFromStorage(threadId);

		this.messageIds = messageIds;
		this.researchIds = researchIds;
		this.messages = messages;
		this.researchPlanIds = researchPlanIds || new Map();
		this.researchReportIds = researchReportIds || new Map();
		this.researchActivityIds = researchActivityIds || new Map();
		this.ongoingResearchId = ongoingResearchId || null;
		this.openResearchId = openResearchId || null;
		if (config) {
			this.config = { ...this.config, ...config };
		}
		this.error = null;
	}

	// 添加消息
	addMessage(message: Omit<Message, 'id'> & { id?: string }) {
		const id = message.id || crypto.randomUUID();
		const newMessage: Message = { id, ...message };

		// 处理研究相关消息
		this.handleResearchMessage(newMessage, id);

		// 只有当消息不存在时才添加到 messageIds
		if (!this.messageIds.includes(id)) {
			this.messageIds = [...this.messageIds, id];
		}
		this.messages = this.updateMapState(this.messages, id, newMessage);
		this.saveChatToStorage();
		return newMessage;
	}

	// 更新消息
	updateMessage(messageId: string, updates: Partial<Message>) {
		const message = this.messages.get(messageId);
		if (!message) return;

		const updatedMessage = { ...message, ...updates };

		// 处理研究完成状态
		if (
			this.ongoingResearchId &&
			updatedMessage.agent === 'reporter' &&
			!updatedMessage.isStreaming
		) {
			this.ongoingResearchId = null;
		}

		this.messages = this.updateMapState(this.messages, messageId, updatedMessage);
		this.saveChatToStorage();
	}

	// 处理研究相关消息的辅助方法
	private handleResearchMessage(newMessage: Message, id: string) {
		const isResearchAgent = ['coder', 'reporter', 'researcher'].includes(newMessage.agent || '');

		if (isResearchAgent) {
			if (!this.ongoingResearchId) {
				this.appendResearch(id);
				this.openResearch(id);
			}
			this.appendResearchActivity(newMessage);
		}
	}

	// 停止消息流式传输的辅助方法
	private stopMessageStreaming(messageId: string) {
		const message = this.getMessage(messageId);
		if (message?.isStreaming) {
			const updatedMessage = { ...message, isStreaming: false };
			this.messages = this.updateMapState(this.messages, messageId, updatedMessage);
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
				// console.log("server:",data,type);
				messageId = data.id;
				let message: Message | undefined;
				let targetMessageId: string;

				if (type === 'tool_call_result') {
					message = this.findMessageByToolCallId(data.tool_call_id);
					console.log('==============================');
					console.log('tool_call_result', data);
					console.log('message', message);
					targetMessageId = message?.id || messageId;
				} else {
					targetMessageId = messageId;
					if (!this.existsMessage(messageId)) {
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
				}

				message ??= this.getMessage(targetMessageId);
				if (message) {
					const mergedMessage = mergeMessage(message, event);
					// 使用重新赋值来触发响应式更新
					this.updateMessage(targetMessageId, mergedMessage);
				}
			}
		} catch (error: unknown) {
			if ((error as Error).name !== 'AbortError') {
				console.error('Chat error:', error);
				this.error = (error as Error).message || 'An error occurred';
			}
			// 更新消息状态
			if (messageId != null) {
				this.stopMessageStreaming(messageId);
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
		let newMessages = new Map(this.messages);
		messageIdsToRemove.forEach((id) => {
			newMessages = this.deleteFromMapState(newMessages, id);
		});
		this.messages = newMessages;
		this.messageIds = messageIdsToKeep;

		// 找到最后一条用户消息并重新发送
		const lastUserMessage = this.findLastUserMessage(messageIdsToKeep);
		if (lastUserMessage) {
			await this.sendMessage(lastUserMessage.content);
		}
	}

	// 查找最后一条用户消息的辅助方法
	private findLastUserMessage(messageIds: string[]): Message | undefined {
		return messageIds
			.slice()
			.reverse()
			.map((id) => this.messages.get(id))
			.find((m) => m && m.role === 'user');
	}

	// 处理选项点击（用于中断反馈）
	async handleOptionClick(option: { text: string; value: string }) {
		if (option.value) {
			await this.sendMessage(option.value);
		}
	}

	// 重置聊天状态的辅助方法
	private resetChatState() {
		this.messageIds = [];
		this.messages = new Map();
		this.researchIds = [];
		this.researchPlanIds = new Map();
		this.researchReportIds = new Map();
		this.researchActivityIds = new Map();
		this.ongoingResearchId = null;
		this.openResearchId = null;
		this.isStreaming = false;
		this.error = null;
		this.input = '';
		this.abortController = null;
	}

	// 清空聊天
	clearChat() {
		this.resetChatState();
		this.saveChatToStorage();
	}

	// 清除特定线程的聊天记录
	clearThreadChat(threadId: string) {
		if (!browser) return;

		try {
			localStorage.removeItem(this.getStorageKey(threadId));
			// 如果是当前线程，也清空内存中的聊天
			if (this.currentThreadId === threadId) {
				this.resetChatState();
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

	// 简化的 getter 方法
	getMessages(): Message[] {
		return this.messageIds.map((id) => this.messages.get(id)).filter(Boolean) as Message[];
	}

	getMessageIds = () => this.messageIds;
	getIsStreaming = () => this.isStreaming;
	getError = () => this.error;
	getInput = () => this.input;
	getConfig = () => this.config;

	// 清除错误
	clearError() {
		this.error = null;
	}

	// 研究相关的简化 getter 方法
	getResearchIds = () => this.researchIds;
	getOngoingResearchId = () => this.ongoingResearchId;
	getOpenResearchId = () => this.openResearchId;
	getResearchActivityIds = (researchId: string) => this.researchActivityIds.get(researchId) || [];
	getResearchPlanId = (researchId: string) => this.researchPlanIds.get(researchId);
	getResearchReportId = (researchId: string) => this.researchReportIds.get(researchId);
	hasResearchReport = (researchId: string) => this.researchReportIds.has(researchId);

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

	// 获取所有本地聊天会话
	getAllChatSessions(): Array<{ name: string; id: string; timestamp: number }> {
		if (!browser) return [];

		try {
			const chats: Array<{ name: string; id: string; timestamp: number }> = [];

			// 遍历 localStorage 查找聊天数据
			for (let i = 0; i < localStorage.length; i++) {
				const key = localStorage.key(i);
				if (key && key.startsWith('akasa_chat_')) {
					try {
						const threadId = key.replace('akasa_chat_', '');
						const chatData = JSON.parse(localStorage.getItem(key) || '{}');

						// 获取第一条用户消息作为聊天标题
						let chatTitle = `Chat ${threadId.slice(0, 8)}`;
						if (chatData.messages && Array.isArray(chatData.messages)) {
							const firstUserMessage = chatData.messages.find(
								([, message]: [string, Message]) => message.role === 'user'
							);
							if (firstUserMessage && firstUserMessage[1].content) {
								chatTitle =
									firstUserMessage[1].content.slice(0, 30) +
									(firstUserMessage[1].content.length > 30 ? '...' : '');
							}
						}

						chats.push({
							name: chatTitle,
							id: threadId,
							timestamp: chatData.timestamp || 0
						});
					} catch (error) {
						console.error('Error parsing chat data:', error);
					}
				}
			}

			// 按时间戳排序，最新的在前
			chats.sort((a, b) => b.timestamp - a.timestamp);
			return chats;
		} catch (error) {
			console.error('Error loading local chats:', error);
			return [];
		}
	}

	// 删除聊天会话
	deleteChatSession(chatId: string): boolean {
		if (!browser) return false;

		try {
			localStorage.removeItem(this.getStorageKey(chatId));
			return true;
		} catch (error) {
			console.error('Error deleting chat session:', error);
			return false;
		}
	}

	// 重命名聊天会话
	renameChatSession(chatId: string, newName: string): boolean {
		if (!browser) return false;

		try {
			const chatKey = this.getStorageKey(chatId);
			const chatData = JSON.parse(localStorage.getItem(chatKey) || '{}');

			// 更新聊天标题
			chatData.title = newName;
			localStorage.setItem(chatKey, JSON.stringify(chatData));
			return true;
		} catch (error) {
			console.error('Error renaming chat session:', error);
			return false;
		}
	}
}

// 创建全局实例
export const chatStore = new ChatStore();
