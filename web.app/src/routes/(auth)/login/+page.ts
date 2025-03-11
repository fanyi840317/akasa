import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { base } from '$app/paths';
import { auth } from '$lib/stores/auth';
import { get } from 'svelte/store';

export const load: PageLoad = async ({ fetch, parent, url }) => {
  // 获取父级布局中的数据，包括用户信息
  const {user} = get(auth); 
  
  // 获取URL中的returnUrl参数
  const returnUrl = url.searchParams.get('returnUrl');
  
  console.log('returnUrl:', );
  // 如果用户已登录，重定向到returnUrl或首页
  if (user) {
    if (returnUrl) {
      throw redirect(302, `${base}${returnUrl}`);
    } else {
      throw redirect(302, `${base}/`);
    }
  }
  
  // 返回页面需要的数据，包括returnUrl
  return {
    title: '登录 - Akasa',
    returnUrl
  };
};