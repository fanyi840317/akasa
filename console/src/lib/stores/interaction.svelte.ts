import { ID, Query } from 'appwrite';
import { databases, appwriteConfig } from '$lib/constants';
import { browser } from '$app/environment';

// 点赞数据接口
export interface Like {
	$id?: string;
	user_id: string;
	event_id: string;
	$createdAt?: string;
	$updatedAt?: string;
}

// 收藏数据接口
export interface Favorite {
	$id?: string;
	user_id: string;
	item_id: string;
	item_type: string;
	title: string;
	description?: string;
	favorite_time: string;
	notes?: string;
	folder?: string;
	tags?: string;
	status?: string;
	folder_id?: string;
	$createdAt?: string;
	$updatedAt?: string;
}

// 交互统计接口
export interface InteractionStats {
	likes: number;
	favorites: number;
}

// 用户交互状态接口
export interface UserInteractionState {
	isLiked: boolean;
	isFavorited: boolean;
}

class InteractionStore {
	// 使用 Svelte 5 的 #state 语法
	stats = $state<Map<string, InteractionStats>>(new Map());
	userStates = $state<Map<string, UserInteractionState>>(new Map());
	isLoading = $state(false);
	error = $state<string | null>(null);

	// 生成缓存键名
	private getCacheKey(eventId: string, userId?: string): string {
		return userId ? `akasa_interaction_${eventId}_${userId}` : `akasa_stats_${eventId}`;
	}

	// 从缓存加载用户交互状态
	private loadUserStateFromCache(eventId: string, userId: string): UserInteractionState {
		if (!browser) return { isLiked: false, isFavorited: false };
		
		try {
			const stored = localStorage.getItem(this.getCacheKey(eventId, userId));
			if (stored) {
				return JSON.parse(stored);
			}
		} catch (error) {
			console.error('Failed to load user interaction state from cache:', error);
		}
		
		return { isLiked: false, isFavorited: false };
	}

	// 保存用户交互状态到缓存
	private saveUserStateToCache(eventId: string, userId: string, state: UserInteractionState) {
		if (!browser) return;
		
		try {
			localStorage.setItem(this.getCacheKey(eventId, userId), JSON.stringify(state));
		} catch (error) {
			console.error('Failed to save user interaction state to cache:', error);
		}
	}

	// 获取事件的交互统计
	async getInteractionStats(eventId: string): Promise<InteractionStats> {
		try {
			this.isLoading = true;
			this.error = null;

			// 获取点赞数 - 使用 interactionsCollectionId
			const likesResponse = await databases.listDocuments(
				appwriteConfig.databaseId,
				appwriteConfig.interactionsCollectionId,
				[
					Query.equal('event_id', eventId)
				]
			);

			// 获取收藏数 - 使用 favoritesCollectionId
			const favoritesResponse = await databases.listDocuments(
				appwriteConfig.databaseId,
				appwriteConfig.favoritesCollectionId,
				[
					Query.equal('item_id', eventId),
					Query.equal('item_type', 'event')
				]
			);

			const stats: InteractionStats = {
				likes: likesResponse.total,
				favorites: favoritesResponse.total
			};

			this.stats.set(eventId, stats);
			return stats;
		} catch (error: any) {
			this.error = error.message || 'Failed to get interaction stats';
			throw error;
		} finally {
			this.isLoading = false;
		}
	}

	// 获取用户对事件的交互状态
	async getUserInteractionState(eventId: string, userId: string): Promise<UserInteractionState> {
		try {
			// 先从缓存加载
			const localState = this.loadUserStateFromCache(eventId, userId);
			
			// 检查用户是否点赞了该事件
			const likesResponse = await databases.listDocuments(
				appwriteConfig.databaseId,
				appwriteConfig.interactionsCollectionId,
				[
					Query.equal('event_id', eventId),
					Query.equal('user_id', userId)
				]
			);

			// 检查用户是否收藏了该事件
			const favoritesResponse = await databases.listDocuments(
				appwriteConfig.databaseId,
				appwriteConfig.favoritesCollectionId,
				[
					Query.equal('item_id', eventId),
					Query.equal('user_id', userId),
					Query.equal('item_type', 'event')
				]
			);

			const isLiked = likesResponse.documents.length > 0;
			const isFavorited = favoritesResponse.documents.length > 0;

			const state: UserInteractionState = { isLiked, isFavorited };
			
			// 保存到缓存和状态
			this.saveUserStateToCache(eventId, userId, state);
			this.userStates.set(`${eventId}_${userId}`, state);
			
			return state;
		} catch (error: any) {
			// 如果服务器请求失败，返回缓存状态
			console.warn('Failed to get user interaction state from server, using cached state:', error);
			const localState = this.loadUserStateFromCache(eventId, userId);
			this.userStates.set(`${eventId}_${userId}`, localState);
			return localState;
		}
	}

