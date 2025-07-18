import { ID, type Models, OAuthProvider } from 'appwrite';
import { browser } from '$app/environment';
import { account} from '$lib/constants';
import type { User } from '$lib/types/user';

// Appwrite configuration

// Auth state
class AuthStore {
	#user = $state<Models.User<Models.Preferences> | null>(null);
	#loading = $state(true);
	#error = $state<string | null>(null);

	get user(): User | null {
		if (!this.#user) return null;
		
		return {
			$id: this.#user.$id,
			name: this.#user.name,
			email: this.#user.email,
			createdAt: new Date(this.#user.$createdAt),
			updatedAt: new Date(this.#user.$updatedAt),
			avatar: this.#user.prefs?.avatar as string | undefined
		};
	}

	get rawUser() {
		return this.#user;
	}

	get loading() {
		return this.#loading;
	}

	get error() {
		return this.#error;
	}

	get isAuthenticated() {
		return this.#user !== null;
	}

	constructor() {
		if (browser) {
			this.checkAuth();
		}
	}

	// Check current authentication status
	async checkAuth() {
		try {
			this.#loading = true;
			this.#error = null;
			const user = await account.get();
			this.#user = user;
		} catch (error: unknown) {
			this.#user = null;
			console.log('User not authenticated', error);
		} finally {
			this.#loading = false;
		}
	}

	// Login with email and password
	async login(email: string, password: string) {
		try {
			this.#loading = true;
			this.#error = null;
			await account.createEmailPasswordSession(email, password);
			const user = await account.get();
			this.#user = user;
			return { success: true };
		} catch (error: unknown) {
			console.log(error);
			this.#error = (error as Error).message || 'Login failed';
			return { success: false, error: this.#error };
		} finally {
			this.#loading = false;
		}
	}

	// Register new user
	async register(email: string, password: string, name: string) {
		try {
			this.#loading = true;
			this.#error = null;
			// Create account
			await account.create(ID.unique(), email, password, name);
			// Auto login after registration
			await account.createEmailPasswordSession(email, password);
			const user = await account.get();
			this.#user = user;
			return { success: true };
		} catch (error: unknown) {
			this.#error = (error as Error).message || 'Registration failed';
			return { success: false, error: this.#error };
		} finally {
			this.#loading = false;
		}
	}

	// Logout
	async logout() {
		try {
			this.#loading = true;
			this.#error = null;
			await account.deleteSession('current');
			this.#user = null;
			return { success: true };
		} catch (error: unknown) {
			this.#error = (error as Error).message || 'Logout failed';
			return { success: false, error: this.#error };
		} finally {
			this.#loading = false;
		}
	}

	// OAuth login with Google
	async loginWithGoogle() {
		try {
			this.#error = null;
			account.createOAuth2Session(OAuthProvider.Google, 
				`${window.location.origin}/console`,
				`${window.location.origin}/login`
			);
		} catch (error: unknown) {
			this.#error = (error as Error).message || 'Google login failed';
			return { success: false, error: this.#error };
		}
	}

	// OAuth login with Apple
	async loginWithApple() {
		try {
			this.#error = null;
			account.createOAuth2Session(OAuthProvider.Apple, 
				`${window.location.origin}/console`,
				`${window.location.origin}/login`
			);
		} catch (error: unknown) {
			this.#error = (error as Error).message || 'Apple login failed';
			return { success: false, error: this.#error };
		}
	}

	// Clear error
	clearError() {
		this.#error = null;
	}
}

// Export singleton instance
export const authStore = new AuthStore();