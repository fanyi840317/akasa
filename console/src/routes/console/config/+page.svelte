<script lang="ts">
	import { onMount } from 'svelte';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Separator } from '$lib/components/ui/separator';
	import { toast } from 'svelte-sonner';
	import { Settings, Save, RotateCcw, CheckCircle, AlertCircle } from '@lucide/svelte';
	import ConfigSection from './config-section.svelte';
	import { configStore } from '$lib/stores/config.svelte';

	// 响应式状态
	let loading = $state(false);
	let saving = $state(false);
	let validating = $state(false);

	// 配置数据
	let config = $state({
		system: {},
		components: {},
		llm: {}
	});

	// 验证结果
	let validationResults = $state<Array<{ section: string; valid: boolean; message: string }>>([]);
	let isValid = $state<boolean>(true);

	// 加载配置
	const loadConfig = async () => {
		loading = true;
		try {
			const result = await configStore.loadConfig();
			if (result.success) {
				config = result.data as { system: Record<string, unknown>; components: Record<string, unknown>; llm: Record<string, unknown> } ?? { system: {}, components: {}, llm: {} };
			} else {
				toast.error('加载配置失败', {
					description: result.error
				});
			}
		} catch (error) {
			toast.error('加载配置失败', {
				description: error instanceof Error ? error.message : String(error)
			});
		} finally {
			loading = false;
		}
	};

	// 保存配置
	const saveConfig = async () => {
		saving = true;
		try {
			const result = await configStore.updateConfig(config);
			if (result.success) {
				toast.success('配置保存成功');
				// 重新加载配置
				await loadConfig();
			} else {
				toast.error('保存配置失败', {
					description: result.error
				});
			}
		} catch (error) {
			toast.error('保存配置失败', {
				description: error instanceof Error ? error.message : String(error)
			});
		} finally {
			saving = false;
		}
	};

	// 重置配置
	const resetConfig = async () => {
		if (!confirm('确定要重置配置到默认值吗？此操作不可撤销。')) {
			return;
		}

		loading = true;
		try {
			const result = await configStore.resetConfig();
			if (result.success) {
				toast.success('配置已重置为默认值');
				// 重新加载配置
				await loadConfig();
			} else {
				toast.error('重置配置失败', {
					description: result.error
				});
			}
		} catch (error) {
			toast.error('重置配置失败', {
				description: error instanceof Error ? error.message : String(error)
			});
		} finally {
			loading = false;
		}
	};

	// 验证配置
	const validateConfig = async () => {
		validating = true;
		try {
			const result = await configStore.validateConfig(config);
			if (result.success) {
				validationResults = result.results || [];
				isValid = result.valid ?? true;
				if (isValid) {
					toast.success('配置验证通过');
				} else {
					toast.error('配置验证失败');
				}
			} else {
				toast.error('验证配置失败', {
					description: result.error
				});
			}
		} catch (error) {
			toast.error('验证配置失败', {
				description: error instanceof Error ? error.message : String(error)
			});
		} finally {
			validating = false;
		}
	};

	// 组件挂载时加载配置
	onMount(() => {
		loadConfig();
	});
</script>

