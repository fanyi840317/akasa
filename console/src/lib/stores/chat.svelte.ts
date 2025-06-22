import { Chat } from '@ai-sdk/svelte';
import type { Message } from '@ai-sdk/svelte';
import { browser } from '$app/environment';

// Chat store 类
class ChatStore {
	chat = $state<Chat | null>(null);
	messages = $state<Message[]>([]);
	status = $state<string>('ready');
	error = $state<string | null>(null);
	input = $state<string>('');
	currentEventId = $state<string | null>(null);

	// 生成存储键名
	private getStorageKey(eventId: string): string {
		return `akasa_chat_${eventId}`;
	}

	// 保存聊天记录到本地存储
	private saveChatToStorage() {
		if (!browser || !this.currentEventId) return;
		
		try {
			const chatData = {
				messages: this.messages,
				timestamp: Date.now()
			};
			localStorage.setItem(this.getStorageKey(this.currentEventId), JSON.stringify(chatData));
		} catch (error) {
			console.error('Failed to save chat to storage:', error);
		}
	}

	// 从本地存储加载聊天记录
	private loadChatFromStorage(eventId: string): Message[] {
		if (!browser) return [];
		
		try {
			const stored = localStorage.getItem(this.getStorageKey(eventId));
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
	initializeChat(apiEndpoint: string = '/api/chat', eventId?: string) {
		// 设置当前事件ID
		if (eventId) {
			this.currentEventId = eventId;
		}

		this.chat = new Chat({
			api: apiEndpoint,
			onError: (error) => {
				console.error('Chat error:', error);
				this.error = error;
			},
			onFinish: (message) => {
				console.log('Chat finished:', message);
				// 消息完成后保存到本地存储
				this.saveChatToStorage();
			}
		});

		// 绑定状态 - 使用$effect来确保响应式更新
		$effect(() => {
			if (this.chat) {
				this.messages = this.chat.messages;
				this.status = this.chat.status;
				this.error = this.chat.error;
				this.input = this.chat.input;
			}
		});
		console.log('Initialized chat:', this.chat);
		console.log('Loaded saved messages:', eventId);
		// 如果有事件ID，先加载历史聊天记录
		if (eventId) {
			const savedMessages = this.loadChatFromStorage(eventId);
			console.log('Loaded saved messages:', savedMessages);	
			if (savedMessages.length > 0) {
				this.chat.messages = savedMessages;
				// 手动更新messages状态
				this.messages = savedMessages;
			}
		}
	}

	// 发送消息
	async sendMessage(content: string) {
		if (!this.chat) {
			throw new Error('Chat not initialized');
		}
		const result = await this.chat.append({ role: 'user', content });
		// 发送消息后保存到本地存储
		this.saveChatToStorage();
		return result;
	}

	// 重新生成消息
	async regenerateMessage() {
		if (!this.chat) {
			throw new Error('Chat not initialized');
		}
		return await this.chat.reload();
	}

	// 清空聊天
	clearChat() {
		if (this.chat) {
			this.chat.messages = [];
		}
		// 清空后也保存到本地存储
		this.saveChatToStorage();
	}

	// 清除特定事件的聊天记录
	clearEventChat(eventId: string) {
		if (!browser) return;
		
		try {
			localStorage.removeItem(this.getStorageKey(eventId));
			// 如果是当前事件，也清空内存中的聊天
			if (this.currentEventId === eventId) {
				this.clearChat();
			}
		} catch (error) {
			console.error('Failed to clear event chat:', error);
		}
	}

	// 切换到不同的事件
	switchToEvent(eventId: string, apiEndpoint: string = '/api/chat') {
		// 如果是同一个事件，不需要重新初始化
		if (this.currentEventId === eventId) {
			return;
		}
		
		// 重新初始化聊天并加载对应的聊天记录
		this.initializeChat(apiEndpoint, eventId);
	}

	// 设置输入值
	setInput(value: string) {
		if (this.chat) {
			this.chat.input = value;
		}
		this.input = value;
	}

	// 获取消息
	getMessages(): Message[] {
		return this.messages;
	}

	// 获取状态
	getStatus(): string {
		return this.status;
	}

	// 获取错误
	getError(): string | null {
		return this.error;
	}

	// 获取输入值
	getInput(): string {
		return this.input;
	}
}

// 创建全局实例
export const chatStore = new ChatStore();