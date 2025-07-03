<script lang="ts">
	import { chatStore } from '$lib/stores/chat.svelte';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import { Badge } from '$lib/components/ui/badge';
	import { X, FileText, Clock, CheckCircle } from '@lucide/svelte';
	import { cn } from '$lib/utils';
	import RainbowText from '$lib/components/ui/rainbow-text.svelte';
	import RollingText from '$lib/components/ui/rolling-text.svelte';
	import MessageItem from './message-item.svelte';

	// Props
	interface Props {
		class?: string;
		researchId: string | null;
	}

	let { class: className, researchId }: Props = $props();

	// 响应式状态
	const researchMessages = $derived.by(() => {
		if (!researchId) return [];
		
		const messages = chatStore.getMessages();
		return messages.filter(msg => {
			// 包含研究相关的消息
			return (
				msg.id === researchId ||
				(msg.agent === 'researcher' && msg.content?.includes(researchId)) ||
				(msg.agent === 'reporter' && msg.content?.includes(researchId)) ||
				(msg.agent === 'coder' && msg.content?.includes(researchId))
			);
		});
	});

	// 研究状态
	const researchState = $derived.by(() => {
		if (!researchId || researchMessages.length === 0) {
			return { status: 'idle', title: 'No Research Selected' };
		}

		const reportMessage = researchMessages.find(msg => msg.agent === 'reporter');
		const researchMessage = researchMessages.find(msg => msg.agent === 'researcher');

		let title = 'Deep Research';
		try {
			if (researchMessage?.content) {
				const parsed = JSON.parse(researchMessage.content);
				title = parsed.title || title;
			}
		} catch {
			// 忽略解析错误
		}

		if (reportMessage) {
			if (reportMessage.isStreaming) {
				return { status: 'generating', title };
			} else {
				return { status: 'completed', title };
			}
		}

		return { status: 'researching', title };
	});

	// 关闭研究报告
	function handleClose() {
		chatStore.openResearchId = null;
	}

	// 处理消息操作（简化版，研究报告中不需要完整的消息操作）
	function handleCopy(messageId: string) {
		console.log('Research message copied:', messageId);
	}

	function handleRegenerate(messageId: string) {
		console.log('Research message regenerate:', messageId);
	}

	function handleLike(messageId: string) {
		console.log('Research message liked:', messageId);
	}

	function handleDislike(messageId: string) {
		console.log('Research message disliked:', messageId);
	}

	function handleOptionClick(option: { text: string; value: string }) {
		console.log('Research option clicked:', option);
	}

	function handleSendMessage(message: string) {
		console.log('Research send message:', message);
	}

	function handleToggleResearch() {
		console.log('Toggle research from research block');
	}
</script>

{#if researchId}
	<Card class={cn('h-full flex flex-col bg-base-200 rounded-2xl', className)}>
		<!-- 头部 -->
		<CardHeader class="flex-row items-center justify-between space-y-0 pb-4">
			<div class="flex items-center gap-3">
				<FileText class="h-5 w-5 text-primary" />
				<div>
					<CardTitle class="text-lg">
						<RainbowText animated={researchState.status !== 'completed'}>
							{#snippet children()}
								{researchState.title}
							{/snippet}
						</RainbowText>
					</CardTitle>
					<div class="flex items-center gap-2 mt-1">
						{#if researchState.status === 'researching'}
							<Badge variant="secondary" class="text-xs">
								<Clock class="h-3 w-3 mr-1" />
								Researching
							</Badge>
						{:else if researchState.status === 'generating'}
							<Badge variant="secondary" class="text-xs">
								<Clock class="h-3 w-3 mr-1 animate-spin" />
								<RollingText>
									{#snippet children()}
										Generating Report
									{/snippet}
								</RollingText>
							</Badge>
						{:else if researchState.status === 'completed'}
							<Badge variant="default" class="text-xs">
								<CheckCircle class="h-3 w-3 mr-1" />
								Completed
							</Badge>
						{/if}
						<span class="text-muted-foreground text-xs">#{researchId.slice(0, 8)}</span>
					</div>
				</div>
			</div>
			<Button variant="ghost" size="sm" onclick={handleClose} title="Close research report">
				<X class="h-4 w-4" />
			</Button>
		</CardHeader>

		<!-- 内容区域 -->
		<CardContent class="flex-1 overflow-hidden p-0">
			<ScrollArea class="h-full">
				<div class="space-y-4 p-6">
					{#if researchMessages.length === 0}
						<div class="flex flex-col items-center justify-center h-32 text-center">
							<FileText class="h-8 w-8 text-muted-foreground mb-2" />
							<p class="text-muted-foreground">No research data available</p>
						</div>
					{:else}
						<!-- 研究消息列表 -->
						{#each researchMessages as message (message.id)}
							<div class="border-l-2 border-primary/20 pl-4">
								<MessageItem
									{message}
									waitForFeedback={false}
									interruptMessage={null}
									onCopy={handleCopy}
									onRegenerate={handleRegenerate}
									onLike={handleLike}
									onDislike={handleDislike}
									onOptionClick={handleOptionClick}
									onSendMessage={handleSendMessage}
									onToggleResearch={handleToggleResearch}
								/>
							</div>
						{/each}
					{/if}
				</div>
			</ScrollArea>
		</CardContent>
	</Card>
{:else}
	<!-- 空状态 -->
	<div class={cn('h-full flex items-center justify-center', className)}>
		<div class="text-center text-muted-foreground">
			<FileText class="h-12 w-12 mx-auto mb-4 opacity-50" />
			<p class="text-lg font-medium mb-2">No Research Selected</p>
			<p class="text-sm">Click on a research card to view the report</p>
		</div>
	</div>
{/if}

<style>
	@reference "../../../app.css";

	/* 自定义滚动条样式 */
	:global(.scroll-area-viewport) {
		scrollbar-width: thin;
		scrollbar-color: hsl(var(--muted-foreground) / 0.2) transparent;
	}

	:global(.scroll-area-viewport:hover) {
		scrollbar-color: hsl(var(--muted-foreground) / 0.4) transparent;
	}

	/* WebKit 浏览器滚动条样式 */
	:global(.scroll-area-viewport::-webkit-scrollbar) {
		width: 6px;
	}

	:global(.scroll-area-viewport::-webkit-scrollbar-track) {
		background: transparent;
	}

	:global(.scroll-area-viewport::-webkit-scrollbar-thumb) {
		background-color: hsl(var(--muted-foreground) / 0.2);
		border-radius: 3px;
	}

	:global(.scroll-area-viewport:hover::-webkit-scrollbar-thumb) {
		background-color: hsl(var(--muted-foreground) / 0.4);
	}
</style>