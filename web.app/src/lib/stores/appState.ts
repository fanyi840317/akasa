import { writable, get } from 'svelte/store';
import type { NavItem } from '../types/types';

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
    selectedTemplate: any | null;
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
        setTemplate: (template: any | null) => {
            store.update(state => ({
                ...state,
                selectedTemplate: template,
                showRightView: template !== null
            }));
        },
        
        // 获取当前状态
        get: () => get(store)
    };
};

export const appStore = createAppStore();

