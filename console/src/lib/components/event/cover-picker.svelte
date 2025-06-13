<script lang="ts">
	import { Link, Upload, X, CheckCircle, AlertCircle } from '@lucide/svelte';
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import * as Popover from '$lib/components/ui/popover';
	import * as Card from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { uploadToImgBB, type UploadProgress } from '$lib/utils';
	import type { Snippet } from 'svelte';
	import Mask from './mask.svelte';

	// 使用 $props() 定义组件属性，接收回调函数
	let { onSelect, onLinkSubmit, userId, children, isOpen = $bindable(false) } = $props<{
		onSelect: (url: string) => void;
		onLinkSubmit: (url: string) => void;
		userId: string; // 添加 userId 属性
		isOpen?: boolean;
		children?: Snippet;
	}>();

	let coverLink = $state('');
	let showValidationError = $state(false); // 控制是否显示验证错误信息

	// 上传状态管理
	let isUploading = $state(false);
	let uploadProgress = $state<UploadProgress | null>(null);
	let uploadError = $state<string | null>(null);
	let uploadSuccess = $state(false);

	// 使用 store 中的数据
	// 修改为包含缩略图 URL 的数据结构
	// 使用 store 中的数据并按提供者分组

	// 本地状态替代 store
	let userImages = $state<{ imageUrl: string; thumbnailUrl?: string; provider?: string }[]>([]);
	let isLoading = $state(false);

	let groupedCoverImages = $derived(
		userImages && userImages.length > 0
			? userImages.reduce(
					(
						acc: Record<string, { imageUrl: string; thumbnailUrl?: string; provider?: string }[]>,
						image
					) => {
						const provider = image.provider || '未知提供者';
						if (!acc[provider]) {
							acc[provider] = [];
						}
						acc[provider].push(image);
						return acc;
					},
					{} as Record<string, { imageUrl: string; thumbnailUrl?: string; provider?: string }[]>
				)
			: {}
	);

	// 在组件挂载或 userId 变化时加载用户图片
	onMount(() => {
		if (userId) {
			loadUserImages(userId);
		}
	});

	// 模拟加载用户图片的函数
	async function loadUserImages(userId: string) {
		isLoading = true;
		try {
			// 这里应该是实际的 API 调用
			// 暂时使用空数组作为占位符
			userImages = [];
		} catch (error) {
			console.error('加载用户图片失败:', error);
			userImages = [];
		} finally {
			isLoading = false;
		}
	}

	// 处理选择已有图片
	function handleSelectExistingImage(imageUrl: string) {
		onSelect(imageUrl);
	}

	// 处理文件选择和上传
	async function handleFileSelect(event: Event) {
		const input = event.target as HTMLInputElement;
		if (!input.files || !input.files[0]) return;

		const file = input.files[0];
		
		// 验证文件类型
		if (!file.type.startsWith('image/')) {
			uploadError = '请选择有效的图片文件';
			return;
		}

		// 验证文件大小 (最大 10MB)
		if (file.size > 10 * 1024 * 1024) {
			uploadError = '图片文件大小不能超过 10MB';
			return;
		}

		// 重置状态
		uploadError = null;
		uploadSuccess = false;
		isUploading = true;
		uploadProgress = null;

		try {
			const result = await uploadToImgBB(file, (progress) => {
				uploadProgress = progress;
			});

			if (result.success && result.data) {
				// 上传成功，添加到用户图片列表
				const newImage = {
					imageUrl: result.data.url,
					thumbnailUrl: result.data.thumb.url,
					provider: 'ImgBB'
				};
				userImages = [newImage, ...userImages];
				
				// 自动选择刚上传的图片
				onSelect(result.data.url);
				
				uploadSuccess = true;
				
				// 3秒后隐藏成功状态
				setTimeout(() => {
					uploadSuccess = false;
				}, 3000);
			} else {
				uploadError = result.error?.message || '上传失败，请重试';
			}
		} catch (error) {
			console.error('上传错误:', error);
			uploadError = error instanceof Error ? error.message : '上传失败，请重试';
		} finally {
			isUploading = false;
			uploadProgress = null;
			input.value = ''; // 清空文件输入
		}
	}

	// 验证链接格式
	function isValidUrl(url: string): boolean {
		try {
			new URL(url);
			return true;
		} catch (e) {
			return false;
		}
	}

	// 处理链接提交
	function handleLinkSubmit() {
		const trimmedLink = coverLink.trim();
		if (!trimmedLink) {
			showValidationError = true;
			return;
		}
		// 使用更严格的URL验证，并检查是否是图片链接（简单判断后缀）
		const imageRegex = /\.(jpg|jpeg|png|gif|webp|bmp)$/i;
		if (!isValidUrl(trimmedLink) || !imageRegex.test(trimmedLink)) {
			showValidationError = true;
			return;
		}

		showValidationError = false;
		onLinkSubmit(trimmedLink);
		coverLink = ''; // 提交后清空输入框
	}

	// 检查链接是否有效以控制按钮状态
	let isSubmitButtonEnabled = $derived.by(() => {
		const trimmedLink = coverLink.trim();
		if (!trimmedLink) return false;
		const imageRegex = /\.(jpg|jpeg|png|gif|webp|bmp)$/i;
		return isValidUrl(trimmedLink) && imageRegex.test(trimmedLink);
	});

	// 取消编辑
	function cancelEdit() {
		isOpen = false;
		coverLink = '';
		showValidationError = false;
		uploadError = null;
		uploadSuccess = false;
	}
