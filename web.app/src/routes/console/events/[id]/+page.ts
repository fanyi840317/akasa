import type { PageLoad } from './$types';

export const load: PageLoad = async () => {
    return {
        showHeader: false,
        title: 'new event',
    };
};