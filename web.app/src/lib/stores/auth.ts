import { writable, get } from 'svelte/store';
import { account } from '../appwrite';
import type { Models } from 'appwrite';
import { ID } from 'appwrite';

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
                update(state => ({ ...state, loading: false }));
            }
        },
        login: async (email: string, password: string, returnUrl?: string) => {
            update(state => ({ ...state, loading: true, error: null }));
            try {
                try {
                    // 检查用户是否已登录
                    const session = await account.getSession('current');
                    
                    if(session != null){
                        // 尝试删除当前会话，以防止"Creation of a session is prohibited when a session is active"错误
                        await account.deleteSession('current');
                    
                    }
                } catch (sessionError) {
                    // 忽略删除会话时的错误，可能是因为没有活跃会话
                    console.log('No active session to delete or session deletion failed');
                }
                
                await account.createEmailPasswordSession(email, password);

                const user = await account.get();
                console.log('User logged in:', user);
                update(state => ({ ...state, user, loading: false }));
            } catch (error: any) {
                update(state => ({ ...state, loading: false, error: error.message }));
                throw error;
            }
        },
        register: async (email: string, password: string, username: string, returnUrl?: string) => {
            update(state => ({ ...state, loading: true, error: null }));
            try {
                // 创建用户账号
                await account.create(ID.unique(), email, password, username);
                
                try {
                    // 尝试删除当前会话，以防止"Creation of a session is prohibited when a session is active"错误
                    await account.deleteSession('current');
                } catch (sessionError) {
                    // 忽略删除会话时的错误，可能是因为没有活跃会话
                    console.log('No active session to delete or session deletion failed');
                }
                
                // 创建邮箱密码会话
                await account.createEmailPasswordSession(email, password);
                const user = await account.get();
                update(state => ({ ...state, user, loading: false }));
                
            } catch (error: any) {
                update(state => ({ ...state, loading: false, error: error.message }));
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