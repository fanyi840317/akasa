<script lang="ts">
    import { cubicInOut } from "svelte/easing";
    import { crossfade } from "svelte/transition";
    import { ScrollArea } from "$lib/components/ui/scroll-area";
    import { cn } from "$lib/utils";

    export let items: Array<{ id: string; name: string; label?: string }> = [];
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
        <ScrollArea orientation="both" scrollbarXClasses="invisible">
            <div
                class={cn("mb-4 flex items-center overflow-y-auto pb-3 md:pb-0", className)}
                {...$$restProps}
            >
                {#each items as item}
                    {@const isActive = selectedId === item.id}
                    <button
                        onclick={() => handleSelect(item.id)}
                        class={cn(
                            "hover:text-primary relative flex h-7 items-center justify-center rounded-full px-4 text-center text-sm transition-colors",
                            isActive ? "text-primary font-medium" : "text-muted-foreground"
                        )}
                    >
                        {#if isActive}
                            <div
                                class="bg-muted absolute inset-0 rounded-full"
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