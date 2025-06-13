<script lang="ts">
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
import { Edit, Settings, Trash2, Copy, Share } from '@lucide/svelte';
import NameEditor from './name-editor.svelte';
import type { Snippet } from 'svelte';

	let { 
		children,
		onNameEdit,
		onSettings
	} = $props<{
		children?: Snippet;
		onNameEdit?: () => void;
		onSettings?: () => void;
	}>();

	// 打开名称编辑器
	function openNameEditor() {
		if (onNameEdit) {
			onNameEdit();
		}
	}

	// 其他菜单项处理函数
	function handleDuplicate() {
		console.log('复制活动');
	}

	function handleShare() {
		console.log('分享活动');
	}

	function handleSettings() {
		if (onSettings) {
			onSettings();
		} else {
			console.log('活动设置');
		}
	}

	function handleDelete() {
		console.log('删除活动');
	}
</script>

<DropdownMenu.Root>
	<DropdownMenu.Trigger>
		{@render children?.()}
	</DropdownMenu.Trigger>
	<DropdownMenu.Content class="w-56 border-border rounded-[16px]" align="start">
		<DropdownMenu.Label>Actions</DropdownMenu.Label>
		<DropdownMenu.Item onclick={openNameEditor}>
			<Edit class="mr-2 h-4 w-4" />
			<span>编辑标题</span>
		</DropdownMenu.Item>
		<!-- <DropdownMenu.Separator /> -->
		<DropdownMenu.Item onclick={handleDuplicate}>
			<Copy class="mr-2 h-4 w-4" />
			<span>复制活动</span>
		</DropdownMenu.Item>
		<DropdownMenu.Item onclick={handleShare}>
			<Share class="mr-2 h-4 w-4" />
			<span>分享活动</span>
		</DropdownMenu.Item>
		<DropdownMenu.Separator />
		<DropdownMenu.Item onclick={handleSettings}>
			<Settings class="mr-2 h-4 w-4" />
			<span>活动设置</span>
		</DropdownMenu.Item>
		<DropdownMenu.Separator />
		<DropdownMenu.Item onclick={handleDelete} class="text-destructive focus:text-destructive">
			<Trash2 class="mr-2 h-4 w-4" />
			<span>删除活动</span>
		</DropdownMenu.Item>
	</DropdownMenu.Content>
</DropdownMenu.Root>