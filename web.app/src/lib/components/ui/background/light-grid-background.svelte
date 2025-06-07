<script lang="ts">
    import { onMount, onDestroy } from 'svelte';

    export let className: string | undefined | null = undefined;
    let container: HTMLElement;
    let mouseX = 0;
    let mouseY = 0;
    let rafId: number | null = null;
    let rect: DOMRect | null = null;
    let resizeObserver: ResizeObserver | null = null;
    let isHovering = false;

    onMount(() => {
        if (!container) return;

        const updateRect = () => {
            if (container) {
                rect = container.getBoundingClientRect();
            }
        };

        updateRect();
        resizeObserver = new ResizeObserver(updateRect);
        resizeObserver.observe(container);
    });

    onDestroy(() => {
        if (rafId) cancelAnimationFrame(rafId);
        if (resizeObserver && container) {
            resizeObserver.unobserve(container);
        }
        resizeObserver = null;
    });

    function updateMousePosition() {
        if (container) {
            container.style.setProperty('--mouse-x', `${mouseX}px`);
            container.style.setProperty('--mouse-y', `${mouseY}px`);
        }
        rafId = null;
    }

    function handleMouseMove(event: MouseEvent) {
        if (!container || !rect) return;

        mouseX = event.clientX - rect.left;
        mouseY = event.clientY - rect.top;

        if (!rafId) {
            rafId = requestAnimationFrame(updateMousePosition);
        }
    }

    function handleMouseEnter() {
        isHovering = true;
    }

    function handleMouseLeave() {
        isHovering = false;
        if (rafId) {
            cancelAnimationFrame(rafId);
            rafId = null;
        }
    }
</script>

<div
    bind:this={container}
    class="mysterious-background-container relative w-full h-full overflow-hidden {className || ''}"
    on:mousemove={handleMouseMove}
    on:mouseenter={handleMouseEnter}
    on:mouseleave={handleMouseLeave}
>
    <!-- 噪点层 -->
    <div class="noise-layer"></div>
    <!-- 光晕层 -->
    <div class="glow-layer" class:active={isHovering} style="--mouse-x: {mouseX}px; --mouse-y: {mouseY}px"></div>
    <!-- 闪光层 -->
    <div class="shimmer-layer"></div>
    <!-- 暗角层 -->
    <div class="vignette-layer"></div>

    <!-- 渐变遮罩 -->
    <div class="absolute inset-0 bg-gradient-to-b from-transparent via-black/5 to-background/40 pointer-events-none"></div>
</div>

<style>
    .mysterious-background-container {
        --mouse-x: 0px;
        --mouse-y: 0px;
        mask-image: linear-gradient(to bottom, transparent, black 15%, black 85%, transparent);
    }

    .mysterious-background-container {
        @apply absolute inset-0 overflow-hidden;
        background: linear-gradient(135deg, rgba(255,255,255,0.02), rgba(255,255,255,0.05));
    }
    
    .noise-layer {
        @apply absolute inset-0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
        opacity: 0.1;
        animation: noise 8s steps(10) infinite;
    }
    
    .glow-layer {
        @apply absolute inset-0;
        background: radial-gradient(
            600px circle at var(--mouse-x) var(--mouse-y),
            rgba(255, 255, 255, 0.1),
            transparent 40%
        );
        mix-blend-mode: plus-lighter;
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .glow-layer.active {
        opacity: 1;
    }
    
    .shimmer-layer {
        @apply absolute inset-0;
        background: linear-gradient(
            45deg,
            transparent 20%,
            rgba(255, 255, 255, 0.05) 40%,
            rgba(255, 255, 255, 0.05) 60%,
            transparent 80%
        );
        background-size: 200% 200%;
        animation: shimmer 6s ease-in-out infinite;
    }
    
    .vignette-layer {
        @apply absolute inset-0;
        background: radial-gradient(
            circle at 50% 50%,
            transparent 20%,
            rgba(0, 0, 0, 0.02) 70%,
            rgba(0, 0, 0, 0.04) 100%
        );
    }
    
    @keyframes noise {
        0%, 100% { transform: translate(0, 0); }
        10% { transform: translate(-5%, -5%); }
        20% { transform: translate(-10%, 5%); }
        30% { transform: translate(5%, -10%); }
        40% { transform: translate(-5%, 15%); }
        50% { transform: translate(-10%, 5%); }
        60% { transform: translate(15%, 0); }
        70% { transform: translate(0, 10%); }
        80% { transform: translate(-15%, 0); }
        90% { transform: translate(10%, 5%); }
    }
    
    @keyframes shimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
</style> 