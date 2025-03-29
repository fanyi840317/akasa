<script lang="ts">
    import { cubicInOut } from "svelte/easing";
    import { crossfade } from "svelte/transition";
    import { ScrollArea } from "$lib/components/ui/scroll-area";
    import { cn } from "$lib/utils";

    export let items: Array<{ id: string; name: string; label?: string; color?: string }> = [];
    export let selectedId: string = items[0]?.id || "";
    export let className: string | undefined | null = undefined;

    const [send, receive] = crossfade({
        duration: 250,
        easing: cubicInOut,
    });

    function handleSelect(id: string) {
        selectedId = id;
        dispatch('select', { id });
    }

    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();
</script>

<div class="relative">
    <div class="lg:max-w-none">
        <ScrollArea orientation="horizontal" scrollbarXClasses="invisible">
            <div
                class={cn("mb-4 grid grid-flow-col auto-cols-max gap-2 pb-3 md:pb-0", className)}
                {...$$restProps}
            >
                {#each items as item}
                    {@const isActive = selectedId === item.id}
                    <button
                        onclick={() => handleSelect(item.id)}
                        class={cn(
                            "hover:text-primary relative flex h-7 min-w-max items-center justify-center rounded-sm px-4 text-center text-sm transition-colors whitespace-nowrap",
                            isActive ? "text-primary font-medium" : "text-muted-foreground/70",
                            item.color && !isActive && `hover:bg-${item.color}/5`
                        )}
                    >
                        {#if isActive}
                            <div
                                class={cn(
                                    "absolute inset-0 rounded-sm bg-primary/5 border-[0.5px] border-primary/10 dark:bg-primary/10 dark:border-primary/20 backdrop-filter backdrop-blur-[2px] shadow-sm"
                                )}
                                in:send={{ key: "activetab" }}
                                out:receive={{ key: "activetab" }}
                            />
                        {/if}
                        <div class="relative">
                            {item.name}
                            {#if item.label}
                                <span
                                    class="ml-2 rounded-md bg-[#adfa1d] px-1.5 py-0.5 text-xs font-medium leading-none text-[#000000] no-underline group-hover:no-underline"
                                >
                                    {item.label}
                                </span>
                            {/if}
                        </div>
                    </button>
                {/each}
            </div>
        </ScrollArea>
    </div>
</div>