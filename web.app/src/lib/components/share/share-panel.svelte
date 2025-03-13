<script lang="ts">
    import { fade, fly } from "svelte/transition";
    import { createEventDispatcher } from "svelte";
    import { X, Link, Twitter, Facebook } from "lucide-svelte";
    import { Button } from "$lib/components/ui/button";

    const dispatch = createEventDispatcher();
    export let url = window.location.href;

    function copyToClipboard() {
        navigator.clipboard.writeText(url);
    }

    function close() {
        dispatch("close");
    }

    const socialLinks = [
        { icon: Twitter, label: "Twitter", color: "text-[#1DA1F2]" },
        { icon: Facebook, label: "Facebook", color: "text-[#4267B2]" },
    ];
</script>

<div
    class="fixed inset-0 bg-background/80 backdrop-blur-sm z-50"
    transition:fade={{ duration: 200 }}
    on:click={close}
/>

<div
    class="fixed right-6 bottom-40 w-80 p-6 rounded-lg bg-background/95 backdrop-blur-md border border-muted z-50 space-y-4"
    transition:fly={{ y: 20, duration: 300 }}
>
    <div class="flex justify-between items-center">
        <h3 class="text-lg font-semibold">分享活动</h3>
        <Button
            variant="ghost"
            size="icon"
            class="h-8 w-8"
            on:click={close}
        >
            <X class="h-4 w-4" />
        </Button>
    </div>

    <div
        class="p-4 rounded-md bg-muted/50 border border-muted flex items-center gap-2 group hover:border-primary transition-colors"
    >
        <div class="flex-1 truncate text-sm">{url}</div>
        <Button
            variant="ghost"
            size="icon"
            class="h-8 w-8 hover:text-primary"
            on:click={copyToClipboard}
        >
            <Link class="h-4 w-4" />
        </Button>
    </div>

    <div class="flex justify-center gap-4">
        {#each socialLinks as { icon: Icon, label, color }}
            <Button
                variant="ghost"
                size="icon"
                class="h-10 w-10 rounded-full {color} opacity-75 hover:opacity-100 transition-opacity"
            >
                <Icon class="h-5 w-5" />
                <span class="sr-only">{label}</span>
            </Button>
        {/each}
    </div>

    <div
        class="absolute inset-0 pointer-events-none overflow-hidden rounded-lg"
    >
        <div
            class="absolute top-0 left-1/2 -translate-x-1/2 w-40 h-40 bg-primary/10 blur-3xl"
        />
        <div
            class="absolute bottom-0 right-0 w-32 h-32 bg-primary/5 blur-2xl"
        />
    </div>
</div>