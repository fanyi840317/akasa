<script lang="ts">
	import { AiInput } from '$lib/components/ai';
	import { Button } from '$lib/components/ui/button';
	import { ScrollArea } from '$lib/components/ui/scroll-area';

	// 状态管理
	let isSubmitted = $state(false);
	let inputValue = $state('');

	function handleSubmit(text: string): void {
		// 设置为已提交状态，触发动画
		isSubmitted = true;

		// 这里可以添加实际的提交逻辑
		console.log('Submitted:', text);

		// 可以在这里添加实际的API调用或其他处理逻辑
		// throw new Error('Function not implemented.');
	}
</script>

<ScrollArea
	orientation="vertical"
	class="rounded-input bg-base-200 h-content relative overflow-hidden border"
>
	<div class="relative h-full w-full">
		<!-- AiInput - 默认居中，提交后移动到底部 -->
		<div
			class="absolute w-full px-4 transition-all duration-700 ease-in-out {!isSubmitted
				? 'top-1/2'
				: 'bottom-4'}"
			style:transform={!isSubmitted ? 'translateY(-70%)' : 'translateY(0)'}
		>
		<!-- 标题和描述 - 在提交后淡出 -->
            {#if !isSubmitted}
			<div class="flex-center flex-col mb-4">
				<h1 class="text-3xl font-extrabold">Create a New Event</h1>
				<p class="text-muted-foreground text-sm">
					Fill in the details below to create a new event.
				</p>
			</div>
            {/if}
			<div class="flex-center gap-4 flex-col">
				<AiInput class="w-full max-w-3xl" onSubmit={handleSubmit} bind:inputValue />
                <div class="flex-center flex-row gap-2">
                    <Button variant="outline" size="sm">查看最近的事件</Button>
                    <Button variant="outline" size="sm">创建新事件</Button>
                    <Button variant="outline" size="sm">21齶190齶2齶 恶10</Button>
                    <Button variant="outline" size="sm">21齶190齶2齶 恶10</Button>
                </div>
			</div>
		</div>

		<!-- 聊天内容区域 - 仅在提交后显示 -->
		{#if isSubmitted}
			<div
				class="px-4 pb-24 pt-4 transition-all delay-300 duration-700 ease-in-out"
				class:opacity-0={!isSubmitted}
				class:opacity-100={isSubmitted}
			>
				<!-- 这里可以添加聊天消息列表 -->
				<div class="space-y-4">
					<div class="bg-card rounded-lg border p-4">
						<p class="text-muted-foreground mb-2 text-sm">You:</p>
						<p>{inputValue}</p>
					</div>
					<!-- 可以在这里添加AI回复 -->
				</div>
			</div>
		{/if}
	</div>
</ScrollArea>
