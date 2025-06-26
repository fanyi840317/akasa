<script lang="ts">
	import { AiInput } from '$lib/components/ai';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
</script>

<ScrollArea orientation="vertical" class="flex-center rounded-input bg-base-200 border h-content">
	<div class="flex-center flex-col h-full gap-4">
		<h1 class="text-3xl font-extrabold">Create a New Event</h1>
		<p class="text-muted-foreground text-sm">Fill in the details below to create a new event.</p>

		<AiInput class="w-4xl max-w-2xl" />
	</div>
</ScrollArea>
