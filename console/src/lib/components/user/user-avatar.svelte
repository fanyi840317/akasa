<script lang="ts">
	import { Avatar, AvatarImage, AvatarFallback } from "$lib/components/ui/avatar";
	import type { User } from "$lib/types/user";

	let {
		user,
		size = "size-8",
		class: className = "",
		fallbackClass = "",
		...restProps
	}: {
		user: {
			name: string;
			avatar?: string;
		};
		size?: string;
		fallbackClass?: string;
		class?: string;
	} = $props();

	// 获取用户名的第一个字母
	const getInitial = (name: string): string => {
		return name.charAt(0).toUpperCase();
	};

	// 根据用户名生成渐变背景色
	const getGradientBackground = (name: string): string => {
		const colors = [
			"from-blue-400 to-blue-600",
			"from-green-400 to-green-600",
			"from-purple-400 to-purple-600",
			"from-pink-400 to-pink-600",
			"from-yellow-400 to-yellow-600",
			"from-red-400 to-red-600",
			"from-indigo-400 to-indigo-600",
			"from-teal-400 to-teal-600",
			"from-orange-400 to-orange-600",
			"from-cyan-400 to-cyan-600"
		];
		
		// 根据用户名的字符码生成一个稳定的索引
		let hash = 0;
		for (let i = 0; i < name.length; i++) {
			hash = name.charCodeAt(i) + ((hash << 5) - hash);
		}
		
		return colors[Math.abs(hash) % colors.length];
	};

	let initial = $derived(getInitial(user.name));
	let gradientClass = $derived(getGradientBackground(user.name));
</script>

<Avatar class="{size} {className} " {...restProps}>
	{#if user.avatar}
		<AvatarImage src={user.avatar} alt={user.name} />
	{/if}
	<AvatarFallback 
		class="bg-gradient-to-br {gradientClass} text-white font-semibold text-sm {fallbackClass}"
	>
		{initial}
	</AvatarFallback>
</Avatar>