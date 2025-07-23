<script lang="ts">
	import { Label } from '$lib/components/ui/label';
	import { Input } from '$lib/components/ui/input';
	import { Switch } from '$lib/components/ui/switch';
	import { Button } from '$lib/components/ui/button';
	import { toast } from 'svelte-sonner';
	import { Save, Loader2 } from '@lucide/svelte';

	// 通用设置状态
	let allowAutoAcceptance = $state(false);
	let maxPlanIterations = $state(1);
	let maxStepsOfResearchPlan = $state(5);
	let maxSearchResults = $state(5);
	let isSaving = $state(false);

	// 保存配置函数
	const saveSettings = async () => {
		// 验证输入
		if (maxPlanIterations < 1) {
			toast.error('计划迭代次数必须大于0');
			return;
		}
		if (maxStepsOfResearchPlan < 1) {
			toast.error('研究计划步骤数必须大于0');
			return;
		}
		if (maxSearchResults < 1) {
			toast.error('搜索结果数必须大于0');
			return;
		}

		isSaving = true;
		try {
			// 这里可以添加实际的保存逻辑，比如调用API
			// 模拟保存延迟
			await new Promise(resolve => setTimeout(resolve, 1000));
			
			toast.success('通用设置保存成功');
		} catch (error) {
			toast.error('保存设置失败', {
				description: error instanceof Error ? error.message : String(error)
			});
		} finally {
			isSaving = false;
		}
	};
</script>

<div class="space-y-6 flex-center">
	<div class="w-full max-w-[776px] mx-auto space-y-6 p-6">
		<!-- 页面标题 -->
		<div class="flex items-center justify-between mb-4">
			<h1 class="text-xl font-semibold">通用设置</h1>
		</div>

		<!-- 设置项列表 -->
		<div class="space-y-3">
			<!-- Allow automatic acceptance of plans -->
			<div class="flex items-center justify-between py-3 border-b border-border">
				<div class="space-y-0.5">
					<h3 class="text-sm font-medium">自动接受计划</h3>
					<p class="text-xs text-muted-foreground">允许系统自动接受生成的计划</p>
				</div>
				<Switch bind:checked={allowAutoAcceptance} />
			</div>

			<!-- Max plan iterations -->
			<div class="flex items-center justify-between py-3 border-b border-border">
				<div class="space-y-0.5">
					<h3 class="text-sm font-medium">最大计划迭代次数</h3>
					<p class="text-xs text-muted-foreground">设置为1进行单步规划，设置为2或更多启用重新规划</p>
				</div>
				<div class="w-20">
					<Input
						id="maxPlanIterations"
						type="number"
						bind:value={maxPlanIterations}
						min="1"
						class="text-center"
					/>
				</div>
			</div>

			<!-- Max steps of a research plan -->
			<div class="flex items-center justify-between py-3 border-b border-border">
				<div class="space-y-0.5">
					<h3 class="text-sm font-medium">研究计划最大步骤数</h3>
					<p class="text-xs text-muted-foreground">默认情况下，每个研究计划有5个步骤</p>
				</div>
				<div class="w-20">
					<Input
						id="maxStepsOfResearchPlan"
						type="number"
						bind:value={maxStepsOfResearchPlan}
						min="1"
						class="text-center"
					/>
				</div>
			</div>

			<!-- Max search results -->
			<div class="flex items-center justify-between py-3 border-b border-border">
				<div class="space-y-0.5">
					<h3 class="text-sm font-medium">最大搜索结果数</h3>
					<p class="text-xs text-muted-foreground">默认情况下，每个搜索步骤有5个结果</p>
				</div>
				<div class="w-20">
					<Input
						id="maxSearchResults"
						type="number"
						bind:value={maxSearchResults}
						min="1"
						class="text-center"
					/>
				</div>
			</div>

			<!-- 保存按钮 -->
			<div class="flex justify-end pt-3">
				<Button
					onclick={saveSettings}
					disabled={isSaving}
					class="min-w-[120px]"
				>
					{#if isSaving}
						<Loader2 class="h-4 w-4 mr-2 animate-spin" />
						保存中...
					{:else}
						<Save class="h-4 w-4 mr-2" />
						保存设置
					{/if}
				</Button>
			</div>
		</div>
	</div>
</div>