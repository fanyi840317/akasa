import { writable, get } from 'svelte/store';
import { databases } from '../appwrite';
import { ID } from 'appwrite';
import type { Models } from 'appwrite';

// Event数据类型定义
type Event = {
    $id?: string;
    title: string;
    location?: string;
    date?: string;
    status?: string;
    content?: string;
    user_id: string;
    creator_name?: string;
    creator_avatar?: string;
};

type EventState = {
    events: Event[];
    currentEvent: Event | null;
    loading: boolean;
    error: string | null;
};

// 从appwrite.ts中获取配置
import { appwriteConfig } from '../appwrite';
const { databaseId } = appwriteConfig;

// 定义events集合ID
const eventsCollectionId = 'events';

const createEventStore = () => {
    const { subscribe, set, update } = writable<EventState>({
        events: [],
        currentEvent: null,
        loading: false,
        error: null
    });

    return {
        subscribe,
        // 获取所有事件
        fetchEvents: async (userId?: string) => {
            update(state => ({ ...state, loading: true, error: null }));
            try {
                let query = [];
                
                // 如果提供了用户ID，则按用户ID筛选
                if (userId) {
                    query.push(`user_id=${userId}`);
                }
                
                const response = await databases.listDocuments(
                    databaseId,
                    eventsCollectionId,
                    query
                );
                
                update(state => ({
                    ...state,
                    events: response.documents as unknown as Event[],
                    loading: false
                }));
                
                return response.documents;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : '获取事件失败';
                update(state => ({ ...state, loading: false, error: errorMessage }));
                throw error;
            }
        },
        
        // 获取单个事件
        fetchEvent: async (eventId: string) => {
            update(state => ({ ...state, loading: true, error: null }));
            try {
                const eventDoc = await databases.getDocument(
                    databaseId,
                    eventsCollectionId,
                    eventId
                );
                
                update(state => ({
                    ...state,
                    currentEvent: eventDoc as unknown as Event,
                    loading: false
                }));
                
                return eventDoc;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : '获取事件详情失败';
                update(state => ({ ...state, loading: false, error: errorMessage }));
                throw error;
            }
        },
        
        // 创建新事件
        createEvent: async (eventData: Omit<Event, '$id'>) => {
            update(state => ({ ...state, loading: true, error: null }));
            try {
                const newEvent = await databases.createDocument(
                    databaseId,
                    eventsCollectionId,
                    ID.unique(),
                    eventData
                );
                
                update(state => ({
                    ...state,
                    events: [...state.events, newEvent as unknown as Event],
                    currentEvent: newEvent as unknown as Event,
                    loading: false
                }));
                
                return newEvent;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : '创建事件失败';
                update(state => ({ ...state, loading: false, error: errorMessage }));
                throw error;
            }
        },
        
        // 更新事件
        updateEvent: async (eventId: string, eventData: Partial<Event>) => {
            update(state => ({ ...state, loading: true, error: null }));
            try {
                const updatedEvent = await databases.updateDocument(
                    databaseId,
                    eventsCollectionId,
                    eventId,
                    eventData
                );
                
                update(state => ({
                    ...state,
                    events: state.events.map(e => e.$id === eventId ? { ...e, ...updatedEvent } : e),
                    currentEvent: state.currentEvent && state.currentEvent.$id === eventId ? 
                        { ...state.currentEvent, ...updatedEvent } : state.currentEvent,
                    loading: false
                }));
                
                return updatedEvent;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : '更新事件失败';
                update(state => ({ ...state, loading: false, error: errorMessage }));
                throw error;
            }
        },
        
        // 删除事件
        deleteEvent: async (eventId: string) => {
            update(state => ({ ...state, loading: true, error: null }));
            try {
                await databases.deleteDocument(
                    databaseId,
                    eventsCollectionId,
                    eventId
                );
                
                update(state => ({
                    ...state,
                    events: state.events.filter(e => e.$id !== eventId),
                    currentEvent: state.currentEvent && state.currentEvent.$id === eventId ? 
                        null : state.currentEvent,
                    loading: false
                }));
                
                return true;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : '删除事件失败';
                update(state => ({ ...state, loading: false, error: errorMessage }));
                throw error;
            }
        },
        
        // 设置当前事件
        setCurrentEvent: (eventData: Event | null) => {
            update(state => ({ ...state, currentEvent: eventData }));
        },
        
        // 清除错误
        clearError: () => {
            update(state => ({ ...state, error: null }));
        },
        
        // 重置状态
        reset: () => {
            set({
                events: [],
                currentEvent: null,
                loading: false,
                error: null
            });
        }
    };
};

// 导出单例实例
export const eventStore = createEventStore();