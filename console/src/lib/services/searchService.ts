// 搜索工具配置服务
import { toast } from 'svelte-sonner';

// 类型定义
export interface SearchEngine {
	name: string;
	display_name: string;
	enabled: boolean;
	requires_api_key: boolean;
	api_key_configured?: boolean;
}

export interface SearchEnginesResponse {
	success: boolean;
	data: {
		engines: SearchEngine[];
		current: string;
		max_results?: number;
	};
	error?: string;
	message?: string;
}

export interface ToolTestResult {
	success: boolean;
	tool_name: string;
	response_time_ms?: number;
	result?: any;
	error?: string;
	timestamp: string;
}

export interface ToolTestResponse {
	success: boolean;
	data: ToolTestResult;
	error?: string;
	message?: string;
}

export interface ToolConfigRequest {
	tool_name: string;
	config: {
		search_engine: string;
		max_results: number;
	};
}

export interface ToolConfigResponse {
	success: boolean;
	data?: any;
	error?: string;
	message?: string;
}

export interface SearchResult {
	title: string;
	url?: string;
	content?: string;
	index: number;
}

// API基础配置
const API_BASE = 'http://localhost:8000/api/tools';

// 错误处理辅助函数
const handleApiError = (error: unknown, context: string): never => {
	const message = error instanceof Error ? error.message : String(error);
	console.error(`${context}:`, error);
	throw new Error(message);
};

// HTTP请求辅助函数
const apiRequest = async <T>(url: string, options?: RequestInit): Promise<T> => {
	try {
		const response = await fetch(url, {
			headers: {
				'Content-Type': 'application/json',
				...options?.headers,
			},
			...options,
		});

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		const result = await response.json();
		if (!result.success) {
			throw new Error(result.error || 'API request failed');
		}

		return result;
	} catch (error) {
		handleApiError(error, `API request to ${url}`);
	}
};

// 搜索引擎服务类
export class SearchService {
	// 获取搜索引擎列表
	static async getSearchEngines(): Promise<SearchEnginesResponse> {
		return apiRequest<SearchEnginesResponse>(`${API_BASE}/search-engines`);
	}

	// 更新搜索引擎配置
	static async updateConfig(config: ToolConfigRequest): Promise<ToolConfigResponse> {
		return apiRequest<ToolConfigResponse>(`${API_BASE}/config`, {
			method: 'POST',
			body: JSON.stringify(config),
		});
	}

	// 测试搜索工具
	static async testSearch(toolName: string, query: string): Promise<ToolTestResponse> {
		return apiRequest<ToolTestResponse>(`${API_BASE}/test`, {
			method: 'POST',
			body: JSON.stringify({
				tool_name: toolName,
				test_query: query,
			}),
		});
	}

	// 获取工具状态
	static async getToolsStatus(): Promise<any> {
		return apiRequest<any>(`${API_BASE}/status`);
	}
}

// 搜索引擎映射工具函数
export const SearchEngineUtils = {
	// 将搜索引擎名称映射到工具名称
	getToolNameFromEngine(engine: string): string {
		const toolMap: Record<string, string> = {
			tavily: 'tavily_search',
			duckduckgo: 'duckduckgo_search',
			brave_search: 'brave_search',
			arxiv: 'arxiv_search',
		};
		return toolMap[engine] || 'duckduckgo_search';
	},

	// 获取搜索引擎的显示名称
	getEngineDisplayName(engine: string): string {
		const engineMap: Record<string, string> = {
			tavily: 'Tavily Search',
			duckduckgo: 'DuckDuckGo',
			brave_search: 'Brave Search',
			arxiv: 'ArXiv',
		};
		return engineMap[engine] || engine;
	},

	// 获取搜索引擎的描述
	getEngineDescription(engine: string): string {
		const descMap: Record<string, string> = {
			tavily: '专业的AI搜索引擎，提供高质量的搜索结果',
			duckduckgo: '注重隐私保护的搜索引擎',
			brave_search: '独立的搜索引擎，注重用户隐私',
			arxiv: '学术论文搜索引擎，专注于科学文献',
		};
		return descMap[engine] || '搜索引擎';
	},

	// 检查搜索引擎是否需要API密钥
	requiresApiKey(engine: string): boolean {
		return ['tavily', 'brave_search'].includes(engine);
	},

	// 验证搜索引擎名称
	isValidEngine(engine: string): boolean {
		return ['tavily', 'duckduckgo', 'brave_search', 'arxiv'].includes(engine);
	},
};

// 搜索结果处理工具
export const SearchResultUtils = {
	// 解析测试结果
	parseTestResult(testResult: ToolTestResult): {
		success: boolean;
		results?: any[];
		error?: string;
	} {
		if (testResult.success) {
			return {
				success: true,
				results: Array.isArray(testResult.result) ? testResult.result : [],
			};
		} else {
			return {
				success: false,
				error: testResult.error,
			};
		}
	},

	// 格式化搜索结果
	formatSearchResult(result: any, index: number): SearchResult {
		return {
			title: result.title || `结果 ${index + 1}`,
			url: result.url,
			content: result.content || result.description,
			index: index + 1,
		};
	},
};