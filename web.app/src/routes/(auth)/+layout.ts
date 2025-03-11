import { redirect } from '@sveltejs/kit';
import type { LayoutLoad } from './$types';
import { base } from '$app/paths';
import { auth } from '$lib/stores/auth';
import { get } from 'svelte/store';

export const load: LayoutLoad = async ({ url }) => {
  // 先初始化auth store
  await auth.init();
  // 获取用户信息
  const { user } = get(auth);
  
  // 获取当前路径
  const path = url.pathname;
  const returnUrl = url.searchParams.get('returnUrl');
  
  // 如果用户已登录且正在访问登录或注册页面，重定向到returnUrl或首页
  // 精确匹配路径并检查重定向目标是否不同
  if (user && (path === `${base}/login` || path === `${base}/register`)) {
    const redirectPath = returnUrl ? `${base}${returnUrl}` : `${base}/`;
    if (redirectPath !== path) {
        console.log(redirectPath);
      throw redirect(302, redirectPath);
    }
  }
  
  // 返回页面需要的数据
  return {
    user
  };
};