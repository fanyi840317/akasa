<script lang="ts">
	import { onMount } from 'svelte';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Badge } from '$lib/components/ui/badge';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '$lib/components/ui/select';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Separator } from '$lib/components/ui/separator';
	import { toast } from 'svelte-sonner';
	import { 
		Search, 
		Settings, 
		Play, 
		RefreshCw,
		CheckCircle,
		XCircle,
		Loader2,
		Info
	} from '@lucide/svelte';
	import { 
		SearchService, 
		SearchEngineUtils, 
		SearchResultUtils,
		type SearchEngine,
		type ToolTestResult
	} from '$lib/services/searchService';

	// 响应式状态
	let isLoading = $state<boolean>(false);
	let isTestingSearch = $state<boolean>(false);
	let searchEngines = $state<SearchEngine[]>([]);
	let currentEngine = $state<string>('');
	let testQuery = $state<string>('人工智能的发展历史');
	let maxResults = $state<number>(5);
	let testResults = $state<any>(null);

	// 加载搜索引擎列表
	const loadConfig = async () => {
		isLoading = true;
		try {
			const response = await SearchService.getSearchEngines();
			if (response.success) {
				searchEngines = response.data.engines || [];
				currentEngine = response.data.current || '';
				maxResults = response.data.max_results || 5;
				toast.success('搜索引擎配置加载成功');
			} else {
				throw new Error(response.error || '加载失败');
			}
		} catch (error) {
			toast.error('加载搜索引擎配置失败', {
				description: error instanceof Error ? error.message : String(error)
			});
			console.error('Error loading search engines:', error);
		} finally {
			isLoading = false;
		}
	};

	// 更新搜索引擎配置
	const updateConfig = async () => {
		if (!currentEngine) {
			toast.error('请选择搜索引擎');
			return;
		}

		if (maxResults < 1 || maxResults > 50) {
			toast.error('最大结果数应在1-50之间');
			return;
		}

		isLoading = true;
		try {
			const response = await SearchService.updateConfig({
				tool_name: SearchEngineUtils.getToolNameFromEngine(currentEngine),
				config: {
					search_engine: currentEngine,
					max_results: maxResults
				}
			});
			
			if (response.success) {
				toast.success('搜索引擎配置更新成功');
			} else {
				throw new Error(response.error || '更新失败');
			}
		} catch (error) {
			toast.error('更新搜索引擎配置失败', {
				description: error instanceof Error ? error.message : String(error)
			});
			console.error('Error updating config:', error);
		} finally {
			isLoading = false;
		}
	};

	// 测试搜索工具
	const testSearch = async () => {
		if (!testQuery.trim()) {
			toast.error('请输入测试查询');
			return;
		}

		if (!currentEngine) {
			toast.error('请先选择搜索引擎');
			return;
		}
		
		isTestingSearch = true;
		testResults = null;
		
		try {
			const toolName = SearchEngineUtils.getToolNameFromEngine(currentEngine);
			const response = await SearchService.testSearch(toolName, testQuery.trim());
			
			if (response.success && response.data) {
				const parsedResult = SearchResultUtils.parseTestResult(response.data);
				if (parsedResult.success) {
					testResults = {
						success: true,
						results: parsedResult.results || []
					};
					const responseTime = response.data.response_time_ms;
					toast.success(`测试成功，找到 ${parsedResult.results?.length || 0} 个结果${responseTime ? `，耗时 ${responseTime}ms` : ''}`);
				} else {
					testResults = {
						success: false,
						error: parsedResult.error
					};
					toast.error('测试失败: ' + (parsedResult.error || '未知错误'));
				}
			} else {
				throw new Error(response.error || '测试失败');
			}
		} catch (error) {
			toast.error('搜索测试失败', {
				description: error instanceof Error ? error.message : String(error)
			});
			console.error('Error testing search:', error);
		} finally {
			isTestingSearch = false;
		}
	};

	// 组件挂载时加载配置
	onMount(() => {
		loadConfig();
	});
</script>

