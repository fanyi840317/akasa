import { writable } from 'svelte/store';

type Message = {
	id: string;
	content: string;
	timestamp: Date;
	type: 'user' | 'assistant';
	chatId?: string;
};

type MessageState = {
	messages: Message[];
	currentChatId: string | null;
};

const createMessageStore = () => {
	const store = writable<MessageState>({
		messages: [],
		currentChatId: null
	});

	return {
		subscribe: store.subscribe,

		// 添加新消息
		addMessage: (content: string, type: 'user' | 'assistant' = 'user', chatId?: string) => {
			const message: Message = {
				id: crypto.randomUUID(),
				content,
				timestamp: new Date(),
				type,
				chatId
			};

			store.update(state => ({
				...state,
				messages: [...state.messages, message]
			}));

			// 模拟本地数据库存储
			if (typeof localStorage !== 'undefined') {
				try {
					const existingMessages = JSON.parse(localStorage.getItem('akasa_messages') || '[]');
					existingMessages.push({
						...message,
						timestamp: message.timestamp.toISOString()
					});
					localStorage.setItem('akasa_messages', JSON.stringify(existingMessages));
				} catch (error) {
					console.error('Failed to save message to localStorage:', error);
				}
			}

			return message;
		},

		// 获取指定聊天的消息
		getMessagesByChatId: (chatId: string) => {
			let messages: Message[] = [];
			store.subscribe(state => {
				messages = state.messages.filter(msg => msg.chatId === chatId);
			})();
			return messages;
		},

		// 设置当前聊天ID
		setCurrentChatId: (chatId: string | null) => {
			store.update(state => ({
				...state,
				currentChatId: chatId
			}));
		},

		// 从本地存储加载消息
		loadMessages: () => {
			if (typeof localStorage !== 'undefined') {
				try {
					const savedMessages = JSON.parse(localStorage.getItem('akasa_messages') || '[]');
					const messages = savedMessages.map((msg: any) => ({
						...msg,
						timestamp: new Date(msg.timestamp)
					}));
					store.update(state => ({
						...state,
						messages
					}));
				} catch (error) {
					console.error('Failed to load messages from localStorage:', error);
				}
			}
		},

		// 清空消息
		clearMessages: () => {
			store.update(state => ({
				...state,
				messages: []
			}));
			if (typeof localStorage !== 'undefined') {
				localStorage.removeItem('akasa_messages');
			}
		}
	};
};

export const messageStore = createMessageStore();
export type { Message };