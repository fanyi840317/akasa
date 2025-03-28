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
    <!-- 网格容器 -->
    <div class="absolute inset-0">
        {#each cells as cell}
            <div 
                class="mesh-cell"
                style="--x: {cell.x}; --y: {cell.y};"
            />
        {/each}
    </div>

    <!-- 鼠标跟随发光效果 -->
    <div 
        class="pointer-events-none absolute w-[300px] h-[300px] transition-all duration-150"
        class:opacity-0={!isHovering}
        style="
            left: {mouseX}px;
            top: {mouseY}px;
            background: radial-gradient(
                circle,
                rgba(255, 255, 255, 0.15) 0%,
                rgba(255, 255, 255, 0.1) 15%,
                rgba(255, 255, 255, 0.05) 30%,
                transparent 60%
            );
            mix-blend-mode: screen;
            transform: translate(-50%, -50%);
            will-change: transform;
        "
    ></div>

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
</style>
