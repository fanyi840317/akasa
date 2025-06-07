import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ parent, url }) => {
  const { user } = await parent();

  // 只有当用户已登录且当前路径是登录或注册页面时才重定向
  if (user && (url.pathname === '/login' || url.pathname === '/register')) {
      throw redirect(303, '/console');
  }
};