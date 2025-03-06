<script lang="ts">
  /**
   * 页面内容容器组件
   * 提供标准的内容区域布局，支持多种布局模式
   */
  let {
    class: className = '',
    padded = true,
    fullHeight = true,
    centered = false,
  } = $props();
</script>

<div 
  class="page-content {className} {padded ? 'p-4 md:p-6' : ''} {fullHeight ? 'h-full' : ''} {centered ? 'flex items-center justify-center' : ''}"
>
  <slot />
</div>
