<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import AiInput from '$lib/components/ai/ai-input.svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Resizable from '$lib/components/ui/resizable/index.js';
	import { BlocksuiteEditor } from '$lib/components/editor/index.js';
	import { EventHeader } from '$lib/components/event';
	import { Loading } from '$lib/components/ui/loading';
	import { eventStore } from '$lib/stores/event.svelte';
	import type { Event } from '$lib/types/event';
	import { toast } from 'svelte-sonner';

	// 页面状态
	let showEditor = $state(false);
	let showTimePicker = $state(false);
	let showMapPicker = $state(false);
	let showCoverPicker = $state(false);

	let blocksuiteEditorRef = $state<any>(null);
	let isLoading = $state(false);
	let isSaving = $state(false);

	// 事件数据
	let eventData = $state<Event | null>(null);
	let eventId = $state<string>('');

	// 从路由参数获取事件ID
	$effect(() => {
		if ($page.params.id) {
			eventId = $page.params.id;
			loadEvent();
		}
	});

	// 监听eventData变化（用于调试）
	$effect(() => {
		if (eventData) {
			console.log(eventData);
		}
	});

	// 加载事件数据
	async function loadEvent() {
		if (!eventId || eventId === 'new') {
			// 创建新事件
			eventData = {
				$id: '',
				name: 'New Event',
				summary: '',
				content: '',
				user_id: 'current-user', // 这里应该从认证状态获取
				status: 'draft',
			};
			return;
		}

		try {
			isLoading = true;
			eventData = await eventStore.getEventById(eventId);
		} catch (error) {
			console.error('加载事件失败:', error);
			// 如果事件不存在，重定向到事件列表
			goto('/console/events');
		} finally {
			isLoading = false;
		}
	}

	// 保存事件
	async function saveEvent() {
		if (!eventData) return;

		try {
			isSaving = true;

			// 从编辑器获取内容
			if (blocksuiteEditorRef?.getContent) {
				eventData.content = await blocksuiteEditorRef.getContent();
			}

			if (eventData.$id && eventData.$id !== '') {
				// 更新现有事件
				await eventStore.updateEvent(eventData.$id, eventData);
			} else {
				// 创建新事件
				const newEvent = await eventStore.createEvent({
					name: eventData.name || eventData.name || 'New Event',
					summary: eventData.summary,
					content: eventData.content,
					user_id: eventData.user_id,
					status: eventData.status || 'draft',
					categories: eventData.categories,
					tags: eventData.tags,
					date: eventData.date,
					privacy: eventData.privacy,
					cover: eventData.cover,
					location_data: eventData.location_data,
					entities_data: eventData.entities_data,
					creator_name: eventData.creator_name,
					creator_avatar: eventData.creator_avatar,
					folder_id: eventData.folder_id
				});
				eventData = newEvent;
				// 更新URL为新事件ID
				goto(`/console/events/${newEvent.$id}`, { replaceState: true });
			}
			
			
			showEditor = false;
			showTimePicker = false;
			showMapPicker = false;
			showCoverPicker = false;
		} catch (error) {
			console.error('保存事件失败:', error);
			toast.error((error as Error).message || '保存失败');
		} finally {
			isSaving = false;
		}
	}

	// 处理名称保存
	function handleNameSave(name: string, summary: string) {
		if (!eventData) return;

		eventData.name = name;
		eventData.summary = summary;
		eventData.name = name; // 同步 name 字段

		// 自动保存
		saveEvent();
	}

	// 处理时间保存
	function handleTimeSave(date: string | Date) {
		if (!eventData) return;

		// 确保date是字符串格式，符合Appwrite要求
		if (typeof date === 'string') {
			eventData.date = date;
		} else if (date instanceof Date) {
			eventData.date = date.toISOString();
		} else if (date && typeof date === 'object' && 'toDate' in date) {
			// 处理DateValue对象
			eventData.date = (date as any).toDate().toISOString();
		} else {
			eventData.date = String(date);
		}
		
		// 自动保存
		saveEvent();
	}

	// 处理地图位置保存
	function handleMapSave(locationData: string) {
		if (!eventData) return;
		
		// 保存位置数据为字符串格式
		eventData.location_data = locationData;
		
		// 自动保存
		saveEvent();
	}

	// 删除事件
	async function handleDeleteEvent() {
		if (!eventData?.$id || !confirm('确定要删除这个事件吗？')) return;

		try {
			await eventStore.deleteEvent(eventData.$id);
			goto('/console/events');
		} catch (error) {
			console.error('删除事件失败:', error);
		}
	}

	// CoverPicker 事件处理函数
	function handleCoverSelect(url: string) {
		if (eventData) {
			eventData.cover = url;
			saveEvent();
		}
	}

	function handleCoverLinkSubmit(url: string) {
		if (eventData) {
			eventData.cover = url;
			saveEvent();
		}
	}



	// 处理设置菜单
	function handleSettings() {
		console.log('打开设置');
	}

	// 键盘快捷键保存
	function handleKeydown(event: KeyboardEvent) {
		if ((event.ctrlKey || event.metaKey) && event.key === 's') {
			event.preventDefault();
			saveEvent();
		}
	}
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="w-full h-full flex flex-col" onkeydown={handleKeydown}>
	{#if isLoading}
		<Loading />
	{:else if eventData}
		<EventHeader
			{eventData}
			{isSaving}
			bind:showEditor
			bind:showTimePicker
			bind:showMapPicker
			bind:showCoverPicker
			onBack={() => goto('/console/events')}
			onNameSave={handleNameSave}
			onTimeSave={handleTimeSave}
			onMapSave={handleMapSave}
			onSave={saveEvent}
			onCoverSelect={handleCoverSelect}
			onCoverLinkSubmit={handleCoverLinkSubmit}
			onSettings={handleSettings}
		/>
		<Resizable.PaneGroup direction="horizontal" class="w-full flex-1 ">
			<Resizable.Pane defaultSize={30} class="p-2 pr-0 flex flex-col h-[calc(100vh-56px)]">
				<div class="flex-end flex-col h-full border rounded-2xl p-4 bg-base-200/50">
					<AiInput class="w-full" />
				</div>
			</Resizable.Pane>
			<Resizable.Handle class="bg-transparent" />
			<Resizable.Pane defaultSize={70} class="flex flex-col p-2">
				<BlocksuiteEditor bind:this={blocksuiteEditorRef} initialJsonContent={eventData.content} />
			</Resizable.Pane>
		</Resizable.PaneGroup>
	{:else}
		<div class="flex-center h-full">
			<div class="text-center">
				<p class="text-lg font-semibold mb-2">事件未找到</p>
				<p class="text-muted-foreground mb-4">请检查事件ID是否正确</p>
				<Button onclick={() => goto('/console/events')}>返回事件列表</Button>
			</div>
		</div>
	{/if}
</div>
