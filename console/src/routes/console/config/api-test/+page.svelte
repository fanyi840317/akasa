<script lang="ts">
	import { onMount } from 'svelte';
	import { toast } from 'svelte-sonner';
	import PageHeader from '$lib/components/ui/page-header.svelte';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Badge } from '$lib/components/ui/badge';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import { Textarea } from '$lib/components/ui/textarea';
	import { 
		Settings, 
		Play, 
		RefreshCw, 
		CheckCircle, 
		XCircle,
		Clock,
		Globe,
		Search,
		FileText,
		BookOpen
	} from '@lucide/svelte';
	import { appStore } from '$lib/stores/app-state';

	appStore.setSidebarCollapsed(false);

	// API配置状态
	let apiConfig = $state({
		backendUrl: 'http://localhost:8000',
		newsApiKey: '',
		githubToken: ''
	});

	// 测试状态
	let testResults = $state<Array<{
		id: string;
		name: string;
		status: 'pending' | 'success' | 'error';
		responseTime?: number;
		response?: any;
		error?: string;
		timestamp: number;
	}>>([]);

	let isTestingAll = $state(false);
	let searchQuery = $state('artificial intelligence');
	let searchResults = $state<any[]>([]);
	let isSearching = $state(false);

	// API端点配置
	const apiEndpoints = [
		{ id: 'health', name: '健康检查', path: '/health', method: 'GET' },
		{ id: 'mystery', name: '神秘事件搜索', path: '/api/research/mystery', method: 'GET' },
		{ id: 'news', name: '新闻搜索', path: '/api/research/news', method: 'GET' },
		{ id: 'academic', name: '学术搜索', path: '/api/research/academic', method: 'GET' },
		{ id: 'github', name: 'GitHub搜索', path: '/api/research/github', method: 'GET' },
		{ id: 'search', name: '综合搜索', path: '/api/research/search', method: 'GET' }
	];

	// 测试单个API端点
	const testEndpoint = async (endpoint: typeof apiEndpoints[0]) => {
		const testId = `${endpoint.id}-${Date.now()}`;
		const startTime = Date.now();
		
		// 添加测试记录
		testResults = [{
			id: testId,
			name: endpoint.name,
			status: 'pending',
			timestamp: startTime
		}, ...testResults];

		try {
			let url = `${apiConfig.backendUrl}${endpoint.path}`;
			
			// 为搜索端点添加查询参数
			if (endpoint.id !== 'health') {
				url += `?q=${encodeURIComponent('test query')}`;
			}

			const response = await fetch(url, {
				method: endpoint.method,
				headers: {
					'Content-Type': 'application/json'
				}
			});

			const responseTime = Date.now() - startTime;
			const data = await response.json();

			// 更新测试结果
			testResults = testResults.map(result => 
				result.id === testId 
					? {
							...result,
							status: response.ok ? 'success' : 'error',
							responseTime,
							response: data,
							error: response.ok ? undefined : `HTTP ${response.status}: ${response.statusText}`
						}
						: result
			);

			if (response.ok) {
				toast.success(`${endpoint.name} 测试成功`);
			} else {
				toast.error(`${endpoint.name} 测试失败`);
			}

		} catch (error) {
			const responseTime = Date.now() - startTime;
			
			// 更新测试结果
			testResults = testResults.map(result => 
				result.id === testId 
					? {
							...result,
							status: 'error',
							responseTime,
							error: error instanceof Error ? error.message : String(error)
						}
						: result
			);

			toast.error(`${endpoint.name} 测试失败: ${error instanceof Error ? error.message : String(error)}`);
		}
	};

	// 测试所有API端点
	const testAllEndpoints = async () => {
		isTestingAll = true;
		try {
			for (const endpoint of apiEndpoints) {
				await testEndpoint(endpoint);
				// 添加延迟避免过快请求
				await new Promise(resolve => setTimeout(resolve, 500));
			}
			toast.success('所有API测试完成');
		} finally {
			isTestingAll = false;
		}
	};

	// 执行搜索测试
	const performSearch = async () => {
		if (!searchQuery.trim()) {
			toast.error('请输入搜索关键词');
			return;
		}

		isSearching = true;
		try {
			const response = await fetch(`${apiConfig.backendUrl}/api/research/search?q=${encodeURIComponent(searchQuery)}`);
			const data = await response.json();

			if (response.ok && data.success) {
				searchResults = data.data.results || [];
				toast.success(`搜索完成，找到 ${searchResults.length} 个结果`);
			} else {
				toast.error('搜索失败: ' + (data.error || '未知错误'));
				searchResults = [];
			}
		} catch (error) {
			toast.error('搜索失败: ' + (error instanceof Error ? error.message : String(error)));
			searchResults = [];
		} finally {
			isSearching = false;
		}
	};

	// 清空测试结果
	const clearResults = () => {
		testResults = [];
		searchResults = [];
	};

	// 格式化时间
	const formatTime = (timestamp: number) => {
		return new Date(timestamp).toLocaleTimeString();
	};

	// 获取状态图标
	const getStatusIcon = (status: string) => {
		switch (status) {
			case 'success': return CheckCircle;
			case 'error': return XCircle;
			case 'pending': return Clock;
			default: return Clock;
		}
	};

	// 获取状态颜色
	const getStatusColor = (status: string) => {
		switch (status) {
			case 'success': return 'text-green-600';
			case 'error': return 'text-red-600';
			case 'pending': return 'text-yellow-600';
			default: return 'text-gray-600';
		}
	};

	// 获取结果类型图标
	const getResultTypeIcon = (type: string) => {
		switch (type) {
			case 'paper': return FileText;
			case 'documentation': return BookOpen;
			case 'article': return FileText;
			case 'website': return Globe;
			case 'mystery_event': return Search;
			default: return FileText;
		}
	};

	onMount(() => {
		// 从localStorage加载配置
		const savedConfig = localStorage.getItem('api-test-config');
		if (savedConfig) {
			try {
				apiConfig = { ...apiConfig, ...JSON.parse(savedConfig) };
			} catch (error) {
				console.error('Failed to load saved config:', error);
			}
		}
	});

	// 保存配置到localStorage
	$effect(() => {
		localStorage.setItem('api-test-config', JSON.stringify(apiConfig));
	});
