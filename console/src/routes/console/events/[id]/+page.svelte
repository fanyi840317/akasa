<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { eventStore } from '$lib/stores/event.svelte.js';
	import { authStore } from '$lib/stores/auth.svelte.js';
	import { interactionStore } from '$lib/stores/interaction.svelte.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import { Badge } from '$lib/components/ui/badge/index.js';
	import {
		CalendarIcon,
		MapPinIcon,
		UserIcon,
		Edit,
		Share,
		MoreHorizontalIcon,
		ArrowLeft,
		ThumbsUp,
		Heart,
		Trash2,
		HeartIcon,
		FlagIcon
	} from '@lucide/svelte';
	import { toast } from 'svelte-sonner';
	import type { Event } from '$lib/types/event';
	import UserAvatar from '$lib/components/user/user-avatar.svelte';
	import { formatDate, formatLocation } from '$lib/utils.js';
	import { Toggle } from '$lib/components/ui/toggle';
	import { BlocksuiteEditor } from '$lib/components/editor';

	// 获取路由参数中的事件ID
	const eventId = $derived($page.params.id);
	let event = $state<Event | null>(null);
	let isLoading = $state(true);
	let error = $state<string | null>(null);

	// 交互状态
	let interactionStats = $state({ likes: 0, favorites: 0 });
	let userInteractionState = $state({ isLiked: false, isFavorited: false });
	let isInteractionLoading = $state(false);

	// 加载事件详情
	onMount(async () => {
		if (!eventId) {
			error = 'Event ID not found';
			isLoading = false;
			return;
		}

		try {
			isLoading = true;
			event = await eventStore.getEventById(eventId);

			// 加载交互数据
			if (authStore.user) {
				interactionStats = await interactionStore.getInteractionStats(eventId);
				userInteractionState = await interactionStore.getUserInteractionState(
					eventId,
					authStore.user.$id
				);
			}
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to load event';
			toast.error('Failed to load event details');
		} finally {
			isLoading = false;
		}
	});

	// 编辑事件
	function handleEdit() {
		if (event) {
			goto(`/console/events/${event.$id}/edit`);
		}
	}

	// 处理点赞
	async function handleToggleLike() {
		if (!authStore.user || !eventId || isInteractionLoading) return;

		try {
			isInteractionLoading = true;
			const newLikedState = await interactionStore.toggleLike(eventId, authStore.user.$id);
			userInteractionState.isLiked = newLikedState;
			// 重新获取统计数据
			interactionStats = await interactionStore.getInteractionStats(eventId);
			toast.success(newLikedState ? '点赞成功！' : '取消点赞');
		} catch (err) {
			toast.error('操作失败，请重试');
		} finally {
			isInteractionLoading = false;
		}
	}

	// 处理收藏
	async function handleToggleFavorite() {
		if (!authStore.user || !eventId || isInteractionLoading) return;

		try {
			isInteractionLoading = true;
			const newFavoritedState = await interactionStore.toggleFavorite(
				eventId,
				authStore.user.$id,
				event?.title
			);
			userInteractionState.isFavorited = newFavoritedState;
			// 重新获取统计数据
			interactionStats = await interactionStore.getInteractionStats(eventId);
			toast.success(newFavoritedState ? '收藏成功！' : '取消收藏');
		} catch (err) {
			toast.error('操作失败，请重试');
		} finally {
			isInteractionLoading = false;
		}
	}

	// 分享事件
	function handleShare() {
		if (event) {
			navigator.clipboard.writeText(window.location.href);
			toast.success('Event link copied to clipboard!');
		}
	}

	// 删除事件
	async function handleDelete() {
		if (!event) return;

		if (confirm('Are you sure you want to delete this event?')) {
			try {
				await eventStore.deleteEvent(event.$id);
				toast.success('Event deleted successfully');
				goto('/console/events');
			} catch (err) {
				toast.error('Failed to delete event');
			}
		}
	}

	// 检查是否是事件创建者
	const isOwner = $derived(event && authStore.user && event.user_id === authStore.user.email);
</script>

<svelte:head>
	<title>{event?.name || 'Event'} - Akasa Console</title>
</svelte:head>

{#if isLoading}
	<div class="flex items-center justify-center min-h-screen">
		<div class="text-center">
			<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
			<p class="text-muted-foreground">Loading event details...</p>
		</div>
	</div>
{:else if error}
	<div class="flex items-center justify-center min-h-screen">
		<Card.Root class="w-full max-w-md">
			<Card.Header>
				<Card.Title class="text-destructive">Error</Card.Title>
			</Card.Header>
			<Card.Content>
				<p class="text-muted-foreground mb-4">{error}</p>
				<Button onclick={() => goto('/console/events')} variant="outline" class="w-full">
					Back to Events
				</Button>
			</Card.Content>
		</Card.Root>
	</div>
{:else if event}
	<!-- 顶部导航栏 -->
	<div class=" border-b flex-center">
		<div
			class="flex w-full max-w-6xl flex-col items-start gap-5 p-6 sm:gap-6 sm:p-9 [@media(min-width:1700px)]:max-w-[1600px]"
		>
			<button
				class="text-xs text-foreground/50 hover:text-foreground flex-row flex-center"
				onclick={() => goto('/console/events')}
			>
				<ArrowLeft class="size-4" />
				<span>Back</span>
			</button>
			<div
				class="flex w-full flex-col items-start justify-between gap-4 sm:flex-row sm:items-center sm:gap-2"
			>
				<div class="flex flex-col gap-2 text-left">
					<div class="flex items-center gap-1.5">
						<UserAvatar
							class="size-6"
							user={{ name: event.creator_name || '', avatar: event.creator_avatar }}
						></UserAvatar>
						<p class="text-sm font-medium text-gray-500">{event.creator_name || 'Unknown'}</p>
					</div>
					<div class="flex items-center gap-2">
						<div class="line-clamp-1 text-base font-semibold sm:text-xl">
							{event.name}
						</div>
					</div>
					<div class="flex flex-row gap-4">
						<div class="flex items-center gap-2">
							<CalendarIcon class="h-4 w-4 text-muted-foreground" />
							<span class="text-xs text-muted-foreground"
								>{formatDate(event.date, { includeYear: true, includeWeekday: true })}</span
							>
						</div>
						<div class="flex items-center gap-2">
							<MapPinIcon class="h-4 w-4 text-muted-foreground" />
							<span class="text-xs text-muted-foreground"
								>{formatLocation(event.location_data)}</span
							>
						</div>
					</div>
				</div>
				<div class="flex flex-row-reverse items-center gap-2 sm:flex-row">
					<Toggle variant="outline" aria-label="Toggle italic">
						<HeartIcon class="size-4" />
					</Toggle>
					<Toggle variant="outline" aria-label="Toggle italic">
						<FlagIcon class="size-4" />
					</Toggle>
				</div>
			</div>
		</div> 
	</div>
	<div class="flex w-full max-w-6xl mx-auto p-6 sm:p-9 [@media(min-width:1700px)]:max-w-[1600px]">
		<Card.Root class="w-full h-[400px] p-0 border-0">
			<BlocksuiteEditor initialJsonContent={event.content} readonly={true} />
		</Card.Root>
	</div>

	<!-- 主要内容区域 -->
{/if}
