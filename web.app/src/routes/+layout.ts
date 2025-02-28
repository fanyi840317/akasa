import { dev } from '$app/environment';
import { injectAnalytics } from '@vercel/analytics/sveltekit';
import { getLocationData } from '$lib/services/location';
import { init } from 'svelte-i18n';
import { auth } from '$lib/stores/auth';
import { account } from '$lib/appwrite';
 
injectAnalytics({ mode: dev ? 'development' : 'production' });

// 初始化位置和语言设置
export const load = async ({ url }) => {
    await auth.init();
    const locationData = await getLocationData();
    init({
        fallbackLocale: 'en',
        initialLocale: locationData.country === 'CN' ? 'zh' : 'en',
    });
    return {
        location: locationData,
    };
};
