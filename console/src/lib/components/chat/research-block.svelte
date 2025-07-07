<script lang="ts">
	import { chatStore } from '$lib/stores/chat.svelte';
	import { Button } from '$lib/components/ui/button';
	import { Card } from '$lib/components/ui/card';
	import { Tabs, TabsContent, TabsList, TabsTrigger } from '$lib/components/ui/tabs';
	import { X, FileText, Copy, Check, RotateCcw } from '@lucide/svelte';
	import { cn } from '$lib/utils';
	import MessageItem from './message-item.svelte';

	// Props
	interface Props {
		class?: string;
		researchId: string | null;
	}

	let { class: className, researchId }: Props = $props();

	// 当前选中的tab
	let activeTab = $state('activities');
	let copied = $state(false);
	
	// 计算属性
	const hasReport = $derived(chatStore.hasResearchReport(researchId || ''));
	const reportStreaming = $derived.by(() => {
		if (!researchId) return false;
		const reportId = chatStore.getResearchReportId(researchId);
		if (!reportId) return false;
		const reportMessage = chatStore.getMessage(reportId);
		return reportMessage?.isStreaming ?? false;
	});
	
	// 当有报告时自动切换到 report tab
	$effect(() => {
		if (hasReport) {
			activeTab = 'report';
		}
	});
	
	// 当 researchId 变化时，如果没有报告则切换到 activities tab
	$effect(() => {
		if (!hasReport) {
			activeTab = 'activities';
		}
	});

	// 响应式状态
	const activityIds = $derived.by(() => {
		if (!researchId) return [];
		return chatStore.getResearchActivityIds(researchId);
	});
	
	const researchMessages = $derived.by(() => {
		if (!researchId || activityIds.length === 0) return [];
		return activityIds.map(id => chatStore.getMessage(id)).filter(Boolean);
	});

	// 分离research和report消息
	const researchOnlyMessages = $derived(
		researchMessages.filter(msg => msg && msg.agent === 'researcher')
	);
	
	const reportMessages = $derived(
		researchMessages.filter(msg => msg && msg.agent === 'reporter')
	);
	
	const ongoing = $derived(chatStore.getOngoingResearchId() === researchId);

	// 研究状态
	const researchState = $derived.by(() => {
		if (!researchId) {
			return { status: 'idle', title: 'No Research Selected' };
		}

		const reportMessage = reportMessages[0];
		const hasReport = chatStore.hasResearchReport(researchId);

		// 获取标题
		let title = 'Deep Research';
		// 优先从计划消息获取标题
		const planId = chatStore.getResearchPlanId(researchId);
		if (planId) {
			const planMessage = chatStore.getMessage(planId);
			if (planMessage?.content) {
				try {
					const parsed = JSON.parse(planMessage.content);
					if (parsed.title) {
						title = parsed.title;
					}
				} catch {
					// 忽略JSON解析错误
				}
			}
		}
		
		// 如果没有从计划获取到标题，尝试从研究消息获取
		if (title === 'Deep Research') {
			const researchMessage = researchOnlyMessages[0];
			if (researchMessage?.content) {
				try {
					// 优先从 **Problem Statement**: 后提取标题
					const problemMatch = researchMessage.content.match(/\*\*Problem Statement\*\*:\s*(.+?)(?:\n|$)/);
					if (problemMatch) {
						title = problemMatch[1].trim();
					} else {
						// 向下兼容：尝试解析JSON格式
						try {
							const parsed = JSON.parse(researchMessage.content);
							title = parsed.title || title;
						} catch {
							// 忽略JSON解析错误
						}
					}
				} catch {
					// 忽略解析错误
				}
			}
		}

		if (hasReport && reportMessage) {
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
	<Card class="relative h-full w-full pt-4">
		<!-- 头部操作按钮 -->
		<div class="absolute right-4 flex h-9 items-center justify-center">
			<Button
				variant="ghost"
				size="sm"
				class="text-gray-400"
				onclick={handleClose}
			>
				<X class="h-4 w-4" />
			</Button>
		</div>

		<!-- 内容区域 -->
		<Tabs class="flex h-full w-full flex-col" bind:value={activeTab}>
			<div class="flex w-full justify-center">
				<TabsList>
					<TabsTrigger value="report" class="px-8" disabled={!hasReport}>
						Report
					</TabsTrigger>
					<TabsTrigger value="activities" class="px-8">
						Activities
					</TabsTrigger>
				</TabsList>
			</div>

			<TabsContent value="report" class="h-full min-h-0 flex-grow px-8">
				<div class="h-full overflow-y-auto px-5 pb-20 custom-scrollbar">
					{#if reportMessages.length > 0}
						{#each reportMessages as message (message?.id)}
							<div class="w-full pt-4 pb-8">
								<MessageItem
									message={message!}
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
					{:else}
						<div class="flex h-full items-center justify-center text-gray-500">
							<div class="text-center">
								<div class="text-lg font-medium">No report available</div>
								<div class="text-sm">Report will be generated after research completion</div>
							</div>
						</div>
					{/if}
				</div>
			</TabsContent>

			<TabsContent value="activities" class="h-full min-h-0 flex-grow px-8">
				<div class="h-full overflow-y-auto custom-scrollbar">
					{#if researchOnlyMessages.length > 0}
						<div class="mt-4">
							{#each researchOnlyMessages as message (message?.id)}
								<MessageItem
									message={message!}
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
							{/each}
						</div>
					{:else}
						<div class="flex h-full items-center justify-center text-gray-500">
							<div class="text-center">
								<div class="text-lg font-medium">No research activities</div>
								<div class="text-sm">Research activities will appear here</div>
							</div>
						</div>
					{/if}
				</div>
			</TabsContent>
		</Tabs>
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