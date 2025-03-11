import type { PageLoad } from './$types';

export const load: PageLoad = async () => {
    return {
        snippets: {
            actions: true,
            rightView: true
        },
        title: "事件列表",
        showHeader: true
    };
}; 