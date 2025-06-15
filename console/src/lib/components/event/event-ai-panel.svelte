<script lang="ts">
	import ChatContent from '$lib/components/ai/chat-content.svelte';
	import { chatStore } from '$lib/stores/chat.svelte';
	import type { Event } from '$lib/types/event';
	import { onMount } from 'svelte';

	// Props
	let {
		class: className = '',
		currentEvent,
        height,
		user,
		onTitleGenerated
	} = $props<{
		class?: string;
        height?: string;
		currentEvent?: Event;
		user?: any;
		onTitleGenerated?: (title: string) => void;
	}>();

	// 建议消息
	const suggestions = [
		'帮我总结这个事件',
		'为这个事件生成标题',
		'分析事件的关键信息',
		'提供改进建议'
	];

	// 初始化聊天
	onMount(() => {
		if (currentEvent?.$id) {
			chatStore.initializeChat('/api/chat', currentEvent.$id);
		} else {
			chatStore.initializeChat('/api/chat');
		}
	});

	// 监听事件变化，切换聊天记录
	$effect(() => {
		if (currentEvent?.id && chatStore.currentEventId !== currentEvent.id) {
			chatStore.switchToEvent(currentEvent.id, '/api/chat');
		}
	});

	// 处理消息提交
	async function handleSubmit(text: string) {
		console.log('Message submitted:', text);

		// 检查是否是生成标题的请求
		if (text.includes('生成') && text.includes('标题') && currentEvent?.content) {
			await handleTitleGeneration(text);
		} else {
			// 发送普通消息
			await chatStore.sendMessage(text);
		}
	}

	// 处理标题生成
	async function handleTitleGeneration(userMessage: string) {
		if (!currentEvent?.content) return;

		try {
			// 先发送用户消息
			await chatStore.sendMessage(userMessage);

			// 添加加载消息
			const loadingMessage = {
				id: Date.now().toString() + '_loading',
				role: 'assistant' as const,
				content: '正在为您生成标题...'
			};
			chatStore.messages = [...chatStore.messages, loadingMessage];

			// 调用API生成标题
			const response = await fetch('/api/ai/generate', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					promptType: 'generateTitle',
					markdownContent: currentEvent.content
				})
			});

			if (!response.ok) {
				throw new Error('生成标题失败');
			}

			const result = await response.json();
			const generatedTitle = result.text?.text || result.text;

			// 移除加载消息，添加标题建议消息
			chatStore.messages = chatStore.messages.filter((m: { id: string; }) => m.id !== loadingMessage.id);
			
			const titleMessage = {
				id: Date.now().toString() + '_title',
				role: 'assistant' as const,
				content: `我为您生成了以下标题建议：\n\n**${generatedTitle}**\n\n您是否要采用这个标题？`,
				data: {
					type: 'title-suggestion',
					title: generatedTitle
				}
			};
			chatStore.messages = [...chatStore.messages, titleMessage];

		} catch (error) {
			console.error('生成标题错误:', error);
			// 移除加载消息，添加错误消息
			chatStore.messages = chatStore.messages.filter((m: { id: string | string[]; }) => !m.id.includes('_loading'));
			const errorMessage = {
				id: Date.now().toString() + '_error',
				role: 'assistant' as const,
				content: '抱歉，生成标题时出现错误，请稍后重试。'
			};
			chatStore.messages = [...chatStore.messages, errorMessage];
		}
	}

	// 处理采用标题
	function handleAdoptTitle(title: string) {
		if (onTitleGenerated) {
			onTitleGenerated(title);
		}
		
		// 添加确认消息
		const confirmMessage = {
			id: Date.now().toString() + '_confirm',
			role: 'assistant' as const,
			content: `已将标题设置为：**${title}**`
		};
		chatStore.messages = [...chatStore.messages, confirmMessage];
	}

	// 处理复制消息
	function handleCopyMessage(messageId: string) {
		const message = chatStore.messages.find((m: { id: string }) => m.id === messageId);
		if (message) {
			navigator.clipboard.writeText(message.content);
			console.log('Message copied:', messageId);
		}
	}

	// 处理重新生成消息
	async function handleRegenerateMessage(messageId: string) {
		console.log('Regenerate message:', messageId);
		await chatStore.regenerateMessage();
	}

	// 处理点赞消息
	function handleLikeMessage(messageId: string) {
		console.log('Like message:', messageId);
		// 这里可以添加点赞的业务逻辑
	}

	// 处理点踩消息
	function handleDislikeMessage(messageId: string) {
		console.log('Dislike message:', messageId);
		// 这里可以添加点踩的业务逻辑
	}
</script>

<ChatContent 
	class={className}
	height={height}
	messages={chatStore.messages}
	status={chatStore.status}
	error={chatStore.error}
	input={chatStore.input}
	{user}
	{suggestions}
	onSubmit={handleSubmit}
	onCopyMessage={handleCopyMessage}
	onRegenerateMessage={handleRegenerateMessage}
	onLikeMessage={handleLikeMessage}
	onDislikeMessage={handleDislikeMessage}
	onAdoptTitle={handleAdoptTitle}
/>