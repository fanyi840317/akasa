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
                // console.log('Rect updated due to resize or mount/enter'); // 用于调试
            }
        };

        // 初始计算 rect
        updateRect();

        // 监听容器尺寸变化
        resizeObserver = new ResizeObserver(updateRect);
        resizeObserver.observe(container);
        // --- 结束 ResizeObserver ---

    });

    onDestroy(() => {
        if (rafId) cancelAnimationFrame(rafId);
        // --- 性能优化 & 鲁棒性: 清理 ResizeObserver ---
        if (resizeObserver && container) {
            resizeObserver.unobserve(container);
        }
        resizeObserver = null; // 移除引用，帮助垃圾回收
        // --- 结束清理 ---
    });

    // 更新 CSS 变量的函数 (由 rAF 调用)
    function updateMousePosition() {
        if (container) {
            // 直接更新 CSS 自定义属性
            container.style.setProperty('--mouse-x', `${mouseX}px`);
            container.style.setProperty('--mouse-y', `${mouseY}px`);
        }
        rafId = null; // 标记 rAF 已完成
    }

    // 鼠标移动处理
    function handleMouseMove(event: MouseEvent) {
        // 必须在 rect 有效且处于悬停状态时才计算
        if (!isHovering || !container || !rect) return;

        // 计算相对于容器左上角的鼠标位置
        mouseX = event.clientX - rect.left;
        mouseY = event.clientY - rect.top;

        // 使用 rAF 节流更新，避免频繁操作 DOM style
        if (!rafId) {
            rafId = requestAnimationFrame(updateMousePosition);
        }
    }

    // 鼠标进入处理
    function handleMouseEnter() {
        isHovering = true;
        // --- 鲁棒性: 进入时重新获取 rect，因为它可能自上次悬停后已改变 ---
        if (container) {
             rect = container.getBoundingClientRect();
        }
        // 无需在此处立即更新位置，CSS :hover 会处理伪元素的 opacity
    }

    // 鼠标离开处理
    function handleMouseLeave() {
        isHovering = false;
        // 取消任何待处理的 rAF 更新
        if (rafId) {
             cancelAnimationFrame(rafId);
             rafId = null;
        }
        // CSS :hover 会自动处理伪元素的隐藏，无需 JS 操作
        // 可以选择性地重置 JS 中的 mouseX/mouseY 或 CSS 变量，但非必需
        // if (container) {
        //   container.style.removeProperty('--mouse-x');
        //   container.style.removeProperty('--mouse-y');
        // }
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
        /* 移除了未使用的 --offset-x, --offset-y */
    }

    /* --- 性能优化: 使用具体类名 --- */
    .mesh-background-container {
        /* 定义鼠标位置 CSS 变量，并提供初始值 */
        --mouse-x: 0px;
        --mouse-y: 0px;
        /* --mesh-size 通过 Svelte 的 class 指令动态设置 */
    }

    .mesh-cell {
        position: absolute;
        /* 使用响应式的 --mesh-size */
        top: calc(var(--y) * var(--mesh-size));
        left: calc(var(--x) * var(--mesh-size));
        width: calc(var(--mesh-size) + 1px); /* +1px 用于重叠或边框效果 */
        height: calc(var(--mesh-size) + 1px);
        background: hsl(var(--foreground) / 0.015);
        contain: strict; /* 保持这个微优化 */
        transition: background .3s ease-in-out, box-shadow .4s ease-in-out;
        /* 根据要求，不添加 pointer-events: none; */
    }

    /* 保留单元格的 hover 效果 */
    .mesh-cell:hover {
        background: hsl(var(--foreground) / 0.04);
        box-shadow: 0 0 20px hsl(var(--foreground) / 0.08);
    }

    /* --- 性能优化: 使用具体类名选择器 & 添加 will-change --- */
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
        /* 直接使用 CSS 变量 */
        left: var(--mouse-x);
        top: var(--mouse-y);
        /* 提示浏览器这些属性会频繁变化，以便优化 */
        will-change: left, top, opacity;
    }

    /* :hover 状态控制伪元素的显隐 */
    .mesh-background-container:hover::before {
        opacity: 1;
    }
</style>