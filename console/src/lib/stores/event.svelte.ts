import { databases, appwriteConfig } from '$lib/constants';
import type { Event } from '$lib/types/event';
import { ID, Query } from 'appwrite';

// 统一的文档映射函数
function mapDocumentToEvent(doc: any): Event {
	return {
		$id: doc.$id,
		name: doc.name || '',
		createdAt: new Date(doc.$createdAt),
		updatedAt: new Date(doc.$updatedAt),
		content: doc.content,
		summary: doc.summary,
		categories: doc.categories,
		tags: doc.tags,
		date: doc.date,
		privacy: doc.privacy,
		user_id: doc.user_id,
		cover: doc.cover,
		location_data: JSON.parse(doc.location_data)|| {},
		status: doc.status,
		entities_data: doc.entities_data,
		creator_name: doc.creator_name,
		creator_avatar: doc.creator_avatar,
		folder_id: doc.folder_id
	} as Event;
}

// 事件状态管理
class EventStore {
	// 使用 Svelte 5 的 #state 语法
	events = $state<Event[]>([]);
	currentEvent = $state<Event | null>(null);
	isLoading = $state(false);
	error = $state<string | null>(null);

	// 获取所有事件
	async getEvents(userId?: string): Promise<Event[]> {
		this.isLoading = true;
		this.error = null;
		try {
			const queries = userId ? [Query.equal('user_id', userId)] : [];
			const response = await databases.listDocuments(
				appwriteConfig.databaseId,
				appwriteConfig.eventsCollectionId,
				queries
			);
			this.events = response.documents.map(mapDocumentToEvent);
			return this.events;
		} catch (err) {
			this.error = err instanceof Error ? err.message : '获取事件失败';
			throw err;
		} finally {
			this.isLoading = false;
		}
	}

	// 根据ID获取单个事件
	async getEventById(eventId: string): Promise<Event> {
		this.isLoading = true;
		this.error = null;
		try {
			const response = await databases.getDocument(
				appwriteConfig.databaseId,
				appwriteConfig.eventsCollectionId,
				eventId
			);
			this.currentEvent = mapDocumentToEvent(response);
			return this.currentEvent;
		} catch (err) {
			this.error = err instanceof Error ? err.message : '获取事件详情失败';
			throw err;
		} finally {
			this.isLoading = false;
		}
	}

	// 创建新事件
	async createEvent(eventData: Omit<Event, '$id' >): Promise<Event> {
		this.isLoading = true;
		this.error = null;
		try {
			// 排除数据库不支持的字段
			const { createdAt, updatedAt, ...dbEventData } = eventData;
			const response = await databases.createDocument(
				appwriteConfig.databaseId,
				appwriteConfig.eventsCollectionId,
				ID.unique(),
				{
					...dbEventData
				}
			);
			const newEvent = mapDocumentToEvent(response);
			this.events = [...this.events, newEvent];
			this.currentEvent = newEvent;
			return newEvent;
		} catch (err) {
			this.error = err instanceof Error ? err.message : '创建事件失败';
			throw err;
		} finally {
			this.isLoading = false;
		}
	}

	// 更新事件
	async updateEvent(eventId: string, eventData: Partial<Event>): Promise<Event> {
		this.isLoading = true;
		this.error = null;
		try {
			// 排除数据库不支持的字段
			const { createdAt, updatedAt, ...dbEventData } = eventData;
			const response = await databases.updateDocument(
				appwriteConfig.databaseId,
				appwriteConfig.eventsCollectionId,
				eventId,
				{
					...dbEventData
				}
			);
			const updatedEvent = mapDocumentToEvent(response);
			
			// 更新本地状态
			this.events = this.events.map(event => 
				event.$id === eventId ? updatedEvent : event
			);
			
			if (this.currentEvent?.$id === eventId) {
				this.currentEvent = updatedEvent;
			}
			
			return updatedEvent;
		} catch (err) {
			this.error = err instanceof Error ? err.message : '更新事件失败';
			throw err;
		} finally {
			this.isLoading = false;
		}
	}

	// 删除事件
	async deleteEvent(eventId: string): Promise<void> {
		this.isLoading = true;
		this.error = null;
		try {
			await databases.deleteDocument(
				appwriteConfig.databaseId,
				appwriteConfig.eventsCollectionId,
				eventId
			);
			
			// 更新本地状态
			this.events = this.events.filter(event => event.$id !== eventId);
			
			if (this.currentEvent?.$id === eventId) {
				this.currentEvent = null;
			}
		} catch (err) {
			this.error = err instanceof Error ? err.message : '删除事件失败';
			throw err;
		} finally {
			this.isLoading = false;
		}
	}

	// 搜索事件
	async searchEvents(searchTerm: string, userId?: string): Promise<Event[]> {
		this.isLoading = true;
		this.error = null;
		try {
			const queries = [
				Query.or([
					Query.search('name', searchTerm),
					Query.search('summary', searchTerm),
					Query.search('content', searchTerm)
				])
			];
			
			if (userId) {
				queries.push(Query.equal('user_id', userId));
			}
			
			const response = await databases.listDocuments(
				appwriteConfig.databaseId,
				appwriteConfig.eventsCollectionId,
				queries
			);
			
			return response.documents.map(mapDocumentToEvent);
		} catch (err) {
			this.error = err instanceof Error ? err.message : '搜索事件失败';
			throw err;
		} finally {
			this.isLoading = false;
		}
	}

	// 根据分类获取事件
	async getEventsByCategory(category: string, userId?: string): Promise<Event[]> {
		this.isLoading = true;
		this.error = null;
		try {
			const queries = [Query.contains('categories', category)];
			
			if (userId) {
				queries.push(Query.equal('user_id', userId));
			}
			
			const response = await databases.listDocuments(
				appwriteConfig.databaseId,
				appwriteConfig.eventsCollectionId,
				queries
			);
			
			return response.documents.map(mapDocumentToEvent);
		} catch (err) {
			this.error = err instanceof Error ? err.message : '获取分类事件失败';
			throw err;
		} finally {
			this.isLoading = false;
		}
	}

	// 清除错误状态
	clearError(): void {
		this.error = null;
	}

	// 设置当前事件
	setCurrentEvent(event: Event | null): void {
		this.currentEvent = event;
	}
}

// 创建全局事件 store 实例
export const eventStore = new EventStore();