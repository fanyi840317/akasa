<script lang="ts">
	import '../app.css';
	import { Toaster } from "$lib/components/ui/sonner/index.js";
	import { ModeWatcher } from "mode-watcher";
	import {onMount} from "svelte";

	let { children } = $props();

	onMount(() => {
		console.log("onMount");
		
	});
	
</script>
<Toaster position="top-center"/>
<ModeWatcher />
<div class="flex-center flex-col min-h-screen">
	{@render children()}
</div>