<div class="container mx-auto p-6 space-y-6">
	<!-- 页面标题 -->
	<div class="flex items-center space-x-2">
		<Search class="h-6 w-6" />
		<h1 class="text-2xl font-bold">搜索工具配置</h1>
		<Badge variant="outline">Search Engine</Badge>
	</div>

	{#if isLoading && !searchEngines.length}
		<div class="flex items-center justify-center py-12">
			<div class="animate-spin h-8 w-8 border-4 border-current border-t-transparent rounded-full"></div>
			<span class="ml-2">加载配置中...</span>
		</div>
	{:else}
		<!-- 搜索引擎配置 -->
		<Card>
			<CardHeader>
				<CardTitle class="flex items-center space-x-2">
					<Settings class="h-5 w-5" />
					<span>搜索引擎设置</span>
				</CardTitle>
			</CardHeader>
			<CardContent class="space-y-4">
				<!-- 搜索引擎选择 -->
				<div class="space-y-2">
					<Label for="search-engine">搜索引擎</Label>
					<Select bind:value={currentEngine}>
						<SelectTrigger>
							<SelectValue placeholder="选择搜索引擎" />
						</SelectTrigger>
						<SelectContent>
							{#each searchEngines as engine (engine.name)}
							<SelectItem value={engine.name}>
								<div class="flex flex-col">
									<span class="font-medium">{SearchEngineUtils.getEngineDisplayName(engine.name)}</span>
									<span class="text-sm text-gray-500">{SearchEngineUtils.getEngineDescription(engine.name)}</span>
								</div>
							</SelectItem>
						{/each}
						</SelectContent>
					</Select>
				</div>

				<!-- 最大结果数 -->
				<div class="space-y-2">
					<Label for="max-results">最大搜索结果数</Label>
					<Input
						id="max-results"
						type="number"
						min="1"
						max="20"
						bind:value={maxResults}
						placeholder="输入最大结果数"
					/>
					<p class="text-sm text-gray-500">建议设置为 1-20 之间的数值</p>
				</div>

				<!-- 保存按钮 -->
				<div class="flex justify-end">
					<Button
						onclick={updateConfig}
				disabled={isLoading}
					>
						{#if isLoading}
							<Loader2 class="h-4 w-4 mr-2 animate-spin" />
						{:else}
							<Settings class="h-4 w-4 mr-2" />
						{/if}
						保存配置
					</Button>
				</div>
			</CardContent>
		</Card>

		<!-- 搜索测试 -->
		<Card>
			<CardHeader>
				<CardTitle class="flex items-center space-x-2">
					<Play class="h-5 w-5" />
					<span>搜索测试</span>
				</CardTitle>
			</CardHeader>
			<CardContent class="space-y-4">
				<!-- 测试查询输入 -->
				<div class="space-y-2">
					<Label for="test-query">测试查询</Label>
					<div class="flex space-x-2">
						<Input
							id="test-query"
							bind:value={testQuery}
							placeholder="输入要测试的搜索查询..."
							class="flex-1"
						/>
						<Button
						onclick={testSearch}
				disabled={isTestingSearch || !testQuery.trim()}
					>
							{#if isTestingSearch}
								<Loader2 class="h-4 w-4 mr-2 animate-spin" />
							{:else}
								<Play class="h-4 w-4 mr-2" />
							{/if}
							测试搜索
						</Button>
					</div>
				</div>

				<!-- 测试结果 -->
				{#if testResults}
					<div class="space-y-3">
						<div class="flex items-center justify-between">
							<Label>测试结果</Label>
							<Badge variant="outline">
								{testResults.results?.length || 0} 个结果
							</Badge>
						</div>
						
						{#if testResults.success}
							<div class="space-y-2">
								{#each testResults.results || [] as result, index (index)}
									<Card class="p-3">
										<div class="space-y-2">
											<div class="flex items-start justify-between">
												<h4 class="font-medium text-sm">
													{result.title || `结果 ${index + 1}`}
												</h4>
												<Badge variant="secondary" class="text-xs">
													#{index + 1}
												</Badge>
											</div>
											{#if result.url}
												<p class="text-xs text-blue-600 truncate">{result.url}</p>
											{/if}
											{#if result.content || result.description}
												<p class="text-sm text-gray-600 line-clamp-2">
													{result.content || result.description}
												</p>
											{/if}
										</div>
									</Card>
								{/each}
							</div>
						{:else}
							<Card class="p-4">
								<div class="flex items-center space-x-2 text-red-600">
									<XCircle class="h-5 w-5" />
									<span class="font-medium">测试失败</span>
								</div>
								{#if testResults.error}
									<p class="text-sm text-gray-600 mt-2">{testResults.error}</p>
								{/if}
							</Card>
						{/if}
					</div>
				{/if}
			</CardContent>
		</Card>

		<!-- 当前配置信息 -->
		<Card>
			<CardHeader>
				<CardTitle class="flex items-center space-x-2">
					<Info class="h-5 w-5" />
					<span>当前配置</span>
				</CardTitle>
			</CardHeader>
			<CardContent>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
					<div class="space-y-2">
						<Label class="text-sm font-medium">当前搜索引擎</Label>
						<div class="flex items-center space-x-2">
							<Badge variant="default">{SearchEngineUtils.getEngineDisplayName(currentEngine)}</Badge>
							<span class="text-sm text-gray-500">{SearchEngineUtils.getEngineDescription(currentEngine)}</span>
						</div>
					</div>
					<div class="space-y-2">
						<Label class="text-sm font-medium">最大结果数</Label>
						<Badge variant="outline">{maxResults} 个结果</Badge>
					</div>
				</div>
			</CardContent>
		</Card>
	{/if}
</div>