<script lang="ts">
	import { cn } from '$lib/utils';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '$lib/components/ui/card';
	import RainbowText from '$lib/components/ui/rainbow-text.svelte';
	import RollingText from '$lib/components/ui/rolling-text.svelte';
	import { chatStore } from '$lib/stores/chat.svelte';

	interface Props {
		class?: string;
		researchId: string;
		onToggleResearch?: () => void;
	}

	let { class: className, researchId, onToggleResearch }: Props = $props();

	// 获取研究相关状态
	const reportId = $derived(chatStore.getResearchReportId(researchId));
	const hasReport = $derived(chatStore.hasResearchReport(researchId));
	const reportGenerating = $derived.by(() => {
		if (!hasReport || !reportId) return false;
		const reportMessage = chatStore.getMessage(reportId);
		return reportMessage?.isStreaming ?? false;
	});
	const openResearchId = $derived( chatStore.openResearchId);

	// 研究状态
	const state = $derived(() => {
		if (hasReport) {
			return reportGenerating ? 'Generating report...' : 'Report generated';
		}
		return 'Researching...';
	});

	// 研究标题
	const title = $derived(() => {
		// 优先从计划消息获取标题
		const planId = chatStore.getResearchPlanId(researchId);
		if (planId) {
			const planMessage = chatStore.getMessage(planId);
			if (planMessage?.content) {
				try {
					const parsed = JSON.parse(planMessage.content);
					if (parsed.title) {
						return parsed.title;
					}
				} catch {
					// 忽略JSON解析错误
				}
			}
		}
		
		// 从研究消息获取标题
		const researchMessage = chatStore.getMessage(researchId);
		if (researchMessage?.content) {
			try {
				// 优先从 **Problem Statement**: 后提取标题
				const problemMatch = researchMessage.content.match(/\*\*Problem Statement\*\*:\s*(.+?)(?:\n|$)/);
				if (problemMatch) {
					return problemMatch[1].trim();
				}
				// 向下兼容：尝试解析JSON格式
				try {
					const parsed = JSON.parse(researchMessage.content);
					return parsed.title || 'Deep Research';
				} catch {
					// 忽略JSON解析错误
				}
			} catch {
				// 忽略解析错误
			}
		}
		return 'Deep Research';
	});

	function handleOpen() {
		if (openResearchId === researchId) {
			chatStore.openResearchId = null;
		} else {
			chatStore.openResearchId = researchId;
		}
		onToggleResearch?.();
	}
</script>

<Card class={cn('w-full', className)}>
	<CardHeader>
		<CardTitle>
			<RainbowText animated={state() !== 'Report generated'}>
				{#snippet children()}
					{title}
				{/snippet}
			</RainbowText>
		</CardTitle>
	</CardHeader>
	<CardFooter>
		<div class="flex w-full items-center">
			<RollingText class="text-muted-foreground flex-grow text-sm">
				{#snippet children()}
					{state}
				{/snippet}
			</RollingText>
			<Button
				variant={openResearchId !== researchId ? 'default' : 'outline'}
				onclick={handleOpen}
			>
				{researchId !== openResearchId ? 'Open' : 'Close'}
			</Button>
		</div>
	</CardFooter>
</Card>