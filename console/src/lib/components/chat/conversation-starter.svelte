<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent } from '$lib/components/ui/card';
	import { cn } from '$lib/utils';

	// Props
	interface Props {
		class?: string;
		onSend?: (message: string) => void;
	}

	let { class: className, onSend }: Props = $props();

	// 预设的对话启动器
	const starters = [
		{
			title: '🔍 Research a Topic',
			description: 'Get comprehensive research on any topic',
			prompt: 'Research the latest developments in artificial intelligence and machine learning'
		},
		{
			title: '📊 Market Analysis',
			description: 'Analyze market trends and opportunities',
			prompt: 'Analyze the current state of the electric vehicle market'
		},
		{
			title: '💡 Innovation Ideas',
			description: 'Explore innovative solutions and ideas',
			prompt: 'What are some innovative solutions for sustainable energy storage?'
		},
		{
			title: '📈 Business Strategy',
			description: 'Develop strategic business insights',
			prompt: 'What are the key strategies for scaling a SaaS business in 2024?'
		}
	];

	function handleStarterClick(prompt: string) {
		onSend?.(prompt);
	}
</script>

<div class={cn('w-full max-w-4xl', className)}>
	<div class="grid grid-cols-1 gap-3 md:grid-cols-2">
		{#each starters as starter}
			<Card class="cursor-pointer transition-all hover:shadow-md hover:scale-[1.02]">
				<CardContent class="p-4">
					<Button
						variant="ghost"
						class="h-auto w-full justify-start p-0 text-left"
						onclick={() => handleStarterClick(starter.prompt)}
					>
						<div class="flex flex-col gap-2">
							<div class="font-medium text-sm">{starter.title}</div>
							<div class="text-muted-foreground text-xs">{starter.description}</div>
						</div>
					</Button>
				</CardContent>
			</Card>
		{/each}
	</div>
</div>