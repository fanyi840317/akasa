<script lang="ts">
  import { X, Minus, Maximize2, PanelRight } from "lucide-svelte";
  import { onMount, type Snippet } from "svelte";
  import type { HTMLAttributes } from "svelte/elements";

  let {
    open = $bindable(false),
    title = "窗口",
    width = 400,
    height = $bindable(500),
    minWidth = 300,
    minHeight = 200,
    windowX = $bindable(100),
    windowY = $bindable(100),
    resizable = true,
    children,
    onClose,
    onDock,
    onMinimize,
    hideDockButton = false,
    class: className = "",
    ...restProps
  }: HTMLAttributes<HTMLDivElement> & {
    open?: boolean;
    title?: string;
    width?: number;
    height?: number;
    minWidth?: number;
    minHeight?: number;
    windowX?: number;
    windowY?: number;
    resizable?: boolean;
    children: Snippet;
    onClose?: () => void;
    onDock?: () => void;
    onMinimize?: () => void;
    hideDockButton?: boolean;
    class?: string;
  } = $props();
  // } = $props<>();

  let windowElement: HTMLDivElement;
  let isResizing = false;
  let dragStartX = 0;
  let dragStartY = 0;
  // let windowX = $state(x);
  // let windowY = $state(y);
  let currentWidth = $state(width);
  let currentHeight = $state(height);
  let isMinimized = $state(false);
  let isMaximized = $state(false);
  let isDocked = $state(false);
  let beforeMaximize = { x: 0, y: 0, width: 0, height: 0 };
  let beforeDock = { x: 0, y: 0, width: 0, height: 0 };

  // $effect(() => {
  //   if (x && x > 0 && y && y > 0) {
  //     windowX = x;
  //     windowY = y;
  //   }
  // });

  // 同步currentHeight变化到height属性
  $effect(() => {
    height = currentHeight;
  });
  function handleDragStart(event: DragEvent) {
    if ((event.target as HTMLElement).closest(".window-controls")) {
      event.preventDefault();
      return;
    }
    if (isMinimized || isDocked) {
      event.preventDefault();
      return;
    }

    dragStartX = event.clientX;
    dragStartY = event.clientY;

  
    // 创建一个透明的拖拽图像
    const dragImage = new Image();
    dragImage.src =
      "data:image/gif;base64,R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs=";
    event.dataTransfer?.setDragImage(dragImage, 0, 0);
  }

  function handleDrag(event: DragEvent) {
    if (isMinimized || isDocked) return;
    if (event.clientX === 0 && event.clientY === 0) return; // 拖拽结束时的无效事件

    const deltaX = event.clientX - dragStartX;
    const deltaY = event.clientY - dragStartY;

    windowX = Math.max(
      0,
      Math.min(window.innerWidth - currentWidth, windowX + deltaX),
    );
    windowY = Math.max(0, Math.min(window.innerHeight - 40, windowY + deltaY));

    dragStartX = event.clientX;
    dragStartY = event.clientY;
  }

  function handleDragEnd(event: DragEvent) {
    // 拖拽结束，不进行自动停靠
  }

  function handleClose() {
    open = false;
    onClose?.();
  }

  function handleMinimize() {
    if (onMinimize) {
      onMinimize();
    } else {
      // 默认最小化行为
      if (isDocked) {
        isDocked = false;
        windowX = beforeDock.x;
        windowY = beforeDock.y;
        currentWidth = beforeDock.width;
        currentHeight = beforeDock.height;
      }
      isMinimized = !isMinimized;
      if (isMinimized) {
        // 最小化到右下角
        windowX = window.innerWidth - 200;
        windowY = window.innerHeight - 100;
        currentWidth = 180;
        currentHeight = 60;
      } else {
        // 恢复原始大小
        windowX = 100;
        windowY = 100;
        currentWidth = width;
        currentHeight = height;
      }
    }
  }

  function handleMaximize() {
    if (isDocked) {
      isDocked = false;
      windowX = beforeDock.x;
      windowY = beforeDock.y;
      currentWidth = beforeDock.width;
      currentHeight = beforeDock.height;
    }

    if (isMaximized) {
      // 恢复
      windowX = beforeMaximize.x;
      windowY = beforeMaximize.y;
      currentWidth = beforeMaximize.width;
      currentHeight = beforeMaximize.height;
      isMaximized = false;
    } else {
      // 最大化
      beforeMaximize = {
        x: windowX,
        y: windowY,
        width: currentWidth,
        height: currentHeight,
      };
      windowX = 0;
      windowY = 0;
      currentWidth = window.innerWidth;
      currentHeight = window.innerHeight;
      isMaximized = true;
    }
  }

  function handleDock() {
    if (isMinimized) return;

    // 简化dock处理，只负责参数传递给父组件
    if (onDock) {
      onDock();
    }
  }

  function handleUndock() {
    if (isDocked) {
      isDocked = false;
      windowX = beforeDock.x;
      windowY = beforeDock.y;
      currentWidth = beforeDock.width;
      currentHeight = beforeDock.height;
    }
  }

  function handleResizeStart(event: MouseEvent, direction: string) {
    if (!resizable || isMinimized || isDocked) return;

    isResizing = true;
    const startX = event.clientX;
    const startY = event.clientY;
    const startWidth = currentWidth;
    const startHeight = currentHeight;
    const startWindowX = windowX;
    const startWindowY = windowY;

    function handleResizeMove(e: MouseEvent) {
      const deltaX = e.clientX - startX;
      const deltaY = e.clientY - startY;

      if (direction.includes("right")) {
        currentWidth = Math.max(minWidth, startWidth + deltaX);
      }
      if (direction.includes("left")) {
        const newWidth = Math.max(minWidth, startWidth - deltaX);
        const widthDiff = newWidth - startWidth;
        currentWidth = newWidth;
        windowX = startWindowX - widthDiff;
      }
      if (direction.includes("bottom")) {
        currentHeight = Math.max(minHeight, startHeight + deltaY);
      }
      if (direction.includes("top")) {
        const newHeight = Math.max(minHeight, startHeight - deltaY);
        const heightDiff = newHeight - startHeight;
        currentHeight = newHeight;
        windowY = startWindowY - heightDiff;
      }
    }

    function handleResizeEnd() {
      isResizing = false;
      document.removeEventListener("mousemove", handleResizeMove);
      document.removeEventListener("mouseup", handleResizeEnd);
    }

    document.addEventListener("mousemove", handleResizeMove);
    document.addEventListener("mouseup", handleResizeEnd);
    event.preventDefault();
  }
  onMount(() => {
    console.log("window mounted");
    // console.log(x, y);
  });
