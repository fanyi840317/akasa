import { dev } from '$app/environment';
import { injectAnalytics } from '@vercel/analytics/sveltekit';
import { getLocationByIP } from '$lib/services/location';
import initI18n from '$lib/i18n';
import { auth } from '$lib/stores/auth';
import { get } from 'svelte/store';
import type { LayoutLoad } from './$types';
import { DEFAULT_LOCATION } from '$lib/types/map';

injectAnalytics({ mode: dev ? 'development' : 'production' });

// 初始化位置和语言设置
export const ssr = false;
// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const load: LayoutLoad = async ({ url, route }) => {
    try {
        // 避免在每次导航时都重新初始化认证
        await auth.init();

        // 获取 auth store 的当前状态
        const { user } = get(auth);

        // 优先使用浏览器语言设置
        const browserLang = navigator.language.split('-')[0];
        if (browserLang && ['en', 'zh'].includes(browserLang)) {
            initI18n(browserLang);
        } else {
            // 如果浏览器语言不支持，则使用IP定位
            getLocationByIP().then(locationData => {
                if (locationData) {
                    initI18n(locationData.country);
                }
            }).catch(error => {
                console.error('获取位置数据失败:', error);
                initI18n(DEFAULT_LOCATION.country);
            });
        }

        return {
            location: DEFAULT_LOCATION,
            user
        };
    } catch (error) {
        console.error('布局加载失败:', error);
        return {
            location: DEFAULT_LOCATION,
            user: null
        };
    }
};
