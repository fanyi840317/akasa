<script lang="ts">
	import { page } from '$app/stores';
	import ChatContainer from '$lib/components/chat/chat-container.svelte';

	// 获取当前聊天线程ID
	const threadId = $derived($page.params.id);
</script>

<ChatContainer {threadId} />
