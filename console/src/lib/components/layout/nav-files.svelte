<script lang="ts">
	import { MessageSquareIcon, MoreHorizontalIcon, TrashIcon, EditIcon } from '@lucide/svelte';
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu/index.js';
	import Button from '../ui/button/button.svelte';

	type ChatItem = {
		id: string;
		name: string;
		type: 'chat';
		isActive?: boolean;
	};

	let {
		chats,
		onChatClick
	}: {
		chats: ChatItem[];
		onChatClick?: (chatId: string) => void;
	} = $props();

	const handleChatClick = (chatId: string) => {
		onChatClick?.(chatId);
	};

</script>

<Sidebar.Menu>
	{#each chats as chat (chat.id)}
		<Sidebar.MenuItem>
			<div class="group flex w-full items-center gap-2">
				<Sidebar.MenuButton
					onclick={() => handleChatClick(chat.id)}
					isActive={chat.isActive}
					class="line-clamp-1 px-3 flex flex-1 items-center gap-2 truncate text-xs
					{chat.isActive?'text-foreground':'text-foreground/50'}"
				>
					<!-- <MessageSquareIcon class="h-4 w-4" /> -->
					{chat.name}
				</Sidebar.MenuButton>
			</div>
		</Sidebar.MenuItem>
	{/each}
</Sidebar.Menu>
