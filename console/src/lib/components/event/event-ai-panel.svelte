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
		onAdopt
	} = $props<{
		class?: string;
        height?: string;
		currentEvent?: Event;
		user?: any;
		onAdopt?: (type: string, data: any) => void;
	}>();

	// 建议消息 - 重构为对象格式
	const suggestions = [
		{ text: '帮我总结这个事件', type: 'summary', action: 'generateSummary' },
		{ text: '为这个事件生成标题', type: 'title', action: 'generateTitle' },
		{ text: '分析事件的关键信息', type: 'entities', action: 'extractEntities' },
		{ text: '提供改进建议', type: 'improvement', action: 'improvementSuggestions' }
	];

	// 提取建议文本用于UI显示
	const suggestionTexts = suggestions.map(s => s.text);

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

		// 检查是否是预定义的建议
		const suggestion = suggestions.find(s => s.text === text);
		
		if (suggestion && currentEvent?.content) {
			// 处理预定义建议
			await handleSuggestionAction(suggestion, text);
		} else {
			// 发送普通消息
			await chatStore.sendMessage(text);
		}
	}

	// 处理建议动作
	async function handleSuggestionAction(suggestion: any, userMessage: string) {
		switch (suggestion.action) {
			case 'generateTitle':
				await handleTitleGeneration(userMessage);
				break;
			case 'generateSummary':
				await handleEventSummary(userMessage);
				break;
			case 'extractEntities':
				await handleKeyInfoAnalysis(userMessage);
				break;
			case 'improvementSuggestions':
				await handleImprovementSuggestions(userMessage);
				break;
			default:
				// 发送普通消息
				await chatStore.sendMessage(userMessage);
		}
	}

	// 通用AI生成处理函数
	async function handleAIGeneration(config: {
		userMessage: string;
		promptType: string;
		loadingText: string;
		errorText: string;
		formatResult: (result: string) => { content: string; data?: any };
	}) {
		if (!currentEvent?.content) return;

		try {
			// 先发送用户消息
			await chatStore.sendMessage(config.userMessage);

			// 添加加载消息
			const loadingMessage = {
				id: Date.now().toString() + '_loading',
				role: 'assistant' as const,
				content: config.loadingText
			};
			chatStore.messages = [...chatStore.messages, loadingMessage];

			// 调用API
			const response = await fetch('/api/ai/generate', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					promptType: config.promptType,
					markdownContent: currentEvent.content
				})
			});

			if (!response.ok) {
				throw new Error(`${config.errorText}`);
			}

			const result = await response.json();
			const generatedContent = result.text?.text || result.text;

			// 移除加载消息
			chatStore.messages = chatStore.messages.filter((m: { id: string; }) => m.id !== loadingMessage.id);
			
			// 格式化结果并添加消息
			const formattedResult = config.formatResult(generatedContent);
			const responseMessage = {
				id: Date.now().toString() + '_' + config.promptType,
				role: 'assistant' as const,
				content: formattedResult.content,
				...(formattedResult.data && { data: formattedResult.data })
			};
			chatStore.messages = [...chatStore.messages, responseMessage];

		} catch (error) {
			console.error(`${config.errorText}:`, error);
			// 移除加载消息，添加错误消息
			chatStore.messages = chatStore.messages.filter((m: { id: string | string[]; }) => !m.id.includes('_loading'));
			const errorMessage = {
				id: Date.now().toString() + '_error',
				role: 'assistant' as const,
				content: `抱歉，${config.errorText}，请稍后重试。`
			};
			chatStore.messages = [...chatStore.messages, errorMessage];
		}
	}

	// 处理标题生成
	async function handleTitleGeneration(userMessage: string) {
		await handleAIGeneration({
			userMessage,
			promptType: 'generateTitle',
			loadingText: '正在为您生成标题...',
			errorText: '生成标题失败',
			formatResult: (result: string) => ({
				content: `我为您生成了以下标题建议：\n\n**${result}**\n\n您是否要采用这个标题？`,
				data: {
					type: 'title-suggestion',
					title: result
				}
			})
		});
	}

	// 处理事件总结
	async function handleEventSummary(userMessage: string) {
		await handleAIGeneration({
			userMessage,
			promptType: 'generateSummary',
			loadingText: '正在为您总结事件...',
			errorText: '生成总结失败',
			formatResult: (result: string) => ({
				content: `## 事件总结\n\n${result}\n\n您是否要保存这个摘要？`,
				data: {
					type: 'summary-suggestion',
					summary: result
				}
			})
		});
	}

	// 处理关键信息分析
	async function handleKeyInfoAnalysis(userMessage: string) {
		await handleAIGeneration({
			userMessage,
			promptType: 'extractEntities',
			loadingText: '正在分析关键信息...',
			errorText: '分析关键信息失败',
			formatResult: (result: string) => {
				try {
					const entities = JSON.parse(result);
					return {
						content: `## 关键信息分析\n\n**人物：** ${entities.people?.map((p: any) => `${p.name}(${p.role})`).join(', ') || '无'}\n\n**地点：** ${entities.locations?.map((l: any) => l.name).join(', ') || '无'}\n\n**时间线：** ${entities.timeline?.map((t: any) => `${t.time}: ${t.event}`).join('\n') || '无'}\n\n您是否要保存这些实体信息？`,
						data: {
							type: 'entities-suggestion',
							entities: entities
						}
					};
				} catch {
					return {
						content: `## 关键信息分析\n\n${result}`
					};
				}
			}
		});
	}

	// 处理改进建议
	async function handleImprovementSuggestions(userMessage: string) {
		await handleAIGeneration({
			userMessage,
			promptType: 'improvementSuggestions',
			loadingText: '正在生成改进建议...',
			errorText: '生成改进建议失败',
			formatResult: (result: string) => ({
				content: `## 改进建议\n\n${result}`
			})
		});
	}

	// 处理采用数据
	function handleAdopt(type: string, data: any) {
		if (onAdopt) {
			onAdopt(type, data);
		}
		
		// 添加确认消息
		let confirmText = '';
		switch (type) {
			case 'title-suggestion':
				confirmText = '已将标题设置为：**' + data.title + '**';
				break;
			case 'summary-suggestion':
				confirmText = '已保存事件摘要';
				break;
			case 'entities-suggestion':
				confirmText = '已保存实体信息';
				break;
			case 'date-suggestion':
				confirmText = '已保存日期信息';
				break;
			case 'location-suggestion':
				confirmText = '已保存地点信息';
				break;
			default:
				confirmText = '已保存数据';
		}
		
		const confirmMessage = {
			id: Date.now().toString() + '_confirm',
			role: 'assistant' as const,
			content: `**${confirmText}**`
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
	suggestions={suggestionTexts}
	onSubmit={handleSubmit}
	onCopyMessage={handleCopyMessage}
	onRegenerateMessage={handleRegenerateMessage}
	onLikeMessage={handleLikeMessage}
	onDislikeMessage={handleDislikeMessage}
	onAdopt={handleAdopt}
/>