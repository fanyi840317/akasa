<script lang="ts">
    import type { LayoutData } from "./$types";
    import type { Snippet } from "svelte";
    import { Shell } from "./components/index.js";
    import { setContext } from 'svelte';
    import { page } from "$app/stores";
    import { ScrollArea } from "$lib/components/ui/scroll-area";
    import { Button } from "$lib/components/ui/button";
    import { SettingDialog } from "./settings/index.js";

    import { Settings } from "lucide-svelte";
    let {
        data,
        children,
    } = $props<{
        data: LayoutData;
        children: Snippet;
    }>();

    let showLeftView = $state(false);
    let showRightView = $state(false);
    let selectedTemplate = $state<any>(null);

    // 根据 page.data.rightView 控制右侧视图
    $effect(() => {
        if ($page.data.rightView) {
            showRightView = true;
        } else if (selectedTemplate) {
            showRightView = true;
        } else {
            showRightView = false;
        }
    });

    setContext('shell', {
        showRightView:Boolean,
        setShowRightView: (value: boolean) => showRightView = value,
        setTemplate: (template: any) => {
            selectedTemplate = template;
            showRightView = true;
        }
    });
</script>

{#snippet leftView()}
    {#if $page.data.leftView?.type === 'notes'}
        <div class="h-full flex flex-col">
            <div class="flex items-center justify-between p-4 border-b">
                <div class="space-y-1">
                    <h2 class="text-lg font-semibold">我的笔记</h2>
                    <p class="text-sm text-muted-foreground">查看和管理您的笔记</p>
                </div>
            </div>
            <ScrollArea class="flex-1">
                <div class="p-4 space-y-4">
                    {#each $page.data.leftView.data as note}
                        <div class="flex flex-col gap-2 p-4 rounded-lg border hover:bg-muted/50 transition-colors">
                            <h3 class="font-medium">{note.title}</h3>
                            <p class="text-sm text-muted-foreground">{note.content}</p>
                        </div>
                    {/each}
                </div>
            </ScrollArea>
        </div>
    {/if}
{/snippet}

{#snippet rightView()}
    {#if selectedTemplate}
        <div class="h-full flex flex-col">
            <div class="flex items-center justify-between p-4 border-b">
                <div class="flex items-center gap-3">
                    {#if selectedTemplate.icon}
                        <div class="icon-container {selectedTemplate.color || 'blue'}">
                            <svelte:component this={selectedTemplate.icon} class="h-4 w-4" />
                        </div>
                    {/if}
                    <div>
                        <h3 class="font-medium">{selectedTemplate.title}</h3>
                        <p class="text-sm text-muted-foreground">{selectedTemplate.subtitle}</p>
                    </div>
                </div>
                <Button variant="ghost" size="icon" onclick={() => showRightView = false}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
                </Button>
            </div>
            <ScrollArea class="flex-1">
                <div class="p-4">
                    <p class="text-muted-foreground">{selectedTemplate.description}</p>
                </div>
            </ScrollArea>
        </div>
    {/if}
{/snippet}

{#snippet headerActions()}
    {#if $page.data.snippets?.actions}
        {#if $page.data.view === 'notes'}
            <div class="flex items-center gap-2">
                <div class="relative">
                    <div class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                    </div>
                    <input 
                        type="search"
                        placeholder="搜索笔记..."
                        class="h-9 rounded-md border border-input px-3 py-1 text-sm shadow-sm w-[200px] pl-8"
                    />
                </div>
                <Button variant="outline" size="sm">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4 mr-2"><path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z"/></svg>
                    <span>筛选</span>
                </Button>
                <Button size="sm">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4 mr-2"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
                    <span>新建笔记</span>
                </Button>
            </div>
        {/if}
    {/if}
{/snippet}

{#snippet child()}
    {@render children()}
{/snippet}
{#snippet dialogView()}
    <SettingDialog />
{/snippet}
<Shell 
    showLeftView={showLeftView}
    showRightView={showRightView}
    dialogView={dialogView}
    child={child}
    actions={headerActions}
    rightView={rightView}
    leftView={leftView}
    showHeader={$page.data.showHeader}
    titles={[{ name: $page.data.title , path:$page.data?.path }]}
    user={$page.data.user}
/>


