import type { PageLoad } from './$types';

export const load: PageLoad = async () => {
	return {
		title: 'API测试',
		description: '配置和测试搜索API接口'
	};
};