</script>

<PageHeader title="API测试" description="配置和测试搜索API接口" />

<ScrollArea class="p-6">
	<div class="max-w-6xl mx-auto space-y-6">
		<!-- API配置 -->
		<Card>
			<CardHeader>
				<CardTitle class="flex items-center gap-2">
					<Settings class="h-5 w-5" />
					API配置
				</CardTitle>
			</CardHeader>
			<CardContent class="space-y-4">
				<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
					<div class="space-y-2">
						<Label for="backend-url">后端服务地址</Label>
						<Input
							id="backend-url"
							bind:value={apiConfig.backendUrl}
							placeholder="http://localhost:3001"
						/>
					</div>
					<div class="space-y-2">
						<Label for="news-api-key">News API Key</Label>
						<Input
							id="news-api-key"
							type="password"
							bind:value={apiConfig.newsApiKey}
							placeholder="输入News API密钥"
						/>
					</div>
					<div class="space-y-2">
						<Label for="github-token">GitHub Token</Label>
						<Input
							id="github-token"
							type="password"
							bind:value={apiConfig.githubToken}
							placeholder="输入GitHub访问令牌"
						/>
					</div>
				</div>
			</CardContent>
		</Card>

		<!-- API端点测试 -->
		<Card>
			<CardHeader>
				<div class="flex items-center justify-between">
					<CardTitle class="flex items-center gap-2">
						<Play class="h-5 w-5" />
						API端点测试
					</CardTitle>
					<div class="flex gap-2">
						<Button variant="outline" size="sm" onclick={clearResults}>
							<RefreshCw class="h-4 w-4 mr-2" />
							清空结果
						</Button>
						<Button onclick={testAllEndpoints} disabled={isTestingAll}>
							{#if isTestingAll}
								<div class="animate-spin h-4 w-4 border-2 border-current border-t-transparent rounded-full mr-2"></div>
							{:else}
								<Play class="h-4 w-4 mr-2" />
							{/if}
							测试所有端点
						</Button>
					</div>
				</div>
			</CardHeader>
			<CardContent>
				<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
					{#each apiEndpoints as endpoint}
						<Card class="border-2">
							<CardContent class="p-4">
								<div class="flex items-center justify-between mb-2">
									<h4 class="font-medium">{endpoint.name}</h4>
									<Badge variant="outline">{endpoint.method}</Badge>
								</div>
								<p class="text-sm text-muted-foreground mb-3">{endpoint.path}</p>
								<Button 
									size="sm" 
									variant="outline" 
									class="w-full"
									onclick={() => testEndpoint(endpoint)}
									disabled={isTestingAll}
								>
									<Play class="h-3 w-3 mr-2" />
									测试
								</Button>
							</CardContent>
						</Card>
					{/each}
				</div>

				<!-- 测试结果 -->
				{#if testResults.length > 0}
					<div class="space-y-3">
						<h4 class="font-medium">测试结果</h4>
						<ScrollArea class="h-64 border rounded-md p-4">
							<div class="space-y-3">
								{#each testResults as result}
									<div class="flex items-start gap-3 p-3 border rounded-md">
										<svelte:component 
											this={getStatusIcon(result.status)} 
											class="h-5 w-5 mt-0.5 {getStatusColor(result.status)}" 
										/>
										<div class="flex-1 min-w-0">
											<div class="flex items-center justify-between mb-1">
												<h5 class="font-medium">{result.name}</h5>
												<div class="flex items-center gap-2 text-sm text-muted-foreground">
													{#if result.responseTime}
														<span>{result.responseTime}ms</span>
													{/if}
													<span>{formatTime(result.timestamp)}</span>
												</div>
											</div>
											{#if result.error}
												<p class="text-sm text-red-600">{result.error}</p>
											{:else if result.response}
												<details class="text-sm">
													<summary class="cursor-pointer text-muted-foreground hover:text-foreground">
														查看响应数据
													</summary>
													<pre class="mt-2 p-2 bg-muted rounded text-xs overflow-auto">{JSON.stringify(result.response, null, 2)}</pre>
												</details>
											{/if}
										</div>
									</div>
								{/each}
							</div>
						</ScrollArea>
					</div>
				{/if}
			</CardContent>
		</Card>

		<!-- 搜索测试 -->
		<Card>
			<CardHeader>
				<CardTitle class="flex items-center gap-2">
					<Search class="h-5 w-5" />
					搜索功能测试
				</CardTitle>
			</CardHeader>
			<CardContent class="space-y-4">
				<div class="flex gap-2">
					<Input
						bind:value={searchQuery}
						placeholder="输入搜索关键词..."
						class="flex-1"
						onkeydown={(e: KeyboardEvent) => {
							if (e.key === 'Enter') {
								performSearch();
							}
						}}
					/>
					<Button onclick={performSearch} disabled={isSearching || !searchQuery.trim()}>
						{#if isSearching}
							<div class="animate-spin h-4 w-4 border-2 border-current border-t-transparent rounded-full mr-2"></div>
						{:else}
							<Search class="h-4 w-4 mr-2" />
						{/if}
						搜索
					</Button>
				</div>

				<!-- 搜索结果 -->
				{#if searchResults.length > 0}
					<div class="space-y-3">
						<h4 class="font-medium">搜索结果 ({searchResults.length})</h4>
						<ScrollArea class="h-96 border rounded-md p-4">
							<div class="space-y-4">
								{#each searchResults as result}
									<Card class="border">
										<CardContent class="p-4">
											<div class="flex items-start gap-3">
												<svelte:component 
													this={getResultTypeIcon(result.type)} 
													class="h-5 w-5 mt-0.5 text-muted-foreground" 
												/>
												<div class="flex-1 min-w-0">
													<div class="flex items-center gap-2 mb-2">
														<Badge variant="secondary">{result.type}</Badge>
														<Badge variant="outline">{result.source}</Badge>
														{#if result.severity}
															<Badge variant="destructive">{result.severity}</Badge>
														{/if}
													</div>
													<h5 class="font-medium mb-1">
														{#if result.url && result.url !== '#'}
															<a href={result.url} target="_blank" rel="noopener noreferrer" class="hover:underline">
																{result.title}
															</a>
														{:else}
															{result.title}
														{/if}
													</h5>
													<p class="text-sm text-muted-foreground mb-2">{result.description}</p>
													{#if result.tags && result.tags.length > 0}
														<div class="flex flex-wrap gap-1">
															{#each result.tags as tag}
																<Badge variant="outline" class="text-xs">{tag}</Badge>
															{/each}
														</div>
													{/if}
												</div>
											</div>
										</CardContent>
									</Card>
								{/each}
							</div>
						</ScrollArea>
					</div>
				{:else if isSearching}
					<div class="flex items-center justify-center h-32">
						<div class="text-center">
							<div class="animate-spin h-8 w-8 border-2 border-current border-t-transparent rounded-full mx-auto mb-2"></div>
							<p class="text-muted-foreground">正在搜索...</p>
						</div>
					</div>
				{/if}
			</CardContent>
		</Card>
	</div>
</ScrollArea>