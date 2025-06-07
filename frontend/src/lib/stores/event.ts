import { writable, get } from 'svelte/store';
import { databases } from '../../../../web.app/src/lib/appwrite';
import { ID, Query } from 'appwrite';
import type { Event } from '../types/event';
import { toast } from "svelte-sonner";
import { _ } from "svelte-i18n";
import { auth } from "./auth";
import { parseI18nFields } from '$lib/utils';

// Event数据类型定义

type EventState = {
    events: Event[];
    currentEvent: Event | null;
    listLoading: boolean;
    eventLoading: boolean;
    error: string | null;
};

// 从appwrite.ts中获取配置
import { appwriteConfig } from '../../../../web.app/src/lib/appwrite';
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
                const query = [];
                
                // 如果提供了用户ID，则按用户ID筛选
                if (userId) {
                    query.push(Query.equal('user_id', userId));
                }
                
                const response = await databases.listDocuments(
                    databaseId,
                    eventsCollectionId,
                    query
                );
                
                // 使用工具方法解析 i18n 字段
                const events = response.documents.map(doc => parseI18nFields(doc as unknown as Event));

                update(state => ({
                    ...state,
                    events: events,
                    listLoading: false
                }));
                
                return events;
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
                
                // 使用工具方法解析 i18n 字段
                const event = parseI18nFields(eventDoc as unknown as Event);
                update(state => ({
                    ...state,
                    currentEvent: event,
                    eventLoading: false
                }));
                
                return event;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : '获取事件详情失败';
                update(state => ({ ...state, eventLoading: false, error: errorMessage }));
                toast.error(errorMessage);
                throw error;
            }
        },
        
        // 创建新事件
        createEvent: async (event: Omit<Event, '$id' | '$createdAt' | '$updatedAt'>) => {
            update(state => ({ ...state, eventLoading: true, error: null }));
            try {
                // 验证事件数据
                if (!event.title) {
                    toast.error(get(_)("validation.title_required"));
                    return null;
                }

                const user = get(auth).user;
                if (!user) {
                    toast.error(get(_)("validation.user_not_logged_in"));
                    return null;
                }

                if (!event.content) {
                    toast.error(get(_)("validation.content_required"));
                    return null;
                }

                const newEvent = await databases.createDocument(
                    databaseId,
                    eventsCollectionId,
                    ID.unique(),
                    {
                        ...event,
                        user_id: user.$id,
                        location_data: JSON.stringify(event.location_data || null),
                        $createdAt: new Date().toISOString(),
                        $updatedAt: new Date().toISOString(),
                    }
                );
                
                // 使用工具方法解析 i18n 字段
                const parsedEvent = parseI18nFields(newEvent as unknown as Event);

                update(state => ({
                    ...state,
                    events: [...state.events, parsedEvent],
                    currentEvent: parsedEvent,
                    eventLoading: false
                }));
                
                toast.success("事件已成功发布！");
                return parsedEvent;
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
                // 验证事件数据
                if (!eventData.title?.trim()) {
                    toast.error(get(_)("validation.title_required"));
                    return null;
                }

                if (!eventData.content?.trim()) {
                    toast.error(get(_)("validation.content_required"));
                    return null;
                }

                const user = get(auth).user;
                if (!user) {
                    toast.error(get(_)("validation.user_not_logged_in"));
                    return null;
                }
                console.log("eventData:  ",eventData);
                const updatedEvent = await databases.updateDocument(
                    databaseId,
                    eventsCollectionId,
                    eventId,
                    {
                        ...eventData,
                        $updatedAt: new Date().toISOString(),
                    }
                );
                
                // 使用工具方法解析 i18n 字段
                const parsedUpdatedEvent = parseI18nFields(updatedEvent as unknown as Event);

                update(state => ({
                    ...state,
                    events: state.events.map(e => e.$id === eventId ? parsedUpdatedEvent : e),
                    currentEvent: state.currentEvent && state.currentEvent.$id === eventId ? 
                        parsedUpdatedEvent : state.currentEvent,
                    eventLoading: false
                }));
                
                toast.success("事件已成功更新！");
                return parsedUpdatedEvent;
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
        
        // 删除多个事件
        deleteEvents: async (eventIds: string[]) => {
            update(state => ({ ...state, listLoading: true, error: null }));
            try {
                const deletedIds: string[] = [];
                for (const eventId of eventIds) {
                    try {
                        await databases.deleteDocument(
                            databaseId,
                            eventsCollectionId,
                            eventId
                        );
                        deletedIds.push(eventId);
                    } catch (error) {
                        console.error(`Failed to delete event ${eventId}:`, error);
                        // Optionally handle individual deletion errors, but continue with others
                    }
                }

                update(state => ({
                    ...state,
                    events: state.events.filter(e => !deletedIds.includes(e.$id as string)),
                    currentEvent: state.currentEvent && deletedIds.includes(state.currentEvent.$id as string) ?
                        null : state.currentEvent,
                    listLoading: false
                }));

                if (deletedIds.length > 0) {
                    toast.success(`${deletedIds.length} 个事件已成功删除！`);
                } else {
                    toast.info("没有事件被删除。");
                }

                return deletedIds;
            } catch (error) {
                // This catch block would only be reached if databases.deleteDocument throws synchronously,
                // which is unlikely for async operations. Individual errors are handled inside the loop.
                const errorMessage = error instanceof Error ? error.message : '批量删除事件失败';
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
        },
    };
};

// 导出单例实例
export const eventStore = createEventStore();