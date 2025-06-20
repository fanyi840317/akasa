import { describe, it, expect, vi, beforeEach } from 'vitest';
import { authStore } from './auth.svelte';

// Mock Appwrite
vi.mock('appwrite', () => {
	const mockAccount = {
		get: vi.fn(),
		create: vi.fn(),
		createEmailPasswordSession: vi.fn(),
		deleteSession: vi.fn(),
		createOAuth2Session: vi.fn()
	};

	const mockClient = {
		setEndpoint: vi.fn().mockReturnThis(),
		setProject: vi.fn().mockReturnThis()
	};

	return {
		Client: vi.fn(() => mockClient),
		Account: vi.fn(() => mockAccount),
		ID: {
			unique: vi.fn(() => 'unique-id')
		}
	};
});

// Mock browser environment
vi.mock('$app/environment', () => ({
	browser: true
}));

describe('AuthStore', () => {
	beforeEach(() => {
		vi.clearAllMocks();
	});

	it('should initialize with loading state', () => {
		expect(authStore.loading).toBe(true);
		expect(authStore.user).toBe(null);
		expect(authStore.isAuthenticated).toBe(false);
	});

	it('should handle successful login', async () => {
		const mockUser = {
			$id: 'user-id',
			name: 'Test User',
			email: 'test@example.com'
		};

		// Mock successful login
		const { Account } = await import('appwrite');
		const mockAccount = new Account({} as any);
		(mockAccount.createEmailPasswordSession as any).mockResolvedValue({});
		(mockAccount.get as any).mockResolvedValue(mockUser);

		const result = await authStore.login('test@example.com', 'password123');

		expect(result.success).toBe(true);
		expect(authStore.user).toEqual(mockUser);
		expect(authStore.isAuthenticated).toBe(true);
	});

	it('should handle failed login', async () => {
		const { Account } = await import('appwrite');
		const mockAccount = new Account({} as any);
		(mockAccount.createEmailPasswordSession as any).mockRejectedValue(
			new Error('Invalid credentials')
		);

		const result = await authStore.login('test@example.com', 'wrongpassword');

		expect(result.success).toBe(false);
		expect(result.error).toBe('Invalid credentials');
		expect(authStore.user).toBe(null);
		expect(authStore.isAuthenticated).toBe(false);
	});

	it('should handle successful registration', async () => {
		const mockUser = {
			$id: 'user-id',
			name: 'New User',
			email: 'new@example.com'
		};

		const { Account } = await import('appwrite');
		const mockAccount = new Account({} as any);
		(mockAccount.create as any).mockResolvedValue({});
		(mockAccount.createEmailPasswordSession as any).mockResolvedValue({});
		(mockAccount.get as any).mockResolvedValue(mockUser);

		const result = await authStore.register('new@example.com', 'password123', 'New User');

		expect(result.success).toBe(true);
		expect(authStore.user).toEqual(mockUser);
		expect(authStore.isAuthenticated).toBe(true);
	});

	it('should handle successful logout', async () => {
		// First set a user
		const mockUser = {
			$id: 'user-id',
			name: 'Test User',
			email: 'test@example.com'
		};

		const { Account } = await import('appwrite');
		const mockAccount = new Account({} as any);
		(mockAccount.deleteSession as any).mockResolvedValue({});

		// Manually set user for testing
		(authStore as any).user = mockUser;

		const result = await authStore.logout();

		expect(result.success).toBe(true);
		expect(authStore.user).toBe(null);
		expect(authStore.isAuthenticated).toBe(false);
	});

	it('should clear error', () => {
		// Manually set error for testing
		(authStore as any).error = 'Test error';
		
		authStore.clearError();
		
		expect(authStore.error).toBe(null);
	});
});