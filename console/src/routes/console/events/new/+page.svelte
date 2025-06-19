<script lang="ts">
	import { onMount } from 'svelte';
	import AiInput from '$lib/components/ai/ai-input.svelte';
    import * as Card from '$lib/components/ui/card';
	import { FolderIcon } from '@lucide/svelte';
</script>

<div class="flex-center flex-col gap-4 py-10">
	<h1 class="text-3xl font-extrabold">Create a New Event</h1>
	<p class="text-sm text-muted-foreground">Fill in the details below to create a new event.</p>

	<AiInput class="w-4xl max-w-2xl" />

    <div class="flex flex-col items-start gap-4 min-w-4xl pt-10">
		<header class="flex-center gap-2">
			<FolderIcon class="w-6 h-6 text-foreground/50" />
			<h1 class="text-sm font-extrabold text-foreground/50">最近一周</h1>
		</header>
		<div class="w-full grid auto-rows-min gap-4 md:grid-cols-3 sm:grid-cols-3">
            <Card.Root class="rounded-[16px] shadow-md">
                <Card.Header>
                    <Card.Title>最近一周</Card.Title>
                    <Card.Description>Event Description</Card.Description>
                </Card.Header>
                <Card.Content>
                    <p>Event Details</p>
                </Card.Content>
            </Card.Root>
			 <Card.Root>
                <Card.Header>
                    <Card.Title>Event Title</Card.Title>
                    <Card.Description>Event Description</Card.Description>
                </Card.Header>
                <Card.Content>
                    <p>Event Details</p>
                </Card.Content>
            </Card.Root>
            <Card.Root>
                <Card.Header>
                    <Card.Title>Event Title</Card.Title>
                    <Card.Description>Event Description</Card.Description>
                </Card.Header>
                <Card.Content>
                    <p>Event Details</p>
                </Card.Content>
            </Card.Root>
		</div>
	</div>
</div>
