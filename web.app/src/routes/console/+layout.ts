import { auth } from '$lib/stores/auth';
import { redirect } from '@sveltejs/kit';
import type { LayoutLoad } from './$types';
import { base } from '$app/paths';
import { get } from 'svelte/store';

export const load = (async ({ url, route }) => {

    const { user } = get(auth);

    console.log(user);
    
    // 如果用户未登录，重定向到登录页面
    if (!user) {
        // const returnUrl = encodeURIComponent(url.pathname);
        // throw redirect(302, `${base}/login?redirect=${returnUrl}`);
    }
    
    // 构建用户信息对象，用于传递给nav-user组件
    const userInfo = user ? {
        name: user.name,
        email: user.email,
        avatar: user.prefs?.avatar || '/images/avatar-placeholder.png'
    } : {
        name: '游客',
        email: '',
        avatar: '/images/avatar-placeholder.png'
    };
    
    return {
        showHeader: false,
        title: '控制台',
        user: userInfo
    };
    
}) satisfies LayoutLoad;