<div class="container mx-auto p-6 space-y-6">
	<!-- 页面标题 -->
	<div class="flex items-center justify-between">
		<div class="flex items-center space-x-2">
			<Settings class="h-6 w-6" />
			<h1 class="text-2xl font-bold">系统配置</h1>
		</div>
		<div class="flex items-center space-x-2">
			<Button
				variant="outline"
				size="sm"
				onclick={validateConfig}
				disabled={validating || loading}
			>
				{#if validating}
					<div class="animate-spin h-4 w-4 border-2 border-current border-t-transparent rounded-full mr-2"></div>
				{:else}
					<CheckCircle class="h-4 w-4 mr-2" />
				{/if}
				验证配置
			</Button>
			<Button
				variant="outline"
				size="sm"
				onclick={resetConfig}
				disabled={loading || saving}
			>
				<RotateCcw class="h-4 w-4 mr-2" />
				重置
			</Button>
			<Button
				size="sm"
				onclick={saveConfig}
				disabled={loading || saving}
			>
				{#if saving}
					<div class="animate-spin h-4 w-4 border-2 border-current border-t-transparent rounded-full mr-2"></div>
				{:else}
					<Save class="h-4 w-4 mr-2" />
				{/if}
				保存配置
			</Button>
		</div>
	</div>

	<!-- 验证结果 -->
	{#if validationResults.length > 0}
		<Card class={isValid ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}>
			<CardHeader>
				<CardTitle class="flex items-center space-x-2">
					{#if isValid}
						<CheckCircle class="h-5 w-5 text-green-600" />
						<span class="text-green-800">配置验证通过</span>
					{:else}
						<AlertCircle class="h-5 w-5 text-red-600" />
						<span class="text-red-800">配置验证失败</span>
					{/if}
				</CardTitle>
			</CardHeader>
			<CardContent>
				<div class="space-y-2">
					{#each validationResults as result, index (index)}
					<div class="flex items-center space-x-2">
							{#if result.valid}
								<CheckCircle class="h-4 w-4 text-green-600" />
							{:else}
								<AlertCircle class="h-4 w-4 text-red-600" />
							{/if}
							<span class="font-medium">{result.section}:</span>
							<span class={result.valid ? 'text-green-700' : 'text-red-700'}>
								{result.message}
							</span>
						</div>
					{/each}
				</div>
			</CardContent>
		</Card>
	{/if}

	{#if loading}
		<div class="flex items-center justify-center py-12">
			<div class="animate-spin h-8 w-8 border-4 border-current border-t-transparent rounded-full"></div>
			<span class="ml-2">加载配置中...</span>
		</div>
	{:else}
		<!-- 配置表单 -->
		<div class="grid gap-6">
			<!-- 系统配置 -->
			<ConfigSection
				title="系统配置"
				description="基础系统设置和环境配置"
				bind:data={config.system}
				fields={[
					{ key: 'name', label: '系统名称', type: 'text', placeholder: '输入系统名称' },
					{ key: 'version', label: '版本', type: 'text', placeholder: '输入版本号' },
					{ key: 'description', label: '描述', type: 'text', placeholder: '输入系统描述' },
					{ key: 'locale', label: '语言', type: 'text', placeholder: 'zh-CN' },
					{ key: 'timezone', label: '时区', type: 'text', placeholder: 'Asia/Shanghai' },
					{ key: 'debug', label: '调试模式', type: 'checkbox' },
					{ key: 'verbose', label: '详细日志', type: 'checkbox' },
					{ key: 'environment', label: '环境', type: 'text', placeholder: 'development' }
				]}
			/>

			<Separator />

			<!-- AI 配置 -->
			<ConfigSection
				title="AI 模型配置"
				description="配置各种 AI 模型的 API 密钥和参数"
				bind:data={config.llm}
				fields={[
					{ key: 'openai.api_key', label: 'OpenAI API Key', type: 'password', placeholder: '输入 OpenAI API Key' },
					{ key: 'openai.base_url', label: 'OpenAI Base URL', type: 'text', placeholder: 'https://api.openai.com/v1' },
					{ key: 'openai.organization', label: 'OpenAI Organization', type: 'text', placeholder: '输入组织 ID' },
					{ key: 'anthropic.api_key', label: 'Anthropic API Key', type: 'password', placeholder: '输入 Anthropic API Key' },
					{ key: 'anthropic.base_url', label: 'Anthropic Base URL', type: 'text', placeholder: 'https://api.anthropic.com' },
					{ key: 'google.api_key', label: 'Google API Key', type: 'password', placeholder: '输入 Google API Key' },
					{ key: 'qwen.api_key', label: 'Qwen API Key', type: 'password', placeholder: '输入 Qwen API Key' },
					{ key: 'qwen.base_url', label: 'Qwen Base URL', type: 'text', placeholder: 'https://dashscope.aliyuncs.com/compatible-mode/v1' },
					{ key: 'ollama.base_url', label: 'Ollama Base URL', type: 'text', placeholder: 'http://localhost:11434' }
				]}
			/>

			<Separator />

			<!-- 组件配置 -->
			<ConfigSection
				title="组件配置"
				description="配置系统各个组件的参数"
				bind:data={config.components}
				fields={[
					{ key: 'search.enabled', label: '启用搜索', type: 'checkbox' },
					{ key: 'search.engine', label: '搜索引擎', type: 'text', placeholder: 'duckduckgo' },
					{ key: 'crawler.enabled', label: '启用爬虫', type: 'checkbox' },
					{ key: 'crawler.max_pages', label: '最大页面数', type: 'number', placeholder: '10' },
					{ key: 'database.enabled', label: '启用数据库', type: 'checkbox' },
					{ key: 'cache.enabled', label: '启用缓存', type: 'checkbox' },
					{ key: 'cache.ttl', label: '缓存过期时间(秒)', type: 'number', placeholder: '3600' }
				]}
			/>

			<Separator />

			<!-- 工具管理快速访问 -->
			<Card class="border-blue-200 bg-blue-50">
				<CardHeader>
					<CardTitle class="flex items-center space-x-2">
						<Settings class="h-5 w-5 text-blue-600" />
						<span class="text-blue-800">工具管理</span>
					</CardTitle>
					<CardDescription class="text-blue-700">
						管理系统中可用的工具，启用或禁用特定功能
					</CardDescription>
				</CardHeader>
				<CardContent>
					<div class="flex items-center justify-between">
						<p class="text-sm text-blue-600">
							配置和管理系统工具，包括搜索引擎、网络爬虫等功能模块
						</p>
						<Button 
							variant="outline" 
							size="sm"
							class="border-blue-300 text-blue-700 hover:bg-blue-100"
							onclick={() => window.location.href = '/console/config/tools'}
						>
							<Settings class="h-4 w-4 mr-2" />
							管理工具
						</Button>
					</div>
				</CardContent>
			</Card>

			<!-- API测试快速访问 -->
			<Card class="border-green-200 bg-green-50">
				<CardHeader>
					<CardTitle class="flex items-center space-x-2">
						<CheckCircle class="h-5 w-5 text-green-600" />
						<span class="text-green-800">API测试</span>
					</CardTitle>
					<CardDescription class="text-green-700">
						测试和验证搜索API接口的连通性和功能
					</CardDescription>
				</CardHeader>
				<CardContent>
					<div class="flex items-center justify-between">
						<p class="text-sm text-green-600">
							配置API端点，测试各种搜索功能，验证系统集成状态
						</p>
						<Button 
							variant="outline" 
							size="sm"
							class="border-green-300 text-green-700 hover:bg-green-100"
							onclick={() => window.location.href = '/console/config/api-test'}
						>
							<CheckCircle class="h-4 w-4 mr-2" />
							API测试
						</Button>
					</div>
				</CardContent>
			</Card>
		</div>
	{/if}
</div>