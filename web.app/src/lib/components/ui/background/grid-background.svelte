<script lang="ts">
    import { onMount, onDestroy } from 'svelte';

    export let className: string | undefined | null = undefined;
    let container: HTMLElement;
    let isHovering = false;

    // 网格配置 (保持固定尺寸)
    const GRID_HEIGHT = 15;
    const GRID_WIDTH = 27;
    let cells: Array<{ x: number; y: number }> = [];

    let mouseX = 0;
    let mouseY = 0;
    let rafId: number | null = null;
    let rect: DOMRect | null = null; // 初始化为 null
    let resizeObserver: ResizeObserver | null = null; // 用于处理容器尺寸变化

    onMount(() => {
        if (!container) return;

        // 生成网格单元格
        cells = Array.from({ length: GRID_WIDTH * GRID_HEIGHT }, (_, i) => ({
            x: i % GRID_WIDTH,
            y: Math.floor(i / GRID_WIDTH)
        }));

        // --- 性能优化 & 鲁棒性: 使用 ResizeObserver 更新 rect ---
        const updateRect = () => {
            if (container) {
                rect = container.getBoundingClientRect();
            }
        };

        // 初始计算 rect
        updateRect();

        // 监听容器尺寸变化
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

    // 更新 CSS 变量的函数 (由 rAF 调用)
    function updateMousePosition() {
        if (container) {
            container.style.setProperty('--mouse-x', `${mouseX}px`);
            container.style.setProperty('--mouse-y', `${mouseY}px`);
        }
        rafId = null;
    }

    // 鼠标移动处理
    function handleMouseMove(event: MouseEvent) {
        if (!isHovering || !container || !rect) return;

        mouseX = event.clientX - rect.left;
        mouseY = event.clientY - rect.top;

        if (!rafId) {
            rafId = requestAnimationFrame(updateMousePosition);
        }
    }

    // 鼠标进入处理
    function handleMouseEnter() {
        isHovering = true;
        if (container) {
            rect = container.getBoundingClientRect();
        }
    }

    // 鼠标离开处理
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
    class="mesh-background-container relative w-full h-full bg-background/5 overflow-hidden [--mesh-size:var(--grid-size)] lg:[--mesh-size:var(--grid-size-large)] {className || ''}"
    on:mousemove={handleMouseMove}
    on:mouseenter={handleMouseEnter}
    on:mouseleave={handleMouseLeave}
>
    {#each cells as cell}
        <div class="mesh-cell" style="--x: {cell.x}; --y: {cell.y};"></div>
    {/each}

    <!-- 渐变遮罩 -->
    <div class="absolute inset-0 bg-gradient-to-b from-transparent via-black/40 to-background/80 pointer-events-none"></div>
</div>

<style>
    /* 全局或组件作用域的基础变量 */
    :root {
        --grid-size: 44px;
        --grid-size-large: 56px;
    }

    .mesh-background-container {
        --mouse-x: 0px;
        --mouse-y: 0px;
    }

    .mesh-cell {
        position: absolute;
        top: calc(var(--y) * var(--mesh-size));
        left: calc(var(--x) * var(--mesh-size));
        width: calc(var(--mesh-size) + 1px);
        height: calc(var(--mesh-size) + 1px);
        background: hsl(var(--foreground) / 0.015);
        contain: strict;
        transition: background .3s ease-in-out, box-shadow .4s ease-in-out;
    }

    .mesh-cell:hover {
        background: hsl(var(--foreground) / 0.04);
        box-shadow: 0 0 20px hsl(var(--foreground) / 0.08);
    }

    .mesh-background-container::before {
        content: '';
        position: absolute;
        width: 200px;
        height: 200px;
        pointer-events: none;
        transition: opacity 150ms ease-out;
        opacity: 0;
        background: radial-gradient(
            circle,
            hsl(var(--foreground) / 0.1) 0%,
            hsl(var(--foreground) / 0.08) 15%,
            hsl(var(--foreground) / 0.04) 30%,
            transparent 60%
        );
        mix-blend-mode: screen;
        transform: translate(-50%, -50%);
        left: var(--mouse-x);
        top: var(--mouse-y);
        will-change: left, top, opacity;
    }

    .mesh-background-container:hover::before {
        opacity: 1;
    }
</style>