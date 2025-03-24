import { writable, get } from 'svelte/store';
import { createLocalStorageStore } from './localStorage';
import type { NavItem } from '../../routes/console/components/types';

type AppState = {
    // 导航相关状态
    selectedItem: string | null;
    selectedEventId: string | null;
    
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
        // 导航相关状态
        selectedItem: null,
        selectedEventId: null,
        
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
        
        // 导航相关方法
        setSelectedItem: (item: string | null) => {
            store.update(state => ({
                ...state,
                selectedItem: item,
                // 当设置主导航项时，清除事件选中状态
                selectedEventId: null
            }));
        },
        
        setSelectedEventId: (id: string | null) => {
            store.update(state => ({
                ...state,
                // 当设置事件选中状态时，清除主导航选中状态
                selectedItem: null,
                selectedEventId: id
            }));
        },
        
        clearSelection: () => {
            store.update(state => ({
                ...state,
                selectedItem: null,
                selectedEventId: null
            }));
        },
        
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

/**
 * 为了向后兼容，导出sidebarStore
 * 注意：新代码应该直接使用appStore而不是sidebarStore
 * 这个store将在未来版本中被移除
 * @deprecated 请使用appStore代替
 */
export const sidebarStore = {
    subscribe: (callback: (value: { selectedItem: string | null; selectedEventId: string | null }) => void) => {
        return appStore.subscribe(state => {
            callback({
                selectedItem: state.selectedItem,
                selectedEventId: state.selectedEventId
            });
        });
    },
    setSelectedItem: appStore.setSelectedItem,
    setSelectedEventId: appStore.setSelectedEventId,
    clearSelection: appStore.clearSelection,
    get: () => {
        const state = appStore.get();
        return {
            selectedItem: state.selectedItem,
            selectedEventId: state.selectedEventId
        };
    }
};