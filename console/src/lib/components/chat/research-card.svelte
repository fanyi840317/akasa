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
	const reportId = $derived.by(() => {
		// 查找与研究ID相关的报告消息
		const messages = chatStore.getMessages();
		return messages.find(msg => 
			msg.agent === 'reporter' && 
			msg.content?.includes(researchId)
		)?.id;
	});
	const hasReport = $derived(reportId !== undefined);
	const reportGenerating = $derived.by(() => {
		if (!hasReport || !reportId) return false;
		const reportMessage = chatStore.messages.get(reportId);
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
		// 查找研究消息
		const messages = chatStore.getMessages();
		const msg = messages.find(m => 
			m.id === researchId || 
			(m.agent === 'researcher' && m.content?.includes(researchId))
		);
		if (msg) {
			try {
				const parsed = JSON.parse(msg.content ?? '{}');
				return parsed.title || 'Deep Research';
			} catch {
				return 'Deep Research';
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