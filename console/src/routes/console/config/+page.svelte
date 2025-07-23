<script lang="ts">
	import { onMount } from 'svelte';
	import { Button } from '$lib/components/ui/button';
	import {
		Card,
		CardContent,
		CardDescription,
		CardHeader,
		CardTitle
	} from '$lib/components/ui/card';
	import { Separator } from '$lib/components/ui/separator';
	import { toast } from 'svelte-sonner';
	import {
		Settings,
		Save,
		RotateCcw,
		CheckCircle,
		AlertCircle,
		Search,
		Wrench
	} from '@lucide/svelte';
	import ConfigSection from './config-section.svelte';
	import { configStore } from '$lib/stores/config.svelte';
	import PageHeader from '$lib/components/ui/page-header.svelte';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import GeneralSettings from '$lib/components/settings/general-settings.svelte';
import SearchSettings from '$lib/components/settings/search-settings.svelte';
	import ContentContainer from '$lib/components/ui/content-container.svelte';

	import * as Tabs from '$lib/components/ui/tabs/index.js';

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
				config = (result.data as {
					system: Record<string, unknown>;
					components: Record<string, unknown>;
					llm: Record<string, unknown>;
				}) ?? { system: {}, components: {}, llm: {} };
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

<div class="h-content bg-base-200 flex flex-col overflow-hidden rounded-2xl border">
	<Tabs.Root value="account" class="flex flex-col h-full">
		<PageHeader title="Settings" class="p-2 flex-shrink-0">
			{#snippet leftContent()}
				<Tabs.List class="bg-transparent">
					<Tabs.Trigger value="account">General</Tabs.Trigger>
					<Tabs.Trigger value="password">Search</Tabs.Trigger>
					<Tabs.Trigger value="mcp">MCP</Tabs.Trigger>
				</Tabs.List>
			{/snippet}
		</PageHeader>
		
		<!-- General Tab Content -->
		<Tabs.Content value="account" class="flex-1 min-h-0">
			<ContentContainer>
				{#snippet children()}
					<GeneralSettings />
				{/snippet}
			</ContentContainer>
		</Tabs.Content>
		
		<!-- Search Tab Content -->
		<Tabs.Content value="password" class="flex-1 min-h-0">
			<ScrollArea class="h-full">
				<SearchSettings />
			</ScrollArea>
		</Tabs.Content>
	</Tabs.Root>
</div>
