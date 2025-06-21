<script lang="ts">
	import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Separator } from '$lib/components/ui/separator';

	interface Field {
		key: string;
		label: string;
		type: 'text' | 'password' | 'number' | 'checkbox';
		placeholder?: string;
		description?: string;
	}

	let {
		title,
		description,
		data = $bindable({}),
		fields = []
	}: {
		title: string;
		description?: string;
		data: Record<string, unknown>;
		fields: Field[];
	} = $props();

	// 获取嵌套对象的值
	const getValue = (obj: Record<string, unknown>, path: string): unknown => {
		return path.split('.').reduce((current: unknown, key) => {
			return current && typeof current === 'object' && current !== null && key in current
				? (current as Record<string, unknown>)[key]
				: '';
		}, obj);
	};

	// 设置嵌套对象的值
	const setValue = (obj: Record<string, unknown>, path: string, value: unknown): void => {
		const keys = path.split('.');
		const lastKey = keys.pop()!;
		
		// 确保路径上的所有对象都存在
		let current: Record<string, unknown> = obj;
		for (const key of keys) {
			if (!current[key] || typeof current[key] !== 'object') {
				current[key] = {};
			}
			current = current[key] as Record<string, unknown>;
		}
		
		// 设置最终值
		current[lastKey] = value;
	};

	// 处理输入变化
	const handleInputChange = (field: Field, event: Event) => {
		const target = event.target as HTMLInputElement;
		let value: unknown;
		
		switch (field.type) {
			case 'checkbox':
				value = target.checked;
				break;
			case 'number':
				value = target.value ? Number(target.value) : undefined;
				break;
			default:
				value = target.value;
				break;
		}
		
		setValue(data, field.key, value);
		// 触发响应式更新
		data = { ...data };
	};
</script>

<Card>
	<CardHeader>
		<CardTitle>{title}</CardTitle>
		{#if description}
			<CardDescription>{description}</CardDescription>
		{/if}
	</CardHeader>
	<CardContent class="space-y-4">
		{#each fields as field, index (field.key)}
			<div class="space-y-2">
				<Label for={`${title}-${field.key}`}>{field.label}</Label>
				{#if field.type === 'checkbox'}
					<div class="flex items-center space-x-2">
						<input
							id={`${title}-${field.key}`}
							type="checkbox"
							checked={getValue(data, field.key) || false}
							onchange={(e) => handleInputChange(field, e)}
							class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
						/>
						<Label for={`${title}-${field.key}`} class="text-sm font-normal">
							{field.description || field.label}
						</Label>
					</div>
				{:else}
					<Input
						id={`${title}-${field.key}`}
						type={field.type}
						value={getValue(data, field.key) || ''}
						placeholder={field.placeholder}
						oninput={(e) => handleInputChange(field, e)}
						class="w-full"
					/>
				{/if}
				{#if field.description && field.type !== 'checkbox'}
					<p class="text-sm text-gray-500">{field.description}</p>
				{/if}
			</div>
			{#if index < fields.length - 1}
				<Separator class="my-4" />
			{/if}
		{/each}
	</CardContent>
</Card>