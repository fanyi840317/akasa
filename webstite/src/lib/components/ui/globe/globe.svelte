<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import { cn } from "$lib/utils";
  import createGlobe from "cobe";

  // 颜色预设
  type ColorPreset = {
    baseColor: [number, number, number];
    markerColor: [number, number, number];
    glowColor: [number, number, number];
    bgColorClass: string;
  };

  const colorPresets: Record<string, ColorPreset> = {
    blackwhite: {
      baseColor: [0.1, 0.1, 0.1],
      markerColor: [1.0, 1.0, 1.0],
      glowColor: [1.0, 1.0, 1.0],
      bgColorClass: "bg-gray-500/5 dark:bg-gray-500/10",
    },
    blue: {
      baseColor: [0.3, 0.3, 0.3],
      markerColor: [0.1, 0.8, 1],
      glowColor: [0.1, 0.6, 1.0],
      bgColorClass: "bg-blue-500/5 dark:bg-blue-500/10",
    },
    purple: {
      baseColor: [0.3, 0.2, 0.3],
      markerColor: [0.6, 0.1, 0.9],
      glowColor: [0.5, 0.1, 0.9],
      bgColorClass: "bg-purple-500/5 dark:bg-purple-500/10",
    },
    green: {
      baseColor: [0.2, 0.3, 0.2],
      markerColor: [0.1, 0.8, 0.3],
      glowColor: [0.1, 0.7, 0.4],
      bgColorClass: "bg-green-500/5 dark:bg-green-500/10",
    },
    red: {
      baseColor: [0.3, 0.2, 0.2],
      markerColor: [0.9, 0.1, 0.1],
      glowColor: [0.8, 0.1, 0.1],
      bgColorClass: "bg-red-500/5 dark:bg-red-500/10",
    },
    orange: {
      baseColor: [0.3, 0.25, 0.2],
      markerColor: [0.9, 0.5, 0.1],
      glowColor: [0.8, 0.4, 0.1],
      bgColorClass: "bg-orange-500/5 dark:bg-orange-500/10",
    },
  };

  // 使用runes模式的props
  let {
    class: className = "",
    targetCoordinates = null as [number, number] | null,
    autoRotate = true,
    onFocus = (_: [number, number]) => {},
    color = "blackwhite", // 默认颜色主题
    bgColor = "", // 向后兼容，如果设置了bgColor，会覆盖color的背景色
  } = $props();

  // 获取当前颜色预设
  $effect(() => {
    currentColorPreset = colorPresets[color] || colorPresets.blackwhite;
  });

  let currentColorPreset = colorPresets.blackwhite;

  let canvasRef: HTMLCanvasElement;
  let globeInstance: ReturnType<typeof createGlobe> | null = null;
  let phi = 0;
  let targetPhi = 0;
  let theta = 0.3;
  let targetTheta = 0.3;
  let width = 0;
  let height = 0;
  let animationFrame: number | undefined = undefined;
  let isAnimatingToLocation = false;

  // 所有标记点
  let markers: { location: [number, number]; size: number }[] = [
    // 默认标记点
    { location: [37.7595, -122.4367], size: 0.05 }, // San Francisco
    { location: [40.7128, -74.006], size: 0.05 }, // New York
    { location: [51.5074, -0.1278], size: 0.05 }, // London
    { location: [35.6762, 139.6503], size: 0.05 }, // Tokyo
    { location: [39.9042, 116.4074], size: 0.05 }, // Beijing
  ];

  // 创建Globe实例的通用函数
  function createGlobeInstance(initialPhi = 0, initialTheta = 0.3) {
    if (!canvasRef) return null;

    const pixelRatio = window.devicePixelRatio || 1;
    return createGlobe(canvasRef, {
      devicePixelRatio: pixelRatio,
      width: width * pixelRatio,
      height: height * pixelRatio,
      phi: initialPhi,
      theta: initialTheta,
      dark: 1,
      diffuse: 1.5,
      mapSamples: 16000,
      mapBrightness: 8,
      baseColor: currentColorPreset.baseColor,
      markerColor: currentColorPreset.markerColor,
      glowColor: currentColorPreset.glowColor,
      markers: markers,
      onRender: (state) => {
        // 如果正在动画到特定位置
        if (isAnimatingToLocation) {
          // 平滑过渡到目标位置
          const phiDiff = targetPhi - phi;
          const thetaDiff = targetTheta - theta;

          // 如果差距很小，认为动画完成
          if (Math.abs(phiDiff) < 0.01 && Math.abs(thetaDiff) < 0.01) {
            isAnimatingToLocation = false;
          } else {
            // 否则继续动画
            phi += phiDiff * 0.05;
            theta += thetaDiff * 0.05;
          }
        } else if (autoRotate) {
          // 正常自动旋转
          phi += 0.003;
        }

        // 更新状态
        state.phi = phi;
        state.theta = theta;
      },
    });
  }

  // 添加新的标记点
  function addMarker(location: [number, number], size: number = 0.05) {
    markers = [...markers, { location, size }];
    if (globeInstance) {
      // 重新创建Globe实例以更新标记点
      recreateGlobe();
    }
  }

  // 旋转到特定坐标
  function focusLocation(location: [number, number]) {
    if (!location || !globeInstance) return;

    // 将经纬度转换为phi和theta
    // 经度转换为phi (longitude -> phi)
    targetPhi = (location[1] / 180) * Math.PI;
    // 纬度转换为theta (latitude -> theta)
    targetTheta = (location[0] / 90) * (Math.PI / 2);

    // 设置动画标志
    isAnimatingToLocation = true;
    autoRotate = false;

    // 添加高亮标记
    addMarker(location, 0.1);

    // 通知父组件，传递坐标
    onFocus(location);
  }

  // 重新创建Globe实例
  function recreateGlobe() {
    if (!canvasRef || !globeInstance) return;

    // 保存当前状态
    const currentPhi = phi;
    const currentTheta = theta;

    // 销毁当前实例
    globeInstance.destroy();

    // 创建新实例
    globeInstance = createGlobeInstance(currentPhi, currentTheta);
  }

  // 监听坐标变化
  $effect(() => {
    if (targetCoordinates && globeInstance) {
      focusLocation(targetCoordinates);
    }
  });

  // 监听颜色变化
  $effect(() => {
    if (globeInstance) {
      recreateGlobe();
    }
  });

  onMount(() => {
    if (!canvasRef) return;

    width = canvasRef.offsetWidth;
    height = canvasRef.offsetHeight;

    globeInstance = createGlobeInstance();

    return () => {
      if (globeInstance) {
        globeInstance.destroy();
      }
      if (animationFrame !== undefined) {
        cancelAnimationFrame(animationFrame);
      }
    };
  });

  onDestroy(() => {
    if (globeInstance) {
      globeInstance.destroy();
    }
    if (animationFrame !== undefined) {
      cancelAnimationFrame(animationFrame);
    }
  });

  // 获取背景颜色类
  let bgColorClass = $derived(bgColor || currentColorPreset.bgColorClass);
</script>

<div
  class={cn(
    "w-[300px] h-[300px]  relative",
    className,
  )}
>
  <canvas
    bind:this={canvasRef}
    class="w-full h-full"
  ></canvas>
  <!-- <div
    class={cn("absolute inset-0 rounded-full blur-2xl", bgColorClass)}
  ></div> -->
</div>