</script>

<Mask bind:show={isOpen} onCancel={cancelEdit} />
<Popover.Root bind:open={isOpen}>
	<Popover.Trigger class={isOpen ? 'relative z-50' : ''}>
		{@render children()}
	</Popover.Trigger>
	<Popover.Content class="w-[500px] h-auto p-0 border-0 bg-transparent z-50" align="start">
		<Card.Root class="h-full flex flex-col pb-0">
			<Card.Header class="flex-shrink-0">
				<Card.Title>Event cover</Card.Title>
				<Card.Description
					>Upload a new image, use a link or select an existing image</Card.Description
				>
				<Card.Action>
					<!-- 上传按钮 -->
					<Button
						variant="secondary"
						onclick={() => document.getElementById('file-upload-input')?.click()}
						size="icon"
						disabled={isUploading}
					>
						{#if isUploading}
							<div class="animate-spin rounded-full h-4 w-4 border-b-2 border-current"></div>
						{:else}
							<Upload class="size-4" />
						{/if}
					</Button>
				</Card.Action>
				
				<!-- 上传状态显示 -->
				{#if isUploading && uploadProgress}
					<div class="mt-3 space-y-2" in:fade={{ duration: 200 }}>
						<div class="flex items-center justify-between text-sm">
							<span class="text-muted-foreground">上传中...</span>
							<span class="text-muted-foreground">{uploadProgress.percentage}%</span>
						</div>
						<div class="w-full bg-secondary rounded-full h-2">
							<div
								class="bg-primary h-2 rounded-full transition-all duration-300"
								style="width: {uploadProgress.percentage}%"
							></div>
						</div>
					</div>
				{/if}
				
				<!-- 上传成功提示 -->
				{#if uploadSuccess}
					<div
						class="mt-3 flex items-center gap-2 text-sm text-green-600"
						in:fade={{ duration: 200 }}
						out:fade={{ duration: 200 }}
					>
						<CheckCircle class="size-4" />
						<span>上传成功！</span>
					</div>
				{/if}
				
				<!-- 上传错误提示 -->
				{#if uploadError}
					<div
						class="mt-3 flex items-center gap-2 text-sm text-destructive"
						in:fade={{ duration: 200 }}
						out:fade={{ duration: 200 }}
					>
						<AlertCircle class="size-4" />
						<span>{uploadError}</span>
						<Button
							variant="ghost"
							size="sm"
							onclick={() => (uploadError = null)}
							class="ml-auto h-auto p-1"
						>
							<X class="size-3" />
						</Button>
					</div>
				{/if}
			</Card.Header>

			<Card.Content class="flex-1 py-0">
				<!-- 链接输入区域 -->
				<!-- <h3 class="text-sm font-medium text-foreground/50">Or</h3> -->
				<div class="space-x-3 flex-row flex">
					<div class="relative w-full">
						<Input
							type="url"
							bind:value={coverLink}
							oninput={() => (showValidationError = false)}
							placeholder="粘贴图片链接..."
							class="pl-10"
						/>
						<Link
							class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground"
						/>

						<Button
							class="absolute right-0.5 top-1/2 transform -translate-y-1/2 py-1 text-muted-foreground"
							onclick={handleLinkSubmit}
							disabled={!isSubmitButtonEnabled}
							size="sm"
						>
							使用此链接
						</Button>
					</div>

					{#if showValidationError}
						<p
							in:fade={{ duration: 200 }}
							out:fade={{ duration: 200 }}
							class="text-xs text-destructive"
						>
							请输入有效的图片链接 (需包含图片文件后缀)
						</p>
					{/if}
				</div>
				<!-- 隐藏的文件输入 -->
				<input
					type="file"
					accept="image/*"
					class="hidden"
					onchange={handleFileSelect}
					id="file-upload-input"
				/>
			</Card.Content>
			<div class="flex-1 flex-center flex-col w-full">
				<!-- <h3 class="text-sm font-medium mb-3 ml-4 text-foreground/50">or 我的图片</h3> -->
				<ScrollArea class="h-56 rounded-b-xl border-t-1 bg-background/50 p-3 w-full">
					{#if isLoading}
						<div class="flex items-center justify-center h-32">
							<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
						</div>
					{:else if Object.keys(groupedCoverImages).length === 0}
						<div class="flex items-center justify-center h-32 text-muted-foreground text-sm">
							暂无可用图片
						</div>
					{:else}
						{#each Object.entries(groupedCoverImages) as [provider, images]}
							<div class="mb-4">
								<h4 class="text-xs font-medium mb-2 text-muted-foreground">{provider}</h4>
								<div class="grid grid-cols-3 gap-2">
									{#each images as image}
										<button
											class="aspect-video overflow-hidden rounded-md cursor-pointer hover:ring-2 hover:ring-primary transition-all"
											onclick={() => handleSelectExistingImage(image.imageUrl)}
										>
											<img
												src={image.thumbnailUrl || image.imageUrl}
												alt="封面图片"
												class="w-full h-full object-cover"
											/>
										</button>
									{/each}
								</div>
							</div>
						{/each}
					{/if}
				</ScrollArea>
			</div>
		</Card.Root>
	</Popover.Content>
</Popover.Root>
