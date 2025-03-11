import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { base } from '$app/paths';
import { auth } from '$lib/stores/auth';
import { get } from 'svelte/store';

export const load: PageLoad = async ({ fetch, parent, url }) => {
  // 获取父级布局中的数据，包括用户信息
  // 注意：(auth)/+layout.ts 已经处理了用户登录状态的重定向逻辑
  // 这里可以直接使用 parent() 获取父级布局的数据
  const parentData = await parent();
  
  
  // 返回页面需要的数据，包括returnUrl
  return {
    title: '注册 - Akasa'
  };
};