import type { PageLoad } from './$types';
import { locale, _ } from 'svelte-i18n';

export const load = (async () => {
    
    locale.set('zh');
    return {};
}) satisfies PageLoad;