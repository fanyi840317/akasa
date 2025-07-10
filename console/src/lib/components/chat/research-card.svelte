<script lang="ts">
	import { cn } from '$lib/utils';
import { Button } from '$lib/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '$lib/components/ui/card';
import RainbowText from '$lib/components/ui/rainbow-text.svelte';
import RollingText from '$lib/components/ui/rolling-text.svelte';
import { chatStore } from '$lib/stores/chat.svelte';
import { parseJSON } from '$lib/tools';

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
	const state = $derived.by(() => {
		if (hasReport) {
			return reportGenerating ? 'Generating report...' : 'Report generated';
		}
		return 'Researching...';
	});

	// 研究标题
	const title = $derived.by(() => {
		// 优先从计划消息获取标题
		const planId = chatStore.getResearchPlanId(researchId);
		if (planId) {
			const planMessage = chatStore.getMessage(planId);
			if (planMessage?.content) {
				const parsed = parseJSON(planMessage.content, { title: '' });
				if (parsed.title) {
					return parsed.title;
				}
			}
		}
		
		// 从研究消息获取标题
		const researchMessage = chatStore.getMessage(researchId);
		if (researchMessage?.content) {
			// 优先从 **Problem Statement**: 后提取标题
			const problemMatch = researchMessage.content.match(/\*\*Problem Statement\*\*:\s*(.+?)(?:\n|$)/);
			if (problemMatch) {
				return problemMatch[1].trim();
			}
			// 向下兼容：尝试解析JSON格式
			const parsed = parseJSON(researchMessage.content, { title: '' });
			if (parsed.title) {
				return parsed.title;
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

<Card class={cn('w-full rounded-2xl', className)}>
	<CardHeader>
		<CardTitle>
			<RainbowText animated={state !== 'Report generated'}>
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