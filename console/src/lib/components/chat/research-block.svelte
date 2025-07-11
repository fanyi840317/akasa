<script lang="ts">
	import { chatStore } from '$lib/stores/chat.svelte';
	import { Button } from '$lib/components/ui/button';
	import { Card } from '$lib/components/ui/card';
	import { Tabs, TabsContent, TabsList, TabsTrigger } from '$lib/components/ui/tabs';
	import { X, FileText, Copy, Check, RotateCcw } from '@lucide/svelte';
	import { cn } from '$lib/utils';
	import ResearchActivitiesBlock from './research-activities-block.svelte';
	import ResearchReportBlock from './research-report-block.svelte';
	import { ScrollArea } from '$lib/components/ui/scroll-area';

	// Props
	interface Props {
		class?: string;
		researchId: string | null;
	}

	let { class: className, researchId }: Props = $props();

	let copied = $state(false);

	// 计算属性
	const hasReport = $derived(chatStore.hasResearchReport(researchId || ''));
	// 当前选中的tab
	let activeTab = $derived(hasReport ? 'report' : 'activities');

	const reportStreaming = $derived.by(() => {
		if (!researchId) return false;
		const reportId = chatStore.getResearchReportId(researchId);
		if (!reportId) return false;
		const reportMessage = chatStore.getMessage(reportId);
		return reportMessage?.isStreaming ?? false;
	});

	// 响应式状态
	const activityIds = $derived.by(() => {
		if (!researchId) return [];
		return chatStore.getResearchActivityIds(researchId);
	});

	const researchMessages = $derived.by(() => {
		if (!researchId || activityIds.length === 0) return [];
		return activityIds.map((id) => chatStore.getMessage(id)).filter(Boolean);
	});

	// 获取报告消息
	const reportMessages = $derived(
		researchMessages.filter((msg) => msg && msg.agent === 'reporter')
	);

	// 关闭研究报告
	function handleClose() {
		chatStore.openResearchId = null;
	}

	function handleCopyReport() {
		if (!researchId) return;
		const reportId = chatStore.getResearchReportId(researchId);
		if (!reportId) return;
		const reportMessage = chatStore.getMessage(reportId);
		if (!reportMessage) return;

		navigator.clipboard.writeText(reportMessage.content);
		copied = true;
		setTimeout(() => {
			copied = false;
		}, 1000);
	}

	function handleRegenerateReport() {
		if (!researchId) return;
		const reportId = chatStore.getResearchReportId(researchId);
		if (reportId) {
			chatStore.regenerateMessage(reportId);
		}
	}
</script>

{#if researchId}
	<Card class="bg-base-200 relative h-full w-full rounded-2xl px-0 pt-2">
		<!-- 头部操作按钮 -->
		<div class="absolute right-4 flex h-9 items-center justify-center">
			<Button variant="ghost" size="sm" class="text-gray-400" onclick={handleClose}>
				<X class="h-4 w-4" />
			</Button>
		</div>

		<!-- 内容区域 -->
		<Tabs class="flex h-full w-full flex-col" bind:value={activeTab}>
			<div class="flex w-full justify-center">
				<TabsList>
					<TabsTrigger value="report" class="px-8" disabled={!hasReport}>Report</TabsTrigger>
					<TabsTrigger value="activities" class="px-8">Activities</TabsTrigger>
				</TabsList>
			</div>

			<TabsContent value="report" class="h-full min-h-0 flex-grow ">
				<ScrollArea class="h-full overflow-y-auto px-4 pb-20">
					{#if reportMessages.length > 0}
						{#each reportMessages as message (message?.id)}
							<ResearchReportBlock
								researchId={researchId!}
								messageId={message!.id}
								editing={false}
							/>
						{/each}
					{:else}
						<div class="flex h-full items-center justify-center text-gray-500">
							<div class="text-center">
								<div class="text-lg font-medium">No report available</div>
								<div class="text-sm">Report will be generated after research completion</div>
							</div>
						</div>
					{/if}
				</ScrollArea>
			</TabsContent>

			<TabsContent value="activities" class="h-full min-h-0 flex-grow">
				<ScrollArea class="h-full overflow-y-auto px-4">
					{#if researchId}
						<ResearchActivitiesBlock {researchId} />
					{:else}
						<div class="flex h-full items-center justify-center text-gray-500">
							<div class="text-center">
								<div class="text-lg font-medium">No research activities</div>
								<div class="text-sm">Research activities will appear here</div>
							</div>
						</div>
					{/if}
				</ScrollArea>
			</TabsContent>
		</Tabs>
	</Card>
{:else}
	<!-- 空状态 -->
	<div class={cn('flex h-full items-center justify-center', className)}>
		<div class="text-muted-foreground text-center">
			<FileText class="mx-auto mb-4 h-12 w-12 opacity-50" />
			<p class="mb-2 text-lg font-medium">No Research Selected</p>
			<p class="text-sm">Click on a research card to view the report</p>
		</div>
	</div>
{/if}
