<script lang="ts">
	import {
		Card,
		CardContent,
		CardHeader,
		CardTitle,
		CardDescription
	} from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import { Tabs, TabsContent, TabsList, TabsTrigger } from '$lib/components/ui/tabs';
	import {
		Collapsible,
		CollapsibleContent,
		CollapsibleTrigger
	} from '$lib/components/ui/collapsible';
	import { ChevronDown } from '@lucide/svelte';
	import { Label } from '$lib/components/ui/label';

	let { class: className } = $props<{
		class: string;
	}>();

	// 绑定数据
	let name = 'Sales agent';
	let handle = 'sales';
	let description = 'Designed to help manage sales processes and maximize customer engagement.';
	let instructions = `You are a sales agent experienced in sales and marketing, with a deep understanding of
	consumer psychology and sales strategies. You can assist with analyzing customer
	interactions, identifying customer needs, highlighting product benefits, and closing
	deals. Use an energetic, persuasive, and confident tone of voice. Use bullet points in
	your answers to highlight key features and benefits. Use an engaging and concise writing
	style, focusing on value propositions and calls to action.`;
</script>

<div class=" p-6 {className}">
	<!-- 名称字段 -->
	<div class="flex w-full max-w-sm flex-col gap-1.5">
		<Label for="name-2">Name</Label>
		<Input type="name" id="name-2" placeholder="Name" />
		<p class="text-muted-foreground text-sm">Enter your email address.</p>
	</div>
</div>
