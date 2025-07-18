<script lang="ts">
	import PageHeader from '$lib/components/ui/page-header.svelte';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Badge } from '$lib/components/ui/badge';
	import { Search, ExternalLink, BookOpen, FileText, Globe } from '@lucide/svelte';
	import { onMount } from 'svelte';

	// 研究状态
	let searchQuery = $state('');
	let isSearching = $state(false);
	let searchResults = $state<Array<{
		id: string;
		title: string;
		description: string;
		url: string;
		source: string;
		type: 'article' | 'paper' | 'website' | 'documentation' | 'mystery_event';
		tags: string[];
		publishedAt?: string;
		location?: string;
		severity?: 'low' | 'medium' | 'high' | 'critical';
	}>>([]);

	// 神秘事件相关状态
	let mysteryEvents = $state<Array<{
		id: string;
		title: string;
		description: string;
		location: string;
		timestamp: number;
		severity: 'low' | 'medium' | 'high' | 'critical';
		source: string;
		tags: string[];
		verified: boolean;
	}>>([]);
	let loadingMysteryEvents = $state(false);

	// 搜索历史
	let searchHistory = $state<Array<{
		id: string;
		query: string;
		timestamp: number;
		resultsCount: number;
	}>>([]);

	// 收藏的研究资源
	let savedResources = $state<Array<{
		id: string;
		title: string;
		url: string;
		description: string;
		type: string;
		savedAt: number;
	}>>([]);

	// API配置 - 从环境变量读取
	const API_CONFIG = {
		news: {
			baseUrl: 'https://newsapi.org/v2',
			apiKey: import.meta.env.VITE_NEWS_API_KEY
		},
		arxiv: {
			baseUrl: 'http://export.arxiv.org/api/query'
		},
		github: {
			baseUrl: 'https://api.github.com/search',
			apiKey: import.meta.env.VITE_GITHUB_TOKEN
		},
		wikipedia: {
			baseUrl: 'https://en.wikipedia.org/api/rest_v1'
		}
	};

	// API状态跟踪
	let apiStatus = $state({
		news: 'unknown',
		github: 'unknown',
		wikipedia: 'unknown',
		arxiv: 'unknown'
	});

	// 真实API搜索接口
	const searchAPIs = {
		mystery: async (query: string) => {
			// 使用Wikipedia API搜索神秘现象相关内容
			try {
				const searchResponse = await fetch(
					`${API_CONFIG.wikipedia.baseUrl}/page/search?q=${encodeURIComponent(query + ' mystery phenomenon UFO')}&limit=10`
				);
				
				if (!searchResponse.ok) {
					apiStatus.wikipedia = 'error';
					throw new Error('Wikipedia搜索请求失败');
				}
				
				const searchData = await searchResponse.json();
				
				const results = [];
				for (const page of searchData.pages?.slice(0, 5) || []) {
					try {
						const summaryResponse = await fetch(
							`${API_CONFIG.wikipedia.baseUrl}/page/summary/${encodeURIComponent(page.title)}`
						);
						const summaryData = await summaryResponse.json();
						
						results.push({
							id: `mystery-${page.id}`,
							title: summaryData.title,
							description: summaryData.extract || '暂无描述',
							url: summaryData.content_urls?.desktop?.page || '#',
							source: 'Wikipedia',
							type: 'mystery_event' as const,
							tags: ['神秘现象', 'Wikipedia'],
							publishedAt: new Date().toISOString(),
							location: '全球',
							severity: 'medium' as const
						});
					} catch (error) {
						console.error('获取页面摘要失败:', error);
					}
				}
				apiStatus.wikipedia = 'success';
				return results;
			} catch (error) {
				apiStatus.wikipedia = 'error';
				console.error('Wikipedia API调用失败:', error);
				return [];
			}
		},
		news: async (query: string) => {
			// 使用News API搜索新闻
			try {
				const apiKey = API_CONFIG.news.apiKey;
				if (!apiKey) {
					apiStatus.news = 'missing_key';
					console.warn('News API密钥未配置，跳过新闻搜索');
					return [
						{
							id: 'news-config',
							title: '配置News API以获取实时新闻',
							description: '请在.env.local文件中配置VITE_NEWS_API_KEY以获取真实新闻数据。访问 https://newsapi.org 获取免费API密钥。',
							url: 'https://newsapi.org',
							source: 'Configuration Required',
							type: 'article' as const,
							tags: ['配置', 'API'],
							publishedAt: new Date().toISOString()
						}
					];
				}
				
				const response = await fetch(
					`${API_CONFIG.news.baseUrl}/everything?q=${encodeURIComponent(query)}&sortBy=publishedAt&pageSize=10&apiKey=${apiKey}`
				);
				const data = await response.json();
				
				if (!response.ok) {
					apiStatus.news = 'error';
					throw new Error(data.message || 'News API请求失败');
				}
				
				apiStatus.news = 'success';
				return data.articles?.map((article: any, index: number) => ({
					id: `news-${index}`,
					title: article.title,
					description: article.description || '暂无描述',
					url: article.url,
					source: article.source?.name || 'Unknown',
					type: 'article' as const,
					tags: ['新闻', '实时'],
					publishedAt: article.publishedAt
				})) || [];
			} catch (error) {
				apiStatus.news = 'error';
				console.error('News API调用失败:', error);
				return [];
			}
		},
		academic: async (query: string) => {
			// 使用arXiv API搜索学术论文
			try {
				const response = await fetch(
					`${API_CONFIG.arxiv.baseUrl}?search_query=all:${encodeURIComponent(query)}&start=0&max_results=10&sortBy=submittedDate&sortOrder=descending`
				);
				
				if (!response.ok) {
					apiStatus.arxiv = 'error';
					throw new Error('arXiv API请求失败');
				}
				
				const xmlText = await response.text();
				
				// 解析XML响应
				const parser = new DOMParser();
				const xmlDoc = parser.parseFromString(xmlText, 'text/xml');
				const entries = xmlDoc.querySelectorAll('entry');
				
				const results = [];
				for (let i = 0; i < entries.length; i++) {
					const entry = entries[i];
					const title = entry.querySelector('title')?.textContent?.trim() || '';
					const summary = entry.querySelector('summary')?.textContent?.trim() || '';
					const id = entry.querySelector('id')?.textContent?.trim() || '';
					const published = entry.querySelector('published')?.textContent?.trim() || '';
					const authors = Array.from(entry.querySelectorAll('author name')).map(author => author.textContent).join(', ');
					
					results.push({
						id: `arxiv-${i}`,
						title: title,
						description: summary.length > 200 ? summary.substring(0, 200) + '...' : summary,
						url: id,
						source: `arXiv - ${authors}`,
						type: 'paper' as const,
						tags: ['学术论文', 'arXiv'],
						publishedAt: published
					});
				}
				apiStatus.arxiv = 'success';
				return results;
			} catch (error) {
				apiStatus.arxiv = 'error';
				console.error('arXiv API调用失败:', error);
				return [];
			}
		},
		github: async (query: string) => {
			// 使用GitHub API搜索代码和仓库
			try {
				const headers: Record<string, string> = {
					'Accept': 'application/vnd.github.v3+json'
				};
				
				if (API_CONFIG.github.apiKey) {
					headers['Authorization'] = `token ${API_CONFIG.github.apiKey}`;
				}
				
				const response = await fetch(
					`${API_CONFIG.github.baseUrl}/repositories?q=${encodeURIComponent(query)}&sort=updated&per_page=10`,
					{ headers }
				);
				const data = await response.json();
				
				if (!response.ok) {
					if (response.status === 403) {
						apiStatus.github = 'rate_limited';
						console.warn('GitHub API速率限制，建议配置访问令牌');
					} else {
						apiStatus.github = 'error';
					}
					throw new Error(data.message || 'GitHub API请求失败');
				}
				
				apiStatus.github = 'success';
				return data.items?.map((repo: any, index: number) => ({
					id: `github-${repo.id}`,
					title: repo.full_name,
					description: repo.description || '暂无描述',
					url: repo.html_url,
					source: `GitHub - ${repo.owner.login}`,
					type: 'documentation' as const,
					tags: ['GitHub', '开源', ...(repo.topics || [])],
					publishedAt: repo.updated_at
				})) || [];
			} catch (error) {
				if (apiStatus.github !== 'rate_limited') {
					apiStatus.github = 'error';
				}
				console.error('GitHub API调用失败:', error);
				return [];
			}
		}
	};

	// 加载最近一周神秘事件
	const loadRecentMysteryEvents = async () => {
		loadingMysteryEvents = true;
		try {
			// 使用Wikipedia API搜索神秘现象
			const mysteryResults = await searchAPIs.mystery('UFO mystery phenomenon');
			
			// 转换为统一格式
			const recentEvents = mysteryResults.map(event => ({
				id: event.id,
				title: event.title,
				description: event.description,
				location: event.location || '全球',
				timestamp: new Date(event.publishedAt!).getTime(),
				severity: event.severity || 'medium',
				source: event.source,
				tags: event.tags,
				verified: true // Wikipedia内容默认为已验证
			}));
			
			mysteryEvents = recentEvents;
			searchResults = mysteryResults;
			
			// 设置默认搜索查询
			searchQuery = 'UFO mystery phenomenon';
			
			// 添加到搜索历史
			const historyItem = {
				id: Date.now().toString(),
				query: 'UFO mystery phenomenon',
				timestamp: Date.now(),
				resultsCount: mysteryResults.length
			};
			searchHistory = [historyItem, ...searchHistory.slice(0, 9)];
			
		} catch (error) {
			console.error('加载神秘事件失败:', error);
		} finally {
			loadingMysteryEvents = false;
		}
	};

	// 通用搜索功能
	const handleSearch = async () => {
		if (!searchQuery.trim()) return;
		
		isSearching = true;
		
		try {
			// 并行调用多个搜索接口
			const [mysteryResults, newsResults, academicResults, githubResults] = await Promise.all([
				searchAPIs.mystery(searchQuery),
				searchAPIs.news(searchQuery),
				searchAPIs.academic(searchQuery),
				searchAPIs.github(searchQuery)
			]);
			
			// 合并搜索结果
			const allResults = [...mysteryResults, ...newsResults, ...academicResults, ...githubResults];
			searchResults = allResults;
			
			// 添加到搜索历史
			const historyItem = {
				id: Date.now().toString(),
				query: searchQuery,
				timestamp: Date.now(),
				resultsCount: allResults.length
			};
			searchHistory = [historyItem, ...searchHistory.slice(0, 9)];
			
		} catch (error) {
			console.error('搜索失败:', error);
		} finally {
			isSearching = false;
		}
	};

	// 保存资源
	const saveResource = (result: typeof searchResults[0]) => {
		const savedItem = {
			id: result.id,
			title: result.title,
			url: result.url,
			description: result.description,
			type: result.type,
			savedAt: Date.now()
		};
		
		if (!savedResources.find(item => item.id === result.id)) {
			savedResources = [savedItem, ...savedResources];
		}
	};

	// 移除保存的资源
	const removeSavedResource = (id: string) => {
		savedResources = savedResources.filter(item => item.id !== id);
	};

	// 获取类型图标
	const getTypeIcon = (type: string) => {
		switch (type) {
			case 'paper': return FileText;
			case 'documentation': return BookOpen;
			case 'article': return FileText;
			case 'website': return Globe;
			case 'mystery_event': return Search;
			default: return FileText;
		}
	};

	// 获取严重程度颜色
	const getSeverityColor = (severity: string) => {
		switch (severity) {
			case 'low': return 'bg-green-100 text-green-800';
			case 'medium': return 'bg-yellow-100 text-yellow-800';
			case 'high': return 'bg-orange-100 text-orange-800';
			case 'critical': return 'bg-red-100 text-red-800';
			default: return 'bg-gray-100 text-gray-800';
		}
	};

	// 格式化日期
	const formatDate = (timestamp: number | string) => {
		const date = typeof timestamp === 'string' ? new Date(timestamp) : new Date(timestamp);
		return date.toLocaleDateString('zh-CN');
	};

	// 处理搜索历史点击
	const handleHistoryClick = (query: string) => {
		searchQuery = query;
		handleSearch();
	};

	onMount(async () => {
		// 加载保存的搜索历史和收藏资源
		const savedHistory = localStorage.getItem('research-history');
		if (savedHistory) {
			searchHistory = JSON.parse(savedHistory);
		}
		
		const savedResourcesData = localStorage.getItem('research-saved');
		if (savedResourcesData) {
			savedResources = JSON.parse(savedResourcesData);
		}
		
		// 自动加载最近一周的神秘事件
		await loadRecentMysteryEvents();
	});

	// 保存到本地存储
	$effect(() => {
		localStorage.setItem('research-history', JSON.stringify(searchHistory));
	});

	$effect(() => {
		localStorage.setItem('research-saved', JSON.stringify(savedResources));
	});
