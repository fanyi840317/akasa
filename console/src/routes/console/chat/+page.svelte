<script lang="ts">
	import { goto } from '$app/navigation';
	import { chatStore } from '$lib/stores/chat.svelte';
	import ChatInput from '$lib/components/chat/chat-input.svelte';
	import { Card, CardContent } from '$lib/components/ui/card';
	import { MessageSquare, Sparkles, Brain, Search } from '@lucide/svelte';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import { onMount } from 'svelte';
	import { appStore } from '$lib/stores/app-state';

	function createNewChat() {
		const threadId = crypto.randomUUID();
		chatStore.initializeChat(threadId);
		return threadId;
	}

	function handleSubmit(text: string) {
		const threadId = createNewChat();
		chatStore.setInput(text);
		chatStore.sendMessage(text);
		goto(`/console/chat/${threadId}`);
	}
	onMount(() => {
		appStore.setSidebarCollapsed(false);
	});
	// 示例提示
	const suggestions = [
		{
			icon: Brain,
			title: "Deep Analysis",
			description: "Analyze complex problems with detailed reasoning",
			prompt: "Help me analyze this complex problem step by step:"
		},
		{
			icon: Search,
			title: "Research & Investigation",
			description: "Research topics with background investigation",
			prompt: "I need you to research and investigate:"
		},
		{
			icon: Sparkles,
			title: "Creative Writing",
			description: "Generate creative content and ideas",
			prompt: "Help me create something creative:"
		},
		{
			icon: MessageSquare,
			title: "General Chat",
			description: "Have a casual conversation",
			prompt: "Let's have a conversation about:"
		}
	];

	function handleSuggestionClick(prompt: string) {
		const threadId = createNewChat();
		chatStore.setInput(prompt);
		goto(`/console/chat/${threadId}`);
	}
</script>

<ScrollArea class="flex flex-col items-center justify-center h-content p-8 border rounded-2xl bg-base-200">
	<div class="w-full space-y-8 m">
		<!-- 标题区域 -->
		<div class="text-center space-y-4 mt-20">
			<!-- <div class="w-16 h-16 mx-auto mb-6 rounded-full bg-primary/10 flex items-center justify-center">
				<MessageSquare class="w-8 h-8 text-primary" />
			</div> -->
			<h1 class="text-4xl font-bold tracking-tight">Start a New Chat</h1>
			<p class="text-xs text-muted-foreground max-w-2xl mx-auto">
				Engage with our AI assistant for deep thinking, research, creative tasks, and more.
			</p>
		</div>

		<!-- 输入区域 -->
		<div class="w-full max-w-2xl mx-auto">
			<ChatInput
				placeholder="Type your message to start a new conversation..."
				onSubmit={handleSubmit}
				autoFocus={true}
			/>
		</div>

		<!-- 建议卡片 -->
		<div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-4xl mx-auto">
			{#each suggestions as suggestion}
				<Card 
					class="cursor-pointer transition-all rounded-[16px] hover:shadow-md hover:scale-[1.02] group"
					onclick={() => handleSuggestionClick(suggestion.prompt)}
				>
					<CardContent >
						<div class="flex items-start gap-4">
							<div class="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center group-hover:bg-primary/20 transition-colors">
								<svelte:component this={suggestion.icon} class="w-5 h-5 text-primary" />
							</div>
							<div class="flex-1">
								<h3 class="font-semibold mb-1 group-hover:text-primary transition-colors">
									{suggestion.title}
								</h3>
								<p class="text-sm text-muted-foreground">
									{suggestion.description}
								</p>
							</div>
						</div>
					</CardContent>
				</Card>
			{/each}
		</div>

		<!-- 功能说明 -->
		<div class="text-center text-sm text-muted-foreground max-w-2xl mx-auto">
			<p>
				Our AI assistant supports deep thinking, background investigation, 
				and iterative planning to provide comprehensive and thoughtful responses.
			</p>
		</div>
	</div>
</ScrollArea>