</script>

{#if open}
  <div
    class="absolute z-9999 bg-base-200 shadow-2xl rounded-box border border-base-300 {className}"
    style="left: {windowX}px; top: {windowY}px; width: {currentWidth}px; height: {isMinimized
      ? 'auto'
      : currentHeight + 'px'}; pointer-events: auto;"
    bind:this={windowElement}
  >
    <!-- 标题栏 -->
    <div
      class="flex items-center justify-between p-3 bg-base-200 rounded-t-box cursor-move select-none "
      draggable="true"
      ondragstart={handleDragStart}
      ondrag={handleDrag}
      ondragend={handleDragEnd}
      role="button"
      tabindex="0"
      style="pointer-events: auto;"
    >
      <h3 class="font-medium text-sm">{title}</h3>
      <div class="window-controls flex items-center gap-1">
        <!-- {#if !hideDockButton}
          <button
            class="btn btn-ghost btn-xs w-6 h-6 p-0 hover:bg-success/20"
            onclick={handleDock}
            title="停靠到右侧"
          >
            <PanelRight class="w-3 h-3" />
          </button>
        {/if} -->
        <button
          class="btn btn-ghost btn-xs w-6 h-6 p-0 hover:bg-warning/20"
          onclick={handleMinimize}
          title="最小化"
        >
          <Minus class="w-3 h-3" />
        </button>
        <!-- <button
          class="btn btn-ghost btn-xs w-6 h-6 p-0 hover:bg-info/20"
          onclick={handleMaximize}
          title="最大化"
        >
          <Maximize2 class="w-3 h-3" />
        </button> -->
        <button
          class="btn btn-ghost btn-xs w-6 h-6 p-0 hover:bg-error/20"
          onclick={handleClose}
          title="关闭"
        >
          <X class="w-3 h-3" />
        </button>
      </div>
    </div>

    <!-- 内容区域 -->
    {#if !isMinimized}
      <div class="flex-1 overflow-hidden">
        {@render children()}
      </div>
    {/if}

    <!-- 调整大小手柄 -->
    {#if resizable && !isMaximized && !isMinimized}
      <!-- 左边缘 -->
      <div
        class="absolute top-0 left-0 w-1 h-full cursor-ew-resize hover:bg-primary/20"
        onmousedown={(e) => handleResizeStart(e, "left")}
        role="button"
        tabindex="0"
      ></div>

      <!-- 右边缘 -->
      <div
        class="absolute top-0 right-0 w-1 h-full cursor-ew-resize hover:bg-primary/20"
        onmousedown={(e) => handleResizeStart(e, "right")}
        role="button"
        tabindex="0"
      ></div>

      <!-- 顶边缘 -->
      <div
        class="absolute top-0 left-0 w-full h-1 cursor-ns-resize hover:bg-primary/20"
        onmousedown={(e) => handleResizeStart(e, "top")}
        role="button"
        tabindex="0"
      ></div>

      <!-- 底边缘 -->
      <div
        class="absolute bottom-0 left-0 w-full h-1 cursor-ns-resize hover:bg-primary/20"
        onmousedown={(e) => handleResizeStart(e, "bottom")}
        role="button"
        tabindex="0"
      ></div>

      <!-- 左上角 -->
      <div
        class="absolute top-0 left-0 w-3 h-3 cursor-nw-resize hover:bg-primary/30"
        onmousedown={(e) => handleResizeStart(e, "top-left")}
        role="button"
        tabindex="0"
      ></div>

      <!-- 右上角 -->
      <div
        class="absolute top-0 right-0 w-3 h-3 cursor-ne-resize hover:bg-primary/30"
        onmousedown={(e) => handleResizeStart(e, "top-right")}
        role="button"
        tabindex="0"
      ></div>

      <!-- 左下角 -->
      <div
        class="absolute bottom-0 left-0 w-3 h-3 cursor-sw-resize hover:bg-primary/30"
        onmousedown={(e) => handleResizeStart(e, "bottom-left")}
        role="button"
        tabindex="0"
      ></div>

      <!-- 右下角 -->
      <div
        class="absolute bottom-0 right-0 w-3 h-3 cursor-nw-resize hover:bg-primary/30"
        onmousedown={(e) => handleResizeStart(e, "bottom-right")}
        role="button"
        tabindex="0"
      ></div>
    {/if}
  </div>
{/if}

<style>
  .cursor-move {
    cursor: move;
  }

  .cursor-ew-resize {
    cursor: ew-resize;
  }

  .cursor-ns-resize {
    cursor: ns-resize;
  }

  .cursor-nw-resize {
    cursor: nw-resize;
  }

  .cursor-ne-resize {
    cursor: ne-resize;
  }

  .cursor-sw-resize {
    cursor: sw-resize;
  }

  .select-none {
    user-select: none;
  }

  .dock-preview {
    border: 2px solid rgba(59, 130, 246, 0.5);
    background: rgba(59, 130, 246, 0.1);
  }
</style>
