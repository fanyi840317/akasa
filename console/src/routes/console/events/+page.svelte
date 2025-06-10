<script lang="ts">
	import { ChevronRightIcon, FolderIcon, FileIcon } from '@lucide/svelte';
	import AiInput from '$lib/components/ai/ai-input.svelte';
	import * as Card from '$lib/components/ui/card';
	import { goto } from '$app/navigation';
</script>

<div class="flex-center flex-col p-10 gap-10">
	<h1 class="text-2xl font-extrabold">what do you want to create today?</h1>
	<AiInput class="w-4xl max-w-2xl" />
	<div class="flex flex-col items-start gap-4 min-w-4xl pt-10">
		<header class="flex-center gap-2">
			<FolderIcon class="w-6 h-6 text-foreground/50" />
			<h1 class="text-sm font-extrabold text-foreground/50">Create by you</h1>
		</header>
		<div class="w-full grid auto-rows-min gap-4 md:grid-cols-3 sm:grid-cols-3">
			{#each Array.from({ length: 20 }) as _, index (index)}
				<!-- <div class="bg-card border aspect-square rounded-xl"></div> -->
				<Card.Root class="h-72" onclick={()=>{goto("/console/events/new")}}>
					<Card.Header>
						<Card.Title>Login to your account</Card.Title>
						<Card.Description>Enter your email below to login to your account</Card.Description>
					</Card.Header>

					<!-- <Card.Action>
                <Button variant="link">Sign Up</Button>
              </Card.Action> -->
					<Card.Content class="h-full"></Card.Content>
					<Card.Footer>view</Card.Footer>
				</Card.Root>
			{/each}
		</div>
	</div>
</div>
<!-- <div class="container px-10">
	<header class="p-6">
		<h1 class="text-foreground text-sm font-extrabold">Connected integrations</h1>
		<p class="text-sm text-foreground/50">Manage your connected data sources</p>
	</header>

</div> -->
