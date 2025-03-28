<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    
    export let className: string | undefined | null = undefined;
    let container: HTMLElement;
    let isHovering = false;
    let resizeObserver: ResizeObserver;
    
    // 网格配置
    const GRID_HEIGHT = 15;  // 固定5排
    const GRID_WIDTH = 27;  // 总列数
    let cells: Array<{x: number; y: number}> = [];
    
    let mouseX = 0;
    let mouseY = 0;
    
    function updateGrid() {
        if (!container) return;
        const rect = container.getBoundingClientRect();
        const containerWidth = rect.width;
        const containerHeight = rect.height;
        
        // 计算网格大小
        const meshSize = Math.min(containerWidth / GRID_WIDTH, containerHeight / GRID_HEIGHT);
        container.style.setProperty('--mesh-size', `${meshSize}px`);
        
        // 计算居中偏移
        const offsetX = (containerWidth - (GRID_WIDTH * meshSize)) / 2;
        const offsetY = (containerHeight - (GRID_HEIGHT * meshSize)) / 2;
        container.style.setProperty('--offset-x', `${offsetX}px`);
        container.style.setProperty('--offset-y', `${offsetY}px`);
    }
    
    onMount(() => {
        if (!container) return;
        
        // 生成网格单元格
        cells = Array.from({ length: GRID_WIDTH * GRID_HEIGHT }, (_, i) => ({
            x: i % GRID_WIDTH,
            y: Math.floor(i / GRID_WIDTH)
        }));
        
        // 监听容器大小变化
        resizeObserver = new ResizeObserver(updateGrid);
        resizeObserver.observe(container);
        
        // 初始化网格
        updateGrid();
    });
    
    onDestroy(() => {
        if (resizeObserver) {
            resizeObserver.disconnect();
        }
    });
    
    function handleMouseMove(event: MouseEvent) {
        if (!container || !isHovering) return;
        const rect = container.getBoundingClientRect();
        mouseX = event.clientX - rect.left;
        mouseY = event.clientY - rect.top;
        requestAnimationFrame(() => {
            container.style.setProperty('--mouse-x', `${mouseX}px`);
            container.style.setProperty('--mouse-y', `${mouseY}px`);
        });
    }

    function handleMouseEnter() {
        isHovering = true;
    }

    function handleMouseLeave() {
        isHovering = false;
    }
</script>

<div
    bind:this={container}
    class="relative w-full h-full bg-black overflow-hidden {className || ''}"
    on:mousemove={handleMouseMove}
    on:mouseenter={handleMouseEnter}
    on:mouseleave={handleMouseLeave}
>
{#each cells as cell}
<div 
    class="mesh-cell"
    style="--x: {cell.x}; --y: {cell.y};"
/>
{/each}

    <!-- 渐变遮罩 -->
    <!-- <div class="absolute inset-0 bg-gradient-to-b from-transparent via-black/80 to-black pointer-events-none"></div> -->
</div> 

<style>
    :global(:root) {
        --mesh-size: 44px;
        --mesh-size-large: 56px;
        --offset-x: 0px;
        --offset-y: 0px;
    }
    
    .mesh-cell {
        position: absolute;
        top: calc(var(--y) * var(--mesh-size) + var(--offset-y));
        left: calc(var(--x) * var(--mesh-size) + var(--offset-x));
        width: calc(var(--mesh-size) + 1px);
        height: calc(var(--mesh-size) + 1px);
        background: hsla(0, 0%, 100%, .04);
        contain: strict;
        transition: background .3s ease-in-out, box-shadow .4s ease-in-out;
        will-change: opacity;
    }
    
    .mesh-cell:hover {
        background: hsla(0, 0%, 100%, .08);
        box-shadow: 0 0 20px hsla(0, 0%, 100%, .1);
    }

    div[class*="relative"]::before {
        content: '';
        position: absolute;
        width: 300px;
        height: 300px;
        pointer-events: none;
        transition: opacity 150ms ease-out;
        opacity: 0;
        background: radial-gradient(
            circle,
            rgba(255, 255, 255, 0.15) 0%,
            rgba(255, 255, 255, 0.1) 15%,
            rgba(255, 255, 255, 0.05) 30%,
            transparent 60%
        );
        mix-blend-mode: screen;
        transform: translate(-50%, -50%);
        will-change: transform, opacity;
        left: var(--mouse-x, 0);
        top: var(--mouse-y, 0);
        contain: strict;
    }

    div[class*="relative"]:hover::before {
        opacity: 1;
    }
</style>
