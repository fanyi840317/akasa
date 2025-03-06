<script lang="ts">
  /**
   * 通用页面容器组件
   * 提供标准页面布局结构，包括内容区域和可选的侧边栏
   */

  // 组件属性
  let {
    class: className = '',
    fullWidth = false,
    fullHeight = true,
  } = $props();

</script>

<div 
  class="relative {fullWidth ? 'w-full' : ''} {fullHeight ? 'h-full' : ''} {className}"
>
  <div class="w-full h-full flex flex-col overflow-hidden">
    <!-- 页面内容 -->
    <slot />
  </div>
</div>