</script>
<div class="h-content bg-base-200 flex flex-col rounded-2xl border overflow-hidden">
<PageHeader title="Research" description="Search and explore research resources, documentation, and knowledge base.">
	{#snippet rightContent()}
		<div class="flex items-center gap-4">
			<!-- API状态指示器 -->
			<div class="flex items-center gap-2">
				<div class="flex items-center gap-1">
					<div class="w-2 h-2 rounded-full {apiStatus.wikipedia === 'success' ? 'bg-green-500' : apiStatus.wikipedia === 'error' ? 'bg-red-500' : 'bg-gray-400'}"></div>
					<span class="text-xs text-muted-foreground">Wiki</span>
				</div>
				<div class="flex items-center gap-1">
					<div class="w-2 h-2 rounded-full {apiStatus.arxiv === 'success' ? 'bg-green-500' : apiStatus.arxiv === 'error' ? 'bg-red-500' : 'bg-gray-400'}"></div>
					<span class="text-xs text-muted-foreground">arXiv</span>
				</div>
				<div class="flex items-center gap-1">
					<div class="w-2 h-2 rounded-full {apiStatus.news === 'success' ? 'bg-green-500' : apiStatus.news === 'missing_key' ? 'bg-yellow-500' : apiStatus.news === 'error' ? 'bg-red-500' : 'bg-gray-400'}"></div>
					<span class="text-xs text-muted-foreground">News</span>
				</div>
				<div class="flex items-center gap-1">
					<div class="w-2 h-2 rounded-full {apiStatus.github === 'success' ? 'bg-green-500' : apiStatus.github === 'rate_limited' ? 'bg-yellow-500' : apiStatus.github === 'error' ? 'bg-red-500' : 'bg-gray-400'}"></div>
					<span class="text-xs text-muted-foreground">GitHub</span>
				</div>
			</div>
			
			<div class="flex items-center gap-2 text-sm text-muted-foreground">
				{#if loadingMysteryEvents}
					<span>Loading mystery events...</span>
				{:else}
					<span>{searchResults.length} results</span>
					{#if mysteryEvents.length > 0}
						<span>•</span>
						<span>{mysteryEvents.length} mystery events</span>
					{/if}
					{#if savedResources.length > 0}
						<span>•</span>
						<span>{savedResources.length} saved</span>
					{/if}
				{/if}
			</div>
		</div>
	{/snippet}
</PageHeader>
<ScrollArea class="p-4">
<div class="flex h-[calc(100vh-8rem)] gap-6">
	<!-- 主要搜索区域 -->
	<div class="flex-1 flex flex-col">
		<!-- 搜索栏 -->
		<div class="mb-6">
			<div class="flex gap-2">
				<div class="relative flex-1">
					<Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
					<Input
						bind:value={searchQuery}
						placeholder="Search for research papers, documentation, articles..."
						class="pl-10"
						onkeydown={(e: KeyboardEvent) => {
							if (e.key === 'Enter') {
								handleSearch();
							}
						}}
					/>
				</div>
				<Button onclick={handleSearch} disabled={isSearching || !searchQuery.trim()}>
					{#if isSearching}
						Searching...
					{:else}
						Search
					{/if}
				</Button>
				<Button variant="outline" onclick={loadRecentMysteryEvents} disabled={loadingMysteryEvents}>
					{#if loadingMysteryEvents}
						Loading...
					{:else}
						Refresh Events
					{/if}
				</Button>
			</div>
		</div>

		<!-- 搜索结果 -->
		<ScrollArea class="flex-1">
			{#if searchResults.length > 0}
				<div class="space-y-4">
					{#each searchResults as result (result.id)}
						<Card class="hover:shadow-md transition-shadow {result.type === 'mystery_event' ? 'border-l-4 border-l-orange-500' : ''}">
							<CardHeader class="pb-3">
								<div class="flex items-start justify-between">
									<div class="flex-1">
										<div class="flex items-center gap-2 mb-2">
											<svelte:component this={getTypeIcon(result.type)} class="h-4 w-4 text-muted-foreground" />
											<Badge variant="secondary">{result.type === 'mystery_event' ? '神秘事件' : result.type}</Badge>
											{#if result.severity}
												<Badge class={getSeverityColor(result.severity)}>
													{result.severity === 'low' ? '低' : result.severity === 'medium' ? '中' : result.severity === 'high' ? '高' : '严重'}
												</Badge>
											{/if}
											<span class="text-sm text-muted-foreground">{result.source}</span>
											{#if result.location}
												<span class="text-sm text-muted-foreground">• 📍 {result.location}</span>
											{/if}
											{#if result.publishedAt}
												<span class="text-sm text-muted-foreground">• {formatDate(result.publishedAt)}</span>
											{/if}
										</div>
										<CardTitle class="text-lg">
											{#if result.url === '#'}
												{result.title}
											{:else}
												<a href={result.url} target="_blank" rel="noopener noreferrer" class="hover:underline flex items-center gap-1">
													{result.title}
													<ExternalLink class="h-4 w-4" />
												</a>
											{/if}
										</CardTitle>
									</div>
									<Button variant="outline" size="sm" onclick={() => saveResource(result)}>
										Save
									</Button>
								</div>
							</CardHeader>
							<CardContent>
								<CardDescription class="mb-3">{result.description}</CardDescription>
								<div class="flex flex-wrap gap-1">
									{#each result.tags as tag}
										<Badge variant="outline" class="text-xs">{tag}</Badge>
									{/each}
								</div>
							</CardContent>
						</Card>
					{/each}
				</div>
			{:else if searchQuery && !isSearching}
				<div class="flex flex-col items-center justify-center h-64 text-center">
					<Search class="h-12 w-12 text-muted-foreground mb-4" />
					<h3 class="text-lg font-medium mb-2">No results found</h3>
					<p class="text-muted-foreground">Try adjusting your search terms or explore different keywords.</p>
				</div>
			{:else if loadingMysteryEvents}
				<div class="flex flex-col items-center justify-center h-64 text-center">
					<Search class="h-12 w-12 text-muted-foreground mb-4 animate-spin" />
					<h3 class="text-lg font-medium mb-2">Loading mystery events...</h3>
					<p class="text-muted-foreground">Fetching recent mysterious phenomena from multiple sources.</p>
				</div>
			{:else}
				<div class="flex flex-col items-center justify-center h-64 text-center">
					<BookOpen class="h-12 w-12 text-muted-foreground mb-4" />
					<h3 class="text-lg font-medium mb-2">Recent Mystery Events Loaded</h3>
					<p class="text-muted-foreground">Explore mysterious phenomena from the past week, or search for specific topics.</p>
				</div>
			{/if}
		</ScrollArea>
	</div>

	<!-- 侧边栏 -->
	<div class="w-80 space-y-6">
		<!-- 神秘事件概览 -->
		{#if mysteryEvents.length > 0}
			<Card>
				<CardHeader class="pb-3">
					<CardTitle class="text-base flex items-center gap-2">
						<Search class="h-4 w-4" />
						Mystery Events Overview
					</CardTitle>
				</CardHeader>
				<CardContent>
					<div class="space-y-3">
						<div class="grid grid-cols-2 gap-2 text-sm">
							<div class="text-center p-2 bg-green-50 rounded">
								<div class="font-medium text-green-800">{mysteryEvents.filter(e => e.severity === 'low').length}</div>
								<div class="text-green-600 text-xs">Low</div>
							</div>
							<div class="text-center p-2 bg-yellow-50 rounded">
								<div class="font-medium text-yellow-800">{mysteryEvents.filter(e => e.severity === 'medium').length}</div>
								<div class="text-yellow-600 text-xs">Medium</div>
							</div>
							<div class="text-center p-2 bg-orange-50 rounded">
								<div class="font-medium text-orange-800">{mysteryEvents.filter(e => e.severity === 'high').length}</div>
								<div class="text-orange-600 text-xs">High</div>
							</div>
							<div class="text-center p-2 bg-red-50 rounded">
								<div class="font-medium text-red-800">{mysteryEvents.filter(e => e.severity === 'critical').length}</div>
								<div class="text-red-600 text-xs">Critical</div>
							</div>
						</div>
						<div class="text-xs text-muted-foreground text-center">
							Verified: {mysteryEvents.filter(e => e.verified).length}/{mysteryEvents.length}
						</div>
						<ScrollArea class="h-32">
							<div class="space-y-2">
								{#each mysteryEvents.slice(0, 3) as event (event.id)}
									<div class="border rounded-md p-2">
										<div class="flex items-center gap-1 mb-1">
											<Badge class="{getSeverityColor(event.severity)} text-xs">
												{event.severity === 'low' ? '低' : event.severity === 'medium' ? '中' : event.severity === 'high' ? '高' : '严重'}
											</Badge>
											{#if event.verified}
												<Badge variant="outline" class="text-xs">✓</Badge>
											{/if}
										</div>
										<h4 class="font-medium text-sm mb-1 line-clamp-1">{event.title}</h4>
										<p class="text-xs text-muted-foreground mb-1 line-clamp-2">{event.description}</p>
										<div class="text-xs text-muted-foreground">
											📍 {event.location} • {formatDate(event.timestamp)}
										</div>
									</div>
								{/each}
							</div>
						</ScrollArea>
					</div>
				</CardContent>
			</Card>
		{/if}

		<!-- 搜索历史 -->
		{#if searchHistory.length > 0}
			<Card>
				<CardHeader class="pb-3">
					<CardTitle class="text-base">Recent Searches</CardTitle>
				</CardHeader>
				<CardContent>
					<ScrollArea class="h-32">
						<div class="space-y-2">
							{#each searchHistory.slice(0, 5) as history (history.id)}
								<button
									class="w-full text-left p-2 rounded-md hover:bg-muted transition-colors"
									onclick={() => handleHistoryClick(history.query)}
								>
									<div class="font-medium text-sm truncate">{history.query}</div>
									<div class="text-xs text-muted-foreground">
										{formatDate(history.timestamp)} • {history.resultsCount} results
									</div>
								</button>
							{/each}
						</div>
					</ScrollArea>
				</CardContent>
			</Card>
		{/if}

		<!-- 保存的资源 -->
		{#if savedResources.length > 0}
			<Card>
				<CardHeader class="pb-3">
					<CardTitle class="text-base">Saved Resources</CardTitle>
				</CardHeader>
				<CardContent>
					<ScrollArea class="h-64">
						<div class="space-y-3">
							{#each savedResources as resource (resource.id)}
								<div class="border rounded-md p-3">
									<div class="flex items-start justify-between mb-2">
										<div class="flex items-center gap-1">
											<svelte:component this={getTypeIcon(resource.type)} class="h-3 w-3 text-muted-foreground" />
											<Badge variant="outline" class="text-xs">{resource.type}</Badge>
										</div>
										<Button variant="ghost" size="sm" onclick={() => removeSavedResource(resource.id)}>
											×
										</Button>
									</div>
									<h4 class="font-medium text-sm mb-1">
										<a href={resource.url} target="_blank" rel="noopener noreferrer" class="hover:underline">
											{resource.title}
										</a>
									</h4>
									<p class="text-xs text-muted-foreground mb-2 line-clamp-2">{resource.description}</p>
									<div class="text-xs text-muted-foreground">
										Saved {formatDate(resource.savedAt)}
									</div>
								</div>
							{/each}
						</div>
					</ScrollArea>
				</CardContent>
			</Card>
		{/if}

		<!-- 快速链接 -->
		<Card>
			<CardHeader class="pb-3">
				<CardTitle class="text-base">Quick Links</CardTitle>
			</CardHeader>
			<CardContent>
				<div class="space-y-2">
					<a href="https://scholar.google.com" target="_blank" rel="noopener noreferrer" class="flex items-center gap-2 p-2 rounded-md hover:bg-muted transition-colors">
						<Globe class="h-4 w-4" />
						<span class="text-sm">Google Scholar</span>
						<ExternalLink class="h-3 w-3 ml-auto" />
					</a>
					<a href="https://arxiv.org" target="_blank" rel="noopener noreferrer" class="flex items-center gap-2 p-2 rounded-md hover:bg-muted transition-colors">
						<FileText class="h-4 w-4" />
						<span class="text-sm">arXiv</span>
						<ExternalLink class="h-3 w-3 ml-auto" />
					</a>
					<a href="https://github.com" target="_blank" rel="noopener noreferrer" class="flex items-center gap-2 p-2 rounded-md hover:bg-muted transition-colors">
						<BookOpen class="h-4 w-4" />
						<span class="text-sm">GitHub</span>
						<ExternalLink class="h-3 w-3 ml-auto" />
					</a>
					<a href="https://stackoverflow.com" target="_blank" rel="noopener noreferrer" class="flex items-center gap-2 p-2 rounded-md hover:bg-muted transition-colors">
						<Globe class="h-4 w-4" />
						<span class="text-sm">Stack Overflow</span>
						<ExternalLink class="h-3 w-3 ml-auto" />
					</a>
				</div>
			</CardContent>
		</Card>
	</div>
</div>
</ScrollArea>

</div>