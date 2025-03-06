<script lang="ts">
  import { onMount } from 'svelte';
  import Map from '$lib/components/map.svelte';
  
  /**
   * 地图视图组件
   * 提供地图显示和相关控件的布局
   */
  let {
    locationData = {
      longitude: 104.06,
      latitude: 30.67
    },
    showControls = true
  } = $props();
  
  let containerRef;
  
  onMount(() => {
    // 地图容器初始化完成后的处理
  });
</script>

<div class="relative flex-1 w-full h-full overflow-hidden" bind:this={containerRef}>
  <div class="absolute inset-0 w-full h-full">
    <Map {locationData} />
  </div>
  
  {#if showControls}
    <div class="absolute bottom-4 right-4 z-10">
      <slot name="controls" />
    </div>
  {/if}
  
  <slot />
</div>
