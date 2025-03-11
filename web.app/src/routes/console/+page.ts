import type { PageLoad } from './$types';
import { redirect } from '@sveltejs/kit';
import { get } from 'svelte/store';
import { auth } from '$lib/stores/auth';
import { base } from '$app/paths';

export const load: PageLoad = async ({ url }) => {
    // 检查用户是否已登录
    const { user } = get(auth);
    
    // 如果用户未登录，重定向到登录页面，并携带当前路径作为参数
    if (!user) {
        const returnUrl = encodeURIComponent(url.pathname);
        throw redirect(302, `${base}/login?returnUrl=${returnUrl}`);
    }
    
    // 构建用户信息对象，用于传递给nav-user组件
    const userInfo = {
        name: user.name,
        email: user.email,
        avatar: user.prefs?.avatar || '/images/avatar-placeholder.png'
    };
    
    return {
        showHeader: false,
        title: '控制台',
        user: userInfo
    };
};