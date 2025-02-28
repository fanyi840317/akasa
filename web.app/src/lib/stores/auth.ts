import { writable } from 'svelte/store';
import { account } from '../appwrite';
import type { Models } from 'appwrite';

type AuthState = {
    user: Models.User<Models.Preferences> | null;
    loading: boolean;
    error: string | null;
};

const createAuthStore = () => {
    const { subscribe, set, update } = writable<AuthState>({
        user: null,
        loading: true,
        error: null
    });

    return {
        subscribe,
        setUser: (user: Models.User<Models.Preferences> | null) => update(state => ({ ...state, user })),
        setLoading: (loading: boolean) => update(state => ({ ...state, loading })),
        setError: (error: string | null) => update(state => ({ ...state, error })),
        init: async () => {
            try {
                const user = await account.get();
                update(state => ({ ...state, user, loading: false }));
            } catch (error) {
                update(state => ({ ...state, user: null, loading: false }));
            }
        },
        logout: async () => {
            try {
                await account.deleteSession('current');
                update(state => ({ ...state, user: null }));
            } catch (error) {
                console.error('Logout failed:', error);
            }
        }
    };
};

export const auth = createAuthStore();