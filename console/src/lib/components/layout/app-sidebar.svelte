<script lang="ts">
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import NavActions from './nav-actions.svelte';
	import type { ComponentProps } from 'svelte';
	import NavFiles from './nav-files.svelte';
	import { PlusIcon } from '@lucide/svelte';
	import LogoIcon from './logo-icon.svelte';

	let {
		actions,
		files,
		chats,
		selectedChatId,
		isOpen = $bindable(true),
		onCreateEvent,
		onFileClick,
		onEventView,
		onEventDelete,
		onChatClick,
		onChatDelete,
		onChatRename,
		...restProps
	}: ComponentProps<typeof Sidebar.Root> & {
		actions?: any;
		isOpen?: boolean;
		chats?:string[];
		files?: any;
		selectedChatId?: string;
		onCreateEvent?: () => void;
		onFileClick?: (fileName: string) => void;
		onEventView?: (eventId: string) => void;
		onEventDelete?: (eventId: string) => void;
		onChatClick?: (chatId: string) => void;
		onChatDelete?: (chatId: string) => void;
		onChatRename?: (chatId: string, newName: string) => void;
	} = $props();

	const handleCreateEvent = () => {
		onCreateEvent?.();
	};
</script>

<Sidebar.Root variant="inset">
	<Sidebar.Header class="py-1">
		<LogoIcon isOpen={true} />
	</Sidebar.Header>
	<Sidebar.Content class="py-6">
		<Sidebar.Group class="px-1">
			<NavActions items={actions} />
		</Sidebar.Group>
		<Sidebar.Group class="px-2">
			<div class="flex items-center justify-between py-1">
				<Sidebar.GroupLabel>Chats</Sidebar.GroupLabel>
				<button 
					class="p-1 rounded-md hover:bg-accent transition-colors" 
					onclick={handleCreateEvent}
					title="创建事件"
				>
					<PlusIcon class="w-4 h-4" />
				</button>
			</div>
			<NavFiles chats={files} {onChatClick}/>
		</Sidebar.Group>
	</Sidebar.Content>
	<Sidebar.Footer />
</Sidebar.Root>
