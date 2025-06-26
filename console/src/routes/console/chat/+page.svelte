<script lang="ts">
	import { AiInput } from '$lib/components/ai';
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

<ScrollArea orientation="vertical" class="relative rounded-input bg-base-200 border h-content overflow-hidden">
	<div class="relative h-full w-full">
		<!-- 标题和描述 - 在提交后淡出 -->
		<div 
			class="absolute inset-0 flex-center flex-col gap-4 transition-all duration-700 ease-in-out"
			class:opacity-0={isSubmitted}
			class:translate-y-[-20px]={isSubmitted}
			class:pointer-events-none={isSubmitted}
		>
			<h1 class="text-3xl font-extrabold">Create a New Event</h1>
			<p class="text-muted-foreground text-sm">Fill in the details below to create a new event.</p>
		</div>

		<!-- AiInput - 默认居中，提交后移动到底部 -->
		<div 
			class="absolute w-full px-4 transition-all duration-700 ease-in-out {isSubmitted ? 'bottom-4 top-1/2 -translate-y-1/2' : ''}"

			style:transform={!isSubmitted ? 'translateY(-50%)' : 'translateY(0)'}
		>
			<div class="flex justify-center">
				<AiInput 
					class="w-full max-w-2xl" 
					onSubmit={handleSubmit}
					bind:inputValue
				/>
			</div>
		</div>

		<!-- 聊天内容区域 - 仅在提交后显示 -->
		{#if isSubmitted}
			<div 
				class="pt-4 pb-24 px-4 transition-all duration-700 delay-300 ease-in-out"
				class:opacity-0={!isSubmitted}
				class:opacity-100={isSubmitted}
			>
				<!-- 这里可以添加聊天消息列表 -->
				<div class="space-y-4">
					<div class="bg-card rounded-lg p-4 border">
						<p class="text-sm text-muted-foreground mb-2">You:</p>
						<p>{inputValue}</p>
					</div>
					<!-- 可以在这里添加AI回复 -->
				</div>
			</div>
		{/if}
	</div>
</ScrollArea>
