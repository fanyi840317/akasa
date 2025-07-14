<script lang="ts">
	import { chatStore } from '$lib/stores/chat.svelte';
	import { cn } from '$lib/utils';
	import { Search, BookOpenText, FileText, PencilRuler } from '@lucide/svelte';
	import { Card } from '$lib/components/ui/card';
	import { Skeleton } from '$lib/components/ui/skeleton';
	import {
		Accordion,
		AccordionContent,
		AccordionItem,
		AccordionTrigger
	} from '$lib/components/ui/accordion';
	import RainbowText from '$lib/components/ui/rainbow-text.svelte';
	import LoadingAnimation from '$lib/components/ui/loading-animation.svelte';
	import AutoScrollContainer from '$lib/components/ui/auto-scroll-container.svelte';
	import Markdown from '$lib/components/ui/markdown.svelte';

	interface Props {
		class?: string;
		researchId: string;
	}

	let { class: className, researchId }: Props = $props();

	const researchMessages = $derived.by(() => {
		const activityIds = chatStore.getResearchActivityIds(researchId);
		if (activityIds.length === 0) return [];
		return activityIds.map((id) => chatStore.getMessage(id)).filter(Boolean);
	});

	// 过滤出研究消息（排除计划和报告）
	const researchOnlyMessages = $derived(
		researchMessages.filter((msg) => msg && msg.agent === 'researcher')
	);

	$effect(() => {
		if (researchOnlyMessages) {
			console.log(researchOnlyMessages);
		}
		for (const message of researchOnlyMessages) {
			message?.toolCalls?.forEach((toolCall) => {
				console.log(toolCall?.result?.trim());
			});
		}
	});

	const ongoing = $derived(chatStore.getOngoingResearchId() === researchId);

	// 解析工具调用结果
	function parseToolCallResult(result: string): any {
		try {
			return JSON.parse(result);
		} catch {
			return null;
		}
	}

	// 渲染搜索结果
	function renderSearchResults(results: any[]): { pages: any[]; images: any[] } {
		const pages = results.filter((r) => r.type === 'page');
		const images = results.filter((r) => r.type === 'image');
		return { pages, images };
	}
</script>

<AutoScrollContainer
	class={cn('flex flex-col py-4', className)}
	scrollTriggers={[researchOnlyMessages.length]}
	continuousScroll={false}
