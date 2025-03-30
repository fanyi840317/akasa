import { dev } from '$app/environment';
import { injectAnalytics } from '@vercel/analytics/sveltekit';
import { getLocationByIP } from '$lib/services/location';
import initI18n from '$lib/i18n';
import { auth } from '$lib/stores/auth';
import { get } from 'svelte/store';
import type { LayoutLoad } from './$types';
import { DEFAULT_LOCATION } from '$lib/types/location.types';

injectAnalytics({ mode: dev ? 'development' : 'production' });

// 初始化位置和语言设置
export const ssr = false;
export const load: LayoutLoad = async ({ url, route }) => {
    try {
        // 避免在每次导航时都重新初始化认证
        await auth.init();
        
        // 只使用 IP 获取位置数据，如果失败则使用默认值
        let locationData;
        try {
            locationData = await getLocationByIP();
        } catch (error) {
            console.error('获取位置数据失败:', error);
            locationData = DEFAULT_LOCATION;
        }

        // 初始化 i18n
        initI18n(locationData.country);

        // 获取 auth store 的当前状态
        const { user } = get(auth);

        return {
            location: locationData,
            user
        };
    } catch (error) {
        console.error('布局加载失败:', error);
        // 返回默认值，确保页面不会白屏
        return {
            location: DEFAULT_LOCATION,
            user: null
        };
    }
};
