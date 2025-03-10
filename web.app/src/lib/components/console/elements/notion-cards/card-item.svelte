<script lang="ts">
  import { cn } from "$lib/utils";
  import * as Card from "$lib/components/ui/card";
  import { Avatar, AvatarFallback, AvatarImage } from "$lib/components/ui/avatar";

  /**
   * Notion风格的卡片项组件
   */
  let {
    title = '',
    coverImage = '',
    coverIcon = '',
    coverBgColor = 'bg-zinc-800',
    avatarSrc = '',
    avatarFallback = '',
    date = '',
    href = '#',
    class: className = '',
    aspectSquare = true,
    width = '280px', // 固定宽度
    height = '280px', // 固定高度
  } = $props();
</script>

<a 
  {href}
  style="width: {width}; height: {height};"
  class={cn(
    "block rounded-2xl overflow-hidden bg-zinc-900 hover:bg-zinc-800 transition-all duration-200 group",
    "hover:-translate-y-1 hover:shadow-lg border border-zinc-800/50",
    aspectSquare ? "aspect-square" : "",
    className
  )}
>
  <!-- 上部分 - 占据1/3高度 -->
  <div class="relative h-1/3 {coverBgColor} rounded-t-2xl">
    {#if coverImage}
      <img 
        src={coverImage} 
        alt={title} 
        class="w-full h-full object-cover rounded-t-2xl"
      />
    {/if}
    
    <!-- 图标位于左侧 -->
    {#if coverIcon}
      <div class="text-zinc-500 absolute left-6 bottom-0 transform translate-y-1/2 scale-125">
        {@html coverIcon}
      </div>
    {/if}
  </div>
  
  <!-- 下部分 - 占据2/3高度 -->
  <div class="p-4 pt-6 h-2/3 flex flex-col">
    <h3 class="text-sm font-medium text-gray-200 mt-2 mb-auto">{title}</h3>
    
    <div class="flex items-center mt-2">
      <Avatar class="h-5 w-5 mr-2">
        <AvatarImage src={avatarSrc} alt="User" />
        <AvatarFallback class="text-[10px] bg-zinc-800 text-zinc-300">{avatarFallback}</AvatarFallback>
      </Avatar>
      <span class="text-xs text-zinc-400">{date}</span>
    </div>
  </div>
</a> 