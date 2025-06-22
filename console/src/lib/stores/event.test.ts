import { describe, it, expect, vi, beforeEach } from 'vitest';
import { eventStore } from './event.svelte';
import { databases } from '$lib/constants';
import type { Event } from '$lib/types/event';

// Mock Appwrite
vi.mock('$lib/constants', () => ({
	databases: {
		listDocuments: vi.fn(),
		getDocument: vi.fn(),
		createDocument: vi.fn(),
		updateDocument: vi.fn(),
		deleteDocument: vi.fn()
	},
	appwriteConfig: {
		databaseId: 'test-db',
		eventsCollectionId: 'test-events'
	}
}));

vi.mock('appwrite', () => ({
	ID: {
		unique: () => 'test-id'
	},
	Query: {
		equal: vi.fn(),
		search: vi.fn(),
		contains: vi.fn(),
		or: vi.fn()
	}
}));

const mockEvent: Event & { $collectionId: string; $databaseId: string; $createdAt: string; $updatedAt: string; $permissions: string[] } = {
	$id: 'test-event-1',
	name: 'Test Event',
	summary: 'Test Summary',
	content: 'Test Content',
	user_id: 'test-user',
	status: 'draft',
	createdAt: new Date(),
	updatedAt: new Date(),
	$collectionId: 'test-events',
	$databaseId: 'test-db',
	$createdAt: new Date().toISOString(),
	$updatedAt: new Date().toISOString(),
	$permissions: []
};

describe('EventStore', () => {
	beforeEach(() => {
		vi.clearAllMocks();
		// 重置 store 状态
		eventStore.events = [];
		eventStore.currentEvent = null;
		eventStore.isLoading = false;
		eventStore.error = null;
	});

	describe('getEvents', () => {
		it('should fetch events successfully', async () => {
			const mockResponse = {
				documents: [mockEvent],
				total: 1
			};
			
			vi.mocked(databases.listDocuments).mockResolvedValue(mockResponse);

			const result = await eventStore.getEvents();

			expect(databases.listDocuments).toHaveBeenCalledWith(
				'test-db',
				'test-events',
				[]
			);
			expect(result).toEqual([mockEvent]);
			expect(eventStore.events).toEqual([mockEvent]);
			expect(eventStore.isLoading).toBe(false);
			expect(eventStore.error).toBe(null);
		});

		it('should handle errors when fetching events', async () => {
			const errorMessage = 'Failed to fetch events';
			vi.mocked(databases.listDocuments).mockRejectedValue(new Error(errorMessage));

			await expect(eventStore.getEvents()).rejects.toThrow(errorMessage);
			expect(eventStore.error).toBe(errorMessage);
			expect(eventStore.isLoading).toBe(false);
		});
	});

	describe('getEventById', () => {
		it('should fetch event by id successfully', async () => {
			vi.mocked(databases.getDocument).mockResolvedValue(mockEvent);

			const result = await eventStore.getEventById('test-event-1');

			expect(databases.getDocument).toHaveBeenCalledWith(
				'test-db',
				'test-events',
				'test-event-1'
			);
			expect(result).toEqual(mockEvent);
			expect(eventStore.currentEvent).toEqual(mockEvent);
		});

		it('should handle errors when fetching event by id', async () => {
			const errorMessage = 'Event not found';
			vi.mocked(databases.getDocument).mockRejectedValue(new Error(errorMessage));

			await expect(eventStore.getEventById('invalid-id')).rejects.toThrow(errorMessage);
			expect(eventStore.error).toBe(errorMessage);
		});
	});

	describe('createEvent', () => {
		it('should create event successfully', async () => {
			const newEventData = {
				name: 'New Event',
				title: 'New Event',
				summary: 'New Summary',
				user_id: 'test-user'
			};

			vi.mocked(databases.createDocument).mockResolvedValue(mockEvent);

			const result = await eventStore.createEvent(newEventData);

			expect(databases.createDocument).toHaveBeenCalledWith(
				'test-db',
				'test-events',
				'test-id',
				expect.objectContaining({
					...newEventData,
					createdAt: expect.any(Date),
					updatedAt: expect.any(Date)
				})
			);
			expect(result).toEqual(mockEvent);
			expect(eventStore.events).toContain(mockEvent);
			expect(eventStore.currentEvent).toEqual(mockEvent);
		});
	});

	describe('updateEvent', () => {
		it('should update event successfully', async () => {
			// 先设置一些初始事件
			eventStore.events = [mockEvent];
			eventStore.currentEvent = mockEvent;

			const updatedEvent = { ...mockEvent, title: 'Updated Title' };
			vi.mocked(databases.updateDocument).mockResolvedValue(updatedEvent);

			const result = await eventStore.updateEvent('test-event-1', { name: 'Updated Title' });

			expect(databases.updateDocument).toHaveBeenCalledWith(
				'test-db',
				'test-events',
				'test-event-1',
				expect.objectContaining({
					name: 'Updated Title',
					updatedAt: expect.any(Date)
				})
			);
			expect(result).toEqual(updatedEvent);
			expect(eventStore.currentEvent).toEqual(updatedEvent);
		});
	});

	describe('deleteEvent', () => {
		it('should delete event successfully', async () => {
			// 先设置一些初始事件
			eventStore.events = [mockEvent];
			eventStore.currentEvent = mockEvent;

			vi.mocked(databases.deleteDocument).mockResolvedValue({} as never);

			await eventStore.deleteEvent('test-event-1');

			expect(databases.deleteDocument).toHaveBeenCalledWith(
				'test-db',
				'test-events',
				'test-event-1'
			);
			expect(eventStore.events).toEqual([]);
			expect(eventStore.currentEvent).toBe(null);
		});
	});

	describe('utility methods', () => {
		it('should clear error', () => {
			eventStore.error = 'Some error';
			eventStore.clearError();
			expect(eventStore.error).toBe(null);
		});

		it('should set current event', () => {
			eventStore.setCurrentEvent(mockEvent);
			expect(eventStore.currentEvent).toEqual(mockEvent);

			eventStore.setCurrentEvent(null);
			expect(eventStore.currentEvent).toBe(null);
		});
	});
});