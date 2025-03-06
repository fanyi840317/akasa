import { dev } from '$app/environment';
import { injectAnalytics } from '@vercel/analytics/sveltekit';
import { getLocationData } from '$lib/services/location';
import { init } from 'svelte-i18n';
import { auth } from '$lib/stores/auth';
import { account } from '$lib/appwrite';
import { base } from '$app/paths';
import { goto } from '$app/navigation';
import { redirect } from '@sveltejs/kit';
import type { LayoutLoad } from './$types';

export const load: LayoutLoad = async ({ parent }) => {
    const parentData = await parent();
    
    if (!parentData.user) {
        throw redirect(302, `${base}/login`);
    }

    return {
        user: parentData.user
    };
};
