import { describe, it, expect, beforeEach, vi } from 'vitest';
import { interactionStore } from './interaction.svelte.js';

// Mock Appwrite dependencies
vi.mock('appwrite', () => ({
	ID: {
		unique: () => 'mock-unique-id'
	},
	Query: {
		equal: (field: string, value: string) => `${field}=${value}`
	}
}));

vi.mock('$lib/constants', () => ({
	databases: {
		listDocuments: vi.fn().mockResolvedValue({ documents: [] }),
		createDocument: vi.fn().mockResolvedValue({ $id: 'mock-id' }),
		deleteDocument: vi.fn().mockResolvedValue({})
	},
	appwriteConfig: {
		databaseId: 'mock-db',
		interactionsCollectionId: 'mock-interactions',
		favoritesCollectionId: 'mock-favorites'
	}
}));

describe('InteractionStore', () => {
	let store: typeof interactionStore;

	beforeEach(() => {
		store = interactionStore;
		// 清理localStorage
		localStorage.clear();
		// 重置所有mock
		vi.clearAllMocks();
	});

	it('should initialize with default values', () => {
		expect(store).toBeDefined();
		expect(store.isLoading).toBe(false);
		expect(store.error).toBe(null);
	});

	it('should get interaction stats', async () => {
		const stats = await store.getInteractionStats('test-event-id');
		expect(stats).toEqual({ likes: 0, favorites: 0 });
	});

	it('should get user interaction state', async () => {
		const state = await store.getUserInteractionState('test-event-id', 'test-user-id');
		expect(state).toEqual({ isLiked: false, isFavorited: false });
	});

	it('should toggle like status', async () => {
		const result = await store.toggleLike('test-event-id', 'test-user-id');
		expect(result).toBe(true);
	});

	it('should toggle favorite status', async () => {
		const result = await store.toggleFavorite('test-event-id', 'test-user-id', 'Test Event');
		expect(result).toBe(true);
	});

	it('should get user favorites', async () => {
		const favorites = await store.getUserFavorites('test-user-id');
		expect(Array.isArray(favorites)).toBe(true);
	});
});