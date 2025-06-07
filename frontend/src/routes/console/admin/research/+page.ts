import type { PageLoad } from './$types';

export const load: PageLoad = async ({ parent }) => {
  // 获取父级布局数据
  const parentData = await parent();
  
  // 返回页面特定的数据，包括要传递给TopBar的标题
  return {
    ...parentData,
    pageTitle: "Week MAY 7 - MAY 13",
    pageSubtitle: "Last Updated: May 12, 2025 12:06 pm"
  };
};