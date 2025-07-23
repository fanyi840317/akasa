<script lang="ts">
	import { onMount } from 'svelte';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Badge } from '$lib/components/ui/badge';
	import {
		Dialog,
		DialogContent,
		DialogHeader,
		DialogTitle,
		DialogTrigger
	} from '$lib/components/ui/dialog';
	import ContentContainer from '$lib/components/ui/content-container.svelte';

	import { toast } from 'svelte-sonner';
	import { Search, Settings, Key, Plus, Loader2, Check, X, Play } from '@lucide/svelte';
	import {
		SearchService,
		SearchEngineUtils,
		SearchResultUtils,
		type SearchEngine,
		type SearchResult
	} from '$lib/services/searchService';

	// 响应式状态
	let isLoading = $state<boolean>(false);
	let searchEngines = $state<SearchEngine[]>([]);
	let selectedEngine = $state<SearchEngine | null>(null);
	let apiKeyInput = $state<string>('');
	let isConfiguring = $state<boolean>(false);
	let dialogOpen = $state<boolean>(false);

	// 测试状态
	let testingEngine = $state<string | null>(null);
	let testResults = $state<SearchResult[]>([]);
	let testError = $state<string | null>(null);
	let engineTestStatus = $state<Record<string, 'success' | 'error' | null>>({});

	// 加载搜索引擎列表
	const loadConfig = async () => {
		isLoading = true;
		try {
			const response = await SearchService.getSearchEngines();
			if (response.success) {
				searchEngines = response.data.engines || [];
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

	// 打开API Key配置对话框
	const openApiKeyDialog = (engine: SearchEngine) => {
		selectedEngine = engine;
		apiKeyInput = '';
		dialogOpen = true;
	};

	// 配置API Key
	const configureApiKey = async () => {
		if (!selectedEngine || !apiKeyInput.trim()) {
			toast.error('请输入有效的API Key');
			return;
		}

		isConfiguring = true;
		try {
			// 这里应该调用API来保存API Key
			// 暂时模拟成功
			await new Promise((resolve) => setTimeout(resolve, 1000));

			// 更新引擎状态
			if (selectedEngine) {
				selectedEngine.api_key_configured = true;
			}

			toast.success(
				`${SearchEngineUtils.getEngineDisplayName(selectedEngine.name)} API Key 配置成功`
			);
			dialogOpen = false;
			apiKeyInput = '';
		} catch (error) {
			toast.error('API Key 配置失败', {
				description: error instanceof Error ? error.message : String(error)
			});
		} finally {
			isConfiguring = false;
		}
	};

	// 测试搜索引擎
	const testEngineSearch = async (engine: SearchEngine) => {
		testingEngine = engine.name;
		testError = null;
		testResults = [];
		engineTestStatus[engine.name] = null;

		try {
			const toolName = SearchEngineUtils.getToolNameFromEngine(engine.name);
			const response = await SearchService.testSearch(toolName, 'AI技术发展');

			if (response.success) {
				const parsed = SearchResultUtils.parseTestResult(response.data);
				if (parsed.success && parsed.results) {
					testResults = parsed.results
						.slice(0, 3)
						.map((result, index) => SearchResultUtils.formatSearchResult(result, index));
					engineTestStatus[engine.name] = 'success';
					toast.success(`${SearchEngineUtils.getEngineDisplayName(engine.name)} 测试成功`);
				} else {
					throw new Error(parsed.error || '搜索结果解析失败');
				}
			} else {
				throw new Error(response.error || '搜索测试失败');
			}
		} catch (error) {
			testError = error instanceof Error ? error.message : String(error);
			engineTestStatus[engine.name] = 'error';
			toast.error(`${SearchEngineUtils.getEngineDisplayName(engine.name)} 测试失败`, {
				description: testError
			});
		} finally {
			testingEngine = null;
		}
	};

	// 组件挂载时加载配置
	onMount(() => {
		loadConfig();
	});
</script>

<ContentContainer>
	{#snippet children()}
		<!-- 页面标题 -->
		<div class="mb-8 flex items-center justify-between">
			<h1 class="text-xl font-semibold">模型列表</h1>
			<Button variant="outline" size="sm" class="text-xs">
				<Settings class="mr-2 h-4 w-4" />
				系统模型设置
			</Button>
		</div>

		{#if isLoading && !searchEngines.length}
			<div class="flex items-center justify-center py-12">
				<div
					class="h-8 w-8 animate-spin rounded-full border-4 border-current border-t-transparent"
				></div>
				<span class="ml-2">加载配置中...</span>
			</div>
		{:else}
			<!-- 搜索引擎列表 -->
			<div class="space-y-4">
				{#each searchEngines as engine (engine.name)}
					<div class="bg-card rounded-lg ">
						<div class="p-6">
						<div class="mb-4 flex items-center justify-between">
							<!-- 左侧：引擎信息 -->
							<div class="flex items-center space-x-4">
								<!-- <div class="w-12 h-12 bg-muted rounded-lg flex items-center justify-center">
								<Search class="h-6 w-6" />
							</div> -->
								<div class="space-y-1">
									<div class="flex flex-col space-x-2">
										<h3 class="text-base font-semibold">
											{SearchEngineUtils.getEngineDisplayName(engine.name)}
										</h3>
										<div class="flex space-x-2">
											<Badge variant="secondary">LLM</Badge>
											{#if engine.requires_api_key}
												<Badge variant="outline">文本输入</Badge>
												<Badge variant="outline">语音转文本</Badge>
												<Badge variant="outline">内容审核</Badge>
												<Badge variant="outline">文本转语音</Badge>
											{/if}
										</div>
									</div>
									<p class="text-muted-foreground text-xs">
										{SearchEngineUtils.getEngineDescription(engine.name)}
									</p>
								</div>
							</div>

							<!-- 右侧：操作区域 -->
							<div class="flex items-center space-x-4">
								<!-- 额度信息 -->
								{#if engine.requires_api_key}
									<div class="bg-muted/30 rounded-lg p-4">
										<div class="mb-2 flex items-center justify-between">
											<span class="text-muted-foreground text-xs">额度</span>
											<span class="h-2 w-2 rounded-full bg-orange-500"></span>
										</div>
										<div class="text-base font-semibold">
											{engine.api_key_configured ? '0' : '0'}
											<span class="text-muted-foreground ml-1 text-xs">
												{engine.api_key_configured ? '消耗额度' : 'Tokens'}
											</span>
										</div>
									</div>
								{:else}
									<div class="bg-muted/30 rounded-lg p-4">
										<div class="flex items-center space-x-2">
											<Check class="h-4 w-4 text-green-500" />
											<span class="text-muted-foreground text-xs">免费可用</span>
										</div>
									</div>
								{/if}

								<!-- 操作按钮 -->
							</div>
						</div>
					</div>
						<div class="bg-muted/50 rounded-b-md p-4">
							<div class="flex items-center justify-between">
								<!-- 左侧：API Key 按钮 -->
								{#if engine.requires_api_key}
									<Dialog bind:open={dialogOpen}>
										<DialogTrigger>
											<Button
												variant={engine.api_key_configured ? "outline" : "default"}
												size="sm"
												class="text-xs"
												onclick={() => openApiKeyDialog(engine)}
											>
												{#if engine.api_key_configured}
													<Key class="mr-2 h-4 w-4" />
													修改密钥
												{:else}
													<Key class="mr-2 h-4 w-4" />
													API-KEY
													<span class="ml-2 h-2 w-2 rounded-full bg-red-500"></span>
												{/if}
											</Button>
										</DialogTrigger>
									</Dialog>
								{:else}
									<div></div>
								{/if}

								<!-- 右侧：测试按钮和状态 -->
								<div class="flex items-center space-x-2">
									<!-- 测试状态显示 -->
									{#if engineTestStatus[engine.name] === 'success'}
										<div class="flex items-center space-x-1">
											<Check class="h-4 w-4 text-green-500" />
											<span class="text-green-500 text-xs">测试通过</span>
										</div>
									{:else if engineTestStatus[engine.name] === 'error'}
										<div class="flex items-center space-x-1">
											<X class="h-4 w-4 text-red-500" />
											<span class="text-red-500 text-xs">测试失败</span>
										</div>
									{/if}

									<!-- 测试按钮 -->
									<Button
										variant="ghost"
										size="sm"
										class="text-xs"
										disabled={testingEngine === engine.name || (engine.requires_api_key && !engine.api_key_configured)}
										onclick={() => testEngineSearch(engine)}
									>
										{#if testingEngine === engine.name}
											<Loader2 class="mr-2 h-4 w-4 animate-spin" />
											测试中
										{:else}
											<Play class="mr-2 h-4 w-4" />
											测试
										{/if}
									</Button>
								</div>
							</div>
						</div>
					</div>
				{/each}
			</div>
		{/if}

		<!-- 测试结果显示 -->
		{#if testResults.length > 0 || testError}
			<div class="bg-card rounded-lg p-6">
				<h3 class="mb-4 text-base font-semibold">搜索测试结果</h3>

				{#if testError}
					<div class="bg-destructive/10 border-destructive/20 rounded-lg border p-4">
						<div class="flex items-center space-x-2">
							<X class="text-destructive h-4 w-4" />
							<span class="text-destructive text-xs font-medium">测试失败</span>
						</div>
						<p class="text-destructive mt-2 text-xs">{testError}</p>
					</div>
				{:else if testResults.length > 0}
					<div class="space-y-3">
						{#each testResults as result, index (index)}
							<div class="bg-muted/50 rounded-lg p-4">
								<div class="flex items-start justify-between">
									<div class="flex-1">
										<h4 class="mb-1 text-xs font-medium">
											<a
												href={result.url}
												target="_blank"
												rel="noopener noreferrer"
												class="text-primary hover:underline"
											>
												{result.title}
											</a>
										</h4>
										<p class="text-muted-foreground mb-2 text-xs">{result.url}</p>
										<p class="text-muted-foreground line-clamp-2 text-xs">{result.content}</p>
									</div>
									<Badge variant="outline" class="ml-4">{index + 1}</Badge>
								</div>
							</div>
						{/each}
					</div>
				{/if}
			</div>
		{/if}
	{/snippet}
</ContentContainer>

<!-- API Key 配置对话框 -->
{#if selectedEngine}
	<DialogContent>
		<DialogHeader>
			<DialogTitle>
				配置 {SearchEngineUtils.getEngineDisplayName(selectedEngine.name)} API Key
			</DialogTitle>
		</DialogHeader>
		<div class="space-y-4 py-4">
			<div class="space-y-2">
				<label class="text-xs font-medium">API Key</label>
				<Input
					type="password"
					bind:value={apiKeyInput}
					placeholder="请输入您的 API Key"
					class="w-full"
				/>
			</div>
			<div class="flex justify-end space-x-2">
				<Button variant="outline" class="text-xs" onclick={() => (dialogOpen = false)}>取消</Button>
				<Button class="text-xs" onclick={configureApiKey} disabled={isConfiguring || !apiKeyInput.trim()}>
					{#if isConfiguring}
						<Loader2 class="mr-2 h-4 w-4 animate-spin" />
					{/if}
					保存
				</Button>
			</div>
		</div>
	</DialogContent>
{/if}
