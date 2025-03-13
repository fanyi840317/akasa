<script lang="ts">
    import { Share2 } from "lucide-svelte";
    import { fade, fly } from "svelte/transition";
    import { createEventDispatcher } from "svelte";
    import { cn } from "$lib/utils";

    let {
        size = "md",
        class: className = "",
        ...restProps
    } = $props<{
        size?: "sm" | "md" | "lg";
        class?: string;
        sizeClasses?: Record<"sm" | "md" | "lg", string>;
    }>();
    const sizeClasses = {
        sm: "w-8 h-8",
        md: "w-12 h-12",
        lg: "w-16 h-16",
    };
    const dispatch = createEventDispatcher();
    let isHovered = false;

    function handleClick() {
        dispatch("click");
    }
</script>

<button
    class={cn(
        "rounded-full bg-background/80 backdrop-blur-sm border-2 border-transparent hover:border-primary transition-all duration-300 group glow-border  items-center justify-center",
        sizeClasses[size as keyof typeof sizeClasses],
        className,
    )}
    on:click={handleClick}
    on:mouseenter={() => (isHovered = true)}
    on:mouseleave={() => (isHovered = false)}
>
    <div class="relative flex items-center justify-center">
        {#if isHovered}
            <div
                class="absolute inset-0 bg-primary/20 blur-xl rounded-full"
                transition:fade
            />
        {/if}
        <Share2
            class="text-muted-foreground group-hover:text-primary transition-colors"
            size={size === "sm" ? 16 : size === "md" ? 20 : 24}
        />
    </div>
</button>

<style>
    .glow-border {
        position: relative;
    }

    .glow-border::before {
        content: "";
        position: absolute;
        inset: -2px;
        border-radius: 9999px;
        padding: 2px;
        background: linear-gradient(90deg, #7c3aed, #c084fc, #7c3aed);
        -webkit-mask:
            linear-gradient(#fff 0 0) content-box,
            linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        background-size: 200% 100%;
        animation: glow 2s linear infinite;
    }

    .glow-border:hover::before {
        animation: blink 1s ease-in-out infinite;
    }

    @keyframes glow {
        0% {
            background-position: 100% 0;
        }
        100% {
            background-position: -100% 0;
        }
    }

    @keyframes blink {
        0%,
        100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
</style>
