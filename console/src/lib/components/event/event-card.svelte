<script lang="ts">
	import { ChevronRightIcon, FolderIcon, FileIcon } from '@lucide/svelte';
	import AiInput from '$lib/components/ai/ai-input.svelte';
	import * as Card from '$lib/components/ui/card';
</script>
<Card.Root class="h-72">
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