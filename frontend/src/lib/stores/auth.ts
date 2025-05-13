import { writable, get } from 'svelte/store';
import { account } from '$lib/appwrite';
import type { Models } from 'appwrite';
import { ID } from 'appwrite';
// import { goto } from '$app/navigation';
// import { base } from '$app/paths';
// import { toast } from 'svelte-sonner';

type AuthState = {
    user: Models.User<Models.Preferences> | null;
    loading: boolean;
    error: string | null;
};

const createAuthStore = () => {
    const { subscribe, update } = writable<AuthState>({
        user: null,
        loading: true,
        error: null
    });

    let initialized = false;

    return {
        subscribe,
        setUser: (user: Models.User<Models.Preferences> | null) => update(state => ({ ...state, user })),
        setLoading: (loading: boolean) => update(state => ({ ...state, loading })),
        setError: (error: string | null) => update(state => ({ ...state, error })),
        init: async () => {
            // 如果已经初始化过，直接返回
            if (initialized) {
                return;
            }
            initialized = true;
            try {
                const user = await account.get();
                update(state => ({ ...state, user: user as Models.User<Models.Preferences>, loading: false }));
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            } catch (error) {
                update(state => ({ ...state, user: null, loading: false }));
            }
        },
        login: async (email: string, password: string) => {
            update(state => ({ ...state, loading: true, error: null }));
            try {
                // 检查用户是否已登录
                const state = get(auth);
                if (state.user) {
                    return state.user;
                }
                // await account.deleteSession('current');
                
                // 创建邮箱密码会话
                await account.createEmailPasswordSession(email, password);
                const user = await account.get();
                update(state => ({ ...state, user: user as Models.User<Models.Preferences>, loading: false }));
                
            } catch (error) {
                update(state => ({ ...state, loading: false, error: (error as Error).message }));
                throw new Error((error as Error).message || '登录失败');
            }
        },
        register: async (email: string, password: string, username: string) => {
            update(state => ({ ...state, loading: true, error: null }));
            try {
                // 检查用户是否已登录
                const state = get(auth);
                if (state.user) {
                    return state.user;
                }
                
                // 创建用户账号
                await account.create(ID.unique(), email, password, username);
                
                
                // 创建邮箱密码会话
                await account.createEmailPasswordSession(email, password);
                const user = await account.get();
                update(state => ({ ...state, user, loading: false }));
                
            } catch (error) {
                update(state => ({ ...state, loading: false, error: (error as Error).message }));
                throw new Error((error as Error).message || '创建失败');
            }
        },
        logout: async () => {
            try {
                await account.deleteSession('current');
                update(state => ({ ...state, user: null }));
            } catch (error) {
                console.error('Logout failed:', error);
                throw new Error((error as Error).message || '创建失败');
            }
        }
    };
};

export const auth = createAuthStore();