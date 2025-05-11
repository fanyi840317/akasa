import { init, register } from 'svelte-i18n';

// 注册语言包
register('en', () => import('./locales/en.json'));
register('zh', () => import('./locales/zh.json'));
// register('ja', () => import('./locales/ja.json'));

// 初始化 i18n
const initI18n = (country?: string) => {
    init({
        fallbackLocale: 'en',
        initialLocale: country === 'CN' ? 'zh' : 'en',
    });
};

export default initI18n; 