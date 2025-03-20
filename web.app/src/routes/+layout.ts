import { dev } from '$app/environment';
import { injectAnalytics } from '@vercel/analytics/sveltekit';
import { getLocationData } from '$lib/services/location';
import initI18n from '$lib/i18n';
import { auth } from '$lib/stores/auth';
import { get } from 'svelte/store';
import type { LayoutLoad } from './$types';

injectAnalytics({ mode: dev ? 'development' : 'production' });

// 初始化位置和语言设置
export const ssr = false;
export const load: LayoutLoad = async ({ url, route }) => {
    // 避免在每次导航时都重新初始化认证
    await auth.init();
    
    const locationData = await getLocationData();

    // 初始化 i18n
    initI18n(locationData.country);

    // 获取 auth store 的当前状态
    const { user } = get(auth);

    return {
        location: locationData,
        user
    };
};
