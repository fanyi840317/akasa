<script lang="ts">
	let { isOpen = true }: { isOpen?: boolean } = $props();
</script>

{#if isOpen}
	<h1 class="text-xl font-extrabold px-4">Aksas</h1>
{:else}
	<div class="flex-center p-2 w-8 h-8 rounded-full bg-accent transition-all duration-500">
		<h1 class="text-md font-extrabold">A</h1>
	</div>
{/if}