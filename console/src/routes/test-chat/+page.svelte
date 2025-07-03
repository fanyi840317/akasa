<script lang="ts">
	import { chatStore } from '$lib/stores/chat.svelte';
	import { cn } from '$lib/utils';
	import MessagesBlock from '$lib/components/chat/messages-block.svelte';
	import ResearchBlock from '$lib/components/chat/research-block.svelte';
	import { onMount } from 'svelte';
	import { Button } from '$lib/components/ui/button';

	const threadId = 'test-thread-123';
	const openResearchId = $derived(chatStore.openResearchId);
	const doubleColumnMode = $derived(openResearchId !== null);

	// 初始化聊天
	onMount(() => {
		chatStore.initializeChat(threadId);
		
		// 添加一些测试数据
		if (chatStore.getMessages().length === 0) {
			chatStore.addMessage({
				threadId,
				role: 'user',
				content: 'Hello, can you help me research about AI development?',
				contentChunks: ['Hello, can you help me research about AI development?']
			});
			
			chatStore.addMessage({
				threadId,
				role: 'assistant',
				content: 'I\'d be happy to help you research AI development. Let me start by gathering some information.',
				contentChunks: ['I\'d be happy to help you research AI development. Let me start by gathering some information.'],
				agent: 'coordinator'
			});
			
			// 添加研究消息
			const researchMessage = chatStore.addMessage({
				threadId,
				role: 'assistant',
				content: JSON.stringify({ title: 'AI Development Research', status: 'researching' }),
				contentChunks: [JSON.stringify({ title: 'AI Development Research', status: 'researching' })],
				agent: 'researcher'
			});
			
			// 添加报告消息
			chatStore.addMessage({
				threadId,
				role: 'assistant',
				content: `# AI Development Research Report\n\nThis is a comprehensive research report about AI development trends and best practices.\n\n## Key Findings\n\n1. **Machine Learning Frameworks**: TensorFlow and PyTorch remain the dominant frameworks\n2. **Large Language Models**: GPT-4, Claude, and other LLMs are revolutionizing AI applications\n3. **Edge AI**: Growing trend towards deploying AI models on edge devices\n\n## Recommendations\n\n- Focus on understanding transformer architectures\n- Learn both supervised and unsupervised learning techniques\n- Stay updated with the latest research papers and implementations`,
				contentChunks: [`# AI Development Research Report\n\nThis is a comprehensive research report about AI development trends and best practices.\n\n## Key Findings\n\n1. **Machine Learning Frameworks**: TensorFlow and PyTorch remain the dominant frameworks\n2. **Large Language Models**: GPT-4, Claude, and other LLMs are revolutionizing AI applications\n3. **Edge AI**: Growing trend towards deploying AI models on edge devices\n\n## Recommendations\n\n- Focus on understanding transformer architectures\n- Learn both supervised and unsupervised learning techniques\n- Stay updated with the latest research papers and implementations`],
				agent: 'reporter'
			});
		}
	});

	// 测试函数：切换研究报告
	function toggleResearch() {
		const researchMessage = chatStore.getMessages().find(m => m.agent === 'researcher');
		if (researchMessage) {
			if (chatStore.openResearchId === researchMessage.id) {
				chatStore.openResearchId = null;
			} else {
				chatStore.openResearchId = researchMessage.id;
			}
		}
	}
</script>

<svelte:head>
	<title>Chat Layout Test</title>
</svelte:head>

<div class="h-screen flex flex-col">
	<!-- 测试控制栏 -->
	<div class="bg-background border-b p-4">
		<div class="flex items-center justify-between">
			<h1 class="text-xl font-semibold">Chat Layout Test</h1>
			<div class="flex items-center gap-4">
				<span class="text-sm text-muted-foreground">
					Mode: {doubleColumnMode ? 'Double Column' : 'Single Column'}
				</span>
				<Button onclick={toggleResearch} variant="outline" size="sm">
					{doubleColumnMode ? 'Close Research' : 'Open Research'}
				</Button>
			</div>
		</div>
	</div>

	<!-- 主要内容区域 -->
	<div class="flex-1 overflow-hidden">
		<div
			class={cn(
				'flex h-full w-full transition-all duration-300 ease-out',
				!doubleColumnMode && 'justify-center',
				doubleColumnMode && 'justify-center gap-8 px-4'
			)}
		>
			<MessagesBlock
				class={cn(
					'shrink-0 transition-all duration-300 ease-out',
					!doubleColumnMode && 'w-full h-full',
					doubleColumnMode && 'w-[538px] h-full'
				)}
				{threadId}
				autoFocus={false}
			/>
			{#if doubleColumnMode}
				<ResearchBlock
					class="w-[min(max(calc((100vw-538px)*0.75),575px),960px)] h-full transition-all duration-300 ease-out"
					researchId={openResearchId}
				/>
			{/if}
		</div>
	</div>
</div>