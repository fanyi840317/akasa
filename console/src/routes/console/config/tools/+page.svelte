<script>
	import { onMount } from 'svelte';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Badge } from '$lib/components/ui/badge';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Separator } from '$lib/components/ui/separator';
	import { toast } from 'svelte-sonner';
	import { 
		Settings, 
		Search, 
		RefreshCw, 
		ToggleLeft, 
		ToggleRight,
		Info,
		CheckCircle,
		XCircle
	} from '@lucide/svelte';

	// 响应式状态
	let loading = $state(false);
	let searchQuery = $state('');
	let tools = $state([]);
	let filteredTools = $state([]);
	let enabledCount = $state(0);
	let totalCount = $state(0);

	// 过滤工具列表
	$effect(() => {
		if (searchQuery.trim() === '') {
			filteredTools = tools;
		} else {
			const query = searchQuery.toLowerCase();
			filteredTools = tools.filter(tool => 
				tool.name.toLowerCase().includes(query) ||
				tool.type.toLowerCase().includes(query) ||
				tool.description.toLowerCase().includes(query)
			);
		}
	});

	// 加载工具列表
	const loadTools = async () => {
		loading = true;
		try {
			const response = await fetch('/api/tools/');
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			const result = await response.json();
			
			if (result.success) {
				tools = result.data.tools;
				enabledCount = result.data.enabled_count;
				totalCount = result.data.total;
				toast.success('工具列表加载成功');
			} else {
				throw new Error(result.error || '加载失败');
			}
		} catch (error) {
			toast.error('加载工具列表失败', {
				description: error instanceof Error ? error.message : String(error)
			});
			console.error('Error loading tools:', error);
		} finally {
			loading = false;
		}
	};

	// 切换工具启用状态
	const toggleTool = async (toolName, currentEnabled) => {
		try {
			// 这里应该调用后端 API 来切换工具状态
			// 目前只是模拟操作
			const newEnabled = !currentEnabled;
			
			// 更新本地状态
			tools = tools.map(tool => 
				tool.name === toolName 
					? { ...tool, enabled: newEnabled }
					: tool
			);
			
			// 更新计数
			enabledCount = tools.filter(tool => tool.enabled).length;
			
			toast.success(`工具 ${toolName} 已${newEnabled ? '启用' : '禁用'}`);
		} catch (error) {
			toast.error('切换工具状态失败', {
				description: error instanceof Error ? error.message : String(error)
			});
		}
	};

	// 获取工具类型的显示样式
	const getTypeVariant = (type) => {
		switch (type.toLowerCase()) {
			case 'search':
				return 'default';
			case 'web':
				return 'secondary';
			case 'api':
				return 'outline';
			default:
				return 'secondary';
		}
	};

	// 组件挂载时加载工具
	onMount(() => {
		loadTools();
	});
</script>

<div class="container mx-auto p-6 space-y-6">
	<!-- 页面标题和操作 -->
	<div class="flex items-center justify-between">
		<div class="flex items-center space-x-2">
			<Settings class="h-6 w-6" />
			<h1 class="text-2xl font-bold">工具管理</h1>
			<Badge variant="outline" class="ml-2">
				{enabledCount}/{totalCount} 已启用
			</Badge>
		</div>
		<div class="flex items-center space-x-2">
			<Button
				variant="outline"
				size="sm"
				onclick={loadTools}
				disabled={loading}
			>
				{#if loading}
					<div class="animate-spin h-4 w-4 border-2 border-current border-t-transparent rounded-full mr-2"></div>
				{:else}
					<RefreshCw class="h-4 w-4 mr-2" />
				{/if}
				刷新
			</Button>
		</div>
	</div>

	<!-- 搜索栏 -->
	<Card>
		<CardContent class="pt-6">
			<div class="flex items-center space-x-2">
				<Search class="h-4 w-4 text-gray-500" />
				<Input
					type="text"
					placeholder="搜索工具名称、类型或描述..."
					bind:value={searchQuery}
					class="flex-1"
				/>
			</div>
		</CardContent>
	</Card>

	{#if loading}
		<div class="flex items-center justify-center py-12">
			<div class="animate-spin h-8 w-8 border-4 border-current border-t-transparent rounded-full"></div>
			<span class="ml-2">加载工具列表中...</span>
		</div>
	{:else if filteredTools.length === 0}
		<Card>
			<CardContent class="pt-6">
				<div class="text-center py-8">
					<Info class="h-12 w-12 text-gray-400 mx-auto mb-4" />
					<h3 class="text-lg font-medium text-gray-900 mb-2">没有找到工具</h3>
					<p class="text-gray-500">
						{searchQuery ? '没有匹配的工具，请尝试其他搜索条件' : '暂无可用工具'}
					</p>
				</div>
			</CardContent>
		</Card>
	{:else}
		<!-- 工具列表 -->
		<div class="grid gap-4">
			{#each filteredTools as tool (tool.name)}
				<Card class="transition-all hover:shadow-md">
					<CardHeader>
						<div class="flex items-center justify-between">
							<div class="flex items-center space-x-3">
								<div class="flex items-center space-x-2">
									{#if tool.enabled}
										<CheckCircle class="h-5 w-5 text-green-600" />
									{:else}
										<XCircle class="h-5 w-5 text-gray-400" />
									{/if}
									<CardTitle class="text-lg">{tool.name}</CardTitle>
								</div>
								<Badge variant={getTypeVariant(tool.type)}>
									{tool.type}
								</Badge>
							</div>
							<Button
								variant="ghost"
								size="sm"
								onclick={() => toggleTool(tool.name, tool.enabled)}
								class="p-2"
							>
								{#if tool.enabled}
									<ToggleRight class="h-5 w-5 text-green-600" />
								{:else}
									<ToggleLeft class="h-5 w-5 text-gray-400" />
								{/if}
							</Button>
						</div>
					</CardHeader>
					<CardContent>
						<div class="space-y-3">
							<!-- 工具描述 -->
							{#if tool.description}
								<p class="text-gray-600">{tool.description}</p>
							{:else}
								<p class="text-gray-400 italic">暂无描述</p>
							{/if}
							
							<!-- 参数列表 -->
							{#if tool.parameters && tool.parameters.length > 0}
								<div>
									<Label class="text-sm font-medium text-gray-700">参数:</Label>
									<div class="flex flex-wrap gap-1 mt-1">
										{#each tool.parameters as param}
											<Badge variant="outline" class="text-xs">
												{param}
											</Badge>
										{/each}
									</div>
								</div>
							{:else}
								<div>
									<Label class="text-sm font-medium text-gray-700">参数:</Label>
									<p class="text-sm text-gray-400 mt-1">无参数</p>
								</div>
							{/if}
							
							<!-- 状态指示 -->
							<div class="flex items-center justify-between pt-2 border-t">
								<div class="flex items-center space-x-2">
									<span class="text-sm text-gray-500">状态:</span>
									<Badge 
										variant={tool.enabled ? 'default' : 'secondary'}
										class={tool.enabled ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'}
									>
										{tool.enabled ? '已启用' : '已禁用'}
									</Badge>
								</div>
							</div>
						</div>
					</CardContent>
				</Card>
			{/each}
		</div>
	{/if}
</div>