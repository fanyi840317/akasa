import { writable, get } from 'svelte/store';
import { databases } from '../appwrite';
import { ID, Query } from 'appwrite';
import type { Models } from 'appwrite';
import type { Event } from '../types/event';
import { toast } from "svelte-sonner";
import { _ } from "svelte-i18n";
import { auth } from "./auth";

// Event数据类型定义

type EventState = {
    events: Event[];
    currentEvent: Event | null;
    listLoading: boolean;
    eventLoading: boolean;
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
        listLoading: false,
        eventLoading: false,
        error: null
    });

    return {
        subscribe,
        // 获取所有事件
        fetchEvents: async (userId?: string) => {
            update(state => ({ ...state, listLoading: true, error: null }));
            try {
                let query = [];
                
                // 如果提供了用户ID，则按用户ID筛选
                if (userId) {
                    query.push(Query.equal('user_id', userId));
                }
                
                const response = await databases.listDocuments(
                    databaseId,
                    eventsCollectionId,
                    query
                );
                
                update(state => ({
                    ...state,
                    events: response.documents as unknown as Event[],
                    listLoading: false
                }));
                
                return response.documents;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : '获取事件失败';
                update(state => ({ ...state, listLoading: false, error: errorMessage }));
                toast.error(errorMessage);
                throw error;
            }
        },
        
        // 获取单个事件
        fetchEvent: async (eventId: string) => {
            update(state => ({ ...state, eventLoading: true, error: null }));
            try {
                const eventDoc = await databases.getDocument(
                    databaseId,
                    eventsCollectionId,
                    eventId
                );
                
                update(state => ({
                    ...state,
                    currentEvent: eventDoc as unknown as Event,
                    eventLoading: false
                }));
                
                return eventDoc;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : '获取事件详情失败';
                update(state => ({ ...state, eventLoading: false, error: errorMessage }));
                toast.error(errorMessage);
                throw error;
            }
        },
        
        // 创建新事件
        createEvent: async (eventData: Event) => {
            update(state => ({ ...state, eventLoading: true, error: null }));
            try {
                // 验证事件数据
                if (!eventData.title) {
                    toast.error(get(_)("validation.title_required"));
                    return null;
                }

                const user = get(auth).user;
                if (!user) {
                    toast.error(get(_)("validation.user_not_logged_in"));
                    return null;
                }

                if (!eventData.content) {
                    toast.error(get(_)("validation.content_required"));
                    return null;
                }

                const newEvent = await databases.createDocument(
                    databaseId,
                    eventsCollectionId,
                    ID.unique(),
                    {
                        ...eventData,
                        user_id: user.$id,
                        $createdAt: new Date().toISOString(),
                        $updatedAt: new Date().toISOString(),
                    }
                );
                
                update(state => ({
                    ...state,
                    events: [...state.events, newEvent as unknown as Event],
                    currentEvent: newEvent as unknown as Event,
                    eventLoading: false
                }));
                
                toast.success("事件已成功发布！");
                return newEvent;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : '创建事件失败';
                update(state => ({ ...state, eventLoading: false, error: errorMessage }));
                toast.error(errorMessage);
                throw error;
            }
        },
        
        // 更新事件
        updateEvent: async (eventId: string, eventData: Partial<Event>) => {
            update(state => ({ ...state, eventLoading: true, error: null }));
            try {
                const updatedEvent = await databases.updateDocument(
                    databaseId,
                    eventsCollectionId,
                    eventId,
                    {
                        ...eventData,
                        $updatedAt: new Date().toISOString(),
                    }
                );
                
                update(state => ({
                    ...state,
                    events: state.events.map(e => e.$id === eventId ? { ...e, ...updatedEvent } : e),
                    currentEvent: state.currentEvent && state.currentEvent.$id === eventId ? 
                        { ...state.currentEvent, ...updatedEvent } : state.currentEvent,
                    eventLoading: false
                }));
                
                toast.success("事件已成功更新！");
                return updatedEvent;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : '更新事件失败';
                update(state => ({ ...state, eventLoading: false, error: errorMessage }));
                toast.error(errorMessage);
                throw error;
            }
        },
        
        // 删除事件
        deleteEvent: async (eventId: string) => {
            update(state => ({ ...state, listLoading: true, error: null }));
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
                    listLoading: false
                }));
                
                toast.success("事件已成功删除！");
                return true;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : '删除事件失败';
                update(state => ({ ...state, listLoading: false, error: errorMessage }));
                toast.error(errorMessage);
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
                listLoading: false,
                eventLoading: false,
                error: null
            });
        }
    };
};

// 导出单例实例
export const eventStore = createEventStore();