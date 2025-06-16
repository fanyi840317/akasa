<script lang="ts">
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import { Settings, DollarSign, BookOpen, Users, LogOut, Sun, Moon, Monitor, ChevronDown } from '@lucide/svelte';
	import { createEventDispatcher } from 'svelte';
	import type { Snippet } from 'svelte';

	let {
		children,
		user,
		onMenuAction,
		onLogout
	} = $props<{
		children?: Snippet;
		user: {
			name: string;
			email?: string;
			avatar?: string;
		};
		onMenuAction?: (action: string) => void;
		onLogout?: () => void;
	}>();

	const dispatch = createEventDispatcher();

	// 菜单项处理函数
	function handleSettings() {
		if (onMenuAction) {
			onMenuAction('settings');
		} else {
			dispatch('menuAction', { action: 'settings' });
		}
	}

	function handlePricing() {
		if (onMenuAction) {
			onMenuAction('pricing');
		} else {
			dispatch('menuAction', { action: 'pricing' });
		}
	}

	function handleDocs() {
		if (onMenuAction) {
			onMenuAction('docs');
		} else {
			dispatch('menuAction', { action: 'docs' });
		}
	}

	function handleCommunity() {
		if (onMenuAction) {
			onMenuAction('community');
		} else {
			dispatch('menuAction', { action: 'community' });
		}
	}

	function handleLogoutClick() {
		if (onLogout) {
			onLogout();
		} else {
			dispatch('logout');
		}
	}

	function handleUpgrade() {
		console.log('升级计划');
	}
</script>

<DropdownMenu.Root>
	<DropdownMenu.Trigger>
		{@render children?.()}
	</DropdownMenu.Trigger>
	<DropdownMenu.Content class="w-64 border-border rounded-[16px]" align="end">
		<!-- 用户信息头部 -->
		<div class="px-4 py-3 border-b">
			<div class="text-sm font-medium text-muted-foreground">
				{user.email || user.name}
			</div>
		</div>

		<!-- 主要菜单项 -->
		<DropdownMenu.Item onclick={handleSettings}>
			<Settings class="mr-2 h-4 w-4" />
			<span>设置</span>
		</DropdownMenu.Item>
		<DropdownMenu.Item onclick={handlePricing}>
			<DollarSign class="mr-2 h-4 w-4" />
			<span>定价</span>
		</DropdownMenu.Item>
		<DropdownMenu.Item onclick={handleDocs}>
			<BookOpen class="mr-2 h-4 w-4" />
			<span>文档</span>
		</DropdownMenu.Item>
		<DropdownMenu.Item onclick={handleCommunity}>
			<Users class="mr-2 h-4 w-4" />
			<span>社区论坛</span>
		</DropdownMenu.Item>

		<DropdownMenu.Separator />
        <DropdownMenu.Label>设置</DropdownMenu.Label>

		<!-- 设置部分 -->
		<div class="px-4 py-3">
			
			<!-- 主题设置 -->
			<div class="flex justify-between items-center mb-3">
				<span class="text-sm">主题</span>
				<div class="flex gap-1 bg-base-200 rounded-full border">
					<button class="p-1 rounded hover:bg-accent">
						<Sun class="w-4 h-4" />
					</button>
					<button class="p-1 rounded hover:bg-accent">
						<Moon class="w-4 h-4" />
					</button>
					<button class="p-1 rounded bg-accent">
						<Monitor class="w-4 h-4" />
					</button>
				</div>
			</div>

			<!-- 语言设置 -->
			<div class="flex justify-between items-center">
				<span class="text-sm">语言</span>
				<div class="flex items-center gap-1 text-sm">
					<span>中文</span>
					<ChevronDown class="w-3 h-3" />
				</div>
			</div>
		</div>

		<DropdownMenu.Separator />

		<!-- 退出登录 -->
		<DropdownMenu.Item onclick={handleLogoutClick} class="text-destructive focus:text-destructive">
			<LogOut class="mr-2 h-4 w-4" />
			<span>退出登录</span>
		</DropdownMenu.Item>
	</DropdownMenu.Content>
</DropdownMenu.Root>