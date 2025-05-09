<script lang="ts">
	import { UserAvatar } from "../ui/avatar";
	import { goto } from "$app/navigation";
	import { LogIn } from "lucide-svelte";
	import { cn } from "$lib/utils";
	import { fly } from 'svelte/transition';

	// Define user type
	type UserData = {
		name: string;
		avatar?: string;
		email?: string;
	} | null;

	let {
		user = null,
		onLogin = () => goto("/login"),
		onLogout = () => {},
		onProfile = () => goto("/profile"),
		class: className = "",
		isShow = $bindable(true),
	} = $props<{
		user?: UserData;
		onLogin?: () => void;
		onLogout?: () => void;
		onProfile?: () => void;
		class?: string;
		isShow?: boolean;
	}>();

</script>
{#if isShow }
<div 
	class={cn(
		"navbar backdrop-blur-sm shadow-sm", 
		className
	)}>
	
	<div class="navbar-start">
		<button
			class="btn btn-ghost text-xl"
			onclick={() => goto("/")}
			onkeydown={(e) => e.key === "Enter" && goto("/")}
		>
			Akasa
		</button>
	</div>
	<div class="navbar-end">
		{#if user}
			<!-- User is logged in -->
			<div class="dropdown dropdown-end">
				<button tabindex="0" class="btn btn-ghost rounded-full">
					<UserAvatar
						src={user.avatar}
						alt={user.name}
						fallback={user.name?.[0] || "U"}
					/>
				</button>
				<ul
					role="menu"
					class="mt-1 z-[1] p-2 shadow menu menu-sm dropdown-content gap-2
					bg-base-300 rounded-lg w-32"
				>
					<li>
						<button
							onclick={onProfile}
							onkeydown={(e) => e.key === "Enter" && onProfile()}
						>
							个人资料
						</button>
					</li>
					<li>
						<button
							onclick={onLogout}
							onkeydown={(e) => e.key === "Enter" && onLogout()}
						>
							退出登录
						</button>
					</li>
				</ul>
			</div>
		{:else}
			<!-- User is not logged in -->
			<button
				class="btn gap-2 btn-ghost"
				onclick={onLogin}
				onkeydown={(e) => e.key === "Enter" && onLogin()}
			>
				<LogIn class="h-4 w-4" />
				<span>登录</span>
			</button>
		{/if}
	</div>
</div>
{/if}
