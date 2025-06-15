<script lang="ts">
	import '../app.css';
	import { Toaster } from "$lib/components/ui/sonner/index.js";
	import { ModeWatcher } from "mode-watcher";

	let { children } = $props();
</script>
<Toaster position="top-center"/>
<ModeWatcher />
<div class="flex flex-col min-h-screen">
	{@render children()}
</div>
