import type { PageLoad } from './$types';

export const load: PageLoad = async () => {
    return {
        showHeader: true,
        title: 'new event',
    };
};