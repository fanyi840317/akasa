import { writable, get } from 'svelte/store';
import type { NavItem } from '../types/types';
import type { Event } from '../types/event';

type AppState = {
    // 视图显示状态
    showLeftView: boolean;
    showRightView: boolean;
    showDialog: boolean;
    
    // 对话框相关状态
    dialogItem: NavItem | null;
    
    // 侧边栏配置
    sidebarCollapsed: boolean;
    sidebarWidth: number;
    sidebarWidthIcon: number;
    
    // 模板相关
    selectedTemplate: unknown | null;

    // 事件创建器状态
    showEventCreator: boolean;
    eventCreatorType: 'experience' | 'documentation' | 'witness' | 'evidence' | null;
    currentEvent: Event | null;

    // Header 浮动状态
    showHeader: boolean;
};

const createAppStore = () => {
    const store = writable<AppState>({
        // 视图显示状态
        showLeftView: false,
        showRightView: false,
        showDialog: false,
        
        // 对话框相关状态
        dialogItem: null,
        
        // 侧边栏配置
        sidebarCollapsed: true,
        sidebarWidth: 256,
        sidebarWidthIcon: 56,
        
        // 模板相关
        selectedTemplate: null,

        // 事件创建器状态
        showEventCreator: false,
        eventCreatorType: null,
        currentEvent: null,

        // Header 浮动状态
        showHeader: true
    });

    return {
        subscribe: store.subscribe,
        
        // 视图显示相关方法
        setShowLeftView: (show: boolean) => {
            store.update(state => ({
                ...state,
                showLeftView: show
            }));
        },
        
        toggleLeftView: () => {
            store.update(state => ({
                ...state,
                showLeftView: !state.showLeftView
            }));
        },
        
        setShowRightView: (show: boolean) => {
            store.update(state => ({
                ...state,
                showRightView: show
            }));
        },
        
        toggleRightView: () => {
            store.update(state => ({
                ...state,
                showRightView: !state.showRightView
            }));
        },
        
        // 对话框相关方法
        setShowDialog: (show: boolean, item: NavItem | null = null) => {
            store.update(state => ({
                ...state,
                showDialog: show,
                dialogItem: item
            }));
        },
        
        // 侧边栏配置方法
        setSidebarCollapsed: (collapsed: boolean) => {
            store.update(state => ({
                ...state,
                sidebarCollapsed: collapsed
            }));
        },
        
        // 模板相关方法
        setTemplate: (template: unknown | null) => {
            store.update(state => ({
                ...state,
                selectedTemplate: template,
                showRightView: template !== null
            }));
        },
        
        // 事件创建器相关方法
        openEventCreator: (type?: 'experience' | 'documentation' | 'witness' | 'evidence') => {
            store.update(state => ({
                ...state,
                showEventCreator: true,
                eventCreatorType: type || null
            }));
        },
        
        closeEventCreator: () => {
            store.update(state => ({
                ...state,
                showEventCreator: false,
                eventCreatorType: null
            }));
        },

        // Header 浮动相关方法
        setShowHeader: (show: boolean) => {
            store.update(state => ({
                ...state,
                showHeader:show
            }));
        },
        
        // 获取当前状态
        get: () => get(store)
    };
};

export const appStore = createAppStore();