>
	{#each researchOnlyMessages as message, i (message?.id)}
		{#if message}
			<div class="px-4 py-2">
				<!-- 消息内容 -->
				{#if message.content}
					<Markdown
						class="prose-sm"
						content={message.content}
						animated={message.isStreaming}
					></Markdown>
				{/if}

				<!-- 工具调用 -->
				{#if message.toolCalls && message.toolCalls.length > 0 && !message.isStreaming}
					{#each message.toolCalls as toolCall (toolCall.id)}
						{#if toolCall.name === 'web_search'}
							<!-- Web搜索工具调用 -->
							<section class="mt-4 pl-4">
								<div class="font-medium italic">
									<RainbowText class="flex items-center" animated={!toolCall.result}>
										{#snippet children()}
											<Search size={16} class="mr-2" />
											<span>Searching for </span>
											<span class="max-w-[500px] overflow-hidden text-ellipsis whitespace-nowrap">
												{toolCall.args?.query || ''}
											</span>
										{/snippet}
									</RainbowText>
								</div>
								{#if toolCall.result}
									{@const searchResults = parseToolCallResult(toolCall.result)}
									{#if searchResults && Array.isArray(searchResults)}
										{@const { pages, images } = renderSearchResults(searchResults)}
										<div class="pr-4">
											<ul class="mt-2 flex flex-wrap gap-4">
												{#each pages as result, idx}
													<li
														class="bg-accent text-muted-foreground flex max-w-40 gap-2 rounded-md px-2 py-1 text-sm"
													>
														<div class="mt-1 h-4 w-4 flex-shrink-0 rounded-sm bg-blue-500"></div>
														<a href={result.url} target="_blank" class="hover:underline">
															{result.title}
														</a>
													</li>
												{/each}
												{#each images as result, idx}
													<li>
														<a href={result.image_url} target="_blank" class="block">
															<img
																src={result.image_url}
																alt={result.image_description}
																class="h-40 w-40 rounded-md object-cover"
															/>
														</a>
													</li>
												{/each}
											</ul>
										</div>
									{/if}
								{:else}
									<!-- 搜索中的骨架屏 -->
									<div class="pr-4">
										<ul class="mt-2 flex flex-wrap gap-4">
											{#each Array(6) as _, idx}
												<li class="flex h-40 w-40 gap-2 rounded-md text-sm">
													<Skeleton
														class="to-accent h-full w-full rounded-md bg-gradient-to-tl from-slate-400"
													/>
												</li>
											{/each}
										</ul>
									</div>
								{/if}
							</section>
						{:else if toolCall.name === 'crawl_tool'}
							<!-- 爬虫工具调用 -->
							<section class="mt-4 pl-4">
								<div>
									<RainbowText
										class="flex items-center text-base font-medium italic"
										animated={!toolCall.result}
									>
										{#snippet children()}
											<BookOpenText size={16} class="mr-2" />
											<span>Reading</span>
										{/snippet}
									</RainbowText>
								</div>
								<ul class="mt-2 flex flex-wrap gap-4">
									<li
										class="bg-accent text-muted-foreground flex h-40 w-40 gap-2 rounded-md px-2 py-1 text-sm"
									>
										<div class="mt-1 h-4 w-4 flex-shrink-0 rounded-sm bg-green-500"></div>
										<a
											href={toolCall.args?.url as string}
											target="_blank"
											class="h-full flex-grow overflow-hidden text-ellipsis whitespace-nowrap hover:underline"
										>
											{toolCall.args?.url || 'Unknown URL'}
										</a>
									</li>
								</ul>
							</section>
						{:else if toolCall.name === 'local_search_tool'}
							<!-- RAG检索工具调用 -->
							<section class="mt-4 pl-4">
								<div class="font-medium italic">
									<RainbowText class="flex items-center" animated={!toolCall.result}>
										{#snippet children()}
											<Search size={16} class="mr-2" />
											<span>Retrieving documents from RAG </span>
											<span class="max-w-[500px] overflow-hidden text-ellipsis whitespace-nowrap">
												{toolCall.args?.keywords || ''}
											</span>
										{/snippet}
									</RainbowText>
								</div>
								{#if toolCall.result}
									{@const documents = parseToolCallResult(toolCall.result)}
									{#if documents && Array.isArray(documents)}
										<div class="pr-4">
											<ul class="mt-2 flex flex-wrap gap-4">
												{#each documents as doc, idx}
													<li
														class="bg-accent text-muted-foreground flex max-w-40 gap-2 rounded-md px-2 py-1 text-sm"
													>
														<FileText size={32} />
														{doc.title}
													</li>
												{/each}
											</ul>
										</div>
									{/if}
								{:else}
									<!-- 检索中的骨架屏 -->
									<div class="pr-4">
										<ul class="mt-2 flex flex-wrap gap-4">
											{#each Array(2) as _, idx}
												<li class="flex h-40 w-40 gap-2 rounded-md text-sm">
													<Skeleton
														class="to-accent h-full w-full rounded-md bg-gradient-to-tl from-slate-400"
													/>
												</li>
											{/each}
										</ul>
									</div>
								{/if}
							</section>
						{:else}
							<!-- 其他工具调用 -->
							<section class="mt-4 pl-4">
								<div class="w-fit overflow-y-auto rounded-md py-0">
									<Accordion type="single" class="w-full">
										<AccordionItem value="item-1">
											<AccordionTrigger>
												<div class="flex items-center font-medium italic">
													<PencilRuler size={16} class="mr-2" />
													<RainbowText
														class="pr-0.5 text-base font-medium italic"
														animated={!toolCall.result}
													>
														{#snippet children()}
															Running {toolCall.name ? `${toolCall.name}()` : 'MCP tool'}
														{/snippet}
													</RainbowText>
												</div>
											</AccordionTrigger>
											<AccordionContent>
												{#if toolCall.result}
													<div
														class="bg-accent max-h-[400px] max-w-[560px] overflow-y-auto rounded-md text-sm"
													>
														<pre class="whitespace-pre-wrap p-4">{toolCall.result.trim()}</pre>
													</div>
												{/if}
											</AccordionContent>
										</AccordionItem>
									</Accordion>
								</div>
							</section>
						{/if}
					{/each}
				{/if}
			</div>

			{#if i !== researchOnlyMessages.length - 1}
				<hr class="my-8" />
			{/if}
		{/if}
	{/each}

	{#if ongoing}
		<LoadingAnimation class="mx-4 my-12" />
	{/if}
</AutoScrollContainer>
