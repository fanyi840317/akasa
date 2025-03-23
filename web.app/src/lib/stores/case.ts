import { writable, get } from 'svelte/store';
import { databases } from '../appwrite';
import { ID } from 'appwrite';
import type { Models } from 'appwrite';

// Case数据类型定义，基于setup_database.js中的结构
type Case = {
    $id?: string;
    cover?: string;
    title: string;
    descrp: string;
    content: string;
    user_id: string;
    happend_time: string; // ISO格式的日期时间字符串
    status?: string;
    priority?: string;
    category?: string;
    folder_id?: string;
    tags?: string;
};

type CaseState = {
    cases: Case[];
    currentCase: Case | null;
    loading: boolean;
    error: string | null;
};

// 从appwrite.ts中获取配置
import { appwriteConfig } from '../appwrite';
const { databaseId, usersCollectionId } = appwriteConfig;

// 定义cases集合ID
const casesCollectionId = 'cases';

const createCaseStore = () => {
    const { subscribe, set, update } = writable<CaseState>({
        cases: [],
        currentCase: null,
        loading: false,
        error: null
    });

    return {
        subscribe,
        // 获取所有案例
        fetchCases: async (userId?: string) => {
            update(state => ({ ...state, loading: true, error: null }));
            try {
                let query = [];
                
                // 如果提供了用户ID，则按用户ID筛选
                if (userId) {
                    query.push(`user_id=${userId}`);
                }
                
                const response = await databases.listDocuments(
                    databaseId,
                    casesCollectionId,
                    query
                );
                
                update(state => ({
                    ...state,
                    cases: response.documents as unknown as Case[],
                    loading: false
                }));
                
                return response.documents;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : '获取案例失败';
                update(state => ({ ...state, loading: false, error: errorMessage }));
                throw error;
            }
        },
        
        // 获取单个案例
        fetchCase: async (caseId: string) => {
            update(state => ({ ...state, loading: true, error: null }));
            try {
                const caseDoc = await databases.getDocument(
                    databaseId,
                    casesCollectionId,
                    caseId
                );
                
                update(state => ({
                    ...state,
                    currentCase: caseDoc as unknown as Case,
                    loading: false
                }));
                
                return caseDoc;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : '获取案例详情失败';
                update(state => ({ ...state, loading: false, error: errorMessage }));
                throw error;
            }
        },
        
        // 创建新案例
        createCase: async (caseData: Omit<Case, '$id'>) => {
            update(state => ({ ...state, loading: true, error: null }));
            try {
                const newCase = await databases.createDocument(
                    databaseId,
                    casesCollectionId,
                    ID.unique(),
                    caseData
                );
                
                update(state => ({
                    ...state,
                    cases: [...state.cases, newCase as unknown as Case],
                    currentCase: newCase as unknown as Case,
                    loading: false
                }));
                
                return newCase;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : '创建案例失败';
                update(state => ({ ...state, loading: false, error: errorMessage }));
                throw error;
            }
        },
        
        // 更新案例
        updateCase: async (caseId: string, caseData: Partial<Case>) => {
            update(state => ({ ...state, loading: true, error: null }));
            try {
                const updatedCase = await databases.updateDocument(
                    databaseId,
                    casesCollectionId,
                    caseId,
                    caseData
                );
                
                update(state => ({
                    ...state,
                    cases: state.cases.map(c => c.$id === caseId ? { ...c, ...updatedCase } : c),
                    currentCase: state.currentCase && state.currentCase.$id === caseId ? 
                        { ...state.currentCase, ...updatedCase } : state.currentCase,
                    loading: false
                }));
                
                return updatedCase;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : '更新案例失败';
                update(state => ({ ...state, loading: false, error: errorMessage }));
                throw error;
            }
        },
        
        // 删除案例
        deleteCase: async (caseId: string) => {
            update(state => ({ ...state, loading: true, error: null }));
            try {
                await databases.deleteDocument(
                    databaseId,
                    casesCollectionId,
                    caseId
                );
                
                update(state => ({
                    ...state,
                    cases: state.cases.filter(c => c.$id !== caseId),
                    currentCase: state.currentCase && state.currentCase.$id === caseId ? 
                        null : state.currentCase,
                    loading: false
                }));
                
                return true;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : '删除案例失败';
                update(state => ({ ...state, loading: false, error: errorMessage }));
                throw error;
            }
        },
        
        // 设置当前案例
        setCurrentCase: (caseData: Case | null) => {
            update(state => ({ ...state, currentCase: caseData }));
        },
        
        // 清除错误
        clearError: () => {
            update(state => ({ ...state, error: null }));
        },
        
        // 重置状态
        reset: () => {
            set({
                cases: [],
                currentCase: null,
                loading: false,
                error: null
            });
        }
    };
};

// 导出单例实例
export const caseStore = createCaseStore();