	// 切换点赞状态
	async toggleLike(eventId: string, userId: string): Promise<boolean> {
		try {
			this.error = null;
			
			// 获取当前状态
			const currentState = this.userStates.get(`${eventId}_${userId}`) || 
				this.loadUserStateFromCache(eventId, userId);

			const newLikedState = !currentState.isLiked;

			if (newLikedState) {
				// 添加点赞 - 使用 interactionsCollectionId
				await databases.createDocument(
					appwriteConfig.databaseId,
					appwriteConfig.interactionsCollectionId,
					ID.unique(),
					{
						user_id: userId,
						event_id: eventId
					}
				);
			} else {
				// 移除点赞
				const userLikes = await databases.listDocuments(
					appwriteConfig.databaseId,
					appwriteConfig.interactionsCollectionId,
					[
						Query.equal('event_id', eventId),
						Query.equal('user_id', userId)
					]
				);

				if (userLikes.documents.length > 0) {
					await databases.deleteDocument(
						appwriteConfig.databaseId,
						appwriteConfig.interactionsCollectionId,
						userLikes.documents[0].$id
					);
				}
			}

			// 更新缓存状态
			const newState: UserInteractionState = {
				...currentState,
				isLiked: newLikedState
			};
			
			this.userStates.set(`${eventId}_${userId}`, newState);
			this.saveUserStateToCache(eventId, userId, newState);

			// 更新统计数据
			await this.getInteractionStats(eventId);

			return newLikedState;
		} catch (error: any) {
			this.error = error.message || 'Failed to toggle like';
			throw error;
		}
	}

	// 切换收藏状态
	async toggleFavorite(eventId: string, userId: string, eventTitle?: string): Promise<boolean> {
		try {
			this.error = null;
			
			// 获取当前状态
			const currentState = this.userStates.get(`${eventId}_${userId}`) || 
				this.loadUserStateFromCache(eventId, userId);

			const newFavoritedState = !currentState.isFavorited;

			if (newFavoritedState) {
				// 添加收藏 - 使用 favoritesCollectionId
				await databases.createDocument(
					appwriteConfig.databaseId,
					appwriteConfig.favoritesCollectionId,
					ID.unique(),
					{
						user_id: userId,
						item_id: eventId,
						item_type: 'event',
						title: eventTitle || 'Event',
						favorite_time: new Date().toISOString(),
						status: 'active'
					}
				);
			} else {
				// 移除收藏
				const userFavorites = await databases.listDocuments(
					appwriteConfig.databaseId,
					appwriteConfig.favoritesCollectionId,
					[
						Query.equal('item_id', eventId),
						Query.equal('user_id', userId),
						Query.equal('item_type', 'event')
					]
				);

				if (userFavorites.documents.length > 0) {
					await databases.deleteDocument(
						appwriteConfig.databaseId,
						appwriteConfig.favoritesCollectionId,
						userFavorites.documents[0].$id
					);
				}
			}

			// 更新缓存状态
			const newState: UserInteractionState = {
				...currentState,
				isFavorited: newFavoritedState
			};
			
			this.userStates.set(`${eventId}_${userId}`, newState);
			this.saveUserStateToCache(eventId, userId, newState);

			// 更新统计数据
			await this.getInteractionStats(eventId);

			return newFavoritedState;
		} catch (error: any) {
			this.error = error.message || 'Failed to toggle favorite';
			throw error;
		}
	}

	// 获取用户收藏的事件列表
	async getUserFavorites(userId: string): Promise<string[]> {
		try {
			this.isLoading = true;
			this.error = null;

			const favoritesResponse = await databases.listDocuments(
				appwriteConfig.databaseId,
				appwriteConfig.favoritesCollectionId,
				[
					Query.equal('user_id', userId),
					Query.equal('item_type', 'event')
				]
			);

			return favoritesResponse.documents.map(doc => doc.item_id);
		} catch (error: any) {
			this.error = error.message || 'Failed to get user favorites';
			throw error;
		} finally {
			this.isLoading = false;
		}
	}

	// 清除错误状态
	clearError() {
		this.error = null;
	}

	// 清除特定事件的缓存
	clearEventCache(eventId: string) {
		this.stats.delete(eventId);
		
		// 清除该事件相关的用户状态
		for (const [key] of this.userStates) {
			if (key.startsWith(`${eventId}_`)) {
				this.userStates.delete(key);
			}
		}
	}
}

// 创建并导出 store 实例
export const interactionStore = new InteractionStore();
export default interactionStore;