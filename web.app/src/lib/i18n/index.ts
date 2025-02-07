import { init, register } from 'svelte-i18n';

register('en', () => import('./locales/en.json'));
register('zh', () => import('./locales/zh.json'));
// register('ja', () => import('./locales/ja.json'));

init({
    fallbackLocale: 'en',
    initialLocale: 'en',
}); 