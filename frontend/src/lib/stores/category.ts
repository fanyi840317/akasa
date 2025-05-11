import { writable } from 'svelte/store';
import { databases } from '$lib/appwrite';
import { Query } from 'appwrite';
import type { Category } from '$lib/types/category';
import { parseI18nFields } from '$lib/utils';

const DATABASE_ID = '67d3a4480018e2e09b68';
const COLLECTION_ID = 'categories';

function createCategoryStore() {
    const { subscribe, set, update } = writable<Category[]>([]);
    const loading = writable(false);
    const error = writable<string | null>(null);

    return {
        subscribe,
        loading,
        error,
        fetchCategories: async () => {
            try {
                loading.set(true);
                error.set(null);
                
                const response = await databases.listDocuments(
                    DATABASE_ID,
                    COLLECTION_ID,
                    [
                        Query.orderAsc('order'),
                        Query.equal('status', 'active')
                    ]
                );

                // 使用工具方法解析 i18n 字段
                const categories = response.documents.map(doc => parseI18nFields(doc as unknown as Category));

                set(categories);
                return categories;
            } catch (err) {
                error.set(err instanceof Error ? err.message : '获取分类失败');
                console.error('Failed to fetch categories:', err);
                return [];
            } finally {
                loading.set(false);
            }
        },
        getCategoryById: async (id: string) => {
            try {
                loading.set(true);
                error.set(null);
                
                const response = await databases.getDocument(
                    DATABASE_ID,
                    COLLECTION_ID,
                    id
                );

                // 使用工具方法解析 i18n 字段
                const category = parseI18nFields(response as unknown as Category);

                return category;
            } catch (err) {
                error.set(err instanceof Error ? err.message : '获取分类详情失败');
                console.error('Failed to fetch category:', err);
                return null;
            } finally {
                loading.set(false);
            }
        }
    };
}

export const categoryStore = createCategoryStore(); 