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
		Trash2
	} from '@lucide/svelte';
	import { toast } from 'svelte-sonner';
	import type { Event } from '$lib/types/event';
	import UserAvatar from '$lib/components/user/user-avatar.svelte';

	// 获取路由参数中的事件ID
	const eventId = $derived($page.params.id);
	let event = $state<Event | null>(null);
	let isLoading = $state(true);
	let error = $state<string | null>(null);

	// 交互状态
	let interactionStats = $state({ likes: 0, favorites: 0 });
	let userInteractionState = $state({ isLiked: false, isFavorited: false });
	let isInteractionLoading = $state(false);

	// 格式化日期
	function formatDate(date: string | Date | undefined): string {
		if (!date) return 'No date';
		const d = typeof date === 'string' ? new Date(date) : date;
		return d.toLocaleDateString('zh-CN', {
			year: 'numeric',
			month: 'long',
			day: 'numeric',
			weekday: 'long'
		});
	}

	// 格式化位置信息
	function formatLocation(locationData: any): string {
		if (!locationData) return 'No location';
		if (typeof locationData === 'string')
			locationData = JSON.parse(locationData);
		if (locationData.address) return locationData.address;
		if (locationData.name) return locationData.name;
		return 'Unknown location';
	}

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
				userInteractionState = await interactionStore.getUserInteractionState(eventId, authStore.user.$id);
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
	<div class=" border-b flex-center py-6">
		<div
				class="flex w-full max-w-[1072px] flex-col items-start gap-5 p-6 sm:gap-6 sm:p-9 [@media(min-width:1700px)]:max-w-[1600px]"
			>
			<button class="p-0 flex-center flex-row gap-1 text-xs" onclick={()=>goto('/console/events')}>
				<ArrowLeft class="size-4"/>
				<span>Back</span>
			</button>
				<div
					class="flex w-full flex-col items-start justify-between gap-4 sm:flex-row sm:items-center sm:gap-2"
				>
					<div class="flex flex-col gap-2 text-left">
						<div class="flex items-center gap-1.5">
							<UserAvatar user={{name: event.creator_name|| '', avatar: event.creator_avatar}}></UserAvatar>	
							<p class="text-sm font-medium text-gray-500">{event.creator_name}</p>
						</div>
						<div class="flex items-center gap-2">
							<div class="line-clamp-1 text-base font-semibold sm:text-xl">
								{event.name}
							</div>
						</div>
						<div class="flex flex-row gap-4">
							<div class="flex items-center gap-2">
								<CalendarIcon class="h-4 w-4 text-muted-foreground" />
								<span class="text-xs text-muted-foreground">{formatDate(event.date)}</span>
							</div>
							<div class="flex items-center gap-2">
								<MapPinIcon class="h-4 w-4 text-muted-foreground" />
								<span class="text-xs text-muted-foreground">{formatLocation(event.location_data)}</span>
							</div>
						</div>
						
					</div>
					<div class="flex flex-row-reverse items-center gap-2 sm:flex-row">
						<button
							class="focus:border-alpha-400 focus-visible:border-alpha-400 disabled:border-alpha-300 border-alpha-400 hover:border-alpha-400 focus-visible:ring-offset-background aria-disabled:border-alpha-300 inline-flex shrink-0 cursor-pointer select-none items-center justify-center gap-1.5 whitespace-nowrap text-nowrap border font-medium outline-none ring-blue-600 transition-[background,border-color,color,transform,opacity,box-shadow] focus-visible:ring-2 focus-visible:ring-offset-1 disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-400 disabled:ring-0 has-[:focus-visible]:ring-2 aria-disabled:cursor-not-allowed aria-disabled:bg-gray-100 aria-disabled:text-gray-400 aria-disabled:ring-0 [&amp;>svg]:pointer-events-none [&amp;>svg]:size-4 [&amp;_svg]:shrink-0 bg-background-subtle text-gray-900 hover:bg-gray-100 focus:bg-gray-100 focus-visible:bg-gray-100 text-sm has-[>kbd]:gap-2 has-[>svg]:px-2 has-[>kbd]:pr-[6px] size-7 rounded-md px-0 sm:hidden"
							aria-label="Flag Generation"
							data-state="closed"
							><svg
								data-testid="geist-icon"
								height="16"
								stroke-linejoin="round"
								viewBox="0 0 16 16"
								width="16"
								style="color: currentcolor;"
								><path
									fill-rule="evenodd"
									clip-rule="evenodd"
									d="M2.5 2.38401C2.64568 2.28957 2.84672 2.17097 3.09632 2.0516C3.67556 1.77457 4.50202 1.5 5.5 1.5C6.36835 1.5 7.01666 1.91731 7.76416 2.47582C7.81395 2.51302 7.86487 2.55137 7.91678 2.59046C8.2325 2.82825 8.58515 3.09385 8.94862 3.30046C9.38732 3.54983 9.90016 3.75 10.5 3.75C11.4771 3.75 12.5081 3.46807 13.2589 3.20897C13.3421 3.18026 13.4226 3.15157 13.5 3.12321V8.81917C13.366 8.88807 13.1923 8.96944 12.9825 9.05151C12.4127 9.27435 11.5825 9.49998 10.5568 9.49998C9.65149 9.49998 9.11435 9.17173 8.42753 8.74001L8.40495 8.72582C7.70405 8.28516 6.85285 7.75 5.5 7.75C4.25466 7.75 3.22521 8.08445 2.5 8.42432V2.38401ZM2.5 10.134V15.25V16H1V15.25V2V1.65215L1.26554 1.42746L1.75 2C1.26554 1.42746 1.26576 1.42728 1.26599 1.42709L1.26646 1.42668L1.26752 1.42579L1.27005 1.42367L1.27679 1.41807L1.29689 1.4017C1.31321 1.38857 1.33537 1.37107 1.36321 1.34985C1.41885 1.30743 1.49735 1.24998 1.59739 1.18261C1.79715 1.04807 2.08466 0.872716 2.44914 0.698399C3.17671 0.350428 4.22526 0 5.5 0C6.90437 0 7.9038 0.707694 8.66198 1.27418C8.72015 1.31765 8.77638 1.3599 8.831 1.40094C9.15213 1.64223 9.41729 1.84147 9.68987 1.99641C9.99337 2.16892 10.2476 2.25 10.5 2.25C11.2275 2.25 12.0715 2.03193 12.7695 1.79103C13.1109 1.67321 13.4025 1.55523 13.6079 1.46707C13.7104 1.42308 13.7908 1.38677 13.8446 1.36197C13.8714 1.34957 13.8916 1.34007 13.9044 1.33395L13.9182 1.32736L13.9206 1.32621L13.9208 1.32612L13.9209 1.32608L13.9209 1.32605L13.9211 1.32597L15 0.798502V2V9.24998V9.6392L14.6817 9.86326L14.25 9.24998C14.6817 9.86326 14.6815 9.86342 14.6813 9.86359L14.6808 9.86394L14.6797 9.86471L14.6771 9.86653L14.6702 9.87124L14.6502 9.88477C14.6341 9.89556 14.6123 9.90981 14.5851 9.92701C14.5307 9.96141 14.4542 10.0077 14.3569 10.0618C14.1624 10.1699 13.8834 10.3098 13.5289 10.4485C12.8202 10.7256 11.8039 11 10.5568 11C9.20395 11 8.35275 10.4648 7.65185 10.0242L7.62928 10.01C6.94245 9.57826 6.40532 9.25 5.5 9.25C4.50202 9.25 3.67557 9.52457 3.09633 9.8016C2.84672 9.92098 2.64568 10.0396 2.5 10.134ZM2.23212 10.3245C2.23169 10.3249 2.23159 10.325 2.23184 10.3248L2.23212 10.3245Z"
									fill="currentColor"
								></path></svg
							></button
						><button
							class="focus:border-alpha-400 focus-visible:border-alpha-400 disabled:border-alpha-300 border-alpha-400 hover:border-alpha-400 focus-visible:ring-offset-background aria-disabled:border-alpha-300 shrink-0 cursor-pointer select-none items-center justify-center gap-1.5 whitespace-nowrap text-nowrap border font-medium outline-none ring-blue-600 transition-[background,border-color,color,transform,opacity,box-shadow] focus-visible:ring-2 focus-visible:ring-offset-1 disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-400 disabled:ring-0 has-[:focus-visible]:ring-2 aria-disabled:cursor-not-allowed aria-disabled:bg-gray-100 aria-disabled:text-gray-400 aria-disabled:ring-0 [&amp;>svg]:pointer-events-none [&amp;>svg]:size-4 [&amp;_svg]:shrink-0 bg-background-subtle text-gray-900 hover:bg-gray-100 focus:bg-gray-100 focus-visible:bg-gray-100 h-8 px-3 text-sm has-[>kbd]:gap-2 has-[>svg]:px-2 has-[>kbd]:pr-[6px] rounded-lg hidden sm:block"
							aria-label="Flag Generation"
							data-state="closed"
							><svg
								data-testid="geist-icon"
								height="16"
								stroke-linejoin="round"
								viewBox="0 0 16 16"
								width="16"
								style="color: currentcolor;"
								><path
									fill-rule="evenodd"
									clip-rule="evenodd"
									d="M2.5 2.38401C2.64568 2.28957 2.84672 2.17097 3.09632 2.0516C3.67556 1.77457 4.50202 1.5 5.5 1.5C6.36835 1.5 7.01666 1.91731 7.76416 2.47582C7.81395 2.51302 7.86487 2.55137 7.91678 2.59046C8.2325 2.82825 8.58515 3.09385 8.94862 3.30046C9.38732 3.54983 9.90016 3.75 10.5 3.75C11.4771 3.75 12.5081 3.46807 13.2589 3.20897C13.3421 3.18026 13.4226 3.15157 13.5 3.12321V8.81917C13.366 8.88807 13.1923 8.96944 12.9825 9.05151C12.4127 9.27435 11.5825 9.49998 10.5568 9.49998C9.65149 9.49998 9.11435 9.17173 8.42753 8.74001L8.40495 8.72582C7.70405 8.28516 6.85285 7.75 5.5 7.75C4.25466 7.75 3.22521 8.08445 2.5 8.42432V2.38401ZM2.5 10.134V15.25V16H1V15.25V2V1.65215L1.26554 1.42746L1.75 2C1.26554 1.42746 1.26576 1.42728 1.26599 1.42709L1.26646 1.42668L1.26752 1.42579L1.27005 1.42367L1.27679 1.41807L1.29689 1.4017C1.31321 1.38857 1.33537 1.37107 1.36321 1.34985C1.41885 1.30743 1.49735 1.24998 1.59739 1.18261C1.79715 1.04807 2.08466 0.872716 2.44914 0.698399C3.17671 0.350428 4.22526 0 5.5 0C6.90437 0 7.9038 0.707694 8.66198 1.27418C8.72015 1.31765 8.77638 1.3599 8.831 1.40094C9.15213 1.64223 9.41729 1.84147 9.68987 1.99641C9.99337 2.16892 10.2476 2.25 10.5 2.25C11.2275 2.25 12.0715 2.03193 12.7695 1.79103C13.1109 1.67321 13.4025 1.55523 13.6079 1.46707C13.7104 1.42308 13.7908 1.38677 13.8446 1.36197C13.8714 1.34957 13.8916 1.34007 13.9044 1.33395L13.9182 1.32736L13.9206 1.32621L13.9208 1.32612L13.9209 1.32608L13.9209 1.32605L13.9211 1.32597L15 0.798502V2V9.24998V9.6392L14.6817 9.86326L14.25 9.24998C14.6817 9.86326 14.6815 9.86342 14.6813 9.86359L14.6808 9.86394L14.6797 9.86471L14.6771 9.86653L14.6702 9.87124L14.6502 9.88477C14.6341 9.89556 14.6123 9.90981 14.5851 9.92701C14.5307 9.96141 14.4542 10.0077 14.3569 10.0618C14.1624 10.1699 13.8834 10.3098 13.5289 10.4485C12.8202 10.7256 11.8039 11 10.5568 11C9.20395 11 8.35275 10.4648 7.65185 10.0242L7.62928 10.01C6.94245 9.57826 6.40532 9.25 5.5 9.25C4.50202 9.25 3.67557 9.52457 3.09633 9.8016C2.84672 9.92098 2.64568 10.0396 2.5 10.134ZM2.23212 10.3245C2.23169 10.3249 2.23159 10.325 2.23184 10.3248L2.23212 10.3245Z"
									fill="currentColor"
								></path></svg
							></button
						>
						<form
							action="javascript:throw new Error('A React form was unexpectedly submitted. If you called form.submit() manually, consider using form.requestSubmit() instead. If you\'re trying to use event.stopPropagation() in a submit event handler, consider also calling event.preventDefault().')"
						>
							<button
								class="focus-visible:ring-offset-background inline-flex shrink-0 cursor-pointer select-none items-center justify-center gap-1.5 whitespace-nowrap text-nowrap border font-medium outline-none ring-blue-600 transition-[background,border-color,color,transform,opacity,box-shadow] focus-visible:ring-2 focus-visible:ring-offset-1 disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-400 disabled:ring-0 has-[:focus-visible]:ring-2 aria-disabled:cursor-not-allowed aria-disabled:bg-gray-100 aria-disabled:text-gray-400 aria-disabled:ring-0 [&amp;>svg]:pointer-events-none [&amp;>svg]:size-4 [&amp;_svg]:shrink-0 disabled:border-alpha-400 text-background aria-disabled:border-alpha-400 border-gray-900 bg-gray-900 hover:border-gray-700 hover:bg-gray-700 focus:border-gray-700 focus:bg-gray-700 focus-visible:border-gray-700 focus-visible:bg-gray-700 text-sm has-[>kbd]:gap-2 has-[>svg]:px-2 has-[>kbd]:pr-[6px] relative h-7 rounded-md px-2 sm:h-8 sm:rounded-lg sm:px-3"
								type="submit"
								><div class="flex items-center justify-center gap-2 transition-opacity">
									<div class="flex w-full items-center justify-center gap-1">
										Open in <svg
											fill="currentColor"
											viewBox="0 0 40 20"
											xmlns="http://www.w3.org/2000/svg"
											class="!w-5"
											><path
												d="M23.3919 0H32.9188C36.7819 0 39.9136 3.13165 39.9136 6.99475V16.0805H36.0006V6.99475C36.0006 6.90167 35.9969 6.80925 35.9898 6.71766L26.4628 16.079C26.4949 16.08 26.5272 16.0805 26.5595 16.0805H36.0006V19.7762H26.5595C22.6964 19.7762 19.4788 16.6139 19.4788 12.7508V3.68923H23.3919V12.7508C23.3919 12.9253 23.4054 13.0977 23.4316 13.2668L33.1682 3.6995C33.0861 3.6927 33.003 3.68923 32.9188 3.68923H23.3919V0Z"
											></path><path
												d="M13.7688 19.0956L0 3.68759H5.53933L13.6231 12.7337V3.68759H17.7535V17.5746C17.7535 19.6705 15.1654 20.6584 13.7688 19.0956Z"
											></path></svg
										>
									</div>
								</div></button
							>
						</form>
					</div>
				</div>
			</div>
	</div>

	<!-- 主要内容区域 -->
	<div class="min-h-screen">
		<div class="container mx-auto px-6 py-8 max-w-4xl">
			<!-- 事件信息卡片 -->
			<Card.Root class="mb-6 overflow-hidden shadow-sm">
				<Card.Content class="p-6">
					<!-- 事件标题 -->
					<div class="mb-6">
						<h1 class="text-2xl font-bold text-foreground mb-2">{event.name}</h1>
						{#if event.summary}
							<p class="text-muted-foreground">{event.summary}</p>
						{/if}
					</div>

					<!-- 事件属性信息 -->
					<div class="space-y-4 mb-6">
						<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
							<!-- 左列 -->
							<div class="space-y-3">
								<div class="flex items-center gap-3">
									<CalendarIcon class="h-4 w-4 text-muted-foreground" />
									<div>
										<p class="text-sm text-muted-foreground">Date</p>
										<p class="text-sm font-medium">{formatDate(event.date)}</p>
									</div>
								</div>
								<div class="flex items-center gap-3">
									<MapPinIcon class="h-4 w-4 text-muted-foreground" />
									<div>
										<p class="text-sm text-muted-foreground">Location</p>
										<p class="text-sm font-medium">{formatLocation(event.location_data)}</p>
									</div>
								</div>
							</div>
							<!-- 右列 -->
							<div class="space-y-3">
								<div class="flex items-center gap-3">
									<UserIcon class="h-4 w-4 text-muted-foreground" />
									<div>
										<p class="text-sm text-muted-foreground">Creator</p>
										<p class="text-sm font-medium">{event.creator_name || 'Unknown'}</p>
									</div>
								</div>
								<div class="flex items-center gap-3">
									<div class="w-4 h-4 rounded-full bg-green-500 flex items-center justify-center">
										<div class="w-1.5 h-1.5 rounded-full bg-white"></div>
									</div>
									<div>
										<p class="text-sm text-muted-foreground">Status</p>
										<p class="text-sm font-medium capitalize">{event.status || 'Active'}</p>
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- 标签和分类 -->
					{#if (event.categories && event.categories.length > 0) || (event.tags && event.tags.length > 0)}
						<div class="border-t pt-4">
							<div class="flex flex-wrap gap-2">
								{#if event.categories && event.categories.length > 0}
									{#each event.categories as category}
										<Badge variant="secondary" class="text-xs">{category}</Badge>
									{/each}
								{/if}
								{#if event.tags && event.tags.length > 0}
									{#each event.tags as tag}
										<Badge variant="outline" class="text-xs">#{tag}</Badge>
									{/each}
								{/if}
							</div>
						</div>
					{/if}
				</Card.Content>
			</Card.Root>

			<!-- 事件内容卡片 -->
			{#if event.content}
				<Card.Root class="shadow-sm">
					<Card.Header class="pb-3">
						<Card.Title class="text-lg font-semibold">Content</Card.Title>
					</Card.Header>
					<Card.Content>
						<div class="prose prose-sm max-w-none text-sm leading-relaxed">
							{@html event.content}
						</div>
					</Card.Content>
				</Card.Root>
			{:else}
				<Card.Root class="shadow-sm">
					<Card.Content class="p-8 text-center">
						<div class="text-muted-foreground">
							<CalendarIcon class="h-8 w-8 mx-auto mb-3 opacity-50" />
							<p class="font-medium mb-1">No content available</p>
							<p class="text-sm">This event doesn't have any detailed content yet.</p>
							{#if isOwner}
							<Button onclick={handleEdit} class="mt-4" variant="outline" size="sm">
								<Edit class="h-4 w-4 mr-2" />
								Add Content
							</Button>
						{/if}
						</div>
					</Card.Content>
				</Card.Root>
			{/if}

			<!-- 实体数据卡片 -->
			{#if event.entities_data}
				<Card.Root class="shadow-sm">
					<Card.Header class="pb-3">
						<Card.Title class="text-lg font-semibold">Entities Data</Card.Title>
					</Card.Header>
					<Card.Content>
						<pre
							class="bg-muted/50 p-4 rounded-lg text-xs overflow-auto border">{event.entities_data}</pre>
					</Card.Content>
				</Card.Root>
			{/if}
		</div>
	</div>
{/if}
