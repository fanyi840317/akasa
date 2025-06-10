<script lang="ts">
	import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "$lib/components/ui/card";
	import { Input } from "$lib/components/ui/input";
	import { Button } from "$lib/components/ui/button";
	import { Tabs, TabsContent, TabsList, TabsTrigger } from "$lib/components/ui/tabs";
	import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "$lib/components/ui/collapsible";
	import { ChevronDown } from "@lucide/svelte";
	
	// 绑定数据
	let name = "Sales agent";
	let handle = "sales";
	let description = "Designed to help manage sales processes and maximize customer engagement.";
	let instructions = `You are a sales agent experienced in sales and marketing, with a deep understanding of
	consumer psychology and sales strategies. You can assist with analyzing customer
	interactions, identifying customer needs, highlighting product benefits, and closing
	deals. Use an energetic, persuasive, and confident tone of voice. Use bullet points in
	your answers to highlight key features and benefits. Use an engaging and concise writing
	style, focusing on value propositions and calls to action.`;
</script>

<div class=" p-6">
	  <!-- 名称字段 -->
      <div class="space-y-2">
        <CardTitle class="text-base font-medium">Name</CardTitle>
        <div class="flex items-center">
            <div class="flex-1">
                <Input placeholder="Legal agents" bind:value={name} />
            </div>
            <div class="ml-2">
                <Button variant="ghost" size="icon" class="h-9 w-9">
                    <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                        <path d="M1.59229 11.8527L6.97453 8.73879L10.8501 12.0619L17.739 7.96033L17.2117 7.10653L10.9171 10.8565L7.05824 7.55017L1.59229 10.7059V11.8527ZM6.86572 9.8688C7.68604 9.8688 8.35566 9.19917 8.35566 8.37885C8.35566 7.55854 7.68604 6.89727 6.86572 6.89727C6.04541 6.89727 5.37576 7.55854 5.37576 8.37885C5.37576 9.19917 6.04541 9.8688 6.86572 9.8688ZM10.8166 12.9408C11.6369 12.9408 12.2982 12.2712 12.2982 11.4508C12.2982 10.6305 11.6369 9.96923 10.8166 9.96923C9.99631 9.96923 9.32666 10.6305 9.32666 11.4508C9.32666 12.2712 9.99631 12.9408 10.8166 12.9408ZM17.128 9.1322C17.9483 9.1322 18.6179 8.46256 18.6179 7.64225C18.6179 6.82193 17.9483 6.15229 17.128 6.15229C16.3077 6.15229 15.638 6.82193 15.638 7.64225C15.638 8.46256 16.3077 9.1322 17.128 9.1322Z" fill="currentColor"></path>
                        <path d="M0.713379 17.0591C0.713379 17.4609 0.981236 17.7204 1.38302 17.7204H18.032C18.4003 17.7204 18.71 17.4274 18.71 17.0507C18.71 16.6824 18.4003 16.3811 18.032 16.3811H2.29541C2.11963 16.3811 2.06104 16.3225 2.06104 16.1467V2.91289C2.06104 2.55296 1.75969 2.24325 1.39139 2.24325C1.01472 2.24325 0.713379 2.55296 0.713379 2.91289V17.0591Z" fill="currentColor"></path>
                    </svg>
                    <ChevronDown class="h-4 w-4" />
                </Button>
            </div>
        </div>
    </div>

    <!-- 句柄字段 -->
    <div class="space-y-2">
        <CardTitle class="text-base font-medium">Handle</CardTitle>
        <CardDescription>Give your agent a handle people can use to message it</CardDescription>
        <div class="flex items-center rounded-md border px-3">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="mr-2 text-muted-foreground">
                <path fill="currentColor" d="M2 8.42c0 3.68 2.61 5.91 6.21 5.91.97 0 1.9-.13 2.47-.3.4-.13.54-.33.54-.54 0-.2-.17-.36-.39-.36-.07 0-.16.01-.27.04-.72.17-1.33.28-2.16.28-3.2 0-5.4-1.84-5.4-5 0-3 2.07-5.11 5.18-5.11 2.75 0 5.04 1.61 5.04 4.5 0 1.7-.6 2.83-1.56 2.83-.65 0-1.01-.36-1.01-.96V5.93c0-.3-.18-.49-.47-.49-.3 0-.48.18-.48.49v.63h-.05c-.3-.68-1.03-1.12-1.9-1.12-1.52 0-2.6 1.23-2.6 3 0 1.79 1.07 3.03 2.62 3.03.9 0 1.6-.47 1.95-1.26h.05c.11.79.8 1.26 1.74 1.26 1.63 0 2.64-1.52 2.64-3.66 0-3.24-2.5-5.35-5.96-5.35C4.55 2.46 2 4.83 2 8.42Zm5.92 2.17c-1.04 0-1.71-.83-1.71-2.15 0-1.3.67-2.13 1.72-2.13 1.08 0 1.76.8 1.76 2.1 0 1.32-.7 2.18-1.77 2.18Z"></path>
            </svg>
            <Input placeholder="legal" bind:value={handle} class="border-0 px-0" />
        </div>
    </div>

    <!-- 描述字段 -->
    <div class="space-y-2">
        <CardTitle class="text-base font-medium">Description</CardTitle>
        <CardDescription>Describe what this agent will help your team with</CardDescription>
        <div class="w-full">
            <textarea 
                rows="4" 
                placeholder="Like ’I help with resource heavy and manual work like instantly producing contract reviews, analyzing large volumes of data, and uncovering new insights.‘" 
                class="w-full min-h-[80px] rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                bind:value={description}
            ></textarea>
        </div>
    </div>

    <!-- 指令字段 -->
    <div class="space-y-2">
        <CardTitle class="text-base font-medium">Instructions</CardTitle>
        <CardDescription>Control your agents behavior by adding custom instructions</CardDescription>
        <div class="w-full">
            <textarea 
                rows="14" 
                placeholder="Like ’Answer all questions in Spanish‘ or ’Always follow our specific tone of voice guideline’" 
                class="w-full min-h-[200px] rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                bind:value={instructions}
            ></textarea>
        </div>
    </div>

    <!-- 高级选项 -->
    <Collapsible class="w-full">
        <CollapsibleTrigger class="flex items-center gap-1 text-sm font-medium">
            <Button variant="ghost" class="px-2 py-1 h-auto">
                Advanced <ChevronDown class="h-4 w-4 ml-1" />
            </Button>
        </CollapsibleTrigger>
        <CollapsibleContent>
            <!-- 高级选项内容 -->
        </CollapsibleContent>
    </Collapsible>
</